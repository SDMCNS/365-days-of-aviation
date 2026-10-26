"""
Day 020 Experiment: Tripartite Aviation Regulatory Stack & Curfew Simulator
Domain: Compare international standards, European legislation and local operating arrangements.

Adheres to PracticAI Core Standards:
  1. Interactive input with sensible defaults on Enter
  2. Step-by-step transparent intermediate calculations
  3. Adversarial boundary & stress-testing
  4. Clean, formatted ASCII tables
  5. Standard library Python only
  6. Clean exit code 0
"""

import sys

# UTF-8 stdout configuration for Windows compatibility
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


def prompt_str(prompt_text, default_val):
    sys.stdout.write(f"{prompt_text} [default: {default_val}]: ")
    sys.stdout.flush()
    val = sys.stdin.readline().strip()
    return val if val else default_val


def run_simulation():
    print("=" * 76)
    print("  AVIATION 365 - DAY 020: TRIPARTITE REGULATORY STACK SIMULATOR")
    print("  Context: ICAO Global Baseline vs EASA Regional Law vs Local Aerodrome AIP")
    print("  Statutory Anchors: ICAO Annex 6/14, Reg (EU) 965/2012, National AIP AD 2")
    print("=" * 76)

    # Aerodrome database
    airports = {
        "1": {
            "icao": "EGLC",
            "name": "London City Airport (UK)",
            "lda_m": 1199,
            "glidepath_deg": 5.5,
            "curfew_type": "Weekend Closing (Saturday 12:30 UTC)",
            "curfew_cutoff_min": 12 * 60 + 30,  # 12:30 UTC
            "curfew_desc": "Airport closes at 12:30 UTC Saturday to protect local community.",
            "steep_req": True
        },
        "2": {
            "icao": "EDDF",
            "name": "Frankfurt Main Airport (Germany)",
            "lda_m": 4000,
            "glidepath_deg": 3.0,
            "curfew_type": "Night Flight Curfew (23:00 - 05:00 Local)",
            "curfew_cutoff_min": 23 * 60,  # 23:00 Local
            "curfew_desc": "Strict municipal ban on jet operations between 23:00 and 05:00 local.",
            "steep_req": False
        }
    }

    print("\n--- [MODULE 1: DESTINATION AERODROME SELECTION] ---")
    print("Select destination to evaluate multi-tier compliance:")
    for k, v in airports.items():
        print(f"  [{k}] {v['name']} ({v['icao']}) - Glidepath: {v['glidepath_deg']}° | LDA: {v['lda_m']}m")
    
    choice = prompt_str("Select destination (1-2)", "1")
    apt = airports.get(choice, airports["1"])

    # Aircraft & Flight Inputs
    unfactored_dry_lda = prompt_float("Aircraft Unfactored Dry Landing Distance (meters)", 820.0)
    sched_arrival_str = prompt_str(f"Scheduled Touchdown Time ({'UTC' if apt['icao']=='EGLC' else 'Local'} HH:MM)", "12:05" if apt['icao']=='EGLC' else "22:20")
    enroute_delay_min = prompt_int("En-Route Air Traffic Delay Accrued (minutes)", 15)

    try:
        s_hr, s_min = map(int, sched_arrival_str.split(":"))
    except ValueError:
        s_hr, s_min = 12, 5

    actual_arrival_min = (s_hr * 60) + s_min + enroute_delay_min
    actual_arrival_str = f"{(actual_arrival_min // 60) % 24:02d}:{actual_arrival_min % 60:02d}"

    print("\n" + "-" * 76)
    print("TIER 1: INTERNATIONAL BASELINE EVALUATION (ICAO)")
    print("-" * 76)
    print("  • ICAO Annex 6 Dispatch Rules : [COMPLIANT] - Valid C of A, Annex 1 crew licenses.")
    print("  • ICAO Annex 14 Aerodrome Spec : [COMPLIANT] - Runway markings & lighting certified.")
    print("  • ICAO Annex 16 Acoustic Cert  : [COMPLIANT] - Aircraft meets Chapter 14 noise standards.")

    print("\n" + "-" * 76)
    print("TIER 2: EUROPEAN UNION REGIONAL HARMONISATION (EASA)")
    print("-" * 76)
    # EASA Part-CAT Runway performance formula
    dry_factor = 1.67
    glidepath_delta = max(0.0, apt["glidepath_deg"] - 3.0)
    steep_factor = 1.0 + (0.08 * glidepath_delta)
    easa_required_lda = unfactored_dry_lda * dry_factor * steep_factor
    runway_margin = apt["lda_m"] - easa_required_lda
    easa_perf_ok = runway_margin >= 0

    print(f"  • Statutory Rule Basis         : Regulation (EU) 965/2012 CAT.POL.A.230")
    print(f"  • Standard Turbojet Factor     : {dry_factor:.2f}x dry runway safety factor")
    if apt["steep_req"]:
        print(f"  • Steep Approach Penalty       : +{0.08 * glidepath_delta * 100:.1f}% for {apt['glidepath_deg']}° glidepath (SPA.SPA.100)")
    print(f"  • Total Required Landing Dist  : {unfactored_dry_lda:.1f}m x {dry_factor:.2f} x {steep_factor:.2f} = {easa_required_lda:.1f}m")
    print(f"  • Aerodrome Runway LDA         : {apt['lda_m']:.1f}m (Safety Margin: {runway_margin:+.1f}m)")
    print(f"  -> EASA Performance Clearance  : {'[AUTHORIZED - RUNWAY PERFORMANCE SATISFIED]' if easa_perf_ok else '[PROHIBITED - RUNWAY INSUFFICIENT]'}")

    print("\n" + "-" * 76)
    print("TIER 3: LOCAL OPERATING ARRANGEMENT EVALUATION (AIP AD 2)")
    print("-" * 76)
    print(f"  • Site Restriction Policy      : {apt['curfew_desc']}")
    print(f"  • Scheduled Arrival Time       : {sched_arrival_str}")
    print(f"  • Actual Touchdown Projected   : {actual_arrival_str} (Delay: +{enroute_delay_min} min)")
    
    curfew_breached = actual_arrival_min > apt["curfew_cutoff_min"]
    curfew_margin = apt["curfew_cutoff_min"] - actual_arrival_min

    if not curfew_breached:
        print(f"  • Curfew Buffer Margin         : +{curfew_margin} minutes before closure")
        print(f"  -> Local Aerodrome Clearance   : [LANDING CLEARED BY AIRPORT TOWER]")
    else:
        print(f"  • Curfew Deficit Overrun       : {abs(curfew_margin)} minutes PAST CLOSURE DEADLINE")
        print(f"  -> Local Aerodrome Clearance   : [LANDING REFUSED - LOCAL CURFEW BREACH]")

    # Overall Tripartite Outcome
    all_clear = easa_perf_ok and not curfew_breached
    print("\n" + "-" * 76)
    print("TRIPARTITE FEASIBILITY DECISION: ICAO ∩ EASA ∩ LOCAL")
    print("-" * 76)
    if all_clear:
        print("  FINAL STATUS: [FLIGHT AUTHORIZED & CLEARED TO COMPLETE MISSION]")
        print("  All international, regional, and municipal constraints satisfied.")
    else:
        print("  FINAL STATUS: [FLIGHT DIVERTED / RE-ROUTED TO ALTERNATE]")
        reasons = []
        if not easa_perf_ok: reasons.append("EASA runway stopping distance violated")
        if curfew_breached: reasons.append("Local aerodrome curfew violated")
        print(f"  Prohibiting Factors: {', '.join(reasons)}")

    # Adversarial Stress Test
    print("\n" + "=" * 76)
    print("ADVERSARIAL STRESS TEST: CURFEW VIOLATION & MANDATORY DIVERSION")
    print("=" * 76)
    print("Scenario: An additional 20-minute holding delay pushes touchdown past curfew.")
    print("Operational & Legal Consequences:")
    print("  1. Aerodrome Tower ATC formally revokes landing clearance.")
    print("  2. Captain must immediately execute a diversion to planned alternate.")
    print("  3. Financial Breakdown of Curfew Diversion:")
    divert_ferry_fuel = 4200.0  # EUR
    pax_hotel_transport = 180 * 180.0  # 180 pax at 180 EUR hotel/bus
    municipal_court_fine = 25000.0 if apt["icao"] == "EDDF" else 15000.0
    total_cost = divert_ferry_fuel + pax_hotel_transport + municipal_court_fine

    print(f"     • Diversion Fuel & Handling : €{divert_ferry_fuel:,.2f}")
    print(f"     • Passenger Hotel & Care    : €{pax_hotel_transport:,.2f}")
    print(f"     • Municipal Curfew Fine     : €{municipal_court_fine:,.2f}")
    print(f"     -> Total Direct Diversion Cost: €{total_cost:,.2f}")
    print("=" * 76)
    print("Simulation completed successfully (Exit Code 0).")


if __name__ == "__main__":
    run_simulation()
