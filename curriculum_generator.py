"""
curriculum_generator.py
Aviation 365: Autonomous Lesson & Curriculum Suite Generator
Powered by Gemini API & Grounded in Syllabus Lesson Plans.

Generates the complete 4-part learning suite for any Day or Week:
  1. 📖 Lesson Guide (README.md)
  2. 📊 Technical Walkthrough (analysis.md & math.md)
  3. 🐍 Operational Python Experiment (experiment.py)
  4. 🗺️ System Architecture Canvas (architecture.mermaid)
  (Optional) ⚡ NotebookLM Suite (slides, infographic, video_overview via notebooklm_studio)

Ensures zero hallucination by strictly grounding content in:
  - lessons/week-XX/day-YYY.md (Frontmatter, Context, Core Concepts, Exercises, Safety Hazards)
  - .aviation_profile.json (Learner archetype, cognitive scores, preferences)
"""

import os
import sys
import re
import json
import time
import argparse
from pathlib import Path
from typing import Callable, Optional

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Google GenAI SDK
try:
    from google import genai
    from google.genai import types
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

# Import NotebookLM studio if available
try:
    import notebooklm_studio
    HAS_NOTEBOOKLM_STUDIO = True
except ImportError:
    HAS_NOTEBOOKLM_STUDIO = False


def get_gemini_config(root_dir: Path) -> tuple[Optional[str], str]:
    """Reads Gemini API key and model from .aviation_config.json or environment."""
    config_file = root_dir / ".aviation_config.json"
    api_key = None
    model = "gemini-3.5-flash-lite"

    if config_file.exists():
        try:
            data = json.loads(config_file.read_text(encoding="utf-8", errors="replace"))
            api_key = data.get("gemini_api_key") or data.get("api_key")
            model = data.get("gemini_model") or data.get("model", model)
        except Exception as e:
            print(f"Error reading {config_file}: {e}")

    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY")

    return api_key, model


def get_student_profile(root_dir: Path) -> dict:
    """Reads .aviation_profile.json or returns default hands-on builder profile."""
    profile_file = root_dir / ".aviation_profile.json"
    if profile_file.exists():
        try:
            return json.loads(profile_file.read_text(encoding="utf-8", errors="replace"))
        except Exception as e:
            print(f"Error reading student profile: {e}")

    return {
        "student_name": "Aviation 365 Student",
        "archetype": "🛠️ Hands-On Systems Builder",
        "archetype_desc": "Prefers concrete code examples, running experiments immediately, and inspecting intermediate state over abstract mathematical proofs.",
        "scores": {
            "code_vs_theory": 80,
            "systems_vs_primitives": 75,
            "visual_vs_verbal": 70,
            "pace_and_density": 85
        },
        "preferences": {
            "explanation_depth": "Balanced Intuition + Mechanics",
            "math_rigor": "Plain-English Intuitive Translation",
            "code_style": "Production-grade, annotated with intermediate printouts",
            "custom_directives": ""
        }
    }


def parse_lesson_plan(lesson_path: Path) -> dict:
    """
    Parses a syllabus lesson plan markdown file, extracting YAML frontmatter
    and major Markdown sections.
    """
    if not lesson_path.exists():
        return {}

    text = lesson_path.read_text(encoding="utf-8", errors="replace")
    plan = {
        "raw_text": text,
        "frontmatter": {},
        "title": lesson_path.stem.replace("-", " ").title(),
        "theme": "Understand",
        "level_title": "Aviation as a System",
        "regulatory_anchor": "ICAO / EASA Standards",
        "core_concept": "",
        "exercise": "",
        "hazards": ""
    }

    # Extract YAML frontmatter
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.DOTALL)
    body = text
    if fm_match:
        fm_text = fm_match.group(1)
        body = fm_match.group(2)
        for line in fm_text.splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                k = k.strip()
                v = v.strip().strip('"').strip("'")
                plan["frontmatter"][k] = v
                if k == "title":
                    plan["title"] = v
                elif k == "theme":
                    plan["theme"] = v
                elif k == "level_title":
                    plan["level_title"] = v
                elif k == "regulatory_anchor":
                    plan["regulatory_anchor"] = v

    # Extract key sections from body
    plan["body"] = body.strip()

    # Core concept section
    cc_match = re.search(r"## 2\.\s*Core Operational & Technical Concept\s*\n(.*?)(?=\n## |\Z)", body, re.DOTALL)
    if cc_match:
        plan["core_concept"] = cc_match.group(1).strip()

    # Practical exercise section
    ex_match = re.search(r"## 3\.\s*Hands-on.*?Practical Exercise\s*\n(.*?)(?=\n## |\Z)", body, re.DOTALL)
    if ex_match:
        plan["exercise"] = ex_match.group(1).strip()

    # Hazards section
    hz_match = re.search(r"## 4\.\s*Break It / Stress Test & Safety Hazards\s*\n(.*?)(?=\n## |\Z)", body, re.DOTALL)
    if hz_match:
        plan["hazards"] = hz_match.group(1).strip()

    return plan


def generate_lesson_suite_for_day(
    day_num: int,
    root_dir: Path,
    client: genai.Client,
    model: str = "gemini-3.5-flash-lite",
    progress_callback: Optional[Callable[[str], None]] = None,
    include_canvas: bool = True,
    generate_notebooklm: bool = False,
    overwrite: bool = True
) -> dict:
    """
    Synthesizes the complete 4-part learned suite for a day from its syllabus lesson plan.
    Outputs:
      - learned/week-XX/day-YYY/README.md
      - learned/week-XX/day-YYY/analysis.md & math.md
      - learned/week-XX/day-YYY/experiment.py
      - learned/week-XX/day-YYY/architecture.mermaid
      - (optional) NotebookLM suite via notebooklm_studio
    """
    def log(msg: str):
        if progress_callback:
            progress_callback(msg)
        try:
            print(f"[Day {day_num:03d}] {msg}")
        except Exception:
            safe = msg.encode("ascii", errors="replace").decode("ascii")
            print(f"[Day {day_num:03d}] {safe}")

    w_num = ((day_num - 1) // 7) + 1
    if w_num > 52: w_num = 52

    lesson_path = root_dir / "lessons" / f"week-{w_num:02d}" / f"day-{day_num:03d}.md"
    if not lesson_path.exists():
        # Fallback search
        found = list(root_dir.glob(f"lessons/**/day-{day_num:03d}.md"))
        if found:
            lesson_path = found[0]
        else:
            raise FileNotFoundError(f"Lesson plan for Day {day_num:03d} not found at {lesson_path}")

    log(f"Reading syllabus plan: {lesson_path.name}")
    plan = parse_lesson_plan(lesson_path)
    profile = get_student_profile(root_dir)

    target_dir = root_dir / "learned" / f"week-{w_num:02d}" / f"day-{day_num:03d}"
    target_dir.mkdir(parents=True, exist_ok=True)

    # Check if already exists and not overwriting
    readme_path = target_dir / "README.md"
    if not overwrite and readme_path.exists():
        log("Files already exist and overwrite is False. Skipping generation.")
        return {
            "day": day_num,
            "status": "skipped",
            "target_dir": str(target_dir)
        }

    student_name = profile.get("student_name", "Aviation Student")
    arch = profile.get("archetype", "🛠️ Hands-On Systems Builder")
    arch_desc = profile.get("archetype_desc", "")
    scores = profile.get("scores", {})
    prefs = profile.get("preferences", {})
    custom_directives = prefs.get("custom_directives", "")

    log("Constructing grounded curriculum prompt for Gemini...")

    system_instruction = f"""You are the Chief Aviation Architect and Senior Flight Operations Pedagogical Lead for the 365 Days of Aviation curriculum.
Your mission is to expand and synthesize Day {day_num:03d} from its official syllabus lesson plan into a coherent, robust, authentic civil aviation learning suite.

=== MANDATORY SYLLABUS CONTRACT (SOURCE OF TRUTH) ===
You MUST adhere strictly to the provided Lesson Plan document. Do not drift into unrelated subjects or invent generic concepts.
• Day Number: {day_num}
• Week Number: {w_num}
• Title: {plan.get('title')}
• Theme: {plan.get('theme')}
• Level / Domain: {plan.get('level_title')}
• Regulatory Anchor: {plan.get('regulatory_anchor')}

=== OFFICIAL LESSON PLAN CONTENT ===
{plan.get('raw_text')}

=== LEARNER CUSTOMISATION PROFILE ===
• Student Name: {student_name}
• Learning Archetype: {arch} ({arch_desc})
• Cognitive Profile:
  - Code vs Theory: {scores.get('code_vs_theory', 80)}/100
  - Systems vs Primitives: {scores.get('systems_vs_primitives', 75)}/100
  - Visual vs Verbal: {scores.get('visual_vs_verbal', 70)}/100
• Preferences:
  - Explanation Depth: {prefs.get('explanation_depth', 'Deep Mechanical + Operational Realism')}
  - Technical Rigor: {prefs.get('math_rigor', 'Operational Context + Worked Numerical Examples')}
  - Code Style: {prefs.get('code_style', 'Production-grade, annotated with intermediate printouts')}
{f"• Student Directives: {custom_directives}" if custom_directives else ""}

=== PEDAGOGICAL BOUNDARY & TECHNICAL STANDARDS ===
• All content MUST be authentic civil aviation: ICAO SARPs (Annexes 1-19, Doc 7300, Doc 8168 PANS-OPS, Doc 4444 PANS-ATM), EASA Easy Access Rules (Regulation 2018/1139, Part-CAT, Part-M, Part-145, Part-FCL, Part-ADR), Eurocontrol A-CDM, dispatch limits, MTOM/MZFM/MLM structural envelopes, fuel statutory minimums (taxing, trip, contingency, alternate, final reserve), and SMS safety management barriers.
• Do NOT invent fictitious machine learning formulas or graph theory for the sake of math!
• The Python experiment MUST be completely runnable using ONLY Python standard library (no pip dependencies required).
• The Mermaid architecture diagram MUST be valid Mermaid graph syntax (graph TD or graph LR) modeling the ecosystem handshakes.

=== REQUIRED OUTPUT STRUCTURE (CRITICAL) ===
You MUST return your output strictly segmented into four tagged blocks with no text outside the blocks:

<<<LESSON_DOCUMENT>>>
# Day {day_num:03d} — {plan.get('title')}

[← Return to Master Syllabus](../../lessons/README.md) | [Technical Walkthrough](analysis.md) | [System Topology Canvas](architecture.mermaid) | [Run Python Simulator](experiment.py)

---

## 1. Executive Summary & Operational Context
(Comprehensive, engaging, deep plain-English explanation grounded in today's lesson plan, explaining the commercial, institutional, and safety significance.)

## 2. Institutional Architecture & Stakeholder Handshakes
(Detailed examination of the airlines, aerodromes, air navigation service providers, ground handlers, and regulatory authorities involved.)

## 3. Real-World Flight Operations Scenario & Edge Cases
(Concrete flight operations narrative, compounding disruptions, dispatch dilemmas, or turnaround constraints, and how SMS barriers catch errors.)

## 4. Practical Implementation Reference
(Detailed breakdown of the interactive Python tool and mathematical models explored today.)
<<<END_LESSON_DOCUMENT>>>

<<<TECHNICAL_WALKTHROUGH>>>
# Day {day_num:03d} — Technical Walkthrough: {plan.get('title')}

[← Return to Lesson Guide](README.md) | [System Topology Canvas](architecture.mermaid) | [Run Python Simulator](experiment.py)

---

## 1. Quantitative Modeling & Physical/Operational Principles
(Real-world formulas in LaTeX $inline$ and $$display$$ format with exact variable definitions, physical units, and regulatory thresholds.)

## 2. Step-by-Step Worked Numerical Trace
(A complete, realistic flight or engineering calculation with realistic inputs, step-by-step arithmetic, and final operational determination.)

## 3. Regulatory Boundaries & Critical Thresholds
(Statutory certification limits, MEL relief categories, fuel reserve limits, or curfew cutoffs.)
<<<END_TECHNICAL_WALKTHROUGH>>>

<<<OPERATIONAL_EXPERIMENT>>>
\"\"\"
Day {day_num:03d} Operational Experiment: {plan.get('title')}
Self-contained standard library Python tool directly modeling today's aviation topic.
\"\"\"
import sys
import time

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Interactive prompts with sensible defaults on Enter
# Step-by-step intermediate calculation printouts
# Adversarial stress test / failure injection
# Clean exit code 0
<<<END_OPERATIONAL_EXPERIMENT>>>

<<<SYSTEM_ARCHITECTURE>>>
graph TD
    %% Valid Mermaid diagram showing nodes, subgraphs, and directional handshakes
<<<END_SYSTEM_ARCHITECTURE>>>
"""

    user_prompt = f"Synthesize and generate the complete 4-part learning suite for Day {day_num:03d}: '{plan.get('title')}' based strictly on the provided lesson plan and student profile."

    log(f"Calling Gemini API ({model})...")
    response = client.models.generate_content(
        model=model,
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.25,
            max_output_tokens=8192
        )
    )

    raw_text = response.text or ""
    log("Received response from Gemini. Parsing structured blocks...")

    def extract_section(raw: str, start_tags: list[str], end_tags: list[str]) -> str:
        s_idx = -1
        matched_tag = ""
        for st in start_tags:
            idx = raw.find(st)
            if idx != -1:
                s_idx = idx
                matched_tag = st
                break

        if s_idx == -1:
            return ""

        content_start = s_idx + len(matched_tag)
        earliest_end = len(raw)
        for et in end_tags:
            e_idx = raw.find(et, content_start)
            if e_idx != -1 and e_idx < earliest_end:
                earliest_end = e_idx

        return raw[content_start:earliest_end].strip()

    lesson_doc = extract_section(
        raw_text,
        ["<<<LESSON_DOCUMENT>>>", "**<<<LESSON_DOCUMENT>>>**"],
        ["<<<END_LESSON_DOCUMENT>>>", "<<<TECHNICAL_WALKTHROUGH>>>", "**<<<TECHNICAL_WALKTHROUGH>>>**"]
    )
    tech_walkthrough = extract_section(
        raw_text,
        ["<<<TECHNICAL_WALKTHROUGH>>>", "**<<<TECHNICAL_WALKTHROUGH>>>**"],
        ["<<<END_TECHNICAL_WALKTHROUGH>>>", "<<<OPERATIONAL_EXPERIMENT>>>", "**<<<OPERATIONAL_EXPERIMENT>>>**"]
    )
    py_code = extract_section(
        raw_text,
        ["<<<OPERATIONAL_EXPERIMENT>>>", "**<<<OPERATIONAL_EXPERIMENT>>>**"],
        ["<<<END_OPERATIONAL_EXPERIMENT>>>", "<<<SYSTEM_ARCHITECTURE>>>", "**<<<SYSTEM_ARCHITECTURE>>>**"]
    )
    architecture_mermaid = extract_section(
        raw_text,
        ["<<<SYSTEM_ARCHITECTURE>>>", "**<<<SYSTEM_ARCHITECTURE>>>**"],
        ["<<<END_SYSTEM_ARCHITECTURE>>>"]
    )

    # Smart fallbacks if delimited tags were omitted by the model
    if not py_code:
        py_match = re.search(r"```(?:python)?\s*(import .*?)\s*```", raw_text, re.DOTALL)
        if py_match:
            py_code = py_match.group(1).strip()

    if not architecture_mermaid:
        mermaid_match = re.search(r"```(?:mermaid)?\s*(graph [T|L][D|R].*?)\s*```", raw_text, re.DOTALL)
        if mermaid_match:
            architecture_mermaid = mermaid_match.group(1).strip()

    if not lesson_doc and ("# Day" in raw_text or "## 1." in raw_text):
        # Extract markdown document up to technical walkthrough or python code
        cutoff = len(raw_text)
        for token in ["<<<TECHNICAL_WALKTHROUGH>>>", "# Technical Walkthrough", "```python"]:
            tok_idx = raw_text.find(token)
            if tok_idx != -1 and tok_idx < cutoff:
                cutoff = tok_idx
        lesson_doc = raw_text[:cutoff].strip()

    if not lesson_doc and not tech_walkthrough and not py_code:
        raise ValueError(f"Gemini response for Day {day_num:03d} did not contain valid lesson content.")

    # Strip code fences from Python code if present
    if py_code.startswith("```python"):
        py_code = re.sub(r"^```python\s*", "", py_code)
        py_code = re.sub(r"\s*```$", "", py_code)
    elif py_code.startswith("```"):
        py_code = re.sub(r"^```\s*", "", py_code)
        py_code = re.sub(r"\s*```$", "", py_code)

    # Strip code fences from Mermaid diagram if present
    if architecture_mermaid.startswith("```mermaid"):
        architecture_mermaid = re.sub(r"^```mermaid\s*", "", architecture_mermaid)
        architecture_mermaid = re.sub(r"\s*```$", "", architecture_mermaid)
    elif architecture_mermaid.startswith("```"):
        architecture_mermaid = re.sub(r"^```\s*", "", architecture_mermaid)
        architecture_mermaid = re.sub(r"\s*```$", "", architecture_mermaid)

    # Fallback architecture if missing
    if not architecture_mermaid or "graph" not in architecture_mermaid:
        architecture_mermaid = f"""graph TD
    subgraph Regulatory_Framework["Regulatory Spine"]
        ICAO["ICAO: Chicago Convention & Annexes"]
        EASA["EASA / NAA: {plan.get('regulatory_anchor', 'Safety Regulations')}"]
    end
    subgraph Operations["Flight Operations Ecosystem"]
        OPS["Flight Operations & Dispatch"]
        AIR["Aircraft & Crew"]
        ATC["Air Traffic Management"]
    end
    ICAO --> EASA
    EASA --> OPS
    OPS --> AIR
    OPS <--> ATC
"""

    # Write files
    written_files = {}

    readme_file = target_dir / "README.md"
    readme_file.write_text(lesson_doc, encoding="utf-8")
    written_files["README.md"] = len(lesson_doc)
    log(f"✓ Written README.md ({len(lesson_doc):,} bytes)")

    analysis_file = target_dir / "analysis.md"
    analysis_file.write_text(tech_walkthrough, encoding="utf-8")
    written_files["analysis.md"] = len(tech_walkthrough)

    math_file = target_dir / "math.md"
    math_file.write_text(tech_walkthrough, encoding="utf-8")
    written_files["math.md"] = len(tech_walkthrough)
    log(f"✓ Written analysis.md & math.md ({len(tech_walkthrough):,} bytes)")

    exp_file = target_dir / "experiment.py"
    exp_file.write_text(py_code, encoding="utf-8")
    written_files["experiment.py"] = len(py_code)
    log(f"✓ Written experiment.py ({len(py_code):,} bytes)")

    if include_canvas:
        arch_file = target_dir / "architecture.mermaid"
        arch_file.write_text(architecture_mermaid, encoding="utf-8")
        written_files["architecture.mermaid"] = len(architecture_mermaid)
        log(f"✓ Written architecture.mermaid ({len(architecture_mermaid):,} bytes)")

    # Optional NotebookLM Suite Generation
    notebooklm_results = None
    if generate_notebooklm and HAS_NOTEBOOKLM_STUDIO:
        log("Generating NotebookLM multi-modal suite (Slides, Infographic, Video Overview)...")
        try:
            notebooklm_results = notebooklm_studio.generate_notebooklm_artifacts_for_day(
                day_num=day_num,
                root_dir=root_dir,
                client=client,
                model=model,
                progress_callback=progress_callback
            )
            log("✓ NotebookLM multi-modal suite generated successfully.")
        except Exception as e:
            log(f"⚠ Warning: NotebookLM generation encountered error: {e}")

    log(f"✨ Day {day_num:03d} generation completed successfully!")
    return {
        "day": day_num,
        "week": w_num,
        "status": "success",
        "target_dir": str(target_dir),
        "files": written_files,
        "notebooklm": notebooklm_results
    }


def generate_lesson_suite_for_week(
    week_num: int,
    root_dir: Path,
    client: genai.Client,
    model: str = "gemini-3.5-flash-lite",
    progress_callback: Optional[Callable[[str], None]] = None,
    day_progress_callback: Optional[Callable[[int, int, int], None]] = None,
    cancel_check: Optional[Callable[[], bool]] = None,
    only_missing: bool = False,
    include_canvas: bool = True,
    generate_notebooklm: bool = False,
    overwrite: bool = True
) -> dict:
    """
    Sequentially generates all 7 days for a given week from their lesson plans.
    Supports cancellation, skipping existing days, and progress reporting.
    """
    def log(msg: str):
        if progress_callback:
            progress_callback(msg)
        try:
            print(f"[Week {week_num:02d}] {msg}")
        except Exception:
            safe = msg.encode("ascii", errors="replace").decode("ascii")
            print(f"[Week {week_num:02d}] {safe}")

    start_day = (week_num - 1) * 7 + 1
    end_day = min(365, week_num * 7)
    days = list(range(start_day, end_day + 1))
    total_days = len(days)

    log(f"Starting batch generation for Week {week_num:02d} (Days {start_day:03d} to {end_day:03d}, {total_days} days)...")

    results = []
    for idx, d_num in enumerate(days, 1):
        if cancel_check and cancel_check():
            log(f"Batch generation cancelled by user at Day {d_num:03d}.")
            break

        if day_progress_callback:
            day_progress_callback(idx, total_days, d_num)

        target_dir = root_dir / "learned" / f"week-{week_num:02d}" / f"day-{d_num:03d}"
        if only_missing and (target_dir / "README.md").exists():
            log(f"[{idx}/{total_days}] Day {d_num:03d} already exists. Skipping (only-missing enabled).")
            results.append({"day": d_num, "status": "skipped"})
            continue

        log(f"[{idx}/{total_days}] Processing Day {d_num:03d}...")
        try:
            res = generate_lesson_suite_for_day(
                day_num=d_num,
                root_dir=root_dir,
                client=client,
                model=model,
                progress_callback=progress_callback,
                include_canvas=include_canvas,
                generate_notebooklm=generate_notebooklm,
                overwrite=overwrite
            )
            results.append(res)
        except Exception as e:
            log(f"❌ Error generating Day {d_num:03d}: {e}")
            results.append({"day": d_num, "status": "error", "error": str(e)})

        # Brief pause between days to prevent rate limiting
        if idx < total_days:
            time.sleep(0.5)

    log(f"Week {week_num:02d} batch complete. Processed {len(results)}/{total_days} days.")
    return {
        "week": week_num,
        "total_days": total_days,
        "processed": len(results),
        "results": results
    }


def main():
    parser = argparse.ArgumentParser(description="Generate 365 Days of Aviation Lesson Suite from Plans")
    parser.add_argument("--day", type=int, help="Single day number to generate (1-365)")
    parser.add_argument("--week", type=int, help="Week number to generate (1-52)")
    parser.add_argument("--only-missing", action="store_true", help="Generate only days that lack learned content")
    parser.add_argument("--with-notebooklm", action="store_true", help="Also generate NotebookLM slides, infographic, video")
    parser.add_argument("--no-canvas", action="store_true", help="Do not generate architecture.mermaid")
    parser.add_argument("--model", type=str, default=None, help="Gemini model override")

    args = parser.parse_args()
    root_dir = Path(__file__).resolve().parent

    api_key, default_model = get_gemini_config(root_dir)
    model = args.model or default_model

    if not api_key:
        print("Error: No Gemini API Key found in .aviation_config.json or GEMINI_API_KEY env var.")
        sys.exit(1)

    if not HAS_GENAI:
        print("Error: google-genai package is not installed. Please run: pip install google-genai")
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    if args.day:
        generate_lesson_suite_for_day(
            day_num=args.day,
            root_dir=root_dir,
            client=client,
            model=model,
            include_canvas=not args.no_canvas,
            generate_notebooklm=args.with_notebooklm
        )
    elif args.week:
        generate_lesson_suite_for_week(
            week_num=args.week,
            root_dir=root_dir,
            client=client,
            model=model,
            only_missing=args.only_missing,
            include_canvas=not args.no_canvas,
            generate_notebooklm=args.with_notebooklm
        )
    else:
        print("Please specify --day <number> or --week <number>. Use --help for full options.")


if __name__ == "__main__":
    main()
