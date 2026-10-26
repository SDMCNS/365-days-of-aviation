"""
Day 014 Experiment: ICAO Global Safety Influence & USOAP Audit Contagion Simulator
Domain: Explain how ICAO influences aviation without acting as a global aviation regulator for every operation.

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


def run_simulation():
    print("=" * 76)
    print("  AVIATION 365 - DAY 014: ICAO GLOBAL SAFETY OVERSIGHT (USOAP) SIMULATOR")
    print("  Context: How ICAO Influences Without Direct Sovereign Enforcement Power")
    print("  Statutory Anchors: Chicago Convention Articles 1, 33, 37, 38, 54, 83 bis")
    print("=" * 76)

    # State Fleet & Economic Context
    fleet_size = prompt_int("Number of Registered Commercial Jet Aircraft in Audited State", 18)
    int_pax_millions = prompt_float("Annual International Passengers Carried (Millions)", 4.5)

    # USOAP 8 Critical Elements Audit Model
    print("\n[CONFIGURING USOAP AUDIT SCORES ACROSS THE 8 CRITICAL ELEMENTS]")
    print("Enter the Effective Implementation (EI %) score for each Critical Element:")
    ce1 = prompt_float("  • CE-1: Primary Aviation Legislation (EI %)", 85.0)
    ce2 = prompt_float("  • CE-2: Operating Regulations (EI %)", 82.0)
    ce3 = prompt_float("  • CE-3: Civil Aviation Authority System & Funding (EI %)", 70.0)
    ce4 = prompt_float("  • CE-4: Technical Personnel Qualifications & Training (EI %)", 52.0)
    ce5 = prompt_float("  • CE-5: Technical Guidance, Tools & Procedures (EI %)", 74.0)
    ce6 = prompt_float("  • CE-6: Licensing, Certification & Approval Obligations (EI %)", 58.0)
    ce7 = prompt_float("  • CE-7: Surveillance Obligations (Airlines/MROs) (EI %)", 42.0)
    ce8 = prompt_float("  • CE-8: Resolution of Safety Concerns (EI %)", 40.0)

    # Weights across Critical Elements based on ICAO protocol questions
    weights = [45, 110, 70, 95, 80, 160, 180, 90]
    scores = [ce1, ce2, ce3, ce4, ce5, ce6, ce7, ce8]
    total_pqs = sum(weights)
    weighted_sum = sum(w * (s / 100.0) for w, s in zip(weights, scores))
    overall_ei = (weighted_sum / total_pqs) * 100.0

    print("\n" + "-" * 76)
    print("USOAP CONTINUOUS MONITORING AUDIT REPORT")
    print("-" * 76)
    ce_names = [
        "CE-1 Primary Legislation",
        "CE-2 Operating Regs",
        "CE-3 CAA Structure/Funding",
        "CE-4 Inspector Qualifications",
        "CE-5 Technical Guidance/SOPs",
        "CE-6 Certification Obligations",
        "CE-7 Surveillance Obligations",
        "CE-8 Safety Issue Resolution"
    ]

    for name, w, s in zip(ce_names, weights, scores):
        status_flag = "[SATISFACTORY]" if s >= 65.0 else "[DEFICIENT]"
        print(f"  {name:<32} (Weight: {w:3d} PQs) : {s:5.1f}%  {status_flag}")

    print("-" * 76)
    print(f"  OVERALL STATE EFFECTIVE IMPLEMENTATION (EI) : {overall_ei:.2f}% (Global Benchmark: ~68.5%)")

    # Evaluation of Significant Safety Concern (SSC)
    ssc_triggered = (ce6 < 60.0 and ce7 < 50.0) or (ce8 < 45.0)

    print("\n" + "-" * 76)
    print("ICAO ACTION & SOVEREIGN REPUTATION DETERMINATION")
    print("-" * 76)
    if ssc_triggered:
        print("  • ICAO Council Notification : [SIGNIFICANT SAFETY CONCERN (SSC) ISSUED]")
        print("    Finding: CAA failed to demonstrate adequate safety oversight and surveillance")
        print("    over commercial air operators under Annex 6.")
        print("  • Article 33 Legal Status   : [MUTUAL RECOGNITION SHIELD WITHDRAWN]")
        print("    Foreign States are legally entitled to refuse entry to aircraft from this State.")
    else:
        print("  • ICAO Council Notification : [NO SIGNIFICANT SAFETY CONCERNS IDENTIFIED]")
        print("  • Article 33 Legal Status   : [FULL MUTUAL RECOGNITION MAINTAINED]")
        print("    All contracting States recognize airworthiness and pilot certificates.")

    # Third-Party Market Reaction Model
    print("\n" + "-" * 76)
    print("THE MULTI-TIER MARKET ENFORCEMENT CASCADE")
    print("-" * 76)
    if ssc_triggered:
        faa_status = "CATEGORY 2 (Deficient - Route expansion frozen, existing flights inspected)"
        eu_status = "ADDED TO EU AIR SAFETY LIST (Regulation EC 2111/2005 - Total Airspace Ban)"
        insurance_surcharge = 350000.0  # USD per aircraft per year
        route_loss_pct = 0.40  # 40% loss of international traffic
    elif overall_ei < 60.0:
        faa_status = "CATEGORY 1 WITH ENHANCED SURVEILLANCE WARNING"
        eu_status = "OPERATOR PLACED ON EU WATCHLIST / TARGETED RAMP INSPECTIONS (SAFA)"
        insurance_surcharge = 75000.0
        route_loss_pct = 0.05
    else:
        faa_status = "CATEGORY 1 (Fully Compliant)"
        eu_status = "UNRESTRICTED ACCESS (Standard SAFA Sampling)"
        insurance_surcharge = 0.0
        route_loss_pct = 0.0

    annual_insurance_hit = fleet_size * insurance_surcharge
    avg_fare_usd = 380.0
    direct_revenue_loss = (int_pax_millions * 1e6) * route_loss_pct * avg_fare_usd
    total_economic_cost = direct_revenue_loss + annual_insurance_hit

    print(f"  • US FAA IASA Audit Rating      : {faa_status}")
    print(f"  • European Union Air Safety List: {eu_status}")
    print(f"  • Hull & Liability Insurance Hit: +${annual_insurance_hit:,.2f}/yr across {fleet_size} jets")
    print(f"  • Estimated Commercial Rev Loss : -${direct_revenue_loss:,.2f}/yr")
    print(f"  -> TOTAL ANNUAL ECONOMIC IMPACT  : -${total_economic_cost:,.2f}/year")

    # Adversarial Stress Test
    print("\n" + "=" * 76)
    print("ADVERSARIAL STRESS TEST: REGIONAL SAFETY OVERSIGHT ORGANIZATION (RSOO) REMEDY")
    print("=" * 76)
    print("Scenario: The State cannot afford to recruit and pay 25 senior widebody inspectors.")
    print("Strategy: State pools sovereignty and technical inspectors into a Regional Safety")
    print("          Oversight Organisation (RSOO) with 4 neighboring States.")
    print("\nSimulating Post-RSOO Re-Audit Metrics:")
    print("  • Shared inspector pool deployed across the region.")
    print("  • CE-4 Inspector Qualification increases from 52.0% -> 82.0%")
    print("  • CE-7 Surveillance frequency increases from 42.0% -> 88.0%")
    print("  • CE-8 Safety Defect Resolution increases from 40.0% -> 85.0%")

    new_scores = [ce1, ce2, ce3, 82.0, ce5, ce6, 88.0, 85.0]
    new_weighted_sum = sum(w * (s / 100.0) for w, s in zip(weights, new_scores))
    new_overall_ei = (new_weighted_sum / total_pqs) * 100.0

    print(f"  • Post-RSOO Effective Implementation : {new_overall_ei:.2f}% (Gain: +{new_overall_ei - overall_ei:.2f}%)")
    print("  • SSC Status                          : [OFFICIALLY RESOLVED AND LIFTED BY ICAO]")
    print("  • Commercial Restoration              : Sovereign airspace bans lifted; insurance restored.")
    print("=" * 76)
    print("Simulation completed successfully (Exit Code 0).")


if __name__ == "__main__":
    run_simulation()
