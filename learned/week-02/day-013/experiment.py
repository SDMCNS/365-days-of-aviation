"""
Day 013 Experiment: Specific Approvals & Operational Authorization Simulator
Domain: Connect international standards to certificates, operational approvals and local procedures.

Adheres to PracticAI Core Standards:
  1. Interactive input with sensible defaults on Enter
  2. Step-by-step transparent intermediate calculations
  3. Adversarial boundary & stress-testing
  4. Clean, formatted ASCII tables
  5. Standard library Python only
  6. Clean exit code 0
"""

import sys
import math

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
    print("  AVIATION 365 - DAY 013: OPERATIONAL APPROVALS & SPECIFIC SPECIFICATIONS")
    print("  Context: Connecting ICAO Annex 6/8 Standards to AOC, OpSpecs & Cockpit SOP")
    print("  Regulatory Anchors: EASA Part-SPA / FAA 14 CFR Part 121 / ICAO Annex 6")
    print("=" * 76)

    # 1. ETOPS / EDTO Configuration
    print("\n--- [MODULE 1: ETOPS / EDTO DISPATCH ENVELOPE] ---")
    oei_speed_ktas = prompt_float("Approved One-Engine-Inoperative (OEI) Cruise Speed (KTAS)", 430.0)
    etops_minutes = prompt_float("AOC OpSpec Approved ETOPS Diversion Time Limit (minutes)", 180.0)
    max_route_divert_dist = prompt_float("Furthest Distance from Route Point to Nearest Adequate Alternate (NM)", 1180.0)

    # Calculate max diversion radius
    d_max_nm = oei_speed_ktas * (etops_minutes / 60.0)
    etops_legal = max_route_divert_dist <= d_max_nm

    print(f"\n  • Single-Engine Cruise Speed : {oei_speed_ktas:.1f} KTAS")
    print(f"  • Approved Diversion Limit   : {etops_minutes:.0f} minutes")
    print(f"  • Max Permissible Range      : {oei_speed_ktas:.1f} x ({etops_minutes:.0f}/60) = {d_max_nm:.1f} NM")
    print(f"  • Planned Route Critical Pt  : {max_route_divert_dist:.1f} NM from nearest alternate")
    print(f"  • ETOPS Legal Dispatch Margin: {d_max_nm - max_route_divert_dist:+.1f} NM")
    print(f"  -> ETOPS DISPATCH STATUS     : {'[AUTHORIZED - LEGAL TO DEPART]' if etops_legal else '[PROHIBITED - ROUTE OUTSIDE ENVELOPE]'}")

    # 2. Low Visibility CAT IIIb Approach Verification
    print("\n--- [MODULE 2: ALL-WEATHER CAT IIIb 4-PILLAR VERIFICATION] ---")
    reported_rvr_m = prompt_float("Reported Touchdown Runway Visual Range (RVR in meters)", 125.0)
    opspec_cat3b = prompt_bool("Pillar 1: Operator AOC OpSpec has CAT IIIb Specific Approval?", True)
    afm_fail_op = prompt_bool("Pillar 2: Aircraft AFM certified Fail-Operational & Dual Autopilots serviceable?", True)
    crew_current = prompt_bool("Pillar 3: Flight Crew current with recurrent simulator autoland checks?", True)
    lvp_active = prompt_bool("Pillar 4: Destination Airport has Low Visibility Procedures (LVP) active?", True)

    # Approach minimums table
    cat_minima = {
        "CAT I": {"min_rvr": 550, "min_dh": 200, "req_p1": False, "desc": "Standard Manual / AP Approach"},
        "CAT II": {"min_rvr": 300, "min_dh": 100, "req_p1": True, "desc": "Precision Approach Fail-Passive"},
        "CAT IIIa": {"min_rvr": 175, "min_dh": 50, "req_p1": True, "desc": "Autoland Fail-Passive"},
        "CAT IIIb": {"min_rvr": 75, "min_dh": 0, "req_p1": True, "desc": "Autoland Fail-Operational with Rollout"}
    }

    pillar_opspec = 1 if opspec_cat3b else 0
    pillar_aircraft = 1 if afm_fail_op else 0
    pillar_crew = 1 if crew_current else 0
    pillar_facility = 1 if lvp_active else 0
    composite_clearance = pillar_opspec * pillar_aircraft * pillar_crew * pillar_facility

    print("\n[Evaluating 4-Pillar Clearance Function: Phi = OpSpec x Aircraft x Crew x Facility]")
    print(f"  • Pillar 1 (Airline OpSpec)      : {'[PASS]' if pillar_opspec else '[FAIL - NO OPSPEC APPROVAL]'}")
    print(f"  • Pillar 2 (Aircraft Airworthy)  : {'[PASS]' if pillar_aircraft else '[FAIL - SYSTEM UNINTELLIGIBLE/MEL]'}")
    print(f"  • Pillar 3 (Flight Crew Currency): {'[PASS]' if pillar_crew else '[FAIL - PILOT CHECKS EXPIRED]'}")
    print(f"  • Pillar 4 (Airport LVP Active)  : {'[PASS]' if pillar_facility else '[FAIL - LVP NOT IN FORCE]'}")

    cat3b_weather_ok = reported_rvr_m >= cat_minima["CAT IIIb"]["min_rvr"]
    final_autoland_legal = composite_clearance == 1 and cat3b_weather_ok

    print(f"\n  • Reported Runway RVR            : {reported_rvr_m:.0f} m (CAT IIIb Minimum: 75 m)")
    print(f"  • Weather Legal Status           : {'[SATISFIES CAT IIIb]' if cat3b_weather_ok else '[BELOW CAT IIIb ABSOLUTE MINIMA]'}")
    print(f"  -> APPROACH CLEARANCE OUTCOME    : {'[CLEARED FOR CAT IIIb AUTOLAND]' if final_autoland_legal else '[APPROACH PROHIBITED - MUST DIVERT]'}")

    # 3. Adversarial Stress Test
    print("\n" + "=" * 76)
    print("ADVERSARIAL STRESS TEST: IN-FLIGHT SYSTEM DEGRADATION AT 500 FT AGL")
    print("=" * 76)
    print("Scenario: Aircraft established on ILS glideslope at 500 ft AGL in 125m fog.")
    print("Event   : Autopilot Channel 2 disconnects with ECAM message 'AUTO FLT AP 2 FAULT'.")
    print("Impact  : Airborne status degrades from Fail-Operational to Fail-Passive (CAT IIIa).")
    
    degraded_rvr_req = cat_minima["CAT IIIa"]["min_rvr"]
    print(f"\n  • Degraded Status Minimum RVR    : {degraded_rvr_req:.0f} m (CAT IIIa Fail-Passive)")
    print(f"  • Actual Touchdown RVR           : {reported_rvr_m:.0f} m")
    
    if reported_rvr_m < degraded_rvr_req:
        print(f"  • Regulatory Deficit             : {reported_rvr_m - degraded_rvr_req:.0f} m below legal limit")
        print("  -> MANDATORY OPERATIONAL ACTION  : [IMMEDIATE MISSED APPROACH - GO AROUND!]")
        print("     Captain must advance thrust levers to TOGA, rotate to go-around attitude,")
        print("     climb to missed approach altitude, and divert to designated alternate.")
    else:
        print("  -> OPERATIONAL ACTION            : [APPROACH CONTINUED UNDER CAT IIIa MINIMA]")

    print("=" * 76)
    print("Simulation completed successfully (Exit Code 0).")


if __name__ == "__main__":
    run_simulation()
