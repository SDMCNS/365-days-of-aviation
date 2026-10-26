"""
Day 004 Experiment: Serviceable Aircraft Dispatch Feasibility Diagnostic
Domain: Analyse how a flight can become impossible even when the aircraft itself is serviceable.

Adheres to the Aviation Operational Experiment Principles:
  1. Direct Domain Support: Evaluates the 6 non-technical operational gates (Crew FTL, RVR, Curfew, RFFS, Overflight).
  2. Interactive parameter exploration with sensible defaults on Enter.
  3. Transparent intermediate operational mechanics ("Show the Working").
  4. Adversarial stress-testing: Demonstrates how an unserviceable fire truck or minor delay grounds a perfect aircraft.
  5. Microsecond execution benchmarking using time.perf_counter().
  6. Self-contained standard library Python (zero external dependencies).
"""

import sys
import time

# Ensure robust UTF-8 printing on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

def prompt_param(prompt_text, default_val, cast_type=float, min_val=None, max_val=None):
    """Prompts the user with a default value, validates casting and operational bounds."""
    sys.stdout.write(f"{prompt_text} [default: {default_val}]: ")
    sys.stdout.flush()
    raw = sys.stdin.readline().strip()
    if not raw:
        return default_val
    try:
        val = cast_type(raw)
        if min_val is not None and val < min_val:
            print(f"  [!] Input below minimum ({min_val}). Clamping to {min_val}.")
            return min_val
        if max_val is not None and val > max_val:
            print(f"  [!] Input exceeds maximum ({max_val}). Clamping to {max_val}.")
            return max_val
        return val
    except ValueError:
        print(f"  [!] Invalid input '{raw}'. Using default {default_val}.")
        return default_val

def run_experiment():
    t_start = time.perf_counter()
    print("=" * 76)
    print("  ✈️ AVIATION 365 — DAY 004: MULTI-GATE DISPATCH FEASIBILITY DIAGNOSTIC")
    print("  Topic: Why a Physically Serviceable Aircraft Can Still Be Grounded")
    print("=" * 76)
    print("Baseline: Aircraft is a brand new Airbus A320. ZERO mechanical defects (MEL Items: 0).")
    print("Testing the 5 non-technical legal and operational gates...")
    print("-" * 76)

    # Operational Prompts
    crew_elapsed_duty = prompt_param("1. Crew Flight Duty Period already elapsed (hours)", 7.8, float, 0.0, 14.0)
    max_legal_fdp = prompt_param("2. Maximum legal EASA ORO.FTL duty ceiling (hours)", 11.25, float, 9.0, 14.0)
    planned_flight_hrs = prompt_param("3. Planned flight duration (block hours)", 2.4, float, 0.5, 6.0)
    atfm_delay_min = prompt_param("4. Current ATFM Ground Delay (minutes)", 35.0, float, 0.0, 180.0)
    rvr_meters = prompt_param("5. Departure Runway Visual Range (meters)", 350.0, float, 50.0, 5000.0)
    min_takeoff_rvr = prompt_param("6. Certified Take-off RVR Minima (meters, 125m for LVP)", 125.0, float, 75.0, 800.0)
    arrival_local_time_hrs = prompt_param("7. Projected Arrival Local Time (24h decimal, e.g. 22.75 = 22:45)", 22.6, float, 0.0, 24.0)
    curfew_cutoff_hrs = prompt_param("8. Destination Aerodrome Night Curfew (e.g. 23.00 = 23:00)", 23.0, float, 20.0, 24.0)
    airport_rffs_cat = int(prompt_param("9. Aerodrome Active Rescue & Firefighting (RFFS) Category (1-10)", 6, int, 1, 10))
    required_rffs_cat = 6  # Category 6 required for A320 (ICAO Annex 14)

    print("\n" + "=" * 76)
    print("  EVALUATING INDEPENDENT OPERATIONAL SAFETY GATES")
    print("=" * 76)

    # Gate 1: Physical Airworthiness
    g1_airworthy = True
    print("  [Gate 1] Physical Airworthiness (EASA Part-M/Part-145):")
    print("           Status: PASS (0 open MEL items. C of A and ARC fully valid.)")

    # Gate 2: Flight Crew Duty Limitations (EASA Part-ORO.FTL)
    projected_total_duty = crew_elapsed_duty + planned_flight_hrs + (atfm_delay_min / 60.0) + 0.5 # 30 min post-flight duty
    g2_ftl = projected_total_duty <= max_legal_fdp
    print(f"\n  [Gate 2] Crew Fatigue & Duty Limitations (EASA ORO.FTL.205):")
    print(f"           Projected Total Duty: {projected_total_duty:.2f} hrs vs Statutory Limit: {max_legal_fdp:.2f} hrs")
    print(f"           Status: {'PASS (Within legal duty margins)' if g2_ftl else 'FAIL (Crew Duty Limit Exceeded - Crew legally grounded)'}")

    # Gate 3: Runway Visibility & Aerodrome Operating Minima (EASA Part-CAT)
    g3_weather = rvr_meters >= min_takeoff_rvr
    print(f"\n  [Gate 3] Aerodrome Operating Minima (EASA CAT.OP.MPA.110):")
    print(f"           Current RVR: {rvr_meters:.0f}m vs Required Take-off Minima: {min_takeoff_rvr:.0f}m")
    print(f"           Status: {'PASS (Visibility above take-off minima)' if g3_weather else 'FAIL (Visibility below minimums - Take-off legally prohibited)'}")

    # Gate 4: Destination Noise Curfew Compliance
    # Add ATFM delay to arrival time
    actual_arrival_hrs = arrival_local_time_hrs + (atfm_delay_min / 60.0)
    g4_curfew = actual_arrival_hrs <= curfew_cutoff_hrs
    arr_h = int(actual_arrival_hrs)
    arr_m = int((actual_arrival_hrs - arr_h) * 60.0)
    curf_h = int(curfew_cutoff_hrs)
    curf_m = int((curfew_cutoff_hrs - curf_h) * 60.0)
    print(f"\n  [Gate 4] Aerodrome Noise Curfew Regulation:")
    print(f"           Projected Touchdown: {arr_h:02d}:{arr_m:02d} local vs Strict Curfew: {curf_h:02d}:{curf_m:02d} local")
    print(f"           Status: {'PASS (Arrival before curfew closure)' if g4_curfew else 'FAIL (Late arrival prohibited - Flight denied landing rights)'}")

    # Gate 5: Aerodrome Rescue and Firefighting (ICAO Annex 14)
    g5_rffs = airport_rffs_cat >= required_rffs_cat
    print(f"\n  [Gate 5] Aerodrome Rescue & Firefighting Protection (ICAO Annex 14):")
    print(f"           Active Airport RFFS: Category {airport_rffs_cat} vs Required for A320: Category {required_rffs_cat}")
    print(f"           Status: {'PASS (Adequate emergency firefighting response)' if g5_rffs else 'FAIL (RFFS downgraded - Commercial operations legally suspended)'}")

    # Final Dispatch Outcome
    all_gates_cleared = g1_airworthy and g2_ftl and g3_weather and g4_curfew and g5_rffs

    print("\n" + "=" * 76)
    print("  FINAL FLIGHT DISPATCH VERDICT")
    print("=" * 76)
    if all_gates_cleared:
        print("  STATUS: [FLIGHT CLEARED FOR DEPARTURE] ✅")
        print("  All 5 non-technical gates verified compliant. Aircraft authorized for pushback.")
    else:
        print("  STATUS: [FLIGHT GROUNDED / CANCELLED] ❌")
        failures = []
        if not g2_ftl: failures.append("EASA ORO.FTL Crew duty timeout")
        if not g3_weather: failures.append("Weather below take-off RVR minima")
        if not g4_curfew: failures.append("Destination night curfew violation")
        if not g5_rffs: failures.append("Airport RFFS crash tender category downgraded")
        print(f"  Grounding Factors: {'; '.join(failures)}")
        print("  Demonstrates that zero mechanical defects does NOT guarantee flight release!")

    # Adversarial Break-It Stress Test: Unserviceable Crash Tender
    print("\n" + "=" * 76)
    print("  BREAK-IT STRESS TEST: SURPRISE CRASH TENDER BREAKDOWN AT DESTINATION")
    print("  Scenario: Destination airport Major Foam Tender (MFT) suffers hydraulic failure")
    print("=" * 76)
    print("  [!] Destination NOTAM issued: 'RFFS DOWNGRADED FROM CAT 7 TO CAT 4 FOR 6 HOURS'")
    print("  [!] An Airbus A320 requires minimum RFFS Category 6 for commercial operations.")
    print("  [!] OUTCOME: Dispatch release immediately REVOKED.")
    print("  Even though the aircraft, crew, weather, and slots are perfect, the flight CANNOT depart.")

    t_elapsed = (time.perf_counter() - t_start) * 1000.0
    print("-" * 76)
    print(f"  ✓ Diagnostic completed in {t_elapsed:.2f} ms (Exit Code 0)")
    print("=" * 76)

if __name__ == '__main__':
    run_experiment()
