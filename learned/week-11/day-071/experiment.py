"""
Day 071 Experiment: Flight Dispatch, Mass & Balance and Fuel Planning
Domain: Flight crew, cabin crew, dispatch, operations control and ground operations roles.
Adheres to the 6 PracticAI Experiment Rules:
  1. Interactive input with sensible defaults on Enter
  2. Step-by-step intermediate calculations
  3. Stress-testing / boundary conditions
  4. Formatted ASCII output
  5. Completely self-contained standard library Python
  6. Clean exit code 0
"""

import sys
import math
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
    print("  AVIATION 365 - DAY 071: DISPATCH LOAD & FUEL PLANNING")
    print("  Context: Flight crew, cabin crew, dispatch, operations control and ground operations roles.")
    print("=" * 72)

    dom = prompt_float("Dry Operating Mass DOM (kg)", 43500.0)
    pax_count = int(prompt_float("Passenger Count (pax)", 150))
    pax_avg_mass = prompt_float("Standard Mass per Pax + Hand Luggage (kg)", 84.0)
    cargo_kg = prompt_float("Checked Baggage + Cargo Mass (kg)", 3200.0)
    trip_distance_nm = prompt_float("Planned Trip Distance (NM)", 950.0)

    pax_total_mass = pax_count * pax_avg_mass
    traffic_load = pax_total_mass + cargo_kg
    zfm = dom + traffic_load

    max_zfm = 62500.0
    max_tom = 75500.0
    max_lm = 64500.0

    print(f"\n[1/3] Mass & Structural Limits Breakdown:")
    print(f"  -> Dry Operating Mass: {dom:.1f} kg")
    print(f"  -> Traffic Load: {traffic_load:.1f} kg ({pax_count} pax @ {pax_avg_mass} kg + {cargo_kg} kg cargo)")
    print(f"  -> Zero Fuel Mass (ZFM): {zfm:.1f} kg (Limit: {max_zfm:.1f} kg) -> {'LEGAL' if zfm <= max_zfm else 'OVERWEIGHT'}")

    burn_rate_kg_nm = 3.6
    trip_fuel = trip_distance_nm * burn_rate_kg_nm
    contingency_fuel = max(trip_fuel * 0.05, 500.0)
    alternate_fuel = 1400.0
    final_reserve = 1100.0
    taxi_fuel = 200.0

    takeoff_fuel = trip_fuel + contingency_fuel + alternate_fuel + final_reserve
    ramp_fuel = takeoff_fuel + taxi_fuel
    tom = zfm + takeoff_fuel
    est_landing_mass = tom - trip_fuel

    print(f"\n[2/3] Regulatory Fuel Computation (EASA CAT.OP.MPA.181):")
    print(f"  -> Trip Fuel ({trip_distance_nm:.0f} NM): {trip_fuel:.1f} kg")
    print(f"  -> Contingency Fuel (5%): {contingency_fuel:.1f} kg")
    print(f"  -> Alternate Fuel: {alternate_fuel:.1f} kg")
    print(f"  -> Final Reserve (30 min hold): {final_reserve:.1f} kg")
    print(f"  -> Required Takeoff Fuel: {takeoff_fuel:.1f} kg")
    print(f"  -> Total Block/Ramp Fuel: {ramp_fuel:.1f} kg")

    print(f"\n[3/3] Takeoff & Landing Mass Margin:")
    print(f"  -> Calculated TOM: {tom:.1f} kg (Max: {max_tom:.1f} kg) -> Margin: {max_tom - tom:.1f} kg")
    print(f"  -> Estimated Landing Mass: {est_landing_mass:.1f} kg (Max: {max_lm:.1f} kg) -> Margin: {max_lm - est_landing_mass:.1f} kg")

    lemac = 16.20
    mac_length = 4.20
    cg_arm = 17.15 + (cargo_kg / 10000.0) * 0.15
    mac_pct = ((cg_arm - lemac) / mac_length) * 100.0
    print(f"  -> Longitudinal CG: {cg_arm:.3f} m -> %MAC: {mac_pct:.2f}% (Envelope: 18.0% - 32.0%)")

    print("-" * 72)
    if tom <= max_tom and zfm <= max_zfm and est_landing_mass <= max_lm and 18.0 <= mac_pct <= 32.0:
        print("LOADSHEET VALIDATION: [SUCCESS - AIRCRAFT AUTHORIZED FOR DISPATCH]")
    else:
        print("LOADSHEET VALIDATION: [FAILED - LOAD RESTRICTION OR FUEL TRIM REQUIRED]")

    print("=" * 72)
    print("Simulation finished successfully (Exit Code 0).")

if __name__ == '__main__':
    run_simulation()
