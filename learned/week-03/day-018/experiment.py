"""
Day 018 Experiment: Aviation Normative Hierarchy & AltMoC Safety Equivalence Classifier
Domain: Distinguish a legal obligation from AMC, GM, a certification specification and an internal company procedure.

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


def run_simulation():
    print("=" * 76)
    print("  AVIATION 365 - DAY 018: NORMATIVE HIERARCHY & ALTMOC CLASSIFIER")
    print("  Context: Hard Law vs AMC vs GM vs Certification Specs vs Company SOPs")
    print("  Governing Anchors: Reg (EU) 2018/1139, ORO.GEN.120, ARO.GEN.120")
    print("=" * 76)

    # 1. Normative Database
    tier_database = {
        "1": {
            "example": "CAT.OP.MPA.181 (Fuel Planning & In-Flight Fuel Management)",
            "tier": "Tier 1: Hard Law (Implementing Regulation)",
            "issued_by": "European Commission (Delegated / Implementing Act)",
            "binding": "LEGALLY BINDING IN ITS ENTIRETY (Direct Applicability)",
            "finding_valid": True,
            "deviation": "Prohibited without formal European Commission Article 71 Exemption."
        },
        "2": {
            "example": "CS-25.1309 (Equipment, Systems and Installations Safety Assessment)",
            "tier": "Tier 2: Certification Specifications (CS)",
            "issued_by": "EASA Executive Director Decision",
            "binding": "BINDING ONCE SELECTED AS TYPE CERTIFICATION BASIS",
            "finding_valid": True,
            "deviation": "Equivalent Safety Finding (ESF) or Special Condition (SC)."
        },
        "3": {
            "example": "AMC1 CAT.OP.MPA.181(a) (Specific Fuel Calculation Formulas)",
            "tier": "Tier 3: Acceptable Means of Compliance (AMC)",
            "issued_by": "EASA Executive Director Decision",
            "binding": "SOFT LAW (Grants Presumption of Conformity; Non-Exclusive)",
            "finding_valid": False,  # Finding cannot cite AMC alone, must cite the IR
            "deviation": "Alternative Means of Compliance (AltMoC) under ORO.GEN.120."
        },
        "4": {
            "example": "GM1 ORO.GEN.200(a)(1) (Guidance on Safety Culture & Management System)",
            "tier": "Tier 4: Guidance Material (GM)",
            "issued_by": "EASA Executive Director Decision",
            "binding": "PURELY ADVISORY (Explanatory / Educational Only)",
            "finding_valid": False,  # Illegal to issue finding on GM!
            "deviation": "Operator completely free to use alternative explanations."
        },
        "5": {
            "example": "Operations Manual Part A Section 8.3 (Airline Crosswind Limits 35 kt)",
            "tier": "Tier 5: Company Operating Procedure (SOP / OM / MOE)",
            "issued_by": "Airline Management (Accepted/Approved by NCA)",
            "binding": "INTERNALLY BINDING ON ALL COMPANY FLIGHT CREW",
            "finding_valid": True,
            "deviation": "Formal Management of Change (MOC) & Manual Revision Approval."
        }
    }

    print("\n--- [MODULE 1: NORMATIVE TIER CLASSIFIER] ---")
    print("Select a regulatory provision to classify:")
    for k, v in tier_database.items():
        print(f"  [{k}] {v['example']}")
    
    choice = prompt_str("Select provision (1-5)", "3")
    norm = tier_database.get(choice, tier_database["3"])

    print("\n" + "-" * 76)
    print(f"CLASSIFICATION RESULT: {norm['tier'].upper()}")
    print("-" * 76)
    print(f"  • Provision Evaluated   : {norm['example']}")
    print(f"  • Enacting Body         : {norm['issued_by']}")
    print(f"  • Legal Bindingness     : {norm['binding']}")
    print(f"  • Can Generate Finding? : {'YES (Valid Legal Ground)' if norm['finding_valid'] else 'NO (Must cite underlying Hard Law)'}")
    print(f"  • Permissible Deviation : {norm['deviation']}")

    # 2. AltMoC Safety Equivalence Engine
    print("\n--- [MODULE 2: ALTMOC QUANTITATIVE SAFETY EQUIVALENCE ENGINE] ---")
    print("Under ORO.GEN.120, an operator can replace an EASA AMC if Safety(AltMoC) >= Safety(AMC).")
    print("Testing an alternative EFB lithium battery containment procedure:")
    
    baseline_amc_uncontained_prob = prompt_float("EASA Baseline AMC Uncontained Fire Rate (per 10^9 hrs)", 7.2)
    altmoc_uncontained_prob = prompt_float("Proposed AltMoC Uncontained Fire Rate (per 10^9 hrs)", 4.8)
    cost_savings_eur = prompt_float("Fleet Implementation Cost Savings (€)", 350000.0)

    print("\n" + "-" * 76)
    print("SAFETY EQUIVALENCE VERIFICATION (ORO.GEN.120)")
    print("-" * 76)
    safety_margin = baseline_amc_uncontained_prob - altmoc_uncontained_prob
    altmoc_valid = altmoc_uncontained_prob <= baseline_amc_uncontained_prob

    print(f"  • Baseline AMC Risk Metric : {baseline_amc_uncontained_prob:.2f} hazards per 10^9 hrs")
    print(f"  • Proposed AltMoC Risk     : {altmoc_uncontained_prob:.2f} hazards per 10^9 hrs")
    print(f"  • Safety Margin Delta      : {safety_margin:+.2f} hazards per 10^9 hrs ({'SAFER' if safety_margin > 0 else 'HIGHER RISK'})")
    print(f"  • Direct Economic Benefit  : €{cost_savings_eur:,.2f} cost avoidance")
    print(f"  -> AltMoC Approval Status  : {'[APPROVED - EQUIVALENT/SUPERIOR SAFETY PROVEN]' if altmoc_valid else '[REJECTED - SAFETY DEGRADATION UNACCEPTABLE]'}")

    # 3. Adversarial Stress Test
    print("\n" + "=" * 76)
    print("ADVERSARIAL STRESS TEST: THE 'GM AUDIT FINDING' DEFENSE CHALLENGE")
    print("=" * 76)
    print("Scenario: An over-zealous NCA inspector issues a formal Level 2 finding against")
    print("          the airline: 'Failed to conduct weekly safety climate surveys as")
    print("          described in GM1 ORO.GEN.200(a)(1)'.")
    print("\nExecuting Compliance Officer Administrative Defense Analysis:")
    print("  1. Statutory Scrutiny:")
    print("     -> GM1 ORO.GEN.200(a)(1) is designated as Guidance Material by EASA Decision.")
    print("     -> Under EU law, GM is soft law lacking direct statutory authority.")
    print("  2. Primary Compliance Check:")
    print("     -> Airline complies with Hard Law requirement ORO.GEN.200 via its approved")
    print("        bi-annual safety committee meetings and confidential reporting system.")
    print("  3. Administrative Resolution:")
    print("     -> Formal written rebuttal submitted to Authority Head of Flight Operations.")
    print("     -> Legal finding officially QUASHED and removed from airline safety record.")
    print("=" * 76)
    print("Simulation completed successfully (Exit Code 0).")


if __name__ == "__main__":
    run_simulation()
