"""
Day 015 Experiment: European Aviation Governance & Standardisation Inspector
Domain: The European Commission, EASA, EU Member States and national competent authorities.

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


def run_simulation():
    print("=" * 76)
    print("  AVIATION 365 - DAY 015: EUROPEAN AVIATION GOVERNANCE & OVERSIGHT")
    print("  Context: Division of Competence (EASA vs NCAs) & Standardisation Audits")
    print("  Statutory Anchor: Regulation (EU) 2018/1139 (EASA Basic Regulation)")
    print("=" * 76)

    # 1. Competence Router Table
    competence_map = {
        "1": {
            "task": "Type Certification of New Commercial Jet (e.g. A321XLR)",
            "authority": "EASA (Direct Centralized Competence)",
            "legal_basis": "Regulation (EU) 748/2012 (Part-21)",
            "role": "EASA certification team evaluates compliance with CS-25."
        },
        "2": {
            "task": "Issue & Oversee Air Operator Certificate (AOC) for Airline",
            "authority": "National Competent Authority (NCA) of Operator State",
            "legal_basis": "Regulation (EU) 965/2012 (Air Ops / Part-CAT)",
            "role": "NCA (e.g. DGAC, LBA, AESA) inspects airline manuals, SMS, and FTL."
        },
        "3": {
            "task": "Third-Country Operator Authorization (e.g. United Airlines to EU)",
            "authority": "EASA (Direct Centralized Competence)",
            "legal_basis": "Regulation (EU) 452/2014 (Part-TCO)",
            "role": "EASA evaluates foreign operator ICAO compliance and safety record."
        },
        "4": {
            "task": "Commercial Pilot License & Type Rating Issuance (ATPL)",
            "authority": "National Competent Authority (NCA) of License Holder",
            "legal_basis": "Regulation (EU) 1178/2011 (Part-FCL)",
            "role": "NCA tests applicant, reviews logbooks, and issues physical license."
        },
        "5": {
            "task": "Certification of Commercial Airport (e.g. Frankfurt EDDF)",
            "authority": "National Competent Authority (NCA) of Aerodrome State",
            "legal_basis": "Regulation (EU) 139/2014 (ADR)",
            "role": "NCA inspects runway friction, obstacle limitation surfaces, and RFFS."
        }
    }

    print("\n--- [MODULE 1: DIVISION OF COMPETENCE ROUTER] ---")
    print("Select an operational scenario to route authority:")
    for k, v in competence_map.items():
        print(f"  [{k}] {v['task']}")
    
    choice = prompt_str("Enter scenario number (1-5)", "2")
    selected = competence_map.get(choice, competence_map["2"])

    print(f"\n  • Operational Domain   : {selected['task']}")
    print(f"  • Competent Authority  : {selected['authority']}")
    print(f"  • Primary EU Rule      : {selected['legal_basis']}")
    print(f"  • Institutional Action : {selected['role']}")

    # 2. EASA Standardisation Inspection Simulation
    print("\n--- [MODULE 2: EASA STANDARDISATION INSPECTION OF AN NCA] ---")
    print("Under Commission Implementing Regulation (EU) No 628/2013, EASA audits")
    print("National Competent Authorities to prevent safety divergence.")
    
    checkpoints = prompt_int("Number of NCA Regulatory Checkpoints Audited", 120)
    class_c = prompt_int("Class C Findings (Observations / Administrative)", 6)
    class_d = prompt_int("Class D Findings (Standard Non-Compliance with EU Rules)", 4)
    class_g = prompt_int("Class G Findings (Immediate / Urgent Safety Risk)", 1)

    # Weights: C=0.05, D=0.30, G=1.00
    w_c, w_d, w_g = 0.05, 0.30, 1.00
    weighted_penalty = (w_c * class_c) + (w_d * class_d) + (w_g * class_g)
    sci = max(0.0, 100.0 - ((weighted_penalty / checkpoints) * 100.0))

    print("\n" + "-" * 76)
    print("EASA STANDARDISATION AUDIT SCORECARD")
    print("-" * 76)
    print(f"  • Total Checkpoints Audited    : {checkpoints}")
    print(f"  • Class C (Observations)       : {class_c}  (Weight: {w_c:.2f} -> Penalty: {class_c * w_c:.2f})")
    print(f"  • Class D (Non-Compliances)    : {class_d}  (Weight: {w_d:.2f} -> Penalty: {class_d * w_d:.2f})")
    print(f"  • Class G (Immediate Hazards)  : {class_g}  (Weight: {w_g:.2f} -> Penalty: {class_g * w_g:.2f})")
    print(f"  • Cumulative Weighted Penalty  : {weighted_penalty:.2f} penalty units")
    print(f"  -> Standardisation Index (SCI) : {sci:.2f}% (Safeguard Threshold: 70.0%)")

    # Regulatory Action & Clock
    print("\n" + "-" * 76)
    print("MANDATORY REGULATORY ACTIONS & CORRECTIVE TIMELINES")
    print("-" * 76)
    if class_g > 0:
        print("  • URGENT SAFETY ALERT (Class G Present):")
        print("    -> 15-DAY CLOCK: NCA must immediately adopt provisional safety measures")
        print("       (e.g. restrict affected operator operations or revoke defective approval).")
    else:
        print("  • Zero immediate safety findings (No Class G).")

    if class_d > 0:
        print("  • NON-COMPLIANCE CORRECTIVE ACTION (Class D Present):")
        print("    -> 90-DAY CLOCK: NCA must submit an agreed Corrective Action Plan (CAP)")
        print("       demonstrating institutional root-cause resolution.")
    else:
        print("  • Full regulatory compliance across all standard checkpoints.")

    safeguard_triggered = (sci < 70.0) or (class_g > 0)
    print(f"\n  • Article 67 Mutual Recognition: {'[MAINTAINED - CONDITIONAL ON CAP]' if not safeguard_triggered else '[RISK OF ARTICLE 70 SAFEGUARD MEASURE]'}")

    # 3. Adversarial Stress Test
    print("\n" + "=" * 76)
    print("ADVERSARIAL STRESS TEST: UNMITIGATED CLASS G & ARTICLE 258 INFRINGEMENT")
    print("=" * 76)
    print("Scenario: Member State NCA fails to resolve Class G finding within 15 days,")
    print("          allowing an un-airworthy cargo airline to continue commercial operations.")
    print("\nEvaluating Escalation Path under EU Aviation & Treaty Law:")
    print("  1. EASA Executive Action:")
    print("     -> Issues negative Standardisation Report directly to the European Commission.")
    print("  2. European Commission Safeguard Measure (Article 70, Reg 2018/1139):")
    print("     -> Suspends mutual recognition of certificates issued by the offending NCA.")
    print("     -> Other 26 Member States legally empowered to reject aircraft & airmen from that State.")
    print("  3. Treaty Infringement Procedure (Article 258 TFEU):")
    print("     -> European Commission launches formal legal action at the European Court of Justice.")
    print("     -> Daily financial penalty fines levied against the Member State until compliance.")
    print("=" * 76)
    print("Simulation completed successfully (Exit Code 0).")


if __name__ == "__main__":
    run_simulation()
