"""
Day 022: ICAO Regulatory Library & PANS-OPS Instrument Procedure Design Simulator
Domain: ICAO Annexes, PANS, Manuals, Circulars, and Global Strategic Plans.
Complies with PracticAI Experiment Rules:
  1. Interactive input with sensible defaults on Enter
  2. Step-by-step intermediate calculations
  3. Stress-testing / boundary conditions
  4. Formatted ASCII output
  5. Completely self-contained standard library Python
  6. Clean exit code 0
"""

import sys
import math

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

def main():
    print("=" * 76)
    print("  AVIATION 365 - DAY 022: ICAO REGULATORY LIBRARY & PANS-OPS SIMULATOR")
    print("  Deconstructing Convention -> Annexes -> PANS -> Manuals -> Circulars")
    print("=" * 76)

    # 1. ICAO Library Document Catalog
    catalog = {
        1: ("ICAO Doc 7300 (Chicago Convention)", "Tier 1: Supreme Treaty", "Binding Treaty", "Articles 1-96 sovereign airspace & Council authority"),
        2: ("ICAO Annex 14 (Aerodromes)", "Tier 2: SARPs", "Standard (Shall) / Rec (Should)", "Physical runway dimensions, obstacle limitation surfaces"),
        3: ("ICAO Doc 8168 (PANS-OPS)", "Tier 3: Operating Procedures", "Worldwide Procedures", "Instrument flight procedure construction & MOC calculations"),
        4: ("ICAO Doc 4444 (PANS-ATM)", "Tier 3: Operating Procedures", "Worldwide Procedures", "Air traffic management, radar separation, flight plan formats"),
        5: ("ICAO Doc 9859 (Safety Management Manual)", "Tier 4: Technical Manual", "Guidance Material", "State Safety Programmes (SSP) and operator SMS frameworks"),
        6: ("ICAO Circular 328 (Unmanned Aircraft)", "Tier 5: Circular", "Informational Study", "Exploratory technical report on remotely piloted aircraft"),
        7: ("ICAO Doc 10004 (Global Aviation Safety Plan)", "Tier 6: Global Strategic Plan", "Assembly Policy Directive", "Strategic roadmap targeting zero fatal accidents by 2030")
    }

    print("\n[PART 1: ICAO DOCUMENT CLASSIFICATION & LEGAL NATURE]")
    print(f"{'Doc Ref':<40} | {'Tier Level':<20} | {'Legal Status'}")
    print("-" * 76)
    for k, v in catalog.items():
        print(f"{v[0]:<40} | {v[1]:<20} | {v[2]}")

    print("\n[PART 2: PANS-OPS (DOC 8168) OBSTACLE CLEARANCE ALTITUDE (OCA) CALCULATOR]")
    print("Evaluating an RNP Approach with surveyed terrain & obstacles across 3 flight segments:")
    print("  - Initial Approach Segment: MOC = 300 m (984 ft)")
    print("  - Intermediate Approach Segment: MOC = 150 m (492 ft)")
    print("  - Final Approach Segment (NPA): MOC = 75 m (246 ft)")
    print("-" * 76)

    threshold_elev_m = prompt_float("Runway Threshold Elevation (meters MSL)", 42.0)
    obs_initial_m = prompt_float("Highest Obstacle in Initial Approach Segment (m MSL)", 720.0)
    obs_inter_m = prompt_float("Highest Obstacle in Intermediate Segment (m MSL)", 480.0)
    obs_final_m = prompt_float("Highest Obstacle in Final Approach Corridor (m MSL)", 115.0)
    terrain_relief_m = prompt_float("Mountainous Terrain Relief Gradient ΔH (m across 10 km)", 600.0)

    # Calculate Mountainous Surcharge for Initial/Intermediate segments
    # Under PANS-OPS Doc 8168 Vol II: If relief > 500m, MOC is surcharged by factor [1 + ΔH/1000] up to 2.0x
    is_mountainous = terrain_relief_m > 500.0
    surcharge_factor = 1.0 + (terrain_relief_m / 1000.0) if is_mountainous else 1.0
    surcharge_factor = min(surcharge_factor, 2.0)

    moc_initial_nom = 300.0
    moc_inter_nom = 150.0
    moc_final_nom = 75.0

    moc_initial_eff = moc_initial_nom * surcharge_factor
    moc_inter_eff = moc_inter_nom * surcharge_factor
    moc_final_eff = moc_final_nom  # Final segment typically retains nominal or protected OAS

    # Required Altitudes
    min_initial_alt_m = obs_initial_m + moc_initial_eff
    min_inter_alt_m = obs_inter_m + moc_inter_eff
    oca_final_m = obs_final_m + moc_final_eff
    och_final_m = oca_final_m - threshold_elev_m

    # Convert to Feet
    M2FT = 3.28084
    min_initial_alt_ft = math.ceil((min_initial_alt_m * M2FT) / 100.0) * 100
    min_inter_alt_ft = math.ceil((min_inter_alt_m * M2FT) / 100.0) * 100
    oca_final_ft = math.ceil(oca_final_m * M2FT)
    och_final_ft = math.ceil(och_final_m * M2FT)

    print("\n[STEP-BY-STEP CALCULATION RESULTS]")
    print(f"1. Mountainous Terrain Surcharge Factor : {surcharge_factor:.2f}x ({'ACTIVE - High Relief' if is_mountainous else 'STANDARD FLAT'})")
    print(f"2. Initial Approach Segment:")
    print(f"   - Controlling Obstacle: {obs_initial_m:.1f} m MSL | Effective MOC: {moc_initial_eff:.1f} m")
    print(f"   - Min Initial Segment Altitude: {min_initial_alt_m:.1f} m -> Published: {min_initial_alt_ft} ft MSL")
    print(f"3. Intermediate Approach Segment:")
    print(f"   - Controlling Obstacle: {obs_inter_m:.1f} m MSL | Effective MOC: {moc_inter_eff:.1f} m")
    print(f"   - Min Intermediate Altitude: {min_inter_alt_m:.1f} m -> Published: {min_inter_alt_ft} ft MSL")
    print(f"4. Final Approach Segment (Non-Precision Approach):")
    print(f"   - Controlling Obstacle: {obs_final_m:.1f} m MSL | Effective MOC: {moc_final_eff:.1f} m")
    print(f"   - Calculated OCA: {oca_final_m:.1f} m MSL ({oca_final_ft} ft MSL)")
    print(f"   - Calculated OCH: {och_final_m:.1f} m AGL ({och_final_ft} ft Height Above Threshold)")
    print(f"   - Published Minimum Descent Altitude (MDA): {math.ceil(oca_final_ft / 10.0) * 10} ft MSL")

    # Part 3: Adversarial Stress Test
    print("\n" + "=" * 76)
    print("  ADVERSARIAL STRESS TEST: UNREPORTED CONSTRUCTION CRANE IN APPROACH PATH")
    print("=" * 76)
    crane_height_m = prompt_float("Erected Crane Height in Intermediate Corridor (m MSL)", 620.0)
    print(f"\nEvaluating crane elevation {crane_height_m:.1f} m against Intermediate MOC ({moc_inter_eff:.1f} m)...")
    required_intermediate_m = crane_height_m + moc_inter_eff
    required_intermediate_ft = math.ceil((required_intermediate_m * M2FT) / 100.0) * 100

    print(f"  -> Original Published Intermediate Altitude : {min_inter_alt_ft} ft MSL")
    print(f"  -> Required Altitude with New Obstacle     : {required_intermediate_ft} ft MSL")

    if required_intermediate_ft > min_inter_alt_ft:
        violation_m = required_intermediate_m - min_inter_alt_m
        print(f"\n  [SAFETY HAZARD DETECTED] PANS-OPS MOC VIOLATED BY {violation_m:.1f} METERS!")
        print("  REGULATORY & OPERATIONAL ACTIONS TRIGGERED:")
        print("    1. Urgent NOTAM issued immediately raising intermediate altitude.")
        print("    2. Approach plate suspended if obstacle penetrates descent gradient (Doc 8168 Table I-4-3-1).")
        print("    3. Aerodrome Safeguarding Authority notifies State Aviation Authority under Annex 14.")
    else:
        print("\n  [CLEARANCE MAINTAINED] Existing procedure altitude provides sufficient MOC margin.")

    print("\n" + "=" * 76)
    print("  SIMULATION COMPLETE — EXIT CODE 0")
    print("=" * 76)

if __name__ == "__main__":
    main()
