#!/usr/bin/env python3
"""Smart Segmenter MVP CLI.

Usage:
  python scripts/segment.py --input video.mp4 --output segments.json [--deep] [--fast]
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class Boundary:
    time_s: float
    source: str


def run_cmd(cmd: list[str]) -> tuple[int, str, str]:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc.returncode, proc.stdout, proc.stderr


def hhmmss_to_seconds(h: str, m: str, s: str) -> float:
    return int(h) * 3600 + int(m) * 60 + float(s)


def extract_json_object(text: str) -> dict[str, Any]:
    if not text:
        return {}
    text = text.strip()
    fence_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if fence_match:
        text = fence_match.group(1)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"(\{.*\})", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                return {}
        return {}


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def probe_video(input_file: Path) -> dict[str, Any]:
    code, _out, err = run_cmd(["ffmpeg", "-hide_banner", "-i", str(input_file)])
    # ffmpeg -i writes probe info to stderr and often returns non-zero without output target.
    _ = code

    duration_s = 0.0
    fps = 30.0
    codec = "unknown"
    resolution = "unknown"
    has_audio = False

    duration_match = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", err)
    if duration_match:
        duration_s = hhmmss_to_seconds(*duration_match.groups())

    for line in err.splitlines():
        if "Video:" in line and codec == "unknown":
            codec_match = re.search(r"Video:\s*([^,\s]+)", line)
            if codec_match:
                codec = codec_match.group(1)

            res_match = re.search(r"(\d{2,5})x(\d{2,5})", line)
            if res_match:
                resolution = f"{res_match.group(1)}x{res_match.group(2)}"

            fps_match = re.search(r"(\d+(?:\.\d+)?)\s*fps", line)
            if fps_match:
                try:
                    fps = float(fps_match.group(1))
                except ValueError:
                    pass

        if "Audio:" in line:
            has_audio = True

    return {
        "duration_s": round(duration_s, 3),
        "fps": fps,
        "codec": codec,
        "resolution": resolution,
        "has_audio": has_audio,
        # MVP: keyframe extraction is not implemented without ffprobe.
        "keyframe_count": 0,
        "keyframe_interval_avg_s": 0.0,
    }


def extract_audio(input_file: Path, tmp_dir: Path) -> Path | None:
    audio_path = tmp_dir / "audio.wav"
    code, _out, err = run_cmd(
        [
            "ffmpeg",
            "-hide_banner",
            "-y",
            "-i",
            str(input_file),
            "-vn",
            "-acodec",
            "pcm_s16le",
            "-ar",
            "16000",
            "-ac",
            "1",
            str(audio_path),
        ]
    )
    if code != 0:
        if "Output file #0 does not contain any stream" in err:
            return None
        raise RuntimeError(f"Audio extraction failed: {err.strip()}")
    return audio_path


def detect_scenes_scenedetect(input_file: Path, fps: float, fast: bool) -> list[dict[str, float]]:
    from scenedetect import ContentDetector, detect

    threshold = 32.0 if fast else 27.0
    min_scene_len = max(10, int(round(fps * (1.4 if fast else 0.8))))
    scene_list = detect(str(input_file), ContentDetector(threshold=threshold, min_scene_len=min_scene_len))

    scenes: list[dict[str, float]] = []
    for start_tc, end_tc in scene_list:
        scenes.append(
            {
                "start_s": round(start_tc.get_seconds(), 3),
                "end_s": round(end_tc.get_seconds(), 3),
            }
        )
    return scenes


def detect_scenes_ffmpeg_fallback(input_file: Path, duration_s: float, fast: bool) -> list[dict[str, float]]:
    threshold = "0.42" if fast else "0.36"
    code, _out, err = run_cmd(
        [
            "ffmpeg",
            "-hide_banner",
            "-i",
            str(input_file),
            "-filter:v",
            f"select='gt(scene,{threshold})',showinfo",
            "-an",
            "-f",
            "null",
            "-",
        ]
    )
    if code != 0 and "showinfo" not in err:
        raise RuntimeError(f"Fallback scene detection failed: {err.strip()}")

    boundary_times: list[float] = []
    for match in re.finditer(r"pts_time:(\d+(?:\.\d+)?)", err):
        t = float(match.group(1))
        if 0.05 < t < max(0.05, duration_s - 0.05):
            boundary_times.append(t)

    # Deduplicate dense neighbors from ffmpeg's scene score spikes.
    boundary_times.sort()
    dedup: list[float] = []
    for t in boundary_times:
        if not dedup or abs(t - dedup[-1]) > 0.6:
            dedup.append(t)

    edges = [0.0] + dedup + [duration_s]
    scenes: list[dict[str, float]] = []
    for i in range(len(edges) - 1):
        scenes.append({"start_s": round(edges[i], 3), "end_s": round(edges[i + 1], 3)})
    return scenes


def detect_visual_scenes(input_file: Path, duration_s: float, fps: float, fast: bool) -> tuple[list[dict[str, float]], str]:
    try:
        scenes = detect_scenes_scenedetect(input_file, fps=fps, fast=fast)
        return scenes, "scenedetect_contentdetector"
    except Exception:
        scenes = detect_scenes_ffmpeg_fallback(input_file, duration_s=duration_s, fast=fast)
        return scenes, "ffmpeg_scene_fallback"


def detect_silence(audio_file: Path | None) -> list[dict[str, float]]:
    if audio_file is None:
        return []

    code, _out, err = run_cmd(
        [
            "ffmpeg",
            "-hide_banner",
            "-i",
            str(audio_file),
            "-af",
            "silencedetect=noise=-30dB:d=0.3",
            "-f",
            "null",
            "-",
        ]
    )
    if code != 0 and "silence_" not in err:
        raise RuntimeError(f"silencedetect failed: {err.strip()}")

    starts: list[float] = []
    ends: list[float] = []
    for line in err.splitlines():
        start_match = re.search(r"silence_start:\s*(\d+(?:\.\d+)?)", line)
        if start_match:
            starts.append(float(start_match.group(1)))
            continue

        end_match = re.search(
            r"silence_end:\s*(\d+(?:\.\d+)?)\s*\|\s*silence_duration:\s*(\d+(?:\.\d+)?)",
            line,
        )
        if end_match:
            ends.append(float(end_match.group(1)))

    silences: list[dict[str, float]] = []
    for i, s in enumerate(starts):
        if i < len(ends) and ends[i] >= s:
            e = ends[i]
            silences.append(
                {
                    "start_s": round(s, 3),
                    "end_s": round(e, 3),
                    "mid_s": round((s + e) / 2.0, 3),
                    "duration_s": round(e - s, 3),
                }
            )
    return silences


def build_gemini_prompt(duration_s: float) -> str:
    prompt_file = Path(__file__).resolve().parents[1] / "prompts" / "gemini_segment.md"
    if prompt_file.exists():
        base_prompt = prompt_file.read_text(encoding="utf-8").strip()
    else:
        base_prompt = (
            "You are a video segment analyst. Return JSON only. No markdown fences.\n"
            "Output schema: {\"segments\": [{\"start_s\": number, \"end_s\": number, "
            "\"label\": \"short title\", \"description\": \"brief summary\", "
            "\"emotion\": \"other\", \"narrative_role\": \"other\", \"visual_style\": \"brief style\", "
            "\"audio\": {\"has_dialogue\": true, \"dialogue_summary\": \"brief\", \"language\": \"en|zh|other\", "
            "\"word_count\": number, \"music_present\": false}, \"confidence\": number}], "
            "\"narrative_arc\": {\"pattern\": \"...\", \"structure_type\": \"...\", \"viral_elements\": [\"...\"]}}\n"
        )
    return (
        f"{base_prompt}\n\n"
        f"Video duration is about {duration_s:.2f}s. Ensure 0 <= start_s < end_s <= {duration_s:.2f}."
    )


def normalize_gemini_segments(data: dict[str, Any], duration_s: float) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    raw_segments = data.get("segments") if isinstance(data, dict) else None
    if not isinstance(raw_segments, list):
        return [], {}

    normalized: list[dict[str, Any]] = []
    for item in raw_segments:
        if not isinstance(item, dict):
            continue
        try:
            start_s = float(item.get("start_s", 0.0))
            end_s = float(item.get("end_s", 0.0))
        except (TypeError, ValueError):
            continue
        start_s = clamp(start_s, 0.0, duration_s)
        end_s = clamp(end_s, 0.0, duration_s)
        if end_s - start_s < 0.2:
            continue

        audio = item.get("audio") if isinstance(item.get("audio"), dict) else {}
        normalized.append(
            {
                "start_s": round(start_s, 3),
                "end_s": round(end_s, 3),
                "label": str(item.get("label", "Untitled Segment"))[:120],
                "description": str(item.get("description", ""))[:500],
                "emotion": str(item.get("emotion", "other"))[:40],
                "narrative_role": str(item.get("narrative_role", "other"))[:40],
                "visual_style": str(item.get("visual_style", ""))[:160],
                "audio": {
                    "has_dialogue": bool(audio.get("has_dialogue", False)),
                    "dialogue_summary": str(audio.get("dialogue_summary", ""))[:240],
                    "language": str(audio.get("language", "unknown"))[:20],
                    "word_count": int(audio.get("word_count", 0) or 0),
                    "music_present": bool(audio.get("music_present", False)),
                },
                "confidence": float(item.get("confidence", 0.6) or 0.6),
            }
        )

    normalized.sort(key=lambda seg: (seg["start_s"], seg["end_s"]))
    narrative_arc = data.get("narrative_arc") if isinstance(data.get("narrative_arc"), dict) else {}
    return normalized, narrative_arc


def deep_semantic_analysis_with_gemini(
    input_file: Path,
    duration_s: float,
    model: str,
    api_key: str,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    from google import genai

    client = genai.Client(api_key=api_key)
    uploaded_file = client.files.upload(file=str(input_file))

    # Best-effort wait for file processing where SDK exposes state.
    for _ in range(30):
        state = getattr(uploaded_file, "state", None)
        state_name = str(getattr(state, "name", state) or "")
        if not state_name or state_name.upper() in {"ACTIVE", "READY"}:
            break
        if state_name.upper() in {"FAILED", "ERROR"}:
            raise RuntimeError(f"Gemini file processing failed: {state_name}")
        time.sleep(1.0)
        name = getattr(uploaded_file, "name", None)
        if name:
            uploaded_file = client.files.get(name=name)

    response = client.models.generate_content(
        model=model,
        contents=[uploaded_file, build_gemini_prompt(duration_s)],
        config={
            "temperature": 0.1,
            "response_mime_type": "application/json",
        },
    )

    text = getattr(response, "text", "") or ""
    parsed = extract_json_object(text)
    segments, narrative_arc = normalize_gemini_segments(parsed, duration_s=duration_s)
    return segments, narrative_arc


def fallback_semantic_from_scenes(scenes: list[dict[str, float]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    segments: list[dict[str, Any]] = []
    for i, sc in enumerate(scenes, start=1):
        segments.append(
            {
                "start_s": sc["start_s"],
                "end_s": sc["end_s"],
                "label": f"Scene {i}",
                "description": "Auto-generated segment from visual/audio boundaries.",
                "emotion": "other",
                "narrative_role": "other",
                "visual_style": "unknown",
                "audio": {
                    "has_dialogue": False,
                    "dialogue_summary": "",
                    "language": "unknown",
                    "word_count": 0,
                    "music_present": False,
                },
                "confidence": 0.45,
            }
        )
    return segments, {
        "pattern": "unknown",
        "structure_type": "unknown",
        "viral_elements": [],
    }


def nearest_value(values: list[float], target: float, tolerance: float) -> float | None:
    if not values:
        return None
    best = min(values, key=lambda x: abs(x - target))
    if abs(best - target) <= tolerance:
        return best
    return None


def fuse_boundaries(
    duration_s: float,
    visual_scenes: list[dict[str, float]],
    silences: list[dict[str, float]],
    semantic_segments: list[dict[str, Any]],
) -> list[Boundary]:
    visual_boundaries = sorted(
        {
            round(scene["end_s"], 3)
            for scene in visual_scenes
            if 0.05 < scene["end_s"] < duration_s - 0.05
        }
    )
    silence_mids = sorted(
        {
            round(sil["mid_s"], 3)
            for sil in silences
            if 0.05 < sil["mid_s"] < duration_s - 0.05
        }
    )

    anchors: list[float] = []
    for seg in semantic_segments:
        end_s = float(seg.get("end_s", 0.0))
        if 0.05 < end_s < duration_s - 0.05:
            anchors.append(round(end_s, 3))

    if not anchors:
        anchors = list(visual_boundaries)

    raw: list[Boundary] = []
    for anchor in anchors:
        visual = nearest_value(visual_boundaries, anchor, tolerance=2.0)
        silence = nearest_value(silence_mids, anchor, tolerance=2.0)

        if visual is not None and silence is not None and abs(visual - silence) < 0.5:
            raw.append(Boundary(time_s=silence, source="visual_scene_change + silence_snap"))
        elif visual is not None:
            raw.append(Boundary(time_s=visual, source="visual_scene_change"))
        elif silence is not None:
            raw.append(Boundary(time_s=silence, source="silence_midpoint"))
        else:
            raw.append(Boundary(time_s=anchor, source="semantic_estimate"))

    raw.sort(key=lambda b: b.time_s)

    merged: list[Boundary] = []
    for b in raw:
        if not merged or abs(b.time_s - merged[-1].time_s) >= 0.6:
            merged.append(b)

    return merged


def overlap_len(a0: float, a1: float, b0: float, b1: float) -> float:
    return max(0.0, min(a1, b1) - max(a0, b0))


def match_semantic_segment(start_s: float, end_s: float, semantic_segments: list[dict[str, Any]]) -> dict[str, Any] | None:
    if not semantic_segments:
        return None
    best = None
    best_overlap = -1.0
    for seg in semantic_segments:
        ov = overlap_len(start_s, end_s, seg["start_s"], seg["end_s"])
        if ov > best_overlap:
            best_overlap = ov
            best = seg
    return best


def build_output_segments(
    duration_s: float,
    fps: float,
    boundaries: list[Boundary],
    semantic_segments: list[dict[str, Any]],
    silences: list[dict[str, float]],
) -> list[dict[str, Any]]:
    cut_times = [0.0] + [b.time_s for b in boundaries] + [duration_s]
    cut_sources = ["video_start"] + [b.source for b in boundaries] + ["video_end"]

    segments: list[dict[str, Any]] = []
    for i in range(len(cut_times) - 1):
        start_s = round(cut_times[i], 3)
        end_s = round(cut_times[i + 1], 3)
        if end_s - start_s < 0.25:
            continue

        semantic = match_semantic_segment(start_s, end_s, semantic_segments) or {}

        seg_duration = end_s - start_s
        silence_dur = 0.0
        for sil in silences:
            silence_dur += overlap_len(start_s, end_s, sil["start_s"], sil["end_s"])
        silence_ratio = round(clamp(silence_dur / max(seg_duration, 1e-6), 0.0, 1.0), 3)

        audio_meta = semantic.get("audio", {}) if isinstance(semantic.get("audio"), dict) else {}
        has_dialogue = bool(audio_meta.get("has_dialogue", silence_ratio < 0.9))

        segment = {
            "id": f"seg_{i + 1:02d}",
            "start": {
                "time_s": start_s,
                "frame": int(round(start_s * fps)),
                "nearest_keyframe_s": start_s,
                "cut_source": cut_sources[i],
            },
            "end": {
                "time_s": end_s,
                "frame": int(round(end_s * fps)),
                "nearest_keyframe_s": end_s,
                "cut_source": cut_sources[i + 1],
            },
            "duration_s": round(seg_duration, 3),
            "label": semantic.get("label", f"Segment {i + 1}"),
            "description": semantic.get("description", "Auto-generated segment."),
            "emotion": semantic.get("emotion", "other"),
            "narrative_role": semantic.get("narrative_role", "other"),
            "visual_style": semantic.get("visual_style", "unknown"),
            "audio": {
                "has_dialogue": has_dialogue,
                "dialogue_summary": audio_meta.get("dialogue_summary", ""),
                "language": audio_meta.get("language", "unknown"),
                "word_count": int(audio_meta.get("word_count", 0) or 0),
                "silence_ratio": silence_ratio,
                "music_present": bool(audio_meta.get("music_present", False)),
            },
            "confidence": round(float(semantic.get("confidence", 0.55)), 3),
            "cut_precision": "smart_cut",
        }
        segments.append(segment)

    if not segments:
        segments.append(
            {
                "id": "seg_01",
                "start": {
                    "time_s": 0.0,
                    "frame": 0,
                    "nearest_keyframe_s": 0.0,
                    "cut_source": "video_start",
                },
                "end": {
                    "time_s": round(duration_s, 3),
                    "frame": int(round(duration_s * fps)),
                    "nearest_keyframe_s": round(duration_s, 3),
                    "cut_source": "video_end",
                },
                "duration_s": round(duration_s, 3),
                "label": "Full Video",
                "description": "Fallback single segment.",
                "emotion": "other",
                "narrative_role": "other",
                "visual_style": "unknown",
                "audio": {
                    "has_dialogue": False,
                    "dialogue_summary": "",
                    "language": "unknown",
                    "word_count": 0,
                    "silence_ratio": 0.0,
                    "music_present": False,
                },
                "confidence": 0.4,
                "cut_precision": "smart_cut",
            }
        )

    return segments


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Smart Segmenter MVP")
    parser.add_argument("--input", required=True, type=Path, help="Input video file path")
    parser.add_argument("--output", required=True, type=Path, help="Output segments JSON file path")
    parser.add_argument("--deep", action="store_true", help="Enable deep semantic mode with Gemini")
    parser.add_argument("--fast", action="store_true", help="Enable fast analysis mode")
    parser.add_argument("--model", default="gemini-2.5-flash", help="Gemini model for --deep")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.deep and args.fast:
        print("--deep and --fast are mutually exclusive", file=sys.stderr)
        return 2

    input_file: Path = args.input
    output_file: Path = args.output
    output_file.parent.mkdir(parents=True, exist_ok=True)

    if not input_file.exists():
        print(f"Input not found: {input_file}", file=sys.stderr)
        return 2

    started_at = time.time()
    warnings: list[str] = []

    try:
        source_meta = probe_video(input_file)
        duration_s = float(source_meta["duration_s"])
        fps = float(source_meta["fps"])

        tmp_dir = output_file.parent / ".segment_tmp"
        tmp_dir.mkdir(parents=True, exist_ok=True)

        audio_file = None
        if source_meta["has_audio"]:
            audio_file = extract_audio(input_file, tmp_dir=tmp_dir)

        visual_scenes, visual_method = detect_visual_scenes(
            input_file,
            duration_s=duration_s,
            fps=fps,
            fast=args.fast,
        )

        silences = detect_silence(audio_file)

        semantic_segments: list[dict[str, Any]] = []
        narrative_arc: dict[str, Any] = {
            "pattern": "unknown",
            "structure_type": "unknown",
            "viral_elements": [],
        }
        gemini_segments_count = 0

        if args.deep:
            api_key = os.environ.get("GEMINI_API_KEY", "").strip()
            if not api_key:
                warnings.append("--deep requested but GEMINI_API_KEY is missing; using fallback semantic segments")
            else:
                try:
                    semantic_segments, narrative_arc = deep_semantic_analysis_with_gemini(
                        input_file=input_file,
                        duration_s=duration_s,
                        model=args.model,
                        api_key=api_key,
                    )
                    gemini_segments_count = len(semantic_segments)
                except Exception as exc:
                    warnings.append(f"Gemini deep analysis failed: {exc}")

        if not semantic_segments:
            semantic_segments, fallback_arc = fallback_semantic_from_scenes(visual_scenes)
            if narrative_arc.get("pattern") == "unknown":
                narrative_arc = fallback_arc

        boundaries = fuse_boundaries(
            duration_s=duration_s,
            visual_scenes=visual_scenes,
            silences=silences,
            semantic_segments=semantic_segments,
        )

        segments = build_output_segments(
            duration_s=duration_s,
            fps=fps,
            boundaries=boundaries,
            semantic_segments=semantic_segments,
            silences=silences,
        )

        processing_time_s = round(time.time() - started_at, 3)
        total_words = sum(seg.get("audio", {}).get("word_count", 0) for seg in semantic_segments)

        output = {
            "version": "1.0",
            "source": {
                "file": input_file.name,
                "duration_s": round(duration_s, 3),
                "fps": fps,
                "codec": source_meta["codec"],
                "resolution": source_meta["resolution"],
                "has_audio": bool(source_meta["has_audio"]),
                "keyframe_count": int(source_meta["keyframe_count"]),
                "keyframe_interval_avg_s": float(source_meta["keyframe_interval_avg_s"]),
            },
            "analysis": {
                "visual_scenes": len(visual_scenes),
                "audio_words": int(total_words),
                "silence_segments": len(silences),
                "gemini_segments": gemini_segments_count,
                "fusion_method": "priority_rules_v1",
                "visual_method": visual_method,
                "mode": "deep" if args.deep else ("fast" if args.fast else "standard"),
                "processing_time_s": processing_time_s,
            },
            "segments": segments,
            "narrative_arc": narrative_arc,
            "warnings": warnings,
        }

        output_file.write_text(json.dumps(output, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

        print(f"Wrote {len(segments)} segments to {output_file}")
        if warnings:
            for w in warnings:
                print(f"WARN: {w}", file=sys.stderr)
        return 0

    except Exception as exc:
        print(f"Failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
