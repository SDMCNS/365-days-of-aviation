"""
Day 016 Experiment: Airline Management System & Finding Escalation Simulator
Domain: The relationship between EU regulations, national implementation, oversight and organisational compliance.

Adheres to PracticAI Core Standards:
  1. Interactive input with sensible defaults on Enter
  2. Step-by-step transparent intermediate calculations
  3. Adversarial boundary & stress-testing
  4. Clean, formatted ASCII tables
  5. Standard library Python only
  6. Clean exit code 0
"""

import sys

# UTF-8 stdout configuration for Windows compatibility
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def prompt_int(prompt_text, default_val):
    sys.stdout.write(f"{prompt_text} [default: {default_val}]: ")
    sys.stdout.flush()
    val = sys.stdin.readline().strip()
    if not val:
        return default_val
    try:
        return int(val)
    except ValueError:
        return default_val


def prompt_bool(prompt_text, default_val=True):
    default_str = "Y" if default_val else "N"
    sys.stdout.write(f"{prompt_text} (Y/N) [default: {default_str}]: ")
    sys.stdout.flush()
    val = sys.stdin.readline().strip().upper()
    if not val:
        return default_val
    return val.startswith("Y")


def run_simulation():
    print("=" * 76)
    print("  AVIATION 365 - DAY 016: AIRLINE REGULATORY OVERSIGHT & ENFORCEMENT")
    print("  Context: Part-ARO Authority Oversight vs Part-ORO Organisational Compliance")
    print("  Statutory Anchors: Regulation (EU) 965/2012 ARO.GEN.350 & ORO.GEN.200")
    print("=" * 76)

    # 1. Audit Parameters
    checkpoints = prompt_int("Total Regulatory Audit Checkpoints (Part-ORO / Part-CAT)", 180)
    level1_findings = prompt_int("Level 1 Findings (Immediate Safety Hazard)", 0)
    level2_findings = prompt_int("Level 2 Findings (Compliance Deficiencies / Standard)", 5)
    days_elapsed = prompt_int("Days Elapsed Since Initial Authority Notification", 45)
    root_cause_submitted = prompt_bool("Has Airline Submitted Agreed Corrective Action Plan (CAP)?", True)

    # Calculate Compliance Index
    penalty = (1.00 * level1_findings) + (0.20 * level2_findings)
    aci = max(0.0, 1.0 - (penalty / checkpoints)) * 100.0

    print("\n" + "-" * 76)
    print("NATIONAL COMPETENT AUTHORITY (NCA) AUDIT SCORECARD")
    print("-" * 76)
    print(f"  • Total Requirements Evaluated : {checkpoints}")
    print(f"  • Compliant Checkpoints        : {checkpoints - level1_findings - level2_findings}")
    print(f"  • Active Level 1 Findings      : {level1_findings} (Statutory Limit: 0)")
    print(f"  • Active Level 2 Findings      : {level2_findings}")
    print(f"  -> Airline Compliance Index    : {aci:.2f}% (Minimum Acceptable: 85.0%)")

    # 2. Finding Clock & Escalation Logic
    print("\n" + "-" * 76)
    print("FINDING STATUS & STATUTORY DEADLINE TRACKING (ARO.GEN.350)")
    print("-" * 76)
    max_level2_days = 90
    escalated_l1 = 0

    if level1_findings > 0:
        aoc_status = "IMMEDIATE SUSPENSION / PARTIAL REVOCATION IN FORCE"
        remedy_desc = "Mandatory operational halt on affected aircraft/routes until provisional measures approved."
    elif level2_findings > 0:
        if days_elapsed > max_level2_days and not root_cause_submitted:
            escalated_l1 = level2_findings
            aoc_status = "ESCALATED TO LEVEL 1 - AOC RESTRICTION MANDATED"
            remedy_desc = f"Failed to close findings within 90 days (Day {days_elapsed}). Automatic escalation under ARO.GEN.350(e)."
        else:
            days_remaining = max_level2_days - days_elapsed
            aoc_status = "AOC UNRESTRICTED - CORRECTIVE ACTION PERIOD ACTIVE"
            remedy_desc = f"{days_remaining} days remaining to submit root-cause evidence and close findings."
    else:
        aoc_status = "FULLY COMPLIANT - ZERO DEFICIENCIES"
        remedy_desc = "Standard continuous monitoring."

    print(f"  • Operating License Status     : [{aoc_status}]")
    print(f"  • Enforcement Action           : {remedy_desc}")

    # 3. Risk-Based Oversight Cycle Determination (ARO.GEN.305)
    if level1_findings > 0 or escalated_l1 > 0:
        cycle_months = 12
        rbo_desc = "High-Risk Operator: Oversight cycle compressed to 12 months with frequent on-site audits."
    elif level2_findings > 3:
        cycle_months = 24
        rbo_desc = "Standard Operator: Baseline 24-month continuous oversight planning cycle."
    elif aci >= 98.0 and root_cause_submitted:
        cycle_months = 36
        rbo_desc = "Low-Risk Mature Operator: Oversight cycle legally extended to 36 months."
    else:
        cycle_months = 24
        rbo_desc = "Baseline 24-month oversight cycle."

    print(f"\n  • Risk-Based Oversight Cycle   : {cycle_months} Months")
    print(f"  • Audit Profile Strategy       : {rbo_desc}")

    # 4. Adversarial Stress Test
    print("\n" + "=" * 76)
    print("ADVERSARIAL STRESS TEST: DEADLINE OVERRUN ESCALATION (DAY 95)")
    print("=" * 76)
    print("Scenario: EuroWings fails to update its fatigue management software by Day 90.")
    print("Authority Action under ARO.GEN.350(e):")
    print("  1. Level 2 finding escalates automatically to Level 1 Finding.")
    print("  2. National Authority amends AOC Operations Specifications immediately:")
    print("     -> Prohibits all flight duty extensions.")
    print("     -> Limits maximum daily sectors from 4 to 2.")
    print("  3. Operational & Commercial Fallout:")
    daily_cancelled_sectors = 12
    pax_per_sector = 160
    eu261_comp_per_pax = 250.0  # EUR standard short-haul delay compensation
    daily_comp_cost = daily_cancelled_sectors * pax_per_sector * eu261_comp_per_pax

    print(f"     • Daily Cancelled Sectors   : {daily_cancelled_sectors} flights")
    print(f"     • Stranded Passengers/Day   : {daily_cancelled_sectors * pax_per_sector:,} passengers")
    print(f"     • Direct EU 261 Liability   : €{daily_comp_cost:,.2f} per day in statutory compensation")
    print("=" * 76)
    print("Simulation completed successfully (Exit Code 0).")


if __name__ == "__main__":
    run_simulation()
