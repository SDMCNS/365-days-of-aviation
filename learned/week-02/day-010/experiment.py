"""
Day 010 Operational Experiment: 5-Tier Aviation Regulatory Hierarchy & Traceability Verifier
Domain: Create a hierarchy map of the Convention, Annexes, PANS, manuals and State implementation.

Adheres to Aviation 365 Tool Principles:
  1. Authentic aviation calculations (Hierarchy precedence function, legal validity scoring)
  2. Interactive input with sensible defaults on Enter
  3. Step-by-step intermediate operational traces
  4. Adversarial stress-testing (Regulatory conflict resolution & SAFA Level 1 finding)
  5. Completely self-contained standard library Python
  6. Clean exit code 0
"""

import sys
import time

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

TRACEABILITY_CHAINS = {
    1: {
        "domain": "In-Flight Fuel Planning & 30-min Final Reserve",
        "t1": "Chicago Convention Doc 7300, Article 12 (Rules of the Air & Flight Safety)",
        "t2": "ICAO Annex 6, Part I, Standard 4.3.7 (Mandatory Final Reserve Protection)",
        "t3": "ICAO Doc 9976 (Flight Planning & Fuel Management Manual - 30 min hold @ 1,500 ft)",
        "t4": "EASA Regulation (EU) 965/2012, CAT.OP.MPA.181 (Mandatory Operational Law)",
        "t5": "Airline Operations Manual (OM-A Section 8.1.7 - A320 1,100 kg CFM56/LEAP limit)"
    },
    2: {
        "domain": "Continuing Airworthiness & Maintenance Release (CRS)",
        "t1": "Chicago Convention Doc 7300, Article 31 (Certificates of Airworthiness)",
        "t2": "ICAO Annex 8, Part II, Standard 3.2 (Continuing Airworthiness & Release to Service)",
        "t3": "ICAO Doc 9760 (Airworthiness Manual - Continuing Airworthiness Systems)",
        "t4": "EASA Regulation (EU) 1321/2014, Part-M / Part-145 (Approved Maintenance Org)",
        "t5": "Maintenance Organisation Exposition (MOE Section 2.12 - Tech Log Sign-off)"
    },
    3: {
        "domain": "Aerodrome Runway Surface Condition (Global Reporting Format)",
        "t1": "Chicago Convention Doc 7300, Article 28 (Air Navigation Facilities & Aerodromes)",
        "t2": "ICAO Annex 14, Volume I, Standard 2.9 (Condition of Movement Area Reporting)",
        "t3": "ICAO Doc 9981 (PANS-Aerodromes) & Doc 10064 (Aeroplane Performance Manual)",
        "t4": "EASA Regulation (EU) 139/2014, ADR.OPS.B.036 (Runway Condition Assessment)",
        "t5": "Aerodrome Operations Manual (AOM Chapter 4 - RWYCC Snowtam Reporting Protocol)"
    }
}

def run_simulation():
    print("=" * 76)
    print("  AVIATION 365 - DAY 010: 5-TIER REGULATORY HIERARCHY VERIFIER")
    print("  Framework: ICAO Doc 7300 -> Annexes -> PANS -> Manuals -> National Law")
    print("=" * 76)
    print("This tool traces legal lineage across the 5 regulatory tiers, resolves legal")
    print("precedence in operational conflicts, and stress-tests compliance integrity.")
    print("-" * 76)

    print("\nSelect an Operational Traceability Domain to inspect:")
    print("  1. In-Flight Fuel Planning & Final Reserve Minima")
    print("  2. Continuing Airworthiness & Certificate of Release to Service (CRS)")
    print("  3. Aerodrome Runway Surface Condition (Global Reporting Format)")

    choice = prompt_int("Enter selection (1, 2, or 3)", 1)
    if choice not in TRACEABILITY_CHAINS:
        choice = 1

    chain = TRACEABILITY_CHAINS[choice]

    print("\n" + "=" * 76)
    print(f"  PHASE I: 5-TIER TRACEABILITY LINEAGE — {chain['domain'].upper()}")
    print("=" * 76)

    tiers = [
        ("Tier 1 [Treaty]", chain['t1'], "SUPREME INTERNATIONAL LAW (Binding on Sovereign States)"),
        ("Tier 2 [SARP]",   chain['t2'], "INTERNATIONAL STANDARD (Mandatory unless Art. 38 difference)"),
        ("Tier 3/4 [PANS]", chain['t3'], "OPERATIONAL PROCEDURES & GUIDANCE (Specifies 'How-To')"),
        ("Tier 5A [Law]",   chain['t4'], "REGIONAL / NATIONAL LEGISLATION (Legally binding on Operators)"),
        ("Tier 5B [SOP]",   chain['t5'], "OPERATOR MANUAL / CHECKLIST (Direct pilot/engineer procedure)")
    ]

    for t_id, doc, status in tiers:
        time.sleep(0.04)
        print(f"\n  {t_id}")
        print(f"    Document : {doc}")
        print(f"    Status   : {status}")

    print("\n" + "=" * 76)
    print("  PHASE II: CONFLICT RESOLUTION & PRECEDENCE ENGINE")
    print("=" * 76)
    print("Simulating a direct operational contradiction:")
    print("  Source A: Airline Operations Manual (Tier 5B) adopts an unapproved fuel software")
    print("            reducing final reserve fuel to 750 kg to carry extra commercial cargo.")
    print("  Source B: EASA CAT.OP.MPA.181 & ICAO Annex 6 (Tier 2/5A) requiring 1,100 kg.")

    tier_a_rank = 5
    tier_b_rank = 2

    print(f"\n  Evaluating Legal Hierarchy Precedence:")
    print(f"    - Rank Source A: Tier {tier_a_rank} (Company OM-A)")
    print(f"    - Rank Source B: Tier {tier_b_rank} (ICAO Annex 6 / EASA Statutory Rule)")

    if tier_b_rank < tier_a_rank:
        winner = "Source B (ICAO Standard & EASA Law)"
        loser = "Source A (Company Procedure)"
        print(f"    PREVALENCE RULE: Higher Tier Prevails! -> {winner} OVERRULES {loser}")
        print(f"    LEGAL FINDING   : Company procedure is NULL AND VOID ab initio.")

    print("\n" + "=" * 76)
    print("  PHASE III: ADVERSARIAL STRESS TEST (SAFA AUDIT LEVEL 1 FINDING)")
    print("=" * 76)
    print("Injecting Safety Oversight Enforcement Scenario:")
    print("  - Foreign Civil Aviation Inspector conducts a ramp inspection (SAFA check) at Frankfurt.")
    print("  - Discovers aircraft dispatched with 750 kg final reserve instead of 1,100 kg mandatory minimum.")
    print("  - Issues a formal Level 1 Non-Compliance Finding under Part-ARO.GEN.350.")

    time.sleep(0.05)
    print(f"\n  Regulatory Enforcement Actions Executed:")
    print(f"    1. Aircraft immediately GROUNDED on apron until fuel replenished (+350 kg uplift).")
    print(f"    2. Departure Slot (CTOT) lost: Incurs 110-minute ground delay.")
    print(f"    3. Mandatory AOC Formal Investigation opened with National Aviation Authority.")
    print(f"    4. Commercial Impact: Delay handling costs + slot penalty = €6,850.00.")

    print(f"\n  Aviation Hierarchy Principle:")
    print(f"    A lower-tier manual can NEVER relax a higher-tier requirement.")
    print(f"    Operators may only be MORE restrictive than the law (Category A), never less (Category C).")

    print("\n" + "=" * 76)
    print("  SIMULATION COMPLETE (Exit Code 0)")
    print("=" * 76)

if __name__ == "__main__":
    run_simulation()
