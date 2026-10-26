"""
Day 008 Operational Experiment: Airspace Sovereignty & Overflight Route Economics
Domain: The Chicago Convention, sovereignty over airspace and the role of ICAO.

Adheres to Aviation 365 Tool Principles:
  1. Authentic aviation calculations (ICAO/Eurocontrol Overflight fee formula, weight factors)
  2. Interactive input with sensible defaults on Enter
  3. Step-by-step intermediate operational calculations
  4. Adversarial stress-testing (Geopolitical airspace closure & technical fuel stop)
  5. Completely self-contained standard library Python
  6. Clean exit code 0
"""

import sys
import math
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
    print("  AVIATION 365 - DAY 008: AIRSPACE SOVEREIGNTY & OVERFLIGHT SIMULATOR")
    print("  Context: ICAO Doc 7300 (Chicago Convention Articles 1, 5, 6 & 12)")
    print("=" * 76)
    print("This tool computes statutory ANSP overflight navigation fees and analyzes")
    print("the economic and trajectory penalty of sovereign airspace transit closures.")
    print("-" * 76)

    # Inputs
    mtom_tons = prompt_float("Aircraft Certified MTOM (metric tons, e.g. B777=351.5, A320=77.0)", 351.5)
    tas_kt = prompt_float("Cruising Ground Speed - TAS (knots)", 480.0)
    nominal_dist_nm = prompt_float("Nominal Great Circle Route Distance (NM)", 5200.0)
    transit_fir_dist_nm = prompt_float("Transit Sovereign Airspace Distance in Key FIR (NM)", 3200.0)
    unit_rate_eur = prompt_float("National ANSP Overflight Unit Rate (€/unit)", 75.0)
    fuel_burn_kg_hr = prompt_float("Average Aircraft Fuel Burn in Cruise (kg/hr)", 6800.0)
    fuel_price_eur_kg = prompt_float("Jet-A1 Fuel Price (€/kg)", 0.85)
    detour_extra_nm = prompt_float("Detour Distance Added if Airspace Closed (NM)", 1450.0)

    print("\n" + "=" * 76)
    print("  PHASE I: STATUTORY ANSP OVERFLIGHT FEE COMPUTATION")
    print("=" * 76)

    # 1. Weight factor w = sqrt(MTOM / 50)
    weight_factor = math.sqrt(mtom_tons / 50.0)
    transit_fir_km = transit_fir_dist_nm * 1.852
    d_hundred_km = transit_fir_km / 100.0
    overflight_fee = d_hundred_km * weight_factor * unit_rate_eur

    print(f"[1/3] Eurocontrol / ICAO Standard Charging Formula:")
    print(f"      Aircraft MTOM             : {mtom_tons:.1f} tons")
    print(f"      Calculated Weight Factor w: sqrt({mtom_tons:.1f} / 50) = {weight_factor:.4f}")
    print(f"      Transit FIR Track Distance: {transit_fir_dist_nm:.1f} NM ({transit_fir_km:,.1f} km)")
    print(f"      Distance Factor (d)       : {d_hundred_km:.2f} (hundreds of km)")
    print(f"      National Unit Rate (U)    : €{unit_rate_eur:.2f} per charge unit")
    print(f"      ----------------------------------------------------------------------")
    print(f"      Total Overflight Navigation Fee: €{overflight_fee:,.2f}")

    print("\n" + "=" * 76)
    print("  PHASE II: ROUTE TRAJECTORY & OPERATIONAL COST AUDIT")
    print("=" * 76)

    hourly_airframe_doc = 2400.0  # Crew, maintenance, lease reserve
    nominal_flight_hr = nominal_dist_nm / tas_kt
    nominal_fuel_burn_kg = nominal_flight_hr * fuel_burn_kg_hr
    nominal_fuel_cost = nominal_fuel_burn_kg * fuel_price_eur_kg
    nominal_time_cost = nominal_flight_hr * hourly_airframe_doc
    nominal_total_cost = nominal_fuel_cost + nominal_time_cost + overflight_fee

    print(f"[2/3] Nominal Great Circle Route Performance:")
    print(f"      Flight Duration           : {nominal_flight_hr:.2f} hours ({nominal_flight_hr * 60:.1f} min)")
    print(f"      Mission Fuel Consumption  : {nominal_fuel_burn_kg:,.0f} kg (€{nominal_fuel_cost:,.2f})")
    print(f"      Airframe & Crew Direct DOC: €{nominal_time_cost:,.2f}")
    print(f"      ANSP Overflight Charges   : €{overflight_fee:,.2f}")
    print(f"      ----------------------------------------------------------------------")
    print(f"      Total Direct Segment Cost : €{nominal_total_cost:,.2f}")

    print("\n" + "=" * 76)
    print("  PHASE III: SOVEREIGN AIRSPACE CLOSURE PENALTY (ARTICLE 1 & 9)")
    print("=" * 76)

    detour_dist_nm = nominal_dist_nm + detour_extra_nm
    detour_flight_hr = detour_dist_nm / tas_kt
    delta_flight_hr = detour_flight_hr - nominal_flight_hr
    delta_burn_kg = delta_flight_hr * fuel_burn_kg_hr
    delta_fuel_cost = delta_burn_kg * fuel_price_eur_kg
    delta_time_cost = delta_flight_hr * hourly_airframe_doc

    # Detour bypasses closed FIR but incurs alternate FIR fees
    alternate_fir_fees = overflight_fee * 1.20
    delta_fees = alternate_fir_fees - overflight_fee
    total_detour_penalty = delta_fuel_cost + delta_time_cost + delta_fees
    detour_total_cost = nominal_total_cost + total_detour_penalty

    print(f"[3/3] Sovereign Airspace Closure Impact:")
    print(f"      Detour Distance Penalty   : +{detour_extra_nm:,.0f} NM (Total: {detour_dist_nm:,.0f} NM)")
    print(f"      Additional Flight Time    : +{delta_flight_hr:.2f} hours (+{delta_flight_hr * 60:.0f} min)")
    print(f"      Additional Fuel Burned    : +{delta_burn_kg:,.0f} kg (Cost: +€{delta_fuel_cost:,.2f})")
    print(f"      Additional Hourly Aircraft DOC: +€{delta_time_cost:,.2f}")
    print(f"      Alternate Airspace Overflight Fees: €{alternate_fir_fees:,.2f} (Net Fee Delta: +€{delta_fees:,.2f})")
    print(f"      ----------------------------------------------------------------------")
    print(f"      Single-Flight Cost Increase: +€{total_detour_penalty:,.2f} (+{(total_detour_penalty/nominal_total_cost)*100:.1f}%)")
    print(f"      Annual Penalty (Daily Pair): €{total_detour_penalty * 2 * 365:,.2f} per year")

    print("\n" + "=" * 76)
    print("  PHASE IV: ADVERSARIAL STRESS TEST (TECHNICAL EN-ROUTE FUEL STOP)")
    print("=" * 76)
    print("Injecting Operational Failure Scenario:")
    print("  - Sovereign State issues an immediate NOTAM closing airspace with zero notice.")
    print("  - Aircraft is en-route; detour exceeds remaining fuel range with statutory reserves.")
    print("  - Captain must divert to an intermediate technical stop in Baku (UBBB) for refueling.")

    tech_stop_handling_fee = 6500.0
    landing_parking_fee = 4200.0
    pax_delay_cost = 18000.0  # Missed connections and ground handling
    tech_stop_burn = 3200.0 * fuel_price_eur_kg  # Descent and climb out fuel burn

    total_diversion_cost = tech_stop_handling_fee + landing_parking_fee + pax_delay_cost + tech_stop_burn
    print(f"\n  Diversion Technical Stop Consequences (Baku - UBBB):")
    print(f"    - Unscheduled Airport Ground Handling & Ramp: €{tech_stop_handling_fee:,.2f}")
    print(f"    - Sovereign Landing & Apron Parking Charges : €{landing_parking_fee:,.2f}")
    print(f"    - Descent & Climb Cycle Fuel Penalty (3,200 kg): €{tech_stop_burn:,.2f}")
    print(f"    - Passenger Missed Connection Care          : €{pax_delay_cost:,.2f}")
    print(f"    ----------------------------------------------------------------------")
    print(f"    Total Unplanned Diversion Loss              : €{total_diversion_cost:,.2f}")
    print(f"\n  Aviation Law Takeaway:")
    print(f"    Under Chicago Convention Article 1, a State's sovereign closure is absolute.")
    print(f"    Airlines have no legal recourse to claim damages against sovereign States for closures,")
    print(f"    making geopolitical risk modeling central to international flight dispatch.")

    print("\n" + "=" * 76)
    print("  SIMULATION COMPLETE (Exit Code 0)")
    print("=" * 76)

if __name__ == "__main__":
    run_simulation()
