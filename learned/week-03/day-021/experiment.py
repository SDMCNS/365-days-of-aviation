"""
Day 021 Experiment: Aviation Ecosystem Governance Blueprint & Dispatch Handshake Engine
Domain: Produce a one-page guide to who makes rules, who oversees compliance and who operates services.

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


def prompt_str(prompt_text, default_val):
    sys.stdout.write(f"{prompt_text} [default: {default_val}]: ")
    sys.stdout.flush()
    val = sys.stdin.readline().strip()
    return val if val else default_val


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
    print("  AVIATION 365 - DAY 021: ONE-PAGE AVIATION ECOSYSTEM GOVERNANCE BLUEPRINT")
    print("  The Triad: 1. Who Makes Rules | 2. Who Oversees Compliance | 3. Who Operates")
    print("  Statutory Framework: Regulation (EU) 2018/1139 & ICAO Chicago Convention")
    print("=" * 76)

    # Master Ecosystem Database
    ecosystem_map = {
        "1": {
            "role": "Commercial Air Transport Airline",
            "rulemaker": "European Commission (DG MOVE) & EASA",
            "overseer": "National Competent Authority (NCA) of Operator State",
            "license": "Air Operator Certificate (AOC) under Regulation (EU) 965/2012",
            "critical_hazard": "Flying with unapproved MEL or expired crew duty limits",
            "statutory_sanction": "AOC suspension / aircraft grounded on apron under Part-ARO"
        },
        "2": {
            "role": "Aircraft Manufacturer & Design Organisation",
            "rulemaker": "European Parliament, Commission & EASA",
            "overseer": "EASA (Direct Centralized Competence in Cologne)",
            "license": "Design Organisation Approval (DOA) & Type Certificate (Part-21)",
            "critical_hazard": "Undetected flight control design flaw violating CS-25",
            "statutory_sanction": "Airworthiness Directive (AD) grounding worldwide fleet"
        },
        "3": {
            "role": "Aircraft Maintenance Repair Station (MRO)",
            "rulemaker": "European Commission & EASA",
            "overseer": "National Competent Authority (or EASA for foreign MROs)",
            "license": "Part-145 Maintenance Organisation Approval (Reg 1321/2014)",
            "critical_hazard": "Unqualified technician signing Certificate of Release to Service",
            "statutory_sanction": "Immediate Part-145 approval revocation under 145.A.95"
        },
        "4": {
            "role": "Commercial Aerodrome Operator",
            "rulemaker": "European Commission & EASA",
            "overseer": "National Competent Authority of Aerodrome State",
            "license": "Aerodrome Operator Certificate (ADR) under Reg (EU) 139/2014",
            "critical_hazard": "Runway friction below minimums or RFFS response time > 3 min",
            "statutory_sanction": "Runway operational closure or category downgrade"
        },
        "5": {
            "role": "Air Navigation Service Provider (ANSP)",
            "rulemaker": "European Commission (Single European Sky) & EASA",
            "overseer": "National Supervisory Authority (NSA)",
            "license": "Air Navigation Services Certificate under Reg (EU) 2017/373",
            "critical_hazard": "Radar / VHF communications blackout in controlled airspace",
            "statutory_sanction": "Airspace flow rate reduced to zero (ground stop)"
        },
        "6": {
            "role": "Third-Country Foreign Airline (Non-EU)",
            "rulemaker": "ICAO (Annexes 1-19) & European Commission",
            "overseer": "EASA (Direct Centralized Safety Assessment)",
            "license": "Third-Country Operator (TCO) Authorization (Reg 452/2014)",
            "critical_hazard": "State of Operator receives ICAO Significant Safety Concern (SSC)",
            "statutory_sanction": "Added to EU Air Safety List (Blacklist) - Total EU ban"
        }
    }

    print("\n--- [MODULE 1: ECOSYSTEM GOVERNANCE EXPLORER] ---")
    print("Select an operational entity to inspect its regulatory architecture:")
    for k, v in ecosystem_map.items():
        print(f"  [{k}] {v['role']}")
    
    choice = prompt_str("Select entity (1-6)", "1")
    entity = ecosystem_map.get(choice, ecosystem_map["1"])

    print("\n" + "-" * 76)
    print(f"GOVERNANCE DOSSIER: {entity['role'].upper()}")
    print("-" * 76)
    print(f"  1. Who Makes the Rules?    : {entity['rulemaker']}")
    print(f"  2. Who Oversees Compliance?: {entity['overseer']}")
    print(f"  3. Certificate / License   : {entity['license']}")
    print(f"  • Core Critical Hazard     : {entity['critical_hazard']}")
    print(f"  • Regulatory Sanction      : {entity['statutory_sanction']}")

    # Module 2: Live Flight Dispatch Handshake Simulation
    print("\n--- [MODULE 2: LIVE 30-MINUTE FLIGHT DISPATCH HANDSHAKE] ---")
    print("Simulating flight DLH400 Frankfurt (EDDF) to New York (KJFK):")
    
    mro_crs = prompt_bool("  [1/4] Part-145 MRO: Has technician signed Certificate of Release to Service?", True)
    disp_ofp = prompt_bool("  [2/4] Airline Dispatch: Has Captain signed fuel-compliant Operational Flight Plan?", True)
    apt_rwy = prompt_bool("  [3/4] Airport ADR: Are runway braking friction & RFFS Cat 9 in service?", True)
    ans_slot = prompt_bool("  [4/4] Eurocontrol / ANSP: Is departure slot (CTOT) cleared without slot delay?", True)

    handshake_cleared = mro_crs and disp_ofp and apt_rwy and ans_slot
    print("\n" + "-" * 76)
    print("FLIGHT RELEASE DECISION MATRIX")
    print("-" * 76)
    print(f"  • Airworthiness Pillar (MRO) : {'[PASS - AIRCRAFT RELEASED]' if mro_crs else '[FAIL - NO CRS IN TECH LOG]'}")
    print(f"  • Operational Pillar (AOC)   : {'[PASS - OFP ACCEPTED]' if disp_ofp else '[FAIL - FUEL/CREW ILLEGAL]'}")
    print(f"  • Aerodrome Pillar (ADR)     : {'[PASS - RUNWAY SAFE]' if apt_rwy else '[FAIL - RUNWAY CONTAMINATED]'}")
    print(f"  • Airspace Pillar (ANSP)     : {'[PASS - SLOT CLEARED]' if ans_slot else '[FAIL - GROUND SLOT DELAY]'}")
    print(f"  -> FINAL DISPATCH RESULT     : {'[CLEARED FOR PUSHBACK & DEPARTURE]' if handshake_cleared else '[DEPARTURE PROHIBITED - GATE HOLD]'}")

    # Module 3: Adversarial Stress Test
    print("\n" + "=" * 76)
    print("ADVERSARIAL STRESS TEST: EMERGING TECH & THE REGULATORY VACUUM")
    print("=" * 76)
    print("Scenario: A startup attempts to launch an autonomous electric passenger drone")
    print("          (eVTOL) across European cities, claiming 'No current drone rules apply'.")
    print("\nEvaluating How the Tripartite Architecture Prevents Regulatory Vacuums:")
    print("  1. The Rulemaker Closes the Gap:")
    print("     -> EASA establishes Special Condition SC-VTOL under Regulation (EU) 2018/1139 Article 56.")
    print("  2. The Oversight Authority Steps In:")
    print("     -> EASA directly certifies the eVTOL airframe under Part-21; National Authorities")
    print("        issue Specific Category Authorizations under Regulation (EU) 2019/947.")
    print("  3. Operational Service Mandate:")
    print("     -> Operator cannot carry paying passengers without an Air Operator Certificate")
    print("        adapted for uncrewed air mobility.")
    print("  -> OUTCOME: The engineered ecosystem architecture prevents regulatory chaos,")
    print("              ensuring safety before passenger service begins.")
    print("=" * 76)
    print("Simulation completed successfully (Exit Code 0).")


if __name__ == "__main__":
    run_simulation()
