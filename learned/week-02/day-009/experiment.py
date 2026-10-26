"""
Day 009 Operational Experiment: ICAO SARPs Compliance & Article 38 State Differences Auditor
Domain: How Standards and Recommended Practices differ, including State differences and implementation.

Adheres to Aviation 365 Tool Principles:
  1. Authentic aviation calculations (USOAP Effective Implementation index, Article 38 categories)
  2. Interactive input with sensible defaults on Enter
  3. Step-by-step intermediate regulatory calculations
  4. Adversarial stress-testing (Sub-standard Category C deviation & Article 33 foreign route ban)
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
    print("  AVIATION 365 - DAY 009: ICAO SARPS & ARTICLE 38 DIFFERENCE AUDITOR")
    print("  Regulatory Foundation: Chicago Convention Articles 33, 37 & 38 (AIP GEN 1.7)")
    print("=" * 76)
    print("This tool analyzes national compliance with ICAO Standards & Recommended Practices,")
    print("categorizes national differences, and evaluates international mutual recognition risks.")
    print("-" * 76)

    total_provisions = int(prompt_float("Total ICAO Safety Standards Audited (Annexes 1, 6, 8, 14)", 320.0))
    compliant_provisions = int(prompt_float("Full Conformity Provisions (Standard enacted directly)", 288.0))
    cat_a_diff = int(prompt_float("Category A Differences (More Exacting / Stricter than ICAO)", 16.0))
    cat_b_diff = int(prompt_float("Category B Differences (Different Character / Equivalent Means)", 10.0))
    cat_c_diff = int(prompt_float("Category C Differences (Sub-Standard / Less Protective)", 6.0))
    intl_fleet_size = int(prompt_float("National Carrier International Airframes", 14.0))

    # Reconcile counts
    sum_provisions = compliant_provisions + cat_a_diff + cat_b_diff + cat_c_diff
    if sum_provisions != total_provisions:
        total_provisions = sum_provisions

    print("\n" + "=" * 76)
    print("  PHASE I: STATE DIFFERENCES AUDIT BREAKDOWN (AIP GEN 1.7)")
    print("=" * 76)

    pct_comp = (compliant_provisions / total_provisions) * 100.0
    pct_cat_a = (cat_a_diff / total_provisions) * 100.0
    pct_cat_b = (cat_b_diff / total_provisions) * 100.0
    pct_cat_c = (cat_c_diff / total_provisions) * 100.0

    print(f"[1/3] National Legal Enactment Breakdown (Total: {total_provisions} standards):")
    print(f"      1. Direct Full Compliance      : {compliant_provisions:>4} ({pct_comp:>5.1f}%) [Conforms to ICAO 'Shall']")
    print(f"      2. Category A (More Exacting)  : {cat_a_diff:>4} ({pct_cat_a:>5.1f}%) [Stricter safety margin]")
    print(f"      3. Category B (Equivalent Form): {cat_b_diff:>4} ({pct_cat_b:>5.1f}%) [e.g. inHg vs hPa, different means]")
    print(f"      4. Category C (Sub-Standard)   : {cat_c_diff:>4} ({pct_cat_c:>5.1f}%) [BELOW ICAO MINIMUM SAFETY LEVEL]")

    print("\n" + "=" * 76)
    print("  PHASE II: USOAP EFFECTIVE IMPLEMENTATION (EI) INDEX")
    print("=" * 76)

    # Effective implementation counts compliant, Cat A, and Cat B (acceptable alternative means)
    effective_count = compliant_provisions + cat_a_diff + cat_b_diff
    ei_score = (effective_count / total_provisions) * 100.0

    print(f"[2/3] ICAO Universal Safety Oversight Audit Programme (USOAP) Scoring:")
    print(f"      Acceptable Enactments (Compliant + Cat A + Cat B): {effective_count} / {total_provisions}")
    print(f"      State Effective Implementation (EI) Score       : {ei_score:.2f}%")
    print(f"      Global ICAO Target Baseline                     : 60.00% (High-priority threshold)")

    if ei_score >= 80.0:
        print(f"      OVERSIGHT RATING: EXCELLENT / MATURE SAFETY SYSTEM")
    elif ei_score >= 60.0:
        print(f"      OVERSIGHT RATING: SATISFACTORY (Above Global Baseline)")
    else:
        print(f"      OVERSIGHT RATING: SIGNIFICANT SAFETY CONCERN (SSC) RISK")

    print("\n" + "=" * 76)
    print("  PHASE III: CONDITIONAL MUTUAL RECOGNITION AUDIT (ARTICLE 33)")
    print("=" * 76)

    print(f"[3/3] Evaluating International Acceptance of State Airworthiness & Crew Licenses:")
    if cat_c_diff == 0:
        print(f"      STATUS: FULL ARTICLE 33 CONFORMITY")
        print(f"      Foreign States MUST recognize certificates and licenses without exception.")
    else:
        print(f"      WARNING: {cat_c_diff} Sub-standard Category C differences registered in AIP GEN 1.7.")
        print(f"      Under Article 33, foreign States are legally permitted to DENY entry to aircraft")
        print(f"      operating under sub-standard national regulations.")

    print("\n" + "=" * 76)
    print("  PHASE IV: ADVERSARIAL STRESS TEST (ARTICLE 33 FOREIGN ROUTE BAN)")
    print("=" * 76)
    print("Injecting International Regulatory Enforcement Scenario:")
    print("  - Foreign oversight body (e.g. EASA TCO or FAA IASA) audits national difference filings.")
    print("  - Discovers 2 Category C differences in Annex 6 (in-flight fuel reserve policy)")
    print("    and 4 Category C differences in Annex 8 (fatigue cracking inspection intervals).")
    print("  - Foreign authority revokes Third Country Operator (TCO) commercial landing permits.")

    monthly_rev_per_aircraft = 1320000.0  # €1.32M per widebody international aircraft/month
    monthly_airline_loss = intl_fleet_size * monthly_rev_per_aircraft
    legal_remediation_cost = 450000.0     # Emergency rulemaking, consultant audit, AIP update

    print(f"\n  Financial & Operational Consequences of Article 33 Denial:")
    print(f"    - Banned International Aircraft Fleet        : {intl_fleet_size} aircraft grounded from international routes")
    print(f"    - Lost Commercial Route Revenue per Month    : €{monthly_airline_loss:,.2f}")
    print(f"    - Emergency State Regulatory Remediation Cost: €{legal_remediation_cost:,.2f}")
    print(f"    ----------------------------------------------------------------------")
    print(f"    - Total 90-Day Sanction Cost                 : €{(monthly_airline_loss * 3 + legal_remediation_cost):,.2f}")

    print(f"\n  Aviation Law Takeaway:")
    print(f"    Article 38 allows a State to differ from ICAO, but Article 33 ensures other nations")
    print(f"    do not have to accept sub-standard aircraft into their skies. Standards protect the network.")

    print("\n" + "=" * 76)
    print("  SIMULATION COMPLETE (Exit Code 0)")
    print("=" * 76)

if __name__ == "__main__":
    run_simulation()
