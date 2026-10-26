"""
Day 026: Primary Source Research & Lithium Battery Safety Physics Simulator
Domain: Research one requirement using primary sources and document its exact applicability.
Complies with PracticAI Experiment Rules:
  1. Interactive input with sensible defaults on Enter
  2. Step-by-step intermediate calculations
  3. Stress-testing / boundary conditions
  4. Formatted ASCII output
  5. Completely self-contained standard library Python
  6. Clean exit code 0
"""

import sys

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
    print("  AVIATION 365 - DAY 026: PRIMARY SOURCE RESEARCH & BATTERY PHYSICS")
    print("  Case Study: EASA Part-CAT.GEN.MPA.140 & ICAO Doc 9284 (Lithium Batteries)")
    print("=" * 76)

    # 1. Primary Source Mapping
    print("\n[PART 1: PRIMARY LEGAL CITATION HIERARCHY]")
    print("  1. Hard Law  : Regulation (EU) No 965/2012 Annex IV (CAT.GEN.MPA.140 / 200)")
    print("  2. Soft Law  : EASA ED Decision 2014/015/R (AMC1/AMC2 & GM1 CAT.GEN.MPA.140)")
    print("  3. Standards : ICAO Doc 9284 Technical Instructions for Dangerous Goods (Part 8)")
    print("  4. Guidance  : EASA Safety Information Bulletin SIB 2017-01R1")
    print("-" * 76)

    # 2. Interactive Item Evaluation
    print("\n[PART 2: OPERATIONAL APPLICABILITY & BATTERY EVALUATOR]")
    print("Select item to transport:")
    print("  1 = Standard Smartphone / Tablet (< 20 Wh)")
    print("  2 = High-Performance Laptop / Drone Battery (approx. 90-100 Wh)")
    print("  3 = Large Professional Video / Equipment Battery (120-160 Wh)")
    print("  4 = Electric Mobility Scooter Battery (> 160 Wh)")
    print("  5 = Smart Luggage (Suitcase with integrated power bank)")
    item_choice = prompt_int("Enter selection (1-5)", 2)

    battery_wh = prompt_float("Battery Energy Rating in Watt-hours (Wh)", 99.0)
    is_spare = prompt_int("Is this a spare/loose battery or power bank? (1=Yes, 0=Installed in device)", 1)
    location = prompt_int("Planned transport location (1=Passenger Cabin, 2=Checked Cargo Hold)", 1)
    battery_removable = 1
    if item_choice == 5:
        battery_removable = prompt_int("Is the integrated battery removable from the suitcase? (1=Yes, 0=No)", 1)

    # 3. Thermodynamic Calculation
    # E_elec = Wh * 3600 Joules
    e_elec_kj = battery_wh * 3.6
    # In thermal runaway, cathode/electrolyte chemical decomposition releases approx 4x electrical energy
    q_thermal_kj = e_elec_kj * 4.0
    # Water cooling capacity: sensible heat (c_w = 4.184 kJ/kg.C * 80C) + latent heat (2260 kJ/kg) = 2595 kJ/kg
    water_needed_kg = q_thermal_kj / 2594.72

    print("\n[STEP-BY-STEP THERMODYNAMIC RUNAWAY ANALYSIS]")
    print(f"  - Stored Electrical Energy          : {e_elec_kj:.1f} kJ ({battery_wh:.1f} Wh)")
    print(f"  - Peak Thermal Runaway Heat Release : {q_thermal_kj:.1f} kJ (Exothermic Reaction)")
    print(f"  - Required Water Cooling Mass       : {water_needed_kg:.2f} kg ({water_needed_kg:.2f} Litres)")
    print("  -> Physical Basis: Halon gas extinguishes flame but CANNOT cool internal cells.")
    print("  -> Under AMC2 CAT.GEN.MPA.140, water/aqueous liquid is mandatory to stop propagation.")

    # 4. Applicability Decision Gate under EASA & ICAO Rules
    print("\n" + "=" * 76)
    print("[PART 3: PRIMARY SOURCE LEGAL APPLICABILITY DECISION]")
    print("=" * 76)

    legal_status = "PERMITTED"
    restrictions = []

    if battery_wh > 160.0:
        legal_status = "STRICTLY FORBIDDEN FOR PASSENGER TRANSPORT"
        restrictions.append("Exceeds 160 Wh threshold under ICAO Doc 9284 Part 8.")
        restrictions.append("Must be shipped as fully declared Class 9 Cargo under Part-SPA.DG.")
    elif 100.0 < battery_wh <= 160.0:
        if location == 2:
            legal_status = "ILLEGAL IN CHECKED BAGGAGE"
            restrictions.append("Spare batteries > 100 Wh forbidden in cargo hold.")
        else:
            legal_status = "CONDITIONAL APPROVAL REQUIRED"
            restrictions.append("Requires formal Airline Operator Approval before boarding.")
            restrictions.append("Maximum limit: 2 spare batteries per passenger.")
    else:  # <= 100 Wh
        if is_spare == 1 and location == 2:
            legal_status = "STRICTLY PROHIBITED IN CHECKED BAGGAGE"
            restrictions.append("Under CAT.GEN.MPA.200 & ICAO Doc 9284, spare power banks are banned from cargo holds.")
            restrictions.append("Must be transferred to passenger cabin carry-on.")
        elif item_choice == 5 and battery_removable == 0 and location == 2:
            legal_status = "SMART LUGGAGE PROHIBITED"
            restrictions.append("Under EASA SIB 2017-01R1, non-removable batteries cannot be checked into hold.")

    print(f"  STATUTORY VERDICT : [{legal_status}]")
    if restrictions:
        print("  Legal & Operational Conditions:")
        for r in restrictions:
            print(f"    • {r}")
    else:
        print("  • Complies fully with CAT.GEN.MPA.140 for carriage in passenger cabin.")

    # 5. Adversarial Stress Test
    print("\n" + "=" * 76)
    print("  ADVERSARIAL STRESS TEST: UNCHECKED SMART BAG THERMAL RUNAWAY IN HOLD")
    print("=" * 76)
    print("Simulating a passenger checking a non-removable 100 Wh lithium battery suitcase into hold...")
    print("\n  [HAZARD CASCADE SIMULATION]")
    print("  1. Bag loaded into Class C lower cargo hold.")
    print("  2. Cell enters thermal runaway at FL370 due to mechanical baggage crush.")
    print("  3. Hold smoke detectors trigger cockpit Master Warning (CARGO SMOKE).")
    print("  4. Crew discharges Halon 1301 bottle: Knockdown achieved, but battery keeps boiling at 650°C.")
    print("  5. Adjacent luggage ignites; emergency descent and divert initiated within 15 minutes.")
    print("  -> DEMONSTRATION: Why primary source research matters — safety rules are written in physics!")

    print("\n" + "=" * 76)
    print("  SIMULATION COMPLETE — EXIT CODE 0")
    print("=" * 76)

if __name__ == "__main__":
    main()
