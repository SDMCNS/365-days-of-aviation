"""
Day 027: Quad-Link Regulatory Traceability & Audit Risk Simulator
Domain: Link a regulatory requirement to an organisation, operational process, safety objective and evidence record.
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

# Traceability Chains Catalog
CHAINS = {
    1: {
        "domain": "Takeoff Obstacle Clearance & Performance",
        "rule": "EASA CAT.POL.A.205 & CS-25.107 (Takeoff Net Flight Path >= 35 ft clearance)",
        "org": "AOC Holder / Nominated Person Flight Operations",
        "sop": "OM-B Section 4: Cockpit EFB Takeoff Calculation & Cross-check Procedure",
        "spi": "Zero runway overruns; Tailstrike rate < 0.05 per 10,000 sectors",
        "evidence": "Digital EFB computation log archived in flight dispatch database (3 months)"
    },
    2: {
        "domain": "Flight Crew Fatigue & Duty Limitations",
        "rule": "EASA ORO.FTL.205 & CS-FTL.1 Table 1 (Maximum Daily FDP Limits)",
        "org": "AOC Holder / Nominated Person Crew Training & Rostering",
        "sop": "OM-A Section 7: Automated Rostering & Commander Discretion Form FTL-104",
        "spi": "Commander Discretion occurrences < 0.8% of total scheduled sectors",
        "evidence": "Digital crew biometric sign-in log & Form FTL-104 submissions to NAA (28 days)"
    },
    3: {
        "domain": "Continuing Airworthiness & Maintenance Release",
        "rule": "EASA Part-145.A.50 & Part-M.A.801 (Certificate of Release to Service - CRS)",
        "org": "Part-145 Maintenance Organisation / Base Maintenance Manager & Part-66 Staff",
        "sop": "MOE Chapter 2.1: Task Card Completion, Sign-off & Critical Dual Inspection",
        "spi": "Maintenance-induced in-flight turnbacks < 0.20 per 1,000 cycles",
        "evidence": "Signed & stamped Aircraft Technical Log CRS page archived for 36 months"
    },
    4: {
        "domain": "Low Visibility Operations (CAT IIIb Autoland)",
        "rule": "EASA Part-SPA.LVO.100 & CS-AWO.100 (All-Weather Operations)",
        "org": "AOC Holder / Chief Pilot Technical & CAMO Maintenance Postholder",
        "sop": "OM-A Section 8.4: Low Visibility Briefing, Monitored Approach SOP, Downgrade Rules",
        "spi": "Autoland go-around / missed approach rate < 1.5% in actual LVP conditions",
        "evidence": "FDM digital flight recorder autoland telemetry & 6-month simulator recurrent logs"
    },
    5: {
        "domain": "Dangerous Goods Transport & Passenger PEDs",
        "rule": "EASA CAT.GEN.MPA.140 / 200 & ICAO Doc 9284 Part 8 (Lithium Battery Controls)",
        "org": "AOC Holder / Ground Handling & Security Quality Manager",
        "sop": "OM-A Section 9.2: Check-in Smart Luggage Verification & Cabin Containment Kit SOP",
        "spi": "Zero undeclared dangerous goods incidents reaching cargo hold",
        "evidence": "Passenger electronic DG declaration log & Cabin Crew incident report forms"
    }
}

def main():
    print("=" * 76)
    print("  AVIATION 365 - DAY 027: QUAD-LINK REGULATORY TRACEABILITY SIMULATOR")
    print("  The 5-Node Chain: Rule -> Org -> Process -> Safety Target -> Evidence")
    print("=" * 76)

    # 1. Interactive Chain Explorer
    print("\n[PART 1: THE 5-NODE TRACEABILITY CHAIN EXPLORER]")
    print("Select an operational aviation domain to inspect:")
    for k, v in CHAINS.items():
        print(f"  {k} = {v['domain']}")
    choice = prompt_int("Enter selection (1-5)", 1)
    ch = CHAINS.get(choice, CHAINS[1])

    print("\n" + "=" * 76)
    print(f"TRACEABILITY MAP FOR: {ch['domain'].upper()}")
    print("=" * 76)
    print(f"  [Node 1: Statutory Rule]       : {ch['rule']}")
    print(f"  [Node 2: Responsible Org/NP]  : {ch['org']}")
    print(f"  [Node 3: Operational SOP]     : {ch['sop']}")
    print(f"  [Node 4: Safety Target (SPI)]  : {ch['spi']}")
    print(f"  [Node 5: Audit Evidence Record]: {ch['evidence']}")

    # 2. Traceability Integrity Metric (TIM) Calculator
    print("\n" + "=" * 76)
    print("[PART 2: ENTERPRISE TRACEABILITY INTEGRITY METRIC (TIM)]")
    print("=" * 76)
    print("Simulating compliance health across all 5 operational domains:")

    active_chains = 0
    total_chains = len(CHAINS)

    for k, v in CHAINS.items():
        # Default scenario: All intact except simulated gap in domain 2 (FTL evidence record missing digital archive)
        default_state = 1 if k != 2 else 0
        state = prompt_int(f"Is chain {k} ({v['domain'][:35]}...) 100% complete? (1=Yes, 0=Missing Evidence/SPI)", default_state)
        if state == 1:
            active_chains += 1

    tim = active_chains / total_chains
    print(f"\nTraceability Integrity Metric (TIM) : {tim:.2f} / 1.00 ({tim*100:.1f}%)")

    # 3. Audit Discovery Probability
    print("\n[PART 3: NATIONAL AVIATION AUTHORITY (NAA) AUDIT EXPOSURE]")
    samples = prompt_int("Number of operational requirements sampled by NAA during annual audit", 20)
    prob_finding = (1.0 - (tim ** samples)) * 100.0

    print(f"  - Sampling Intensity           : {samples} independent operational records")
    print(f"  - Probability of Audit Finding : {prob_finding:.2f}%")
    if prob_finding > 50.0:
        print("  -> AUDIT VERDICT: HIGH RISK! Substantial probability of Level 1/2 non-compliance findings.")
    elif prob_finding > 10.0:
        print("  -> AUDIT VERDICT: MODERATE RISK. Isolated record deficiencies detected.")
    else:
        print("  -> AUDIT VERDICT: CLEAN OVERSIGHT AUDIT. Robust closed-loop traceability demonstrated.")

    # 4. Adversarial Stress Test
    print("\n" + "=" * 76)
    print("  ADVERSARIAL STRESS TEST: UNRECORDED AIRCRAFT FLIGHT CONTROL REPLACEMENT")
    print("=" * 76)
    print("Simulating an elevator servo actuator replacement signed verbally without a Tech Log CRS...")
    print("\n  [SAFETY & LEGAL FAILURE CASCADE]")
    print("  1. Aircraft operates 3 commercial passenger flights with uncertified flight control.")
    print("  2. NAA Ramp Inspector requests the CRS for work performed at outstation.")
    print("  3. Finding: No Part-145.A.50 Certificate of Release to Service exists in Technical Log.")
    print("  4. Legal Mandate under Part-M.A.801: Aircraft Certificate of Airworthiness (CofA) is INVALIDATED.")
    print("  5. Immediate Level 1 Audit Finding served. Aircraft grounded on ramp.")
    print("  6. Full functional duplicate inspection and re-certification required before flight release.")
    print("  -> LESSON: In aviation law, if there is no evidence record, IT NEVER HAPPENED!")

    print("\n" + "=" * 76)
    print("  SIMULATION COMPLETE — EXIT CODE 0")
    print("=" * 76)

if __name__ == "__main__":
    main()
