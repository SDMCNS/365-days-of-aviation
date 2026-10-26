"""
Day 025: Regulatory Degradation & Flawed Material Hazard Simulator
Domain: Identify the risks of obsolete, superseded, unofficial or out-of-context regulatory material.
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

def main():
    print("=" * 76)
    print("  AVIATION 365 - DAY 025: REGULATORY DEGRADATION & FLOWN HAZARD SIMULATOR")
    print("  Evaluating the 4 Pathologies: Obsolete, Superseded, Unofficial, Out-of-Context")
    print("=" * 76)

    # Part 1: Interactive Pathology Diagnostic
    print("\n[PART 1: REGULATORY PATHOLOGY DIAGNOSTIC]")
    print("Select a common operational compliance pitfall:")
    print("  1 = Flight dispatch using pre-2022 EASA flat 5% contingency fuel rule")
    print("  2 = Maintenance release citing legacy JAR-145 rather than EASA Part-145")
    print("  3 = Dispatcher applying FAA Part 121 45-min domestic reserve to EASA flight")
    print("  4 = Pilot training department using unofficial third-party forum summaries")
    pitfall_choice = prompt_int("Enter selection (1-4)", 1)

    pathology_map = {
        1: ("Pathology 2: Superseded Amendment within Active Regulation",
            "Regulation (EU) 2021/1296 superseded the flat 5% rule on 30 Oct 2022.",
            "HIGH RISK: Fuel reserves calculated below statutory individual fuel scheme."),
        2: ("Pathology 1: Obsolete / Revoked Legislation",
            "Joint Aviation Requirements (JARs) were repealed upon entry into force of EU law.",
            "CRITICAL: Certificate of Release to Service (CRS) issued under JAR is legally void."),
        3: ("Pathology 4: Out-of-Context Jurisdictional Cross-Contamination",
            "FAA FAR 121 and EASA Part-CAT have mutually exclusive alternate fuel architectures.",
            "SEVERE: Aircraft may land without statutory 30-min final reserve + alternate fuel."),
        4: ("Pathology 3: Unofficial / Non-Authentic Material",
            "Only European Union law published in the Official Journal (Eur-Lex) is authentic.",
            "MODERATE-HIGH: Operator cannot defend procedures in court using unverified third-party text.")
    }

    diag = pathology_map.get(pitfall_choice, pathology_map[1])
    print("\nDiagnostic Assessment:")
    print(f"  • Category   : {diag[0]}")
    print(f"  • Root Cause : {diag[1]}")
    print(f"  • Impact     : {diag[2]}")

    # Part 2: Poisson Document Invalidation Model
    print("\n" + "=" * 76)
    print("[PART 2: POISSON AMENDMENT VELOCITY & DOCUMENT INVALIDATION MODEL]")
    print("=" * 76)
    doc_age_months = prompt_float("Age of unverified regulatory document (months)", 18.0)
    amendment_rate_annual = prompt_float("Annual amendment velocity λ (average updates/year)", 2.4)

    doc_age_years = doc_age_months / 12.0
    expected_amendments = amendment_rate_annual * doc_age_years
    prob_superseded = (1.0 - math.exp(-expected_amendments)) * 100.0

    print(f"\nStatistical Invalidation Metrics:")
    print(f"  - Document Elapsed Age       : {doc_age_years:.2f} years ({doc_age_months:.1f} months)")
    print(f"  - Expected Regulatory Updates: {expected_amendments:.2f} amending acts")
    print(f"  - Probability of Invalidation: {prob_superseded:.2f}%")
    if prob_superseded > 90.0:
        print("  -> EVALUATION: STATISTICALLY CERTAIN TO BE OBSOLETE! Mandatory Eur-Lex audit required.")
    elif prob_superseded > 50.0:
        print("  -> EVALUATION: HIGH DEGRADATION RISK. Likely contains superseded AMC/GM.")
    else:
        print("  -> EVALUATION: ACCEPTABLE CURRENCY WINDOW.")

    # Part 3: Cross-Jurisdictional Fuel Policy Discrepancy
    print("\n" + "=" * 76)
    print("[PART 3: JURISDICTIONAL FUEL SHORTFALL CALCULATOR (EASA vs FAA)]")
    print("=" * 76)
    trip_fuel_kg = prompt_float("Planned Trip Fuel (kg)", 35000.0)
    burn_rate_kg_hr = prompt_float("Holding Fuel Consumption (kg/hr)", 3600.0)
    alternate_dist_nm = prompt_float("Distance to Destination Alternate Aerodrome (NM)", 180.0)

    # Calculations
    # EASA Part-CAT:
    # Contingency (typically 3% with ERA or 5% basic)
    easa_contingency_kg = trip_fuel_kg * 0.05
    # Alternate fuel: approx 12 kg/NM for widebody + 15 min approach
    easa_alternate_kg = (alternate_dist_nm * 12.0) + (burn_rate_kg_hr * 0.25)
    # Final Reserve: 30 minutes at 1500 ft
    easa_final_reserve_kg = burn_rate_kg_hr * 0.50
    easa_total_min_fuel = trip_fuel_kg + easa_contingency_kg + easa_alternate_kg + easa_final_reserve_kg

    # Flawed Out-of-Context Rule: FAA Domestic Part 121 (Trip + 45 min reserve at cruise, omitting alternate)
    faa_domestic_reserve_kg = burn_rate_kg_hr * 0.75
    flawed_total_fuel = trip_fuel_kg + faa_domestic_reserve_kg

    fuel_deficit_kg = easa_total_min_fuel - flawed_total_fuel
    lost_endurance_min = (fuel_deficit_kg / burn_rate_kg_hr) * 60.0

    print("\nFuel Architecture Breakdown:")
    print(f"  [EASA Part-CAT Requirements]:")
    print(f"    • Trip Fuel                     : {trip_fuel_kg:.1f} kg")
    print(f"    • Contingency Fuel (5%)         : {easa_contingency_kg:.1f} kg")
    print(f"    • Destination Alternate Fuel    : {easa_alternate_kg:.1f} kg")
    print(f"    • Statutory Final Reserve (30m) : {easa_final_reserve_kg:.1f} kg")
    print(f"    • Total Minimum Legal Fuel      : {easa_total_min_fuel:.1f} kg")

    print(f"\n  [Flawed / Out-of-Context Domestic Rule Calculation]:")
    print(f"    • Trip Fuel + 45-min Reserve    : {flawed_total_fuel:.1f} kg")
    print(f"    • Resulting Fuel Deficit        : {fuel_deficit_kg:.1f} kg ({lost_endurance_min:.1f} minutes of flight endurance)")

    # Part 4: Adversarial Stress Test
    print("\n" + "=" * 76)
    print("  ADVERSARIAL STRESS TEST: SAFA RAMP CHECK REGULATORY DETENTION")
    print("=" * 76)
    print("Aircraft touches down at European hub; Ramp Inspector boards cockpit...")
    print("Inspector audits the Operational Flight Plan (OFP) and fuel log against EASA Part-CAT:")
    
    if fuel_deficit_kg > 0:
        print(f"\n  [CRITICAL SAFETY FINDING DETECTED: {fuel_deficit_kg:.1f} KG ILLEGAL FUEL SHORTFALL]")
        print("  ENFORCEMENT SANCTIONS EXECUTED:")
        print("    1. EC SAFA Ramp Inspection Class 3 Finding issued (Direct Influence on Safety).")
        print("    2. Aircraft Grounded on Stand — Immediate detention notice served to Commander.")
        print("    3. Operator's Home Civil Aviation Authority notified under Part-ARO.RAMP.")
        print("    4. Insurance Underwriter Formally Notified: Flight operated outside Air Operator Certificate terms.")
        print(f"    5. Financial Penalty & Delay Cost: Approx €{int(fuel_deficit_kg * 8.5) + 35000} (refuelling, wet-lease, delay fees).")
    else:
        print("  -> Full compliance verified. Ramp release signed.")

    print("\n" + "=" * 76)
    print("  SIMULATION COMPLETE — EXIT CODE 0")
    print("=" * 76)

if __name__ == "__main__":
    main()
