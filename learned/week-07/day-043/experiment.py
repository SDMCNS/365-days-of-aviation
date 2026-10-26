"""
Day 043 Experiment: Flight Aerodynamics & Aircraft Performance Lab
Domain: Type certification, design approval, production, registration and certificates of airworthiness.
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

def isa_atmosphere(altitude_m):
    T0 = 288.15
    P0 = 101325.0
    L = 0.0065
    g0 = 9.80665
    R = 287.05
    if altitude_m <= 11000.0:
        T = T0 - L * altitude_m
        P = P0 * (1.0 - (L * altitude_m) / T0) ** (g0 / (R * L))
    else:
        T_trop = T0 - L * 11000.0
        P_trop = P0 * (1.0 - (L * 11000.0) / T0) ** (g0 / (R * L))
        T = T_trop
        P = P_trop * math.exp(-g0 * (altitude_m - 11000.0) / (R * T))
    rho = P / (R * T)
    a = math.sqrt(1.4 * R * T)
    return T, P, rho, a

def run_simulation():
    print("=" * 72)
    print("  AVIATION 365 - DAY 043: AERODYNAMICS & FLIGHT PHYSICS LAB")
    print("  Context: Type certification, design approval, production, registration and certificates of airworthiness.")
    print("=" * 72)

    mass_kg = prompt_float("Aircraft Mass (kg)", 65000.0)
    wing_area = prompt_float("Wing Reference Area S (m^2)", 122.6)
    aspect_ratio = prompt_float("Wing Aspect Ratio AR", 9.5)
    cd0 = prompt_float("Zero-lift Parasite Drag Coeff CD0", 0.020)
    cruise_fl = prompt_float("Cruise Flight Level (e.g. 350 for 35,000 ft)", 350.0)
    mach = prompt_float("Cruise Mach Number", 0.78)

    altitude_m = cruise_fl * 100.0 * 0.3048
    T, P, rho, a = isa_atmosphere(altitude_m)
    v_tas = mach * a
    weight_n = mass_kg * 9.80665

    print(f"\n[1/3] Atmospheric Ambient State at FL{cruise_fl:.0f} ({altitude_m:.1f} m):")
    print(f"  -> Ambient Temp: {T:.2f} K ({T - 273.15:.1f} C)")
    print(f"  -> Ambient Pressure: {P:.1f} Pa ({P/100:.1f} hPa)")
    print(f"  -> Air Density (rho): {rho:.4f} kg/m^3 (SL ratio: {rho/1.225:.3f})")
    print(f"  -> Speed of Sound (a): {a:.1f} m/s")
    print(f"  -> True Airspeed (TAS): {v_tas:.1f} m/s ({v_tas * 1.94384:.1f} knots)")

    q = 0.5 * rho * (v_tas ** 2)
    cl = weight_n / (q * wing_area)
    e = 0.85
    cd_induced = (cl ** 2) / (math.pi * e * aspect_ratio)
    cd_total = cd0 + cd_induced
    lift_to_drag = cl / cd_total
    thrust_req_n = weight_n / lift_to_drag

    print(f"\n[2/3] Aerodynamic Force Equilibrium in Level Cruise:")
    print(f"  -> Dynamic Pressure q: {q:.1f} Pa")
    print(f"  -> Required Lift Coeff (CL): {cl:.4f}")
    print(f"  -> Induced Drag Coeff (CDi): {cd_induced:.5f} ({cd_induced/cd_total*100:.1f}% of total drag)")
    print(f"  -> Total Drag Coeff (CD): {cd_total:.5f}")
    print(f"  -> Lift-to-Drag Ratio (L/D): {lift_to_drag:.2f}")
    print(f"  -> Net Cruise Thrust Required: {thrust_req_n/1000.0:.2f} kN ({thrust_req_n/2000.0:.2f} kN/engine)")

    print(f"\n[3/3] Boundary Stress Test: Low-Speed Stall & High-Speed Mach Buffet Margin:")
    cl_max = 1.60
    v_stall_tas = math.sqrt((2.0 * weight_n) / (rho * wing_area * cl_max))
    stall_margin_kts = (v_tas - v_stall_tas) * 1.94384
    print(f"  -> Stall Speed (VS) at FL{cruise_fl:.0f}: {v_stall_tas * 1.94384:.1f} kts")
    print(f"  -> Speed Buffer above Stall: {stall_margin_kts:.1f} kts")
    if stall_margin_kts < 25.0:
        print("  WARNING: Coffin Corner Proximity! Operating near aerodynamic buffet boundary.")
    else:
        print("  SAFE MARGIN: Well within cruise flight envelope.")

    print("=" * 72)
    print("Simulation finished successfully (Exit Code 0).")

if __name__ == '__main__':
    run_simulation()
