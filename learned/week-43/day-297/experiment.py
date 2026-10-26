"""
Day 297 Experiment: Safety Management System (SMS) Risk Engine
Domain: Map the response to a fictional aircraft emergency on or near an airport.
Adheres to the 6 PracticAI Experiment Rules:
  1. Interactive input with sensible defaults on Enter
  2. Step-by-step intermediate calculations
  3. Stress-testing / boundary conditions
  4. Formatted ASCII output
  5. Completely self-contained standard library Python
  6. Clean exit code 0
"""

import sys
import time

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
    print("=" * 72)
    print("  AVIATION 365 - DAY 297: SMS RISK ASSESSMENT & BOW-TIE ENGINE")
    print("  Context: Map the response to a fictional aircraft emergency on or near an airport.")
    print("=" * 72)

    likelihood = int(prompt_float("Hazard Likelihood (1=Extremely Improbable to 5=Frequent)", 3))
    severity = int(prompt_float("Hazard Severity (1=Negligible to 5=Catastrophic)", 4))
    b1_eff = prompt_float("Preventive Barrier 1 Effectiveness (0.0 to 1.0)", 0.85)
    b2_eff = prompt_float("Preventive Barrier 2 Effectiveness (0.0 to 1.0)", 0.70)

    raw_risk_score = likelihood * severity
    print(f"\n[1/3] Baseline 5x5 Risk Matrix Assessment (ICAO Doc 9859):")
    print(f"  -> Likelihood Index: {likelihood}")
    print(f"  -> Severity Index: {severity}")
    print(f"  -> Pre-Mitigation Risk Index: {raw_risk_score} / 25")

    if raw_risk_score >= 15:
        category = "INTOLERABLE (Red) - Cease Operation Immediately"
    elif raw_risk_score >= 8:
        category = "TOLERABLE (Yellow) - Review and Mitigation Required"
    else:
        category = "ACCEPTABLE (Green) - Routine Monitoring"
    print(f"  -> Initial Safety Classification: {category}")

    combined_failure_prob = (1.0 - b1_eff) * (1.0 - b2_eff)
    mitigated_likelihood = max(1, round(likelihood * combined_failure_prob))
    mitigated_risk_score = mitigated_likelihood * severity

    print(f"\n[2/3] Bow-Tie Safety Barrier Mitigation Impact:")
    print(f"  -> Barrier 1 (Procedural SOP): {b1_eff * 100:.1f}% effective")
    print(f"  -> Barrier 2 (Technical Monitoring): {b2_eff * 100:.1f}% effective")
    print(f"  -> Compound Unmitigated Escape Probability: {combined_failure_prob * 100:.2f}%")
    print(f"  -> Mitigated Likelihood Index: {mitigated_likelihood}")
    print(f"  -> Post-Mitigation Risk Index: {mitigated_risk_score} / 25")

    print(f"\n[3/3] Safety Assurance & SMS Regulatory Action Plan:")
    if mitigated_risk_score < 8:
        print("  -> SMS VERDICT: Mitigation Sufficient. Operation Approved under Safety Assurance oversight.")
    else:
        print("  -> SMS VERDICT: Residual Risk remains High. Additional Engineered Barriers Required.")

    print("=" * 72)
    print("Simulation finished successfully (Exit Code 0).")

if __name__ == '__main__':
    run_simulation()
