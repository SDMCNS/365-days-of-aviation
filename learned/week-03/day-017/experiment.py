"""
Day 017 Experiment: Regulatory Traceability Table & Compliance Gap Analysis Engine
Domain: Create a regulatory traceability table: requirement, source, responsible authority, regulated organisation and evidence.

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
    print("  AVIATION 365 - DAY 017: REGULATORY TRACEABILITY & COMPLIANCE MATRIX")
    print("  Context: 5-Point Traceability (Requirement -> Source -> Authority -> Org -> Evidence)")
    print("  Governing Anchors: Reg (EU) 965/2012, Reg (EU) 1321/2014, Reg (EU) 139/2014")
    print("=" * 76)

    # Master Traceability Database
    traceability_db = {
        "1": {
            "name": "Pre-Flight Fuel Planning",
            "req": "Mandatory carriage of taxi, trip, contingency (5%), alternate & 30-min final reserve fuel.",
            "source": "Reg (EU) 965/2012 CAT.OP.MPA.181 & AMC1",
            "authority": "National Competent Authority (NCA)",
            "org": "Commercial Air Transport Airline (Part-CAT)",
            "policy": "Operations Manual Part A (OM-A) Section 8.1.7",
            "procedure": "Flight Dispatch SOP Manual Section 4.2",
            "evidence": "Signed Operational Flight Plan (OFP) & Aircraft Tech Log (ATL) Fuel Page"
        },
        "2": {
            "name": "Flight Crew Fatigue & Duty Limits",
            "req": "Flight Duty Period (FDP) capped based on sectors and start time; mandatory rest periods.",
            "source": "Reg (EU) 965/2012 ORO.FTL.205 & CS-FTL.1",
            "authority": "National Competent Authority (NCA)",
            "org": "Commercial Air Transport Airline (Part-CAT)",
            "policy": "Operations Manual Part A (OM-A) Section 7",
            "procedure": "Crew Scheduling System Standard Operating Procedures",
            "evidence": "Rostering System Duty Records & Commander Discretion Reports (Form 104)"
        },
        "3": {
            "name": "Aircraft Maintenance Release",
            "req": "Aircraft cannot be operated without a formal release certifying maintenance completion.",
            "source": "Reg (EU) 1321/2014 M.A.801 & 145.A.50",
            "authority": "NCA / EASA (for Foreign MROs)",
            "org": "Part-145 Maintenance Organisation / CAMO",
            "policy": "Maintenance Organisation Exposition (MOE) Chapter 2",
            "procedure": "Aircraft Line Maintenance Release Work Instructions",
            "evidence": "Certificate of Release to Service (CRS) signed in Aircraft Technical Log"
        },
        "4": {
            "name": "Low Visibility All-Weather Operations",
            "req": "Specific approval required for CAT II/III precision approaches; autoland limits.",
            "source": "Reg (EU) 965/2012 SPA.LVO.100 & AMC1",
            "authority": "National Competent Authority (NCA)",
            "org": "Commercial Air Transport Airline (Part-CAT)",
            "policy": "Operations Manual Part A & B (OM-A/B) All-Weather Operations",
            "procedure": "Low Visibility Instrument Approach Briefing Card SOP",
            "evidence": "AOC OpSpecs Attachment, AFM Autoland Cert & Pilot 6-Month Sim Check Form"
        },
        "5": {
            "name": "Aerodrome Rescue & Firefighting (RFFS)",
            "req": "Aerodrome must maintain dedicated RFFS category with emergency response time <= 3 minutes.",
            "source": "Reg (EU) 139/2014 ADR.OPS.B.010",
            "authority": "National Competent Authority (NCA)",
            "org": "Certified Aerodrome Operator (ADR)",
            "policy": "Aerodrome Manual Chapter 5 (Emergency Services)",
            "procedure": "Airport Fire Service Standard Operating Procedures",
            "evidence": "Daily RFFS Watch Readiness Log & Annual Full-Scale Drill Reports"
        },
        "6": {
            "name": "Dangerous Goods Carriage by Air",
            "req": "Mandatory acceptance inspection, package labeling, segregation & captain notification.",
            "source": "Reg (EU) 965/2012 CAT.GEN.MPA.200 & ICAO Doc 9284",
            "authority": "National Competent Authority (NCA)",
            "org": "Commercial Air Transport Airline (Part-CAT)",
            "policy": "Operations Manual Part A (OM-A) Section 9",
            "procedure": "Cargo Handling & Dangerous Goods Acceptance SOP",
            "evidence": "Completed DG Acceptance Checklist & NOTOC signed by Captain"
        }
    }

    print("\n--- [MODULE 1: MASTER TRACEABILITY INSPECTOR] ---")
    print("Available Operational Regulatory Chains:")
    for k, v in traceability_db.items():
        print(f"  [{k}] {v['name']}")
    
    choice = prompt_str("Select chain to inspect (1-6)", "1")
    item = traceability_db.get(choice, traceability_db["1"])

    print("\n" + "-" * 76)
    print(f"TRACEABILITY RECORD: {item['name'].upper()}")
    print("-" * 76)
    print(f"  1. Operational Requirement : {item['req']}")
    print(f"  2. Statutory Source Law    : {item['source']}")
    print(f"  3. Responsible Authority   : {item['authority']}")
    print(f"  4. Regulated Organisation  : {item['org']}")
    print(f"  • Company Policy Reference : {item['policy']}")
    print(f"  • Documented Procedure/SOP : {item['procedure']}")
    print(f"  5. Auditable Proof Evidence: {item['evidence']}")

    # Module 2: System Traceability Completeness & Gap Analysis
    print("\n--- [MODULE 2: AIRLINE TRACEABILITY GAP ANALYSIS] ---")
    print("Simulating an NCA audit across all 6 core operational domains...")
    
    inject_gap = prompt_bool("Simulate a missing evidence artifact (e.g. un-archived OFP logs)?", False)
    
    total_domains = len(traceability_db)
    valid_chains = total_domains if not inject_gap else (total_domains - 1)
    completeness_index = (valid_chains / total_domains) * 100.0

    print("\n" + "-" * 76)
    print("TRACEABILITY COMPLETENESS AUDIT RESULT")
    print("-" * 76)
    print(f"  • Total Regulatory Domains Evaluated : {total_domains}")
    print(f"  • Unbroken 5-Point Traceability Chains: {valid_chains}")
    print(f"  • Broken Chains / Compliance Gaps    : {total_domains - valid_chains}")
    print(f"  -> System Traceability Metric (Theta): {completeness_index:.2f}%")

    if completeness_index == 100.0:
        audit_outcome = "PASS - UNRESTRICTED COMPLIANCE (Zero Audit Findings)"
        remedy = "Full regulatory assurance across all audited domains."
    else:
        audit_outcome = "FAIL - FORMAL LEVEL 2 AUDIT FINDING ISSUED (Part-ARO.GEN.350)"
        remedy = "Compliance blind spot detected. Operator has 90 days to establish auditable archive SOP."

    print(f"  • Audit Finding Decision             : [{audit_outcome}]")
    print(f"  • Regulatory Consequence             : {remedy}")

    # Module 3: Adversarial Stress Test
    print("\n" + "=" * 76)
    print("ADVERSARIAL STRESS TEST: MANAGEMENT OF CHANGE LEAD-TIME DEFICIT")
    print("=" * 76)
    print("Scenario: EASA publishes an amendment to Fuel Scheme rules (Implementing Reg).")
    print("  • Statutory Lead Time until Effective Date: 60 Days")
    print("  • Operator Internal MOC Required Timeline :")
    print("    - Gap Analysis & Policy Drafting       : 20 Days")
    print("    - Manual OM-A Revision & Translation   : 25 Days")
    print("    - Authority Prior Approval Review      : 30 Days")
    print("    - Flight Crew & Dispatcher Retraining  : 15 Days")
    print("    - Total Internal MOC Time Required     : 90 Days")

    lead_deficit = 90 - 60
    print(f"\n  • Regulatory Lead Time Deficit           : {lead_deficit} Days BEHIND DEADLINE")
    print("  -> OPERATIONAL CONSEQUENCE               : [ILLEGAL NON-COMPLIANT OPERATION]")
    print("     On the statutory effective date, the airline's operations manual will be")
    print("     legally invalid. Ramp inspections (SAFA) will issue Category 3 findings,")
    print("     grounding aircraft on foreign airport aprons until manuals are re-approved.")
    print("=" * 76)
    print("Simulation completed successfully (Exit Code 0).")


if __name__ == "__main__":
    run_simulation()
