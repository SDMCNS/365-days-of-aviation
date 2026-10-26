"""
Day 005 Operational Experiment: Flight Lifecycle & Trajectory Burn Simulator
Domain: Trace a hypothetical flight from passenger booking to arrival at destination.

Adheres to Aviation 365 Tool Principles:
  1. Authentic aviation calculations (Top of Descent 3:1 rule, trajectory fuel burn, EASA reserves)
  2. Interactive input with sensible defaults on Enter
  3. Step-by-step intermediate operational traces
  4. Adversarial stress-testing (severe en-route headwind and alternate diversion)
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

def prompt_str(prompt_text, default_val):
    sys.stdout.write(f"{prompt_text} [default: {default_val}]: ")
    sys.stdout.flush()
    val = sys.stdin.readline().strip()
    return val if val else default_val

def run_simulation():
    print("=" * 76)
    print("  AVIATION 365 - DAY 005: FLIGHT LIFECYCLE & TRAJECTORY BURN SIMULATOR")
    print("  Mission: London Heathrow (EGLL) to Munich Franz Josef Strauss (EDDM)")
    print("=" * 76)
    print("This operational tool traces the 12 key milestones of a commercial flight,")
    print("computes the vertical profile (Top of Descent), and integrates stage fuel burn.")
    print("-" * 76)

    dist_nm = prompt_float("Great Circle & Airway Mission Distance (NM)", 520.0)
    cruise_fl = prompt_float("Cruising Flight Level (e.g., 350 for FL350)", 350.0)
    tas_kt = prompt_float("True Airspeed in Cruise - TAS (knots)", 440.0)
    wind_comp = prompt_float("Headwind (+) or Tailwind (-) Component (knots)", 25.0)
    passengers = int(prompt_float("Boarded Passenger Count", 156.0))
    ramp_fuel_kg = prompt_float("Block Fuel Loaded at Stand (kg)", 5500.0)

    dest_elev_ft = 1487.0  # EDDM elevation
    cruise_alt_ft = cruise_fl * 100.0

    print("\n" + "=" * 76)
    print("  PHASE I: PRE-FLIGHT DISPATCH & TRAJECTORY COMPUTATIONS")
    print("=" * 76)

    # 1. Top of Descent (TOD) Calculation (3:1 rule)
    alt_to_lose = cruise_alt_ft - dest_elev_ft
    tod_dist_nm = (alt_to_lose / 1000.0) * 3.0
    print(f"[1/4] Vertical Profile & Top of Descent (TOD):")
    print(f"      Cruising Altitude: {cruise_alt_ft:,.0f} ft | Destination Elevation: {dest_elev_ft:,.0f} ft")
    print(f"      Altitude to Lose : {alt_to_lose:,.0f} ft")
    print(f"      Top of Descent   : {tod_dist_nm:.1f} NM before EDDM threshold (3:1 Rule)")

    # 2. Speed and Segment Profiles
    ground_speed_kt = tas_kt - wind_comp
    if ground_speed_kt < 150:
        ground_speed_kt = 150.0

    climb_dist_nm = 70.0
    climb_time_min = 20.0
    climb_fuel_kg = 920.0

    descent_dist_nm = tod_dist_nm
    descent_time_min = (descent_dist_nm / (tas_kt * 0.75)) * 60.0  # average descent TAS ~ 330 kt
    descent_fuel_kg = 280.0  # Idle descent

    approach_fuel_kg = 180.0
    taxi_fuel_kg = 150.0

    cruise_dist_nm = max(0.0, dist_nm - (climb_dist_nm + descent_dist_nm))
    cruise_time_hr = cruise_dist_nm / ground_speed_kt
    cruise_time_min = cruise_time_hr * 60.0
    cruise_burn_rate_kg_hr = 2300.0  # A320 CFM56 / LEAP nominal
    cruise_fuel_kg = cruise_time_hr * cruise_burn_rate_kg_hr

    trip_fuel_kg = climb_fuel_kg + cruise_fuel_kg + descent_fuel_kg + approach_fuel_kg
    total_mission_burn_kg = taxi_fuel_kg + trip_fuel_kg

    # Statutory Reserves
    contingency_fuel_kg = 0.05 * trip_fuel_kg  # 5% ICAO contingency
    alternate_fuel_kg = 750.0  # Nuremberg (EDDN, 90 NM)
    final_reserve_kg = 1100.0  # 30 min holding at 1,500 ft AAL
    min_legal_block_fuel_kg = taxi_fuel_kg + trip_fuel_kg + contingency_fuel_kg + alternate_fuel_kg + final_reserve_kg

    print(f"\n[2/4] Trajectory Time & Distance Integration:")
    print(f"      Climb Segment  : {climb_dist_nm:.1f} NM | {climb_time_min:.1f} min | Burn: {climb_fuel_kg:,.0f} kg")
    print(f"      Cruise Segment : {cruise_dist_nm:.1f} NM | {cruise_time_min:.1f} min @ GS {ground_speed_kt:.0f} kt | Burn: {cruise_fuel_kg:,.0f} kg")
    print(f"      Descent Segment: {descent_dist_nm:.1f} NM | {descent_time_min:.1f} min | Burn: {descent_fuel_kg:,.0f} kg")
    print(f"      Approach/Land  : Terminal Area Maneuvering | Burn: {approach_fuel_kg:,.0f} kg")
    print(f"      ----------------------------------------------------------------------")
    print(f"      Total Trip Distance: {dist_nm:.1f} NM | Airborne Time: {(climb_time_min + cruise_time_min + descent_time_min):.1f} min")
    print(f"      Total Trip Fuel    : {trip_fuel_kg:,.1f} kg")

    print(f"\n[3/4] Statutory Fuel Plan Compliance (EASA Fuel Scheme):")
    print(f"      Taxi Fuel             : {taxi_fuel_kg:,.0f} kg")
    print(f"      Trip Fuel             : {trip_fuel_kg:,.1f} kg")
    print(f"      Contingency (5%)      : {contingency_fuel_kg:,.1f} kg")
    print(f"      Alternate (EDDN)      : {alternate_fuel_kg:,.0f} kg")
    print(f"      Final Reserve (30 min): {final_reserve_kg:,.0f} kg")
    print(f"      ----------------------------------------------------------------------")
    print(f"      Minimum Legal Block   : {min_legal_block_fuel_kg:,.1f} kg")
    print(f"      Actual Fuel Loaded    : {ramp_fuel_kg:,.1f} kg")

    fuel_legal = ramp_fuel_kg >= min_legal_block_fuel_kg
    margin_kg = ramp_fuel_kg - min_legal_block_fuel_kg
    if fuel_legal:
        print(f"      STATUS: LEGAL DISPATCH (Surplus Discretionary Fuel: +{margin_kg:,.1f} kg)")
    else:
        print(f"      STATUS: DISPATCH REJECTED (Deficit: {margin_kg:,.1f} kg below legal minimum!)")

    print("\n" + "=" * 76)
    print("  PHASE II: THE 12 OPERATIONAL MILESTONES (EXECUTION TRACE)")
    print("=" * 76)

    milestones = [
        ("M01", "D-180d", "Commercial Booking & PNR Creation (GDS / Amadeus)"),
        ("M02", "D-30d",  "Airport Slot Pair Verified (EGLL/EDDM Level 3 WASG)"),
        ("M03", "D-7d",   "Crew Assigned & Legal Rest Certified (EASA ORO.FTL)"),
        ("M04", "D-3h",   "Aircraft Maintenance CRS & MEL Review (EASA Part-M)"),
        ("M05", "D-2h",   "CFP Generated & ICAO FPL Accepted by Eurocontrol IFPS"),
        ("M06", "D-1h",   "Flight Crew Briefing & Tech Log Acceptance Signed"),
        ("M07", "D-35m",  "Gate Boarding Reconciled (DCS positive bag match)"),
        ("M08", "D-15m",  "Final Loadsheet & Trim Sheet Transmitted via ACARS"),
        ("M09", "D-5m",   "Pre-Departure Clearance (DCL) & A-CDM Pushback Cleared"),
        ("M10", "D+10m",  "Airborne Rotation Runway 27R & SID Transition"),
        ("M11", "D+75m",  "Cruising FL350, RVSM Compliant -> Top of Descent Initialized"),
        ("M12", "D+1h40m","Touchdown Runway 08R, In-Blocks Stand 214 & Tech Log Signed")
    ]

    for code, offset, desc in milestones:
        time.sleep(0.03)
        print(f"  [{code}] {offset:<8} | {desc}")

    print("\n" + "=" * 76)
    print("  PHASE III: OPERATIONAL STRESS TEST (IN-FLIGHT ADVERSITY)")
    print("=" * 76)
    print("Injecting En-Route Adversity:")
    print("  - Unexpected jet stream headwind increases to 75 knots across Southern Germany.")
    print("  - Munich Terminal Area initiates 20-minute holding pattern due to snow clearing.")

    severe_headwind = 75.0
    revised_gs = max(100.0, tas_kt - severe_headwind)
    revised_cruise_time_hr = cruise_dist_nm / revised_gs
    revised_cruise_burn = revised_cruise_time_hr * cruise_burn_rate_kg_hr
    holding_burn_kg = (20.0 / 60.0) * 2200.0  # 20 min holding at 2200 kg/hr

    total_actual_burn_kg = taxi_fuel_kg + climb_fuel_kg + revised_cruise_burn + descent_fuel_kg + approach_fuel_kg + holding_burn_kg
    fuel_remaining_at_eddm = ramp_fuel_kg - total_actual_burn_kg
    required_reserve = alternate_fuel_kg + final_reserve_kg

    print(f"\n  Headwind Impact: Groundspeed drops from {ground_speed_kt:.0f} kt to {revised_gs:.0f} kt")
    print(f"  En-Route Cruise Fuel Increase: +{(revised_cruise_burn - cruise_fuel_kg):,.1f} kg")
    print(f"  Terminal Holding Fuel Burn   : +{holding_burn_kg:,.1f} kg")
    print(f"  ----------------------------------------------------------------------")
    print(f"  Total Incurred Mission Burn  : {total_actual_burn_kg:,.1f} kg")
    print(f"  Remaining Fuel on Final EDDM : {fuel_remaining_at_eddm:,.1f} kg")
    print(f"  Statutory Reserve Requirement: {required_reserve:,.1f} kg (EDDN + 30m Final)")

    if fuel_remaining_at_eddm >= required_reserve:
        print(f"\n  [PASS] Operational Safe Recovery:")
        print(f"         Aircraft lands at EDDM with {fuel_remaining_at_eddm - required_reserve:,.1f} kg above reserves.")
    elif fuel_remaining_at_eddm >= final_reserve_kg:
        print(f"\n  [CAUTION] Contingency & Alternate Fuel Consumed:")
        print(f"         Alternate fuel partially committed. Captain must declare 'MINIMUM FUEL' to ATC.")
    else:
        deficit = final_reserve_kg - fuel_remaining_at_eddm
        print(f"\n  [EMERGENCY] Final Reserve Encroached by {deficit:,.1f} kg!")
        print(f"         Immediate Captain action: Declare 'MAYDAY MAYDAY MAYDAY FUEL' or divert to EDDN.")

    print("\n" + "=" * 76)
    print("  SIMULATION COMPLETE (Exit Code 0)")
    print("=" * 76)

if __name__ == "__main__":
    run_simulation()
