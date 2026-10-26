"""
Day 024: Aviation Regulatory Source Register & Transition Risk Simulator
Domain: Construct a searchable source register with document title, identifier, version, date, status and scope.
Complies with PracticAI Experiment Rules:
  1. Interactive input with sensible defaults on Enter
  2. Step-by-step intermediate calculations
  3. Stress-testing / boundary conditions
  4. Formatted ASCII output
  5. Completely self-contained standard library Python
  6. Clean exit code 0
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

def prompt_str(prompt_text, default_val):
    sys.stdout.write(f"{prompt_text} [default: '{default_val}']: ")
    sys.stdout.flush()
    val = sys.stdin.readline().strip()
    return val if val else default_val

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

def prompt_float(prompt_text, default_val):
    sys.stdout.write(f"{prompt_text} [default: {default_val}]: ")
    sys.stdout.flush()
    val = sys.stdin.readline().strip()
    if not val:
        return default_val
    try:
        return float(val)
    except ValueError:
        return default_val

# Enterprise Regulatory Register Data Store
REGISTER = [
    {
        "id": "REG-01",
        "title": "Basic Aviation Safety Regulation",
        "identifier": "Regulation (EU) 2018/1139",
        "version": "Consolidated 2023",
        "in_force": "2018-09-11",
        "status": "Active",
        "scope": "All EU Civil Aviation, EASA competence, design, ops, licensing",
        "manual_ref": "OM-A Chapter 1 / CAME Part 0",
        "postholder": "Accountable Manager",
        "weight": 5.0,
        "days_overdue": 0
    },
    {
        "id": "REG-02",
        "title": "Air Operations — Commercial Air Transport",
        "identifier": "Reg (EU) No 965/2012 Annex IV (Part-CAT)",
        "version": "Amended by Reg (EU) 2021/1296 (Fuel Scheme)",
        "in_force": "2022-10-30",
        "status": "Active",
        "scope": "Commercial passenger and cargo airline operations",
        "manual_ref": "OM-A Chapters 8 & 9 (Flight Prep & Fuel)",
        "postholder": "Nominated Person Flight Operations",
        "weight": 5.0,
        "days_overdue": 0
    },
    {
        "id": "REG-03",
        "title": "Flight Time Limitations (FTL)",
        "identifier": "Reg (EU) No 965/2012 Subpart ORO.FTL & CS-FTL.1",
        "version": "Issue 2 / ED Decision 2014/002/R",
        "in_force": "2016-02-18",
        "status": "Active",
        "scope": "Commercial crew duty, rest, and fatigue management",
        "manual_ref": "OM-A Chapter 7 (Flight Time Limitations)",
        "postholder": "Nominated Person Crew Training / Crew Rostering",
        "weight": 4.5,
        "days_overdue": 0
    },
    {
        "id": "REG-04",
        "title": "Continuing Airworthiness Management (Part-CAMO)",
        "identifier": "Reg (EU) No 1321/2014 Annex Vc (Part-CAMO)",
        "version": "Amended by Reg (EU) 2020/270 (SMS in CAMO)",
        "in_force": "2021-12-02",
        "status": "Active",
        "scope": "Fleet airworthiness management, maintenance programs, ARC",
        "manual_ref": "CAME Section 1.2 (Management System)",
        "postholder": "Nominated Person Continuing Airworthiness",
        "weight": 4.8,
        "days_overdue": 0
    },
    {
        "id": "REG-05",
        "title": "Approved Maintenance Organisation (Part-145)",
        "identifier": "Reg (EU) No 1321/2014 Annex II (Part-145)",
        "version": "Amended by Reg (EU) 2021/1963 (Safety Management)",
        "in_force": "2022-12-02",
        "status": "Active",
        "scope": "Aircraft line and base maintenance, CRS release",
        "manual_ref": "MOE Section 1.1 (Quality Policy)",
        "postholder": "Base Maintenance Manager",
        "weight": 4.5,
        "days_overdue": 0
    },
    {
        "id": "REG-06",
        "title": "Aerodrome Operations & Global Reporting Format",
        "identifier": "Reg (EU) No 139/2014 (Part-ADR.OPS.B.037)",
        "version": "Amended by Reg (EU) 2020/2148 (GRF)",
        "in_force": "2021-08-12",
        "status": "Active",
        "scope": "Runway surface condition assessment & RCR reporting",
        "manual_ref": "Aerodrome Manual Chapter 4 (Runway Ops)",
        "postholder": "Airport Operations Director",
        "weight": 4.0,
        "days_overdue": 0
    },
    {
        "id": "REG-07",
        "title": "All-Weather Operations Modernization (AWO)",
        "identifier": "Reg (EU) 2021/2237 & ED Decision 2022/012/R",
        "version": "Consolidated AWO Book",
        "in_force": "2022-10-30",
        "status": "Active",
        "scope": "Enhanced Flight Vision (EFVS), Low Visibility Takeoff (LVTO)",
        "manual_ref": "OM-A Section 8.4 / OM-B A320 FCOM",
        "postholder": "Chief Pilot Technical",
        "weight": 3.8,
        "days_overdue": 0
    }
]

def main():
    print("=" * 76)
    print("  AVIATION 365 - DAY 024: REGULATORY SOURCE REGISTER & RISK SIMULATOR")
    print("  Controlled Inventory Architecture: Identifier, Version, Status, Scope")
    print("=" * 76)

    # 1. Searchable Source Register
    print("\n[PART 1: INTERACTIVE REGISTER QUERY ENGINE]")
    keyword = prompt_str("Enter search filter (e.g. 'Fuel', 'FTL', 'CAMO', 'Air', or press Enter for all)", "").lower()

    matches = [r for r in REGISTER if keyword in r["title"].lower() or keyword in r["identifier"].lower() or keyword in r["scope"].lower()]

    print(f"\nFound {len(matches)} matching regulatory instruments:")
    print("-" * 76)
    for m in matches:
        print(f"[{m['id']}] {m['title']}")
        print(f"  • Identifier : {m['identifier']}")
        print(f"  • Version    : {m['version']} | Status: {m['status']} (In force: {m['in_force']})")
        print(f"  • Scope      : {m['scope']}")
        print(f"  • Company Ref: {m['manual_ref']} | Owner: {m['postholder']}")
        print("-" * 76)

    # 2. Regulatory Change Transition Calculator
    print("\n[PART 2: REGULATORY AMENDMENT TRANSITION WINDOW CALCULATOR]")
    print("Evaluating a newly promulgated EASA regulation in the Official Journal:")
    amendment_name = prompt_str("Amending Regulation Title", "Commission Reg (EU) 2024/XXXX (Cybersecurity Part-IS)")
    days_to_deadline = prompt_int("Days remaining until mandatory implementation deadline", 75)
    manuals_updated = prompt_int("Are internal manuals (OM/CAME) already revised & submitted? (1=Yes, 0=No)", 0)

    print("\nEvaluating transition progress...")
    if days_to_deadline > 180:
        phase = "PLANNING PHASE (Normal Lead Time)"
        action = "Initiate Safety Management of Change (MOC) gap assessment."
    elif 60 < days_to_deadline <= 180:
        phase = "IMPLEMENTATION PHASE (Active Drafts)"
        action = "Revise company procedures, schedule crew/staff differences training."
    elif 0 <= days_to_deadline <= 60:
        phase = "CRITICAL READINESS WINDOW"
        action = "Submit revised OM/CAME to NAA for formal approval. Conduct dry-run audit."
    else:
        phase = "EXPIRED / REGULATORY BREACH!"
        action = "Immediate Level 1 Finding! Operations conducted without legal basis."

    print(f"  -> Transition Phase: {phase}")
    print(f"  -> Recommended Operational Action: {action}")

    # 3. Enterprise Regulatory Risk Index (ERRI)
    print("\n" + "=" * 76)
    print("[PART 3: ENTERPRISE REGULATORY RISK INDEX (ERRI) EVALUATOR]")
    print("=" * 76)

    total_weight = sum(r["weight"] for r in REGISTER)
    risk_sum = 0.0

    for r in REGISTER:
        # If simulated rule has unrevised manuals and is near or past deadline
        is_cur = 1 if r["id"] != "REG-02" or manuals_updated == 1 else 0
        overdue_days = max(0, -days_to_deadline) if r["id"] == "REG-02" and manuals_updated == 0 else 0
        erri_contrib = r["weight"] * ((1 - is_cur) + min(10.0, overdue_days / 30.0))
        risk_sum += erri_contrib

    normalized_erri = (risk_sum / total_weight) * 10.0
    print(f"Total Registered Instruments Tracked: {len(REGISTER)}")
    print(f"Enterprise Regulatory Risk Index (ERRI): {normalized_erri:.2f} / 10.0")
    if normalized_erri == 0.0:
        print("  STATUS: [COMPLIANCE MONITORING HEALTHY] All manuals reflect current law.")
    elif normalized_erri < 3.0:
        print("  STATUS: [MANAGED TRANSITION] Active transition within acceptable safety margins.")
    else:
        print("  STATUS: [ELEVATED COMPLIANCE DEFICIT] Imminent risk of NAA audit findings.")

    # 4. Adversarial Stress Test
    print("\n" + "=" * 76)
    print("  ADVERSARIAL STRESS TEST: EXPIRED REGULATORY TRANSITION (FUEL SCHEME)")
    print("=" * 76)
    print("Simulating arrival of mandatory deadline with UNREVISED fuel planning manuals...")
    print("\n  [AUDIT FAILURE CASCADE INITIATED]")
    print("  Events under EASA Part-ARO & Part-CAT:")
    print("    1. NAA Oversight Inspector conducts unannounced audit of Dispatch & Flight Prep.")
    print("    2. Discovery: Flight plans generated under superseded 5% contingency rule instead of Reg (EU) 2021/1296 Individual Fuel Scheme.")
    print("    3. Formal Finding: LEVEL 1 FINDING issued under ARO.GEN.350 (Direct Safety Impact).")
    print("    4. Action Mandate: Operator given 72 hours to suspend operations or ground affected flights.")
    print("    5. Financial Impact: Wet-lease charter costs, passenger compensation under Reg EC 261/2004, brand damage.")

    print("\n" + "=" * 76)
    print("  SIMULATION COMPLETE — EXIT CODE 0")
    print("=" * 76)

if __name__ == "__main__":
    main()
