#!/usr/bin/env python3
"""
Render a local HTML preview for team-research outputs (tabs + paper-style layout).

This script is intentionally dependency-free (stdlib only) and generates a single
offline HTML file with inline CSS/JS.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import html
import json
import re
import sys
from pathlib import Path
from typing import Any


EMAIL_RE = re.compile(r"\b([A-Z0-9._%+-]+)@([A-Z0-9.-]+\.[A-Z]{2,})\b", re.IGNORECASE)


def read_text(path: str) -> str:
    return Path(path).read_text("utf-8", errors="replace")


def load_json(path: str) -> Any:
    return json.loads(read_text(path))


def write_text(path: str, text: str) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def maybe_redact_emails(text: str, *, redact: bool) -> str:
    if not redact:
        return text

    def _sub(m: re.Match[str]) -> str:
        local = m.group(1)
        domain = m.group(2)
        if len(local) <= 2:
            local_mask = "***"
        else:
            local_mask = local[0] + "***" + local[-1]
        # Keep TLD shape but mask domain labels.
        parts = domain.split(".")
        if len(parts) >= 2:
            tld = parts[-1]
            domain_mask = "***." + tld
        else:
            domain_mask = "***"
        return f"{local_mask}@{domain_mask}"

    return EMAIL_RE.sub(_sub, text)


def esc(s: Any) -> str:
    if s is None:
        return ""
    return html.escape(str(s), quote=True)


def slugify(s: str) -> str:
    s = (s or "").strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s or "tab"


def md_to_html(md: str) -> str:
    """A tiny markdown subset renderer (headings, lists, code fences, inline code, paragraphs)."""
    lines = md.splitlines()
    out: list[str] = []
    in_code = False
    list_mode = None  # "ul" or "ol"

    def close_list() -> None:
        nonlocal list_mode
        if list_mode == "ul":
            out.append("</ul>")
        elif list_mode == "ol":
            out.append("</ol>")
        list_mode = None

    for raw in lines:
        line = raw.rstrip("\n")

        if line.strip().startswith("```"):
            if not in_code:
                close_list()
                out.append("<pre class=\"code\"><code>")
                in_code = True
            else:
                out.append("</code></pre>")
                in_code = False
            continue

        if in_code:
            out.append(esc(line))
            continue

        if not line.strip():
            close_list()
            out.append("<div class=\"spacer\"></div>")
            continue

        # Headings
        if line.startswith("### "):
            close_list()
            out.append(f"<h3>{esc(line[4:])}</h3>")
            continue
        if line.startswith("## "):
            close_list()
            out.append(f"<h2>{esc(line[3:])}</h2>")
            continue
        if line.startswith("# "):
            close_list()
            out.append(f"<h1>{esc(line[2:])}</h1>")
            continue

        # Ordered list "1. "
        m_ol = re.match(r"^\s*(\d+)\.\s+(.*)$", line)
        if m_ol:
            if list_mode != "ol":
                close_list()
                out.append("<ol>")
                list_mode = "ol"
            out.append(f"<li>{_inline_md(m_ol.group(2))}</li>")
            continue

        # Unordered list "- "
        m_ul = re.match(r"^\s*-\s+(.*)$", line)
        if m_ul:
            if list_mode != "ul":
                close_list()
                out.append("<ul>")
                list_mode = "ul"
            out.append(f"<li>{_inline_md(m_ul.group(1))}</li>")
            continue

        close_list()
        out.append(f"<p>{_inline_md(line)}</p>")

    close_list()
    if in_code:
        out.append("</code></pre>")
    return "\n".join(out)


def _inline_md(text: str) -> str:
    # Inline code: `...`
    parts: list[str] = []
    i = 0
    while i < len(text):
        if text[i] == "`":
            j = text.find("`", i + 1)
            if j == -1:
                parts.append(esc(text[i:]))
                break
            parts.append(f"<code>{esc(text[i + 1:j])}</code>")
            i = j + 1
            continue
        parts.append(esc(text[i]))
        i += 1
    return "".join(parts)


def zh_skill_label(skill: str) -> str:
    mapping = {
        "blog-tutorial-writer": "教程（blog-tutorial-writer）",
        "blog-list-writer": "榜单（blog-list-writer）",
        "blog-showdown-writer": "工具对决（blog-showdown-writer）",
        "case-roundup-writer": "小博文/案例短文（case-roundup-writer）",
    }
    return mapping.get(skill or "", skill or "-")


def zh_risk_label(level: str) -> str:
    m = {"LOW": "低", "MEDIUM": "中", "HIGH": "高", "PENDING": "待定"}
    return m.get((level or "").upper(), level or "-")


def zh_validation_label(val: str) -> str:
    m = {"PENDING": "待校验", "DONE": "已校验"}
    return m.get((val or "").upper(), val or "-")


def zh_constraint_label(label: str) -> str:
    # digest currently has English labels; map to Chinese.
    m = {
        "InVideo competitor": "竞品：InVideo",
        "Landing page": "落地页",
        "Official creative centers": "官方创意中心",
        "Pricing / unit economics": "单价与单位经济",
        "UGC ads mode / demo": "UGC Ads 模式与 Demo",
        "Use case library": "Use Case 库",
    }
    return m.get(label, label)


def extract_digest_constraints(context_md: str) -> list[str]:
    lines = context_md.splitlines()
    out: list[str] = []
    in_section = False
    for line in lines:
        if line.strip() == "## 3. Extracted Research Constraints":
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if not in_section:
            continue
        m = re.match(r"^\s*-\s+(.*)$", line)
        if m:
            item = m.group(1).strip()
            if item:
                out.append(item)
    return out


def build_basecamp_structure(context_json: dict[str, Any]) -> dict[int, dict[str, Any]]:
    lists = [x for x in (context_json.get("lists") or []) if isinstance(x, dict)]
    todos = [x for x in (context_json.get("todos") or []) if isinstance(x, dict)]

    todos_by_list: dict[int, list[dict[str, Any]]] = {}
    for t in todos:
        lid = t.get("list_id")
        if isinstance(lid, int):
            todos_by_list.setdefault(lid, []).append(t)

    list_by_id: dict[int, dict[str, Any]] = {}
    for li in lists:
        lid = li.get("id")
        if isinstance(lid, int):
            list_by_id[lid] = li

    # Attach todos for rendering convenience.
    for lid, li in list_by_id.items():
        li["_todos"] = sorted(todos_by_list.get(lid, []), key=lambda x: (x.get("status") or "", x.get("id") or 0))
    return list_by_id


def build_mapping_index(mapping_json: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    idx: dict[str, list[dict[str, Any]]] = {}
    for it in mapping_json.get("items") or []:
        if not isinstance(it, dict):
            continue
        did = it.get("direction_id")
        if not isinstance(did, str):
            continue
        idx[did] = [x for x in (it.get("matched_todos") or []) if isinstance(x, dict)]
    return idx


def render_preview(
    *,
    context_md: str | None,
    context_json: dict[str, Any] | None,
    directions_json: dict[str, Any] | None,
    decision_md: str | None,
    mapping_json: dict[str, Any] | None,
    redact_emails: bool,
) -> str:
    generated_at = _dt.datetime.now().strftime("%Y-%m-%d %H:%M")

    seed = (directions_json or {}).get("seed") if isinstance(directions_json, dict) else None
    seed = seed or "UGC ads"

    # constraints from digest
    constraints_raw = extract_digest_constraints(context_md or "") if context_md else []
    constraints_zh = [zh_constraint_label(x) for x in constraints_raw]

    # basecamp structured data
    list_by_id = build_basecamp_structure(context_json or {}) if context_json else {}
    sources = (context_json or {}).get("sources") if isinstance(context_json, dict) else None
    sources = sources or []
    todos_count = len((context_json or {}).get("todos") or []) if isinstance(context_json, dict) else 0
    lists_count = len((context_json or {}).get("lists") or []) if isinstance(context_json, dict) else 0

    directions = (directions_json or {}).get("directions") if isinstance(directions_json, dict) else None
    directions = directions or []

    mapping_idx = build_mapping_index(mapping_json or {}) if mapping_json else {}

    # Build tabs content.
    tabs = []

    # Overview tab (Chinese summary)
    overview_cards = []
    overview_cards.append(
        f"""
        <div class="card">
          <div class="card-title">概览</div>
          <div class="kv">
            <div class="k">Seed</div><div class="v"><span class="pill">{esc(seed)}</span></div>
            <div class="k">生成时间</div><div class="v">{esc(generated_at)}</div>
            <div class="k">Basecamp Roots</div><div class="v">{len(sources)}</div>
            <div class="k">列表数</div><div class="v">{lists_count}</div>
            <div class="k">Todos 数</div><div class="v">{todos_count}</div>
            <div class="k">DataForSEO 校验</div><div class="v"><span class="pill warn">未配置，待校验</span></div>
          </div>
        </div>
        """
    )
    overview_cards.append(
        f"""
        <div class="card">
          <div class="card-title">研究约束（来自 Basecamp）</div>
          <div class="muted">这些约束用来避免研究漂移，确保方向能落回 backlog。</div>
          <ul class="chips">
            {''.join(f'<li class="chip">{esc(x)}</li>' for x in constraints_zh) if constraints_zh else '<li class="muted">未提取到约束</li>'}
          </ul>
        </div>
        """
    )
    tabs.append(("概览", "\n".join(overview_cards)))

    # Basecamp tab
    basecamp_parts = []
    basecamp_parts.append('<div class="card"><div class="card-title">Basecamp Roots</div>')
    if sources:
        basecamp_parts.append('<ul class="linklist">')
        for s in sources:
            if not isinstance(s, dict):
                continue
            name = (s.get("name") or "").strip()
            app_url = s.get("app_url") or ""
            basecamp_parts.append(f'<li><a href="{esc(app_url)}" target="_blank" rel="noreferrer">{esc(name or app_url)}</a></li>')
        basecamp_parts.append("</ul>")
    else:
        basecamp_parts.append('<div class="muted">未加载 context.json 的 sources</div>')
    basecamp_parts.append("</div>")

    # lists grouped by parent_root_id
    def parent_key(li: dict[str, Any]) -> tuple[int, int]:
        pr = li.get("parent_root_id")
        lid = li.get("id")
        return (int(pr) if isinstance(pr, int) else 0, int(lid) if isinstance(lid, int) else 0)

    all_lists = [li for li in list_by_id.values()]
    for li in sorted(all_lists, key=parent_key):
        title = (li.get("name") or "").strip()
        app_url = li.get("app_url") or ""
        todos = li.get("_todos") or []
        basecamp_parts.append('<div class="card">')
        basecamp_parts.append('<details open>')
        basecamp_parts.append(
            f'<summary><span class="summary-title">{esc(title or "未命名列表")}</span>'
            f'<span class="summary-meta">{len(todos)} 条</span></summary>'
        )
        if app_url:
            basecamp_parts.append(f'<div class="meta"><a href="{esc(app_url)}" target="_blank" rel="noreferrer">{esc(app_url)}</a></div>')
        if not todos:
            basecamp_parts.append('<div class="muted">（空）</div>')
        else:
            basecamp_parts.append('<ul class="todo-list">')
            for t in todos:
                content = maybe_redact_emails((t.get("content") or "").strip(), redact=redact_emails)
                status = t.get("status") or ""
                app = t.get("app_url") or ""
                tid = t.get("id")
                basecamp_parts.append(
                    f'<li><span class="badge">{esc(status)}</span> '
                    f'<span class="mono">{esc(tid)}</span> '
                    f'{esc(content)}'
                    + (f' <a class="tiny" href="{esc(app)}" target="_blank" rel="noreferrer">打开</a>' if app else "")
                    + "</li>"
                )
            basecamp_parts.append("</ul>")
        basecamp_parts.append("</details>")
        basecamp_parts.append("</div>")

    # digest fallback
    if context_md:
        basecamp_parts.append('<div class="card"><div class="card-title">Basecamp Digest（原文）</div>')
        basecamp_parts.append(md_to_html(maybe_redact_emails(context_md, redact=redact_emails)))
        basecamp_parts.append("</div>")

    tabs.append(("Basecamp 背景", "\n".join(basecamp_parts)))

    # Directions tab
    dir_parts = []
    dir_parts.append('<div class="card"><div class="card-title">方向集（中文为主，附英文标题）</div>')
    dir_parts.append('<div class="muted">每个方向都映射到 Basecamp todo，方便闭环推进。</div></div>')

    for d in directions:
        if not isinstance(d, dict):
            continue
        did = d.get("direction_id") or d.get("id") or "-"
        angle_cn = maybe_redact_emails(d.get("angle_cn") or "", redact=redact_emails)
        titles = d.get("english_titles") if isinstance(d.get("english_titles"), list) else []
        target = maybe_redact_emails(d.get("target_audience") or "", redact=redact_emails)
        deliverable = maybe_redact_emails(d.get("deliverable") or "", redact=redact_emails)
        rec = d.get("recommended_skill") or ""
        risk = ((d.get("risk") or {}).get("cannibalization")) if isinstance(d.get("risk"), dict) else None
        risk = risk or "-"
        val = ((d.get("validation") or {}).get("dataforseo")) if isinstance(d.get("validation"), dict) else None
        val = val or "-"

        mapped = mapping_idx.get(str(did), [])
        pinned_ids = []
        trace = d.get("basecamp_trace")
        if isinstance(trace, dict) and isinstance(trace.get("todo_ids"), list):
            pinned_ids = [x for x in trace.get("todo_ids") if isinstance(x, int)]

        dir_parts.append('<div class="card direction">')
        dir_parts.append('<div class="direction-head">')
        dir_parts.append(f'<div class="direction-id mono">{esc(did)}</div>')
        dir_parts.append(f'<div class="pills"><span class="pill">{esc(zh_skill_label(rec))}</span>'
                         f'<span class="pill soft">蚕食风险：{esc(zh_risk_label(risk))}</span>'
                         f'<span class="pill soft">校验：{esc(zh_validation_label(val))}</span></div>')
        dir_parts.append("</div>")

        if angle_cn:
            angle_html = esc(angle_cn)
        else:
            angle_html = '<span class="muted">（缺少中文角度）</span>'
        dir_parts.append(f'<div class="direction-angle">{angle_html}</div>')

        if titles:
            dir_parts.append('<div class="subhead">英文标题候选</div>')
            dir_parts.append('<ul class="linklist">')
            for t in titles:
                if isinstance(t, str) and t.strip():
                    dir_parts.append(f"<li>{esc(t.strip())}</li>")
            dir_parts.append("</ul>")

        if target:
            dir_parts.append('<div class="subhead">目标受众</div>')
            dir_parts.append(f'<div class="text">{esc(target)}</div>')

        if deliverable:
            dir_parts.append('<div class="subhead">交付物</div>')
            dir_parts.append(f'<div class="text">{esc(deliverable)}</div>')

        # Mapping display
        dir_parts.append('<div class="subhead">Basecamp 对应</div>')
        if not mapped and pinned_ids:
            dir_parts.append('<div class="muted">（仅有 pinned todo，但映射文件未加载）</div>')
        if not mapped and not pinned_ids:
            dir_parts.append('<div class="muted">（无匹配 todo）</div>')
        else:
            dir_parts.append('<details>')
            dir_parts.append(f'<summary>查看匹配的 todos（{len(mapped)} 条）</summary>')
            dir_parts.append('<ul class="todo-list">')
            for mt in mapped:
                content = maybe_redact_emails(mt.get("content") or "", redact=redact_emails)
                conf = mt.get("confidence")
                appu = mt.get("app_url") or ""
                tid = mt.get("todo_id")
                rat = mt.get("rationale") or ""
                dir_parts.append(
                    f'<li><span class="mono">{esc(tid)}</span> '
                    f'<span class="pill tiny">{esc(conf)}</span> '
                    f'{esc(content)}'
                    + (f' <a class="tiny" href="{esc(appu)}" target="_blank" rel="noreferrer">打开</a>' if appu else "")
                    + (f'<div class="muted tiny">理由：{esc(rat)}</div>' if rat else "")
                    + "</li>"
                )
            dir_parts.append("</ul>")
            dir_parts.append("</details>")

        dir_parts.append("</div>")

    tabs.append(("方向集", "\n".join(dir_parts)))

    # Decision tab
    decision_parts = []
    decision_parts.append('<div class="card"><div class="card-title">决策简报</div>')
    decision_parts.append('<div class="muted">这是下一步行动的最短路径建议。</div></div>')
    if decision_md:
        decision_parts.append('<div class="card">')
        decision_parts.append(md_to_html(maybe_redact_emails(decision_md, redact=redact_emails)))
        decision_parts.append("</div>")
    else:
        decision_parts.append('<div class="card"><div class="muted">未提供 decision brief 文件</div></div>')
    tabs.append(("决策简报", "\n".join(decision_parts)))

    # Mapping tab (table)
    map_parts = []
    map_parts.append('<div class="card"><div class="card-title">方向到 Todo 映射</div>')
    map_parts.append('<div class="muted">支持搜索过滤（按方向ID / todo 文本）。</div></div>')

    map_rows = []
    for d in directions:
        if not isinstance(d, dict):
            continue
        did = str(d.get("direction_id") or d.get("id") or "")
        for mt in mapping_idx.get(did, []):
            map_rows.append(
                {
                    "direction_id": did,
                    "todo_id": mt.get("todo_id"),
                    "confidence": mt.get("confidence"),
                    "content": maybe_redact_emails(mt.get("content") or "", redact=redact_emails),
                    "app_url": mt.get("app_url") or "",
                    "rationale": mt.get("rationale") or "",
                }
            )

    map_parts.append(
        """
        <div class="card">
          <div class="filters">
            <input id="filterBox" type="text" placeholder="搜索方向ID / todo 内容..." />
            <div class="muted tiny" id="filterMeta"></div>
          </div>
          <div class="table-wrap">
            <table class="tbl" id="mapTable">
              <thead>
                <tr>
                  <th>方向ID</th>
                  <th>Todo</th>
                  <th>置信度</th>
                  <th>理由</th>
                </tr>
              </thead>
              <tbody>
        """
    )
    for r in map_rows:
        todo_cell = f'<span class="mono">{esc(r["todo_id"])}</span> {esc(r["content"])}'
        if r["app_url"]:
            todo_cell += f' <a class="tiny" href="{esc(r["app_url"])}" target="_blank" rel="noreferrer">打开</a>'
        map_parts.append(
            "<tr>"
            f'<td class="mono">{esc(r["direction_id"])}</td>'
            f"<td>{todo_cell}</td>"
            f'<td><span class="pill tiny">{esc(r["confidence"])}</span></td>'
            f'<td class="muted tiny">{esc(r["rationale"])}</td>'
            "</tr>"
        )
    map_parts.append(
        """
              </tbody>
            </table>
          </div>
        </div>
        """
    )
    tabs.append(("映射", "\n".join(map_parts)))

    # Appendix tab
    appendix_parts = []
    appendix_parts.append('<div class="card"><div class="card-title">附录</div>')
    appendix_parts.append('<div class="muted">输入文件、复现命令与校验提示。</div></div>')

    appendix_parts.append(
        """
        <div class="card">
          <div class="card-title">下一步（DataForSEO）</div>
          <ul>
            <li>当前环境未配置 DataForSEO，方向集的 SERP/Volume/Title Lock 仍处于“待校验”。</li>
            <li>建议优先校验：D01（新手工作流）、D05（落地页拆解）、D08（模型对决）的关键词与 SERP 形式。</li>
          </ul>
        </div>
        """
    )

    tabs.append(("附录", "\n".join(appendix_parts)))

    # Tab navigation HTML
    stable_tab_key = {
        "概览": "overview",
        "Basecamp 背景": "basecamp",
        "方向集": "directions",
        "决策简报": "decision",
        "映射": "mapping",
        "附录": "appendix",
    }
    tab_ids = [
        f"tab-{stable_tab_key.get(name, f'section-{i+1}')}" for i, (name, _body) in enumerate(tabs)
    ]
    nav_items = []
    for (name, _), tid in zip(tabs, tab_ids):
        nav_items.append(f'<button class="tab" data-tab="{esc(tid)}">{esc(name)}</button>')

    tab_panels = []
    for (name, body), tid in zip(tabs, tab_ids):
        tab_panels.append(f'<section class="panel" id="{esc(tid)}">{body}</section>')

    title = f"UGC Ads 研究预览（{seed}）"

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{esc(title)}</title>
  <style>
    :root {{
      --bg0: #f3efe6;
      --bg1: #f7f1e1;
      --paper: #fbf6ea;
      --paper2: #f7f1e1;
      --ink: #1f2328;
      --muted: rgba(31,35,40,0.68);
      --line: rgba(31,35,40,0.12);
      --shadow: 0 10px 28px rgba(0,0,0,0.08);
      --shadow2: 0 4px 14px rgba(0,0,0,0.08);
      --accent: #2f6f5f;
      --warn: #a46a10;
      --mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
      --serif: ui-serif, "Iowan Old Style", "Palatino Linotype", Palatino, "Noto Serif CJK SC", "Songti SC", STSong, serif;
      --sans: ui-sans-serif, system-ui, -apple-system, "Segoe UI", "Noto Sans CJK SC", "PingFang SC", "Hiragino Sans GB", Arial, sans-serif;
    }}
    * {{ box-sizing: border-box; }}
    html, body {{ height: 100%; }}
    body {{
      margin: 0;
      color: var(--ink);
      font-family: var(--sans);
      background:
        radial-gradient(1200px 800px at 10% 10%, rgba(47,111,95,0.08), transparent 60%),
        radial-gradient(900px 700px at 90% 20%, rgba(164,106,16,0.08), transparent 55%),
        linear-gradient(180deg, var(--bg0), #ffffff 60%, var(--bg0));
    }}
    .wrap {{
      max-width: 1120px;
      margin: 28px auto 64px;
      padding: 0 18px;
    }}
    header {{
      display: flex;
      gap: 16px;
      align-items: baseline;
      justify-content: space-between;
      padding: 18px 18px;
      border: 1px solid var(--line);
      border-radius: 14px;
      background: linear-gradient(180deg, var(--paper), var(--paper2));
      box-shadow: var(--shadow2);
    }}
    .title {{
      font-family: var(--serif);
      letter-spacing: 0.2px;
      line-height: 1.1;
    }}
    .title h1 {{
      margin: 0;
      font-size: 22px;
      font-weight: 700;
    }}
    .title .sub {{
      margin-top: 6px;
      font-size: 12px;
      color: var(--muted);
    }}
    .tabs {{
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      align-items: center;
      justify-content: flex-end;
    }}
    .tab {{
      appearance: none;
      border: 1px solid var(--line);
      background: rgba(255,255,255,0.6);
      padding: 8px 10px;
      border-radius: 999px;
      font-size: 13px;
      cursor: pointer;
      transition: transform 120ms ease, background 120ms ease, border-color 120ms ease;
      color: var(--ink);
    }}
    .tab:hover {{ transform: translateY(-1px); border-color: rgba(31,35,40,0.22); }}
    .tab.active {{
      background: rgba(47,111,95,0.12);
      border-color: rgba(47,111,95,0.35);
    }}
    main {{ margin-top: 16px; }}
    .panel {{ display: none; }}
    .panel.active {{ display: block; }}
    .card {{
      border: 1px solid var(--line);
      border-radius: 14px;
      background: linear-gradient(180deg, var(--paper), var(--paper2));
      box-shadow: var(--shadow2);
      padding: 16px 16px;
      margin: 14px 0;
    }}
    .card-title {{
      font-family: var(--serif);
      font-size: 14px;
      font-weight: 700;
      letter-spacing: 0.2px;
      margin-bottom: 10px;
    }}
    .muted {{ color: var(--muted); }}
    .tiny {{ font-size: 12px; }}
    .mono {{ font-family: var(--mono); }}
    .pill {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 10px;
      border-radius: 999px;
      border: 1px solid var(--line);
      background: rgba(255,255,255,0.55);
      font-size: 12px;
      white-space: nowrap;
    }}
    .pill.warn {{ border-color: rgba(164,106,16,0.35); background: rgba(164,106,16,0.10); color: #6b470c; }}
    .pill.soft {{ background: rgba(255,255,255,0.35); }}
    .pill.tiny {{ padding: 2px 8px; font-size: 11px; }}
    .chips {{ list-style: none; padding: 0; margin: 10px 0 0; display: flex; flex-wrap: wrap; gap: 8px; }}
    .chip {{
      border: 1px solid var(--line);
      background: rgba(255,255,255,0.45);
      border-radius: 999px;
      padding: 6px 10px;
      font-size: 12px;
    }}
    .kv {{
      display: grid;
      grid-template-columns: 120px 1fr;
      gap: 10px 12px;
      align-items: baseline;
    }}
    .kv .k {{ color: var(--muted); font-size: 12px; }}
    .kv .v {{ font-size: 13px; }}
    a {{ color: var(--accent); text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .linklist {{ margin: 0; padding-left: 18px; }}
    .todo-list {{ margin: 10px 0 0; padding-left: 18px; }}
    .badge {{
      display: inline-block;
      padding: 2px 8px;
      border-radius: 999px;
      border: 1px solid var(--line);
      background: rgba(255,255,255,0.45);
      font-size: 11px;
      color: var(--muted);
      margin-right: 6px;
    }}
    details > summary {{
      cursor: pointer;
      list-style: none;
      display: flex;
      gap: 10px;
      align-items: baseline;
      justify-content: space-between;
    }}
    details > summary::-webkit-details-marker {{ display: none; }}
    .summary-title {{
      font-family: var(--serif);
      font-weight: 700;
    }}
    .summary-meta {{
      color: var(--muted);
      font-size: 12px;
    }}
    .meta {{ margin-top: 6px; font-size: 12px; color: var(--muted); }}
    .spacer {{ height: 8px; }}
    h1, h2, h3 {{ margin: 10px 0; font-family: var(--serif); }}
    h1 {{ font-size: 18px; }}
    h2 {{ font-size: 15px; }}
    h3 {{ font-size: 13px; }}
    p {{ margin: 8px 0; line-height: 1.6; }}
    code {{
      font-family: var(--mono);
      font-size: 0.92em;
      padding: 0.1em 0.35em;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: rgba(255,255,255,0.45);
    }}
    pre.code {{
      overflow: auto;
      padding: 12px;
      border-radius: 12px;
      border: 1px solid var(--line);
      background: rgba(255,255,255,0.45);
      box-shadow: inset 0 1px 0 rgba(255,255,255,0.6);
    }}
    pre.code code {{
      border: none;
      background: transparent;
      padding: 0;
      font-size: 12px;
      line-height: 1.5;
      display: block;
      white-space: pre;
    }}
    .direction-head {{
      display: flex;
      gap: 12px;
      align-items: flex-start;
      justify-content: space-between;
    }}
    .direction-id {{
      font-size: 12px;
      color: var(--muted);
      letter-spacing: 0.2px;
    }}
    .direction-angle {{
      margin-top: 10px;
      font-size: 14px;
      line-height: 1.7;
    }}
    .subhead {{
      margin-top: 12px;
      font-size: 12px;
      color: var(--muted);
      letter-spacing: 0.2px;
    }}
    .text {{ margin-top: 6px; line-height: 1.6; }}
    .filters {{
      display: flex;
      gap: 10px;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 10px;
    }}
    #filterBox {{
      flex: 1;
      border: 1px solid var(--line);
      border-radius: 12px;
      padding: 10px 12px;
      font-size: 13px;
      background: rgba(255,255,255,0.55);
      outline: none;
    }}
    #filterBox:focus {{ border-color: rgba(47,111,95,0.35); box-shadow: 0 0 0 4px rgba(47,111,95,0.08); }}
    .table-wrap {{ overflow: auto; border-radius: 12px; border: 1px solid var(--line); }}
    table.tbl {{
      width: 100%;
      border-collapse: collapse;
      min-width: 860px;
      background: rgba(255,255,255,0.35);
    }}
    .tbl th, .tbl td {{
      padding: 10px 12px;
      border-bottom: 1px solid rgba(31,35,40,0.10);
      vertical-align: top;
      font-size: 13px;
    }}
    .tbl th {{
      position: sticky;
      top: 0;
      background: rgba(251,246,234,0.98);
      text-align: left;
      font-family: var(--serif);
      font-size: 12px;
      letter-spacing: 0.2px;
    }}
    .tbl tr:hover td {{ background: rgba(47,111,95,0.05); }}

    @media (max-width: 720px) {{
      header {{ flex-direction: column; align-items: flex-start; }}
      .tabs {{ justify-content: flex-start; }}
      .kv {{ grid-template-columns: 100px 1fr; }}
    }}
  </style>
</head>
<body>
  <div class="wrap">
    <header>
      <div class="title">
        <h1>{esc(title)}</h1>
        <div class="sub">本地预览（离线单文件），最后更新：{esc(generated_at)}</div>
      </div>
      <nav class="tabs" id="tabs">
        {''.join(nav_items)}
      </nav>
    </header>
    <main>
      {''.join(tab_panels)}
    </main>
  </div>
  <script>
    (function() {{
      const tabs = Array.from(document.querySelectorAll('.tab'));
      const panels = Array.from(document.querySelectorAll('.panel'));
      function setActive(tabId) {{
        tabs.forEach(b => b.classList.toggle('active', b.dataset.tab === tabId));
        panels.forEach(p => p.classList.toggle('active', p.id === tabId));
        try {{
          localStorage.setItem('team_research_active_tab', tabId);
        }} catch (e) {{}}
        const url = new URL(window.location.href);
        url.hash = 'tab=' + encodeURIComponent(tabId);
        history.replaceState(null, '', url.toString());
      }}
      function resolveInitial() {{
        const h = (window.location.hash || '').replace(/^#/, '');
        if (h.startsWith('tab=')) {{
          const id = decodeURIComponent(h.slice(4));
          if (document.getElementById(id)) return id;
        }}
        try {{
          const saved = localStorage.getItem('team_research_active_tab');
          if (saved && document.getElementById(saved)) return saved;
        }} catch (e) {{}}
        return panels[0]?.id;
      }}
      tabs.forEach(b => b.addEventListener('click', () => setActive(b.dataset.tab)));
      const initial = resolveInitial();
      if (initial) setActive(initial);

      // Mapping filter
      const box = document.getElementById('filterBox');
      const table = document.getElementById('mapTable');
      const meta = document.getElementById('filterMeta');
      if (box && table) {{
        function applyFilter() {{
          const q = (box.value || '').toLowerCase().trim();
          const rows = Array.from(table.querySelectorAll('tbody tr'));
          let visible = 0;
          rows.forEach(r => {{
            const text = r.innerText.toLowerCase();
            const ok = !q || text.includes(q);
            r.style.display = ok ? '' : 'none';
            if (ok) visible++;
          }});
          if (meta) meta.textContent = q ? ('显示 ' + visible + ' / ' + rows.length + ' 条') : ('共 ' + rows.length + ' 条');
        }}
        box.addEventListener('input', applyFilter);
        applyFilter();
      }}
    }})();
  </script>
</body>
</html>
"""


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Render a local HTML preview for team research outputs.")
    parser.add_argument("--context-md", required=True, help="Path to Basecamp digest context.md")
    parser.add_argument("--context-json", required=False, default=None, help="Path to normalized context.json (optional)")
    parser.add_argument("--directions-json", required=True, help="Path to 03-team-directions.json")
    parser.add_argument("--decision-md", required=True, help="Path to 04-decision-brief.md")
    parser.add_argument("--mapping-json", required=True, help="Path to 05-basecamp-mapping.json")
    parser.add_argument("--out", required=True, help="Output HTML path")
    parser.add_argument("--redact-emails", action="store_true", help="Redact email addresses in rendered content")
    args = parser.parse_args(argv)

    missing = []

    def exists(p: str | None) -> bool:
        return bool(p) and Path(p).exists()

    if not exists(args.context_md):
        missing.append(args.context_md)
    if not exists(args.directions_json):
        missing.append(args.directions_json)
    if not exists(args.decision_md):
        missing.append(args.decision_md)
    if not exists(args.mapping_json):
        missing.append(args.mapping_json)
    if missing:
        print("❌ Missing required input files:", file=sys.stderr)
        for m in missing:
            print(f"- {m}", file=sys.stderr)
        return 2

    context_md = read_text(args.context_md)
    context_json = load_json(args.context_json) if exists(args.context_json) else None
    directions_json = load_json(args.directions_json)
    decision_md = read_text(args.decision_md)
    mapping_json = load_json(args.mapping_json)

    html_doc = render_preview(
        context_md=context_md,
        context_json=context_json,
        directions_json=directions_json,
        decision_md=decision_md,
        mapping_json=mapping_json,
        redact_emails=bool(args.redact_emails),
    )
    write_text(args.out, html_doc)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
