"""
Day 006 Operational Experiment: Commercial Objectives vs Operational Constraints Optimizer
Domain: Connect commercial revenue objectives to operational, technical and regulatory constraints.

Adheres to Aviation 365 Tool Principles:
  1. Authentic aviation calculations (Structural limits MZFM/MTOM/MLM, Cost of Carry, Fuel Tankering)
  2. Interactive input with sensible defaults on Enter
  3. Step-by-step intermediate operational calculations
  4. Adversarial stress-testing (High density altitude reduction & night curfew penalty)
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
    print("  AVIATION 365 - DAY 006: AIRLINE COMMERCIAL VS OPERATIONAL OPTIMIZER")
    print("  Aircraft Model: Airbus A320-200 (CFM56-5B4)")
    print("=" * 76)
    print("Balancing commercial payload & economic fuel tankering against CS-25 structural")
    print("weight boundaries (MZFM, MTOM, MLM) and statutory operational reserve rules.")
    print("-" * 76)

    # Aircraft structural parameters
    oew_kg = 42600.0        # Operating Empty Weight
    mzfm_kg = 62500.0       # Max Zero Fuel Mass (wing root bending)
    mtom_kg = 77000.0       # Max Take-Off Mass (structural)
    mlm_kg = 66000.0        # Max Landing Mass (landing gear impact energy)

    pax_count = int(prompt_float("Commercial Booked Passengers", 168.0))
    pax_avg_mass_kg = prompt_float("Standard Mass per Passenger + Bags (kg)", 84.0)
    cargo_kg = prompt_float("High-Yield Belly Freight Demand (kg)", 4200.0)
    flight_time_hr = prompt_float("Sector Flight Duration (hours)", 2.5)
    trip_fuel_kg = prompt_float("Nominal Mission Trip Fuel Required (kg)", 5200.0)
    reserves_fuel_kg = prompt_float("Statutory Reserve Fuel - Alternate + Final (kg)", 2100.0)
    p_orig = prompt_float("Origin Fuel Price (€/kg)", 0.80)
    p_dest = prompt_float("Destination Fuel Price (€/kg)", 0.95)
    tankered_fuel_kg = prompt_float("Proposed Tankered Fuel for Return Sector (kg)", 3000.0)

    print("\n" + "=" * 76)
    print("  PHASE I: STRUCTURAL PAYLOAD & ZERO FUEL WEIGHT EVALUATION")
    print("=" * 76)

    pax_payload_kg = pax_count * pax_avg_mass_kg
    total_payload_kg = pax_payload_kg + cargo_kg
    zfw_kg = oew_kg + total_payload_kg
    zfw_margin_kg = mzfm_kg - zfw_kg

    print(f"[1/4] Zero Fuel Weight (ZFW) Verification:")
    print(f"      Operating Empty Weight (OEW): {oew_kg:,.0f} kg")
    print(f"      Passenger Payload ({pax_count} pax @ {pax_avg_mass_kg} kg): {pax_payload_kg:,.0f} kg")
    print(f"      Belly Cargo Payload         : {cargo_kg:,.0f} kg")
    print(f"      Total Commercial Payload    : {total_payload_kg:,.0f} kg")
    print(f"      ----------------------------------------------------------------------")
    print(f"      Calculated Zero Fuel Weight : {zfw_kg:,.0f} kg")
    print(f"      Maximum Zero Fuel Mass (MZFM): {mzfm_kg:,.0f} kg")

    if zfw_kg <= mzfm_kg:
        print(f"      STATUS: ZFW COMPLIANT (Margin to Wing Root Limit: +{zfw_margin_kg:,.0f} kg)")
    else:
        print(f"      STATUS: MZFM EXCEEDED BY {abs(zfw_margin_kg):,.0f} kg! (Cargo must be offloaded)")

    print("\n" + "=" * 76)
    print("  PHASE II: ECONOMIC FUEL TANKERING ANALYSIS (COST OF CARRY)")
    print("=" * 76)

    # Cost of carry ~ 3.8% per flight hour
    k_carry = 0.038
    extra_burn_kg = tankered_fuel_kg * k_carry * flight_time_hr
    fuel_delivered_at_dest_kg = tankered_fuel_kg - extra_burn_kg

    gross_fuel_savings = fuel_delivered_at_dest_kg * (p_dest - p_orig)
    cost_of_extra_burn = extra_burn_kg * p_orig
    net_tankering_benefit = gross_fuel_savings - cost_of_extra_burn
    breakeven_price_ratio = 1.0 + (k_carry * flight_time_hr)
    actual_price_ratio = p_dest / p_orig if p_orig > 0 else 1.0

    print(f"[2/4] Fuel Tankering Economics:")
    print(f"      Fuel Price Differential     : Origin €{p_orig:.2f}/kg vs Dest €{p_dest:.2f}/kg (+{(actual_price_ratio - 1.0)*100:.1f}%)")
    print(f"      Break-even Price Ratio      : {breakeven_price_ratio:.3f} (Required differential: +{(breakeven_price_ratio - 1.0)*100:.1f}%)")
    print(f"      Tankered Uplift at Stand    : {tankered_fuel_kg:,.0f} kg")
    print(f"      Cost of Carry Burn Incurred : {extra_burn_kg:,.1f} kg burned to transport fuel")
    print(f"      Fuel Available at Dest Stand: {fuel_delivered_at_dest_kg:,.1f} kg")
    print(f"      Gross Fuel Purchase Savings : €{gross_fuel_savings:,.2f}")
    print(f"      Cost of Transport Burn      : €{cost_of_extra_burn:,.2f}")
    print(f"      Net Economic Tankering Value: €{net_tankering_benefit:,.2f}")

    if net_tankering_benefit > 0:
        print(f"      ECONOMIC VERDICT: FAVORABLE (+€{net_tankering_benefit:,.2f} net profit)")
    else:
        print(f"      ECONOMIC VERDICT: UNFAVORABLE (Lost €{abs(net_tankering_benefit):,.2f} in transport burn)")

    print("\n" + "=" * 76)
    print("  PHASE III: TAKE-OFF & LANDING STRUCTURAL WEIGHT AUDIT")
    print("=" * 76)

    min_ramp_fuel_kg = trip_fuel_kg + reserves_fuel_kg
    actual_ramp_fuel_kg = min_ramp_fuel_kg + tankered_fuel_kg

    tow_kg = zfw_kg + actual_ramp_fuel_kg
    tow_margin_kg = mtom_kg - tow_kg

    total_trip_burn_kg = trip_fuel_kg + extra_burn_kg
    landing_weight_kg = tow_kg - total_trip_burn_kg
    mlm_margin_kg = mlm_kg - landing_weight_kg

    print(f"[3/4] Take-Off Weight (TOW) vs Structural MTOM:")
    print(f"      Zero Fuel Weight (ZFW)      : {zfw_kg:,.0f} kg")
    print(f"      Total Ramp Fuel Loaded      : {actual_ramp_fuel_kg:,.0f} kg (Min: {min_ramp_fuel_kg:,.0f} kg + Tanker: {tankered_fuel_kg:,.0f} kg)")
    print(f"      Take-Off Weight (TOW)       : {tow_kg:,.0f} kg")
    print(f"      Maximum Take-Off Mass (MTOM): {mtom_kg:,.0f} kg")
    if tow_kg <= mtom_kg:
        print(f"      STATUS: MTOM COMPLIANT (Structural Margin: +{tow_margin_kg:,.0f} kg)")
    else:
        print(f"      STATUS: MTOM EXCEEDED BY {abs(tow_margin_kg):,.0f} kg! [DISPATCH ILLEGAL]")

    print(f"\n[4/4] Landing Weight vs Structural MLM (Landing Gear Limit):")
    print(f"      Take-Off Weight (TOW)       : {tow_kg:,.0f} kg")
    print(f"      Less Mission Trip Burn      : -{total_trip_burn_kg:,.1f} kg")
    print(f"      Calculated Landing Weight   : {landing_weight_kg:,.1f} kg")
    print(f"      Maximum Landing Mass (MLM)  : {mlm_kg:,.0f} kg")
    if landing_weight_kg <= mlm_kg:
        print(f"      STATUS: MLM COMPLIANT (Landing Margin: +{mlm_margin_kg:,.1f} kg)")
    else:
        print(f"      STATUS: MLM EXCEEDED BY {abs(mlm_margin_kg):,.1f} kg! [STRUCTURAL EXCEEDANCE]")
        print(f"      OPERATIONAL ACTION: Tankering MUST be reduced by at least {abs(mlm_margin_kg):,.1f} kg")
        print(f"                          or commercial payload bumped to protect landing gear certified limits.")

    print("\n" + "=" * 76)
    print("  PHASE IV: ADVERSARIAL STRESS TEST (ENVIRONMENTAL & REGULATORY GATES)")
    print("=" * 76)
    print("Injecting Real-World Disruptions:")
    print("  1. Hot Summer Runway: Ambient temperature at Frankfurt reaches 38°C (ISA+23).")
    print("     Second-segment climb gradient reduces Performance-Limited MTOM to 72,500 kg.")
    print("  2. Turnaround Delay: Departure delayed by 45 minutes, threatening Madrid 23:30 night curfew.")

    perf_limited_mtom_kg = 72500.0
    print(f"\n  [Test 1: Hot & High Density Altitude Restriction]")
    print(f"           Structural MTOM     : {mtom_kg:,.0f} kg")
    print(f"           Regulated MTOM (38°C): {perf_limited_mtom_kg:,.0f} kg")
    print(f"           Planned TOW         : {tow_kg:,.0f} kg")

    if tow_kg <= perf_limited_mtom_kg:
        print(f"           RESULT: PASS (Fits within temperature-degraded runway performance)")
    else:
        payload_cut_needed = tow_kg - perf_limited_mtom_kg
        print(f"           RESULT: FAIL! TOW exceeds runway climb limit by {payload_cut_needed:,.0f} kg!")
        print(f"           COMMERCIAL IMPACT: Offload all {tankered_fuel_kg:,.0f} kg tankered fuel immediately,")
        if payload_cut_needed > tankered_fuel_kg:
            remaining_cut = payload_cut_needed - tankered_fuel_kg
            print(f"                              plus offload {remaining_cut:,.0f} kg of commercial belly cargo!")

    print(f"\n  [Test 2: Airport Curfew & EU261 Delay Cascade]")
    scheduled_arr_min = 22 * 60 + 30  # 22:30
    actual_delay_min = 65.0
    actual_arr_min = scheduled_arr_min + actual_delay_min
    curfew_min = 23 * 60 + 30          # 23:30 strict curfew

    arr_hr = int(actual_arr_min // 60)
    arr_m = int(actual_arr_min % 60)
    print(f"           Scheduled Arrival : 22:30 | Projected Arrival: {arr_hr:02d}:{arr_m:02d}")
    print(f"           Madrid Night Curfew: 23:30 local")

    if actual_arr_min <= curfew_min:
        print(f"           RESULT: LANDS WITHIN CURFEW (Margin: {curfew_min - actual_arr_min:.0f} min)")
    else:
        curfew_breach_min = actual_arr_min - curfew_min
        print(f"           RESULT: CURFEW BREACH BY {curfew_breach_min:.0f} MINUTES!")
        print(f"           COMMERCIAL PENALTY: Aircraft diverted to Valencia (LEVC).")
        print(f"                               Mandatory passenger hotel accommodation: €25,000")
        print(f"                               EU261 Compensation (168 pax @ €250): €42,000")
        print(f"                               Total Irregularity Cost: €67,000 (Wipes out 30 days of route profits)")

    print("\n" + "=" * 76)
    print("  SIMULATION COMPLETE (Exit Code 0)")
    print("=" * 76)

if __name__ == "__main__":
    run_simulation()
