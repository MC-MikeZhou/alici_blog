# Transcript Analysis: The ONLY 7 Prompts You Need for AI Video

**Video ID**: zzBmvzR-URg
**Video URL**: https://www.youtube.com/watch?v=zzBmvzR-URg
**Analysis Date**: 2026-01-26
**Transcript Entries**: 467

---

## Executive Summary

This video presents **7 core prompting styles** for AI video generation, emphasizing a simple, clear, and intentional approach over complicated prompts. The tutorial is built around the **image-to-video workflow** using Google Veo 3 (though techniques apply to Sora 2, Kling, and other models). The creator demonstrates that best results come from combining multiple prompt styles strategically.

**Key Philosophy**: "The best AI videos aren't made using complicated prompts. They're generated using simple, clear, intentional prompts that the AI models actually respond to."

---

## 7 Prompt Styles Summary

### 1. Cinematic Prompts (Camera Work)
**Focus**: Controlling camera movement throughout the scene
**Key Insight**: "It's not just about what you're seeing, but how you're observing it."

**Camera Movements**:
- **Static shot** - Camera stays perfectly still (peace, contemplation)
- **Zoom in + rotate** - Personal, focused on facial expressions
- **Pan** - Follow subject as it moves
- **Shaky handheld** - Chaotic, immersive environment
- **Bird's eye view** - Cold, detached perspective
- **Orbit/rotate** - "The camera rotates" or "the camera orbits" for circular motion
- **Tilt up/down** - Vertical camera movement
- **Camera pullback** - Reveal wider context

**Example Prompts**:
- "Static shot of a soldier on a battlefield, camera stays perfectly still"
- "Zoom in and rotate around to focus on his face"
- "Camera flies above to a bird's eye view"
- "Shaky handheld camera highlights the chaotic environment"

**Best Practice**: Can combine different camera motions together

---

### 2. Timestamp Prompting (Sequential Control)
**Focus**: Divide AI video into multiple segments with different actions per segment
**Key Insight**: "We can actually tell the AI video generator exactly what motions to happen along each segment"

**Example - 8-second astronaut video**:
- **0-3 seconds**: Camera zooms in towards astronaut
- **3-5 seconds**: Camera tilts down to show recording device
- **5-8 seconds**: Camera tilts back up to see astronaut looking at sky

**Second Example - Astronaut + creature**:
- **First segment**: "Camera zooming to an over-the-shoulder shot of the astronaut"
- **Second segment**: "Zoom in closely on the creature in space"

**Use Case**: Best way to organize multiple actions happening inside a scene
**Benefit**: "A lot more control over the sequence of events that are happening and exactly how you want them to happen"

---

### 3. Cutscene Prompting (Multiple Angles)
**Focus**: Generate multiple camera angles in a single AI video
**Key Insight**: "This video shows a full body of the astronaut turning and walking towards a spaceship. But then it cuts to a close-up shot of his footsteps."

**Example Prompt**:
```
"The astronaut turns and walks towards a spaceship."
Cut to the boots of the astronaut walking along the terrain inside a cinematic film
```

**Three-Segment Example**:
- Segment 1: Astronaut on alien world (wide shot)
- Segment 2: Close-up of his expression of wonder and awe
- Segment 3: Final shot of him exploring the planet

**Implementation**: Combine with timestamp prompting for maximum control
**Effect**: "Turns AI video generator into a storyboard tool or video editor"

**LIMITATION - Critical Warning**:
- If you prompt for cuts that are completely different from original video
- Or requires AI to imagine a lot of new things (e.g., "inside the mouth of the plant")
- AI has "a hard time maintaining consistency in the video style"
- Can shift from realistic to 3D animated style unexpectedly
- **Best Practice**: "Make sure the scene you're cutting to isn't too overly different from your original shot"

---

### 4. GPT Prompts (AI-Assisted Prompting)
**Focus**: Use AI language models to help write prompts
**Attribution**: "I learned this from the AI video school channel"

**Workflow**:
1. Get prompt documentation from AI video model (e.g., Google Veo 3 manual)
2. Copy relevant information: formula, techniques, examples
3. Create custom GPT in ChatGPT Explore tab
4. Upload PDF documentation to knowledge section
5. Give GPT job description: "prompt helper that writes prompts for Google Veo 3"
6. User enters scene description → GPT generates detailed prompt

**Example Output Structure**:
- Cinematography elements
- Sound effects
- Style
- Lighting
- Action happening in the scene

**ADVANTAGE**:
- Reduces time spent typing prompts
- Generates longer, detailed prompts automatically

**LIMITATIONS - Critical Issues**:

**Issue 1: Confusing Syntax**
- Example: "wide morning shot" (incorrect)
- Should be: "wide angle shot in the morning"
- Problems are "fairly minor" but require manual correction

**Issue 2: Documentation Blindspots** (MOST IMPORTANT)
- "AI documentation rarely tells you what the AI video generator is bad at"
- "The difference between being good at prompting and being bad at prompting is actually understanding the limitations of the AI video, what it can't do"
- GPT trained on incomplete information leads to unsolvable problems

**Real Example - Crowd Animation Failure**:
- GPT prompted: "crowd of angry towns folks surround her on both sides shouting and pointing"
- **What AI videos can't do well**: Animating crowds of people
- "Either they're all going to do the same thing at the same time, which happens in Veo 3, or they're just going to turn to like blobs and blur together"
- This limitation "is not mentioned in the official prompt guide from Google Veo 3"

**Better Workaround**:
```
Instead of: "crowd of angry townspeople surround her, shouting and pointing"
Use: "She looks around nervously while these people stare at her in silence in a weird eerie way"
```
- Conveys same emotion (uneasiness, fear)
- Much easier for AI to animate
- "She's in hostile territory" message comes across without complex crowd actions

**RECOMMENDATION**:
- "GPT prompt helper is very useful for more advanced users that actually understand the nuances"
- For beginners: "Stick to simpler, shorter, more intentional prompts"
- "Much easier to go in and figure things out when they don't work exactly how you expect it"

---

### 5. Anchor Prompts (Consistency Reminders)
**Focus**: Remind AI of important visual elements that shouldn't change
**Key Insight**: "AI does weird stuff. Things that seem super obvious to you are not obvious to the AI at all"

**Problem Example**:
- Prompted: "Character smiling and show happy expression"
- AI completely transformed the character's appearance
- Lost the ash and red embers covering face (important visual element)

**Solution Example 1 - Physical Appearance**:
```
"Character smiling with happy expression"
ANCHOR: "There should be red embers and ash on him"
```
Result: Happy expression + preserved visual style

**Solution Example 2 - Subject Relationship**:
- Problem: Orc character slides off wolf during fight scene
- Solution: Add anchor "the orc should be on the back riding the direwolf"
- Result: AI maintains relationship between two subjects

**Solution Example 3 - Unseen Elements**:
- Character has armor on left shoulder, blue tribal tattoo on right shoulder
- Profile shot only shows left side (armor)
- Without anchor: AI adds armor to both shoulders
- **Anchor prompt**: "The orc has no armor on the right shoulder. Dark blue geometric tribal tattoos on the orc's shoulder"
- Result: AI understands complete character appearance

**Use Case**: "Sometimes you have to use anchors to help the AI video generators understand parts of the scene that it can't see yet to understand how to generate parts of the scene later on that it can't see right now"

**Philosophy**: Won't be 100% consistent to original shot, but "by anchoring what his full appearance looks like, we can create a video where his shoulder looks a lot more like the original character"

---

### 6. Image Prompting (Reference Images)
**Focus**: Use AI-generated images as starting frames for video generation
**Key Insight**: "To maximize AI videos capabilities, you got to use image prompting"

**Why Image Prompting**:
- "To get the most beautiful shots, like these surrealistic scenes, it's really only possible to do this consistently if you're using image prompts"
- Best way to get multiple shots of consistent character
- Best way to generate multiple camera angles

**Workflow Example - Koi Fish**:
1. Generate image: "Surrealism photo, a giant koi fish in the canals of Venice City"
2. Use Kling 2.5 video generator to animate
3. Prompt: "The fish floats forwards through the air"

**Prompt Philosophy**: "Be direct and clear in exactly how you want the scene to unfold"

**Example Prompts**:
- "A city floating in the clouds. The lights blink on and off. Surrealism."
- "The giant giraffe waves in the ocean and eats leaves from the tree."
- "She blinks."
- "The paper covering falls off her face to reveal mechanical gears inside."

**Character Consistency Use Case**:
- Start with front view of character in plant store
- Use AI image model (Nomo Banana) to create:
  - Side profile studying at desk
  - Photo watering plants
  - Lunch break looking out window
- Generate multiple video shots using these reference images

**Advanced Tool - Q1 Image Edit Camera Angle Control**:
- Upload image reference of character
- Real-time camera controls:
  - Rotate by 45° (left or right)
  - Zoom in/out
  - Tilt up (bird's eye) or down (worm's eye)
- Note: "Textures on face are kind of smooth, need image upscaler for higher resolution or sharper details"
- Still "a pretty incredible AI image tool for controlling camera angles"

---

### 7. Start and End Frame Prompting
**Focus**: Control both beginning and end of video shot
**Description**: "Use an image for the first frame of the video but also use an image to control what's going on in the last frame of the video"

**How It Works**: "When you combine these things together, the AI video can actually render a complete scene of your character between the two frames"

**Use Case**: Join images together to control full shot trajectory

---

### 8. Negative Prompting (Tell AI What NOT to Do)
**Focus**: Easier to tell AI what you don't want than describe what you do want
**Key Insight**: "Sometimes to get what you want from the AI, it's actually easier to just tell it what you don't want to happen"

**Example 1 - Simple Removal**:
- Scene: Astronaut on lunar colony
- Problem: Moon outside window looks off, perspective wrong
- Solution: Add "no windows" to prompt
- Result: Same shot, no windows on wall

**Example 2 - Sound Control**:
- Scene: Soldier aiming weapon
- Problem: AI adds gunshots and burst of smoke from gas mask
- Wanted: Quiet scene of cautious observation
- **Heavy negative prompt**: "Completely silent and quiet and no gunshots, no clicking, no trigger"
- Result: "Sort of worked" - can hear flames in background without firing weapon

**Philosophy**: "Instead of trying to describe exactly what the wall should look like... by using this negative prompt and telling the AI what I don't want to see inside the scene, it can generate that same shot"

---

## Image-to-Video Workflow

### Core Process
The video demonstrates that all examples were created using the **image-to-video technique**:

**Step 1: Reference Image**
- Give AI video generator a reference image
- Example: "Image frame of a soldier in a trench I want to animate"

**Step 2: Descriptive Prompt**
- Enter prompt describing how scene should play out
- Can focus on subject action OR camera motion

**Example - Subject-Focused Prompt**:
- Didn't add camera motions
- Focused on subject: "Him pulling a small wooden cross from underneath his jacket"

**Key Tools Mentioned**:
- **Google Veo 3** - Primary tool demonstrated
- **Kling 2.5** - Used for surrealistic scene animation
- **Nomo Banana** - AI image model for character reference photos
- **Q1 Image Edit Camera Angle Control** - Real-time camera angle generation

### Workflow Philosophy
- Start with clear reference image
- Use simple, direct prompts
- Layer multiple prompt styles (cinematic + timestamp + cutscene + anchor)
- Keep it "simple, clear, and easy for the AI to understand"

---

## Example Prompts (Actual Prompt Text)

### Cinematic Movement Examples
```
1. "Static shot of a soldier on a battlefield. The camera stays perfectly still, highlighting a moment of peace and contemplation."

2. "Zoom in and rotate around to focus on his face" (same soldier, more personal shot)

3. "Pan to follow our subject as it rolls into the battlefield"

4. "Shaky handheld camera highlights the chaotic environment of soldiers in trench getting hit with artillery shells"

5. "Camera flies above to a bird's eye view"

6. "The camera rotates" or "the camera orbits" (circular motion)
```

### Timestamp + Cutscene Examples
```
1. Astronaut 8-second video:
   0-3s: "Camera zooms in towards him"
   3-5s: "Tilts down to show him looking at recording device"
   5-8s: "Camera tilts back up to see him looking up towards sky"

2. Astronaut + creature:
   Segment 1: "Camera zooming to an over-the-shoulder shot of the astronaut"
   Segment 2: "End the scene by zooming in closely on the creature in space"

3. Astronaut walking:
   "The astronaut turns and walks towards a spaceship. Cut to the boots of the astronaut walking along the terrain inside a cinematic film."

4. Three-segment alien planet:
   Timestamp 1: "Astronaut on an alien world" (wide shot)
   Timestamp 2: "Cut to close-up shot of his expression of wonder and awe on his face"
   Timestamp 3: "Final shot of him exploring the alien planet"
```

### Anchor Prompt Examples
```
1. Facial expression preservation:
   "Character smiling with happy expression, red embers and ash on him"

2. Subject relationship:
   "Orc on the back riding the direwolf" (during fight scene)

3. Unseen elements:
   "The orc has no armor on the right shoulder. Dark blue geometric tribal tattoos on the orc's shoulder."
```

### Image-to-Video Simple Prompts
```
1. "Him pulling a small wooden cross from underneath his jacket"

2. "The fish floats forwards through the air"

3. "A city floating in the clouds. The lights blink on and off. Surrealism."

4. "The giant giraffe waves in the ocean and eats leaves from the tree."

5. "She blinks."

6. "The paper covering falls off her face to reveal mechanical gears inside."
```

### Negative Prompt Examples
```
1. "No windows" (remove windows from wall)

2. "Completely silent and quiet and no gunshots, no clicking, no trigger" (prevent weapon firing sounds)
```

---

## Key Insights & Best Practices

### Core Philosophy
1. **Simplicity Over Complexity**
   - "The best AI videos aren't made using complicated prompts"
   - "Simple, clear, intentional prompts that the AI models actually respond to"
   - "Be direct and clear in exactly how you want the scene to unfold"

2. **Intentionality Matters**
   - Focus on what's important to convey
   - Choose camera work deliberately for emotional effect
   - Static = peaceful, shaky = chaotic, bird's eye = detached

3. **Understanding Limitations is Key**
   - "The difference between being good at prompting and being bad at prompting is actually understanding the limitations of the AI video, what it can't do"
   - Know what AI struggles with (crowds, complex actions)
   - Design prompts around these limitations

### Prompt Design Best Practices

**DO**:
- Use cinematic prompts to control emotional tone through camera work
- Combine multiple prompt styles strategically
- Use anchors to preserve important visual elements
- Start with image references for consistency
- Use negative prompts when it's easier to exclude than describe
- Keep prompts clear and direct
- For beginners: stick to simpler, shorter prompts

**DON'T**:
- Prompt for complex crowd animations
- Cut to scenes that are too different from original shot (style inconsistency)
- Assume AI understands "obvious" things (it doesn't)
- Over-rely on GPT prompt helpers without understanding limitations
- Ignore the AI model's documented weaknesses

### Layering Strategy
- **Base Layer**: Image prompt (reference frame)
- **Motion Layer**: Cinematic prompts (camera work)
- **Structure Layer**: Timestamp prompting (segments)
- **Complexity Layer**: Cutscene prompting (multiple angles)
- **Consistency Layer**: Anchor prompts (preserve elements)
- **Refinement Layer**: Negative prompts (remove unwanted)

### Emotional Control Through Camera
| Emotion/Tone | Camera Technique |
|--------------|------------------|
| Peace, Contemplation | Static shot |
| Personal, Intimate | Zoom in + rotate on face |
| Dynamic, Following | Pan with subject |
| Chaotic, Immersive | Shaky handheld |
| Detached, Cold | Bird's eye view |
| Revealing, Epic | Camera pullback |
| Focus, Intensity | Orbit/rotate around subject |

---

## Limitations & Workarounds

### Major Limitations Identified

**1. Crowd Animation** (CRITICAL)
- **Problem**: AI can't animate crowds of people performing different actions
- **Symptoms**:
  - Everyone does same thing at same time (Veo 3)
  - People turn into blobs and blur together
- **Workaround**:
  - Use static crowd staring in silence
  - Focus on main character's nervous reactions
  - Convey tension through atmosphere rather than crowd action

**2. Style Consistency in Cutscenes**
- **Problem**: Drastic scene changes can cause style shifts
- **Example**: Realistic style → 3D animated style when cutting to "inside mouth of plant"
- **Workaround**: Keep cutscenes similar to original shot environment

**3. Obvious Elements Aren't Obvious to AI**
- **Problem**: "Things that seem super obvious to you are not obvious to the AI at all"
- **Example**: Ash and embers on face get removed when prompting for smile
- **Workaround**: Use anchor prompts to explicitly preserve important elements

**4. Unseen Elements Default to Assumptions**
- **Problem**: AI generates based only on what it can see
- **Example**: Armor on one shoulder → AI adds armor to both shoulders
- **Workaround**: Anchor prompts describing complete character

**5. GPT Prompt Helper Blindspots**
- **Problem**: Official documentation doesn't include what AI is bad at
- **Impact**: GPT helpers suggest prompts that will fail
- **Workaround**:
  - Understand AI limitations yourself
  - Use GPT helpers only as starting point
  - Test and iterate based on actual results

### Technical Quality Issues

**Q1 Camera Angle Tool**:
- Textures can be smooth/low resolution
- Need image upscaler for sharper details
- But real-time generation is impressive

**Sound/Audio Issues**:
- AI adds sounds based on visual context (weapon aiming → gunshots)
- Can be difficult to suppress (negative prompts "sort of worked")
- May need multiple attempts to get desired audio result

---

## Tool Comparisons

### Models Mentioned

**Google Veo 3** (Primary)
- Used for most demonstrations
- Documentation available for prompt formulas
- Known crowd animation issue: everyone does same thing at same time

**Sora 2**
- Mentioned as compatible with techniques
- No specific examples shown

**Kling 2.5**
- Used for surrealistic koi fish scene
- Demonstrated image-to-video capability

**Cling** (likely Kling alternate spelling)
- Listed as compatible with techniques

**Veo** (likely Veo 3 short form)
- Listed as compatible

### Cross-Compatibility Statement
"By the way, the prompt techniques I'm showing work for Google Veo 3, but they can also be applied to different AI video models like Sora 2 or Seance or Cling."

**Implication**: The 7 prompt styles are model-agnostic fundamentals, not tool-specific hacks

### Supporting Tools

**AI Image Models**:
- **Nomo Banana** - Character reference generation
- **Q1 Image Edit Camera Angle Control** - Real-time camera angle generation

**ChatGPT**:
- Custom GPT creation for prompt assistance
- Explore tab → create custom GPT
- Upload documentation PDFs to knowledge section

---

## Sora 2 Specific Information

### Direct Mentions
Sora 2 is mentioned **twice** in the transcript:

1. **Tool Compatibility Statement** (Line 158):
   - "By the way, the prompt techniques I'm showing work for Google Veo 3, but they can also be applied to different AI video models like Sora 2 or Seance or Cling."

2. **Same statement repeated** (Line 483):
   - Identical phrasing in plain text version

### Implied Information About Sora 2

**What we can infer**:
- Sora 2 supports the same 7 prompt style fundamentals
- Image-to-video workflow should work with Sora 2
- Cinematic, timestamp, cutscene, GPT, anchor, image, and negative prompting apply
- Likely shares similar limitations (crowd animation, style consistency)

**What is NOT covered**:
- No Sora 2-specific examples demonstrated
- No Sora 2 unique features discussed
- No Sora 2 vs Veo 3 performance comparison
- No Sora 2-specific prompt syntax differences
- No Sora 2 prompt documentation referenced

### Takeaway for Sora 2
The video treats Sora 2 as functionally equivalent to other AI video models for the purposes of these 7 prompt techniques. The creator's focus on Google Veo 3 appears to be for demonstration purposes only, with the expectation that principles transfer directly to Sora 2.

---

## Metadata & Attribution

**Video Length**: ~18 minutes (based on 467 transcript entries)
**Content Type**: Tutorial / Educational
**Production Quality**: High (multiple example scenes, soldier/astronaut/orc character demonstrations)
**Teaching Style**: Demonstration-first, principle-second

**Key Attribution**:
- GPT Prompts technique credited to: "AI video school channel"

**Recommended Follow-up**:
- Creator mentions guide on "five levels of AI video generation that will take you from a complete beginner to an advanced pro"

---

## Content Density Analysis

**Transcript Characteristics**:
- 467 timestamped entries
- Heavy use of visual demonstrations (indicated by [music] tags)
- Clear section breaks between prompt styles
- Multiple examples per technique
- Real prompts provided (copy-pasteable)

**Practical Value**:
- 7 distinct techniques with clear use cases
- 15+ concrete prompt examples
- 3 major limitations identified with workarounds
- Tool recommendations (Nomo Banana, Q1 Camera Control)
- GPT prompt helper tutorial included

---

## Potential Article Angles

### For Alici AI Blog

**Option 1: Tutorial Deep Dive**
- Title: "7 AI Video Prompt Techniques That Actually Work (Sora 2, Kling, Veo 3)"
- Focus: Step-by-step implementation of each technique
- Include: Workflow diagram for image-to-video process

**Option 2: Best Practices + Limitations**
- Title: "What AI Video Generators Can't Do (And How to Work Around It)"
- Focus: Crowd animation, style consistency, anchor prompts
- Include: Before/After examples of workarounds

**Option 3: Prompt Strategy Framework**
- Title: "How to Layer 7 Prompt Styles for Cinematic AI Videos"
- Focus: Combining techniques strategically
- Include: Decision tree for which style to use when

**Option 4: Beginner's Guide**
- Title: "AI Video Prompting: Simple > Complicated (7 Essential Techniques)"
- Focus: Simplicity philosophy, direct prompts
- Include: Starter prompt templates

**Option 5: Tool Comparison + Techniques**
- Title: "Sora 2 vs Kling vs Veo 3: Which Prompt Techniques Work Best?"
- Focus: Cross-tool compatibility of 7 techniques
- Include: Model-specific limitations matrix

---

## Quotable Insights (Social Media / Pull Quotes)

1. "The best AI videos aren't made using complicated prompts. They're generated using simple, clear, intentional prompts that the AI models actually respond to."

2. "The difference between being good at prompting and being bad at prompting is actually understanding the limitations of the AI video, what it can't do."

3. "Things that seem super obvious to you are not obvious to the AI at all."

4. "It's not just about what you're seeing, but how you're observing it." (on cinematic prompts)

5. "Sometimes to get what you want from the AI, it's actually easier to just tell it what you don't want to happen." (on negative prompting)

6. "Turns AI video generator into a storyboard tool or video editor." (on timestamp + cutscene prompting)

7. "To get the most beautiful shots, like these surrealistic scenes, it's really only possible to do this consistently if you're using image prompts."

8. "AI documentation rarely tells you what the AI video generator is bad at."

9. "Be direct and clear in exactly how you want the scene to unfold."

10. "Make sure the scene you're cutting to isn't too overly different from your original shot." (cutscene limitation)

---

## End of Analysis

**Total Sections**: 10
**Prompt Examples Extracted**: 15+
**Techniques Documented**: 7 core + 1 bonus (start/end frame)
**Limitations Identified**: 5 major
**Tools Mentioned**: 7 (Veo 3, Sora 2, Kling 2.5, Nomo Banana, Q1 Camera Control, ChatGPT, Cling)

**Ready for article production**: Yes
**Recommended Writer Skill**: `blog-tutorial-writer` (1,800-2,500 words)
**Alternate Option**: `case-roundup-writer` (300-600 words, focus on prompt examples)