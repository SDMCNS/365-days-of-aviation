"""
Day 001 Experiment: Aviation Connectivity, Commerce & Public Service Analyzer
Domain: What aviation does: transport, connectivity, commerce, public service and national infrastructure.

Adheres to the Aviation Operational Experiment Principles:
  1. Direct Domain Support: Models authentic air route connectivity, belly cargo valuation, and PSO lifeline economics.
  2. Interactive parameter exploration with sensible defaults on Enter.
  3. Transparent intermediate operational mechanics ("Show the Working").
  4. Adversarial stress-testing: Simulates a 7-day airspace shutdown / weather closure.
  5. Microsecond execution benchmarking using time.perf_counter().
  6. Self-contained standard library Python (zero external dependencies).
"""

import sys
import time
import math

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
    print("  ✈️ AVIATION 365 — DAY 001: AIR CONNECTIVITY & ECONOMIC VALUE ANALYZER")
    print("  Topic: What aviation does: transport, connectivity, commerce & public service")
    print("=" * 76)
    print("\nSelect an operational route scenario to analyze:")
    print("  1. Major Commercial Trunk Route (e.g., London–Frankfurt: Hub connectivity & high-value belly cargo)")
    print("  2. Regional Business & Tourism Corridor (e.g., Milan–Munich: Business travel & catalytic GDP)")
    print("  3. Remote Island Lifeline Route (e.g., Scottish Highlands or Greek Islands: Public Service Obligation)")
    
    choice = int(prompt_param("Choose scenario (1-3)", 1, int, 1, 3))

    if choice == 1:
        route_name = "Inter-Hub Commercial Trunk (London LHR - Frankfurt FRA)"
        def_freq = 35.0          # 5 flights daily = 35 weekly
        def_seats = 180.0        # A320neo / B737 MAX
        def_load_factor = 84.0   # 84%
        def_fare = 175.0         # EUR average one-way
        def_cargo_tons = 3.5     # Tonnes belly cargo per flight
        def_cargo_val_kg = 160.0 # High value: pharmaceuticals, electronics ($160/kg)
        def_flight_hrs = 1.4     # 1h 24m block time
        def_hub_weight = 2.0     # Mega hub destination
        is_pso = False
    elif choice == 2:
        route_name = "Regional Business Corridor (Milan LIN - Munich MUC)"
        def_freq = 18.0          # ~2-3 daily
        def_seats = 110.0        # Embraer E195-E2 / A220
        def_load_factor = 78.0   # 78%
        def_fare = 195.0         # EUR average
        def_cargo_tons = 1.2     # Tonnes per flight
        def_cargo_val_kg = 85.0  # Precision machinery & parts ($85/kg)
        def_flight_hrs = 1.1     # 1h 06m
        def_hub_weight = 1.5     # Major regional hub
        is_pso = False
    else:
        route_name = "Remote Island Lifeline Route (Public Service Obligation / PSO)"
        def_freq = 14.0          # 2 daily flights
        def_seats = 48.0         # ATR 42-600 / Dash 8
        def_load_factor = 62.0   # 62%
        def_fare = 65.0          # Regulated capped tariff
        def_cargo_tons = 0.8     # Emergency medicines, fresh blood, critical mail
        def_cargo_val_kg = 220.0 # Specialized medical/perishable supplies ($220/kg)
        def_flight_hrs = 0.8     # 48m block time
        def_hub_weight = 1.0     # Spoke / regional airfield
        is_pso = True

    print(f"\nConfiguring Route: {route_name}")
    print("-" * 76)
    weekly_flights = prompt_param("Weekly flight frequency (round trips/departures)", def_freq, float, 1.0, 140.0)
    aircraft_seats = prompt_param("Aircraft seat capacity", def_seats, float, 9.0, 600.0)
    load_factor_pct = prompt_param("Average Passenger Load Factor (%)", def_load_factor, float, 20.0, 100.0)
    avg_fare = prompt_param("Average passenger fare ($)", def_fare, float, 20.0, 3000.0)
    cargo_tons_per_flt = prompt_param("Average belly cargo payload per flight (tonnes)", def_cargo_tons, float, 0.0, 50.0)
    cargo_val_per_kg = prompt_param("Average economic value of cargo ($/kg)", def_cargo_val_kg, float, 5.0, 1500.0)
    flight_time_hrs = prompt_param("Average flight stage length (block hours)", def_flight_hrs, float, 0.3, 16.0)
    hub_multiplier = prompt_param("Destination Hub Multiplier (1.0 = Spoke, 1.5 = Reg Hub, 2.0 = Mega Hub)", def_hub_weight, float, 1.0, 2.5)

    print("\n" + "=" * 76)
    print("  STEP-BY-STEP OPERATIONAL & ECONOMIC CALCULATIONS")
    print("=" * 76)

    # 1. Passenger Transport Metrics
    weekly_seats = weekly_flights * aircraft_seats
    weekly_pax = weekly_seats * (load_factor_pct / 100.0)
    annual_pax = weekly_pax * 52.0
    weekly_ticket_rev = weekly_pax * avg_fare
    annual_ticket_rev = weekly_ticket_rev * 52.0

    print(f"\n[1] PASSENGER CONNECTIVITY:")
    print(f"  • Total Weekly Seat Capacity: {weekly_seats:,.0f} seats across {weekly_flights:.0f} flights")
    print(f"  • Weekly Passengers Carried:   {weekly_pax:,.0f} passengers ({load_factor_pct:.1f}% load factor)")
    print(f"  • Annual Passenger Volume:     {annual_pax:,.0f} passengers/year")
    print(f"  • Direct Passenger Revenue:    ${weekly_ticket_rev:,.2f}/week (${annual_ticket_rev:,.2f}/year)")

    # 2. Air Cargo & High-Value Supply Chain
    weekly_cargo_kg = weekly_flights * cargo_tons_per_flt * 1000.0
    weekly_cargo_value = weekly_cargo_kg * cargo_val_per_kg
    annual_cargo_value = weekly_cargo_value * 52.0

    print(f"\n[2] AIR COMMERCE & HIGH-VALUE CARGO:")
    print(f"  • Weekly Freight Carried:      {weekly_cargo_kg:,.0f} kg ({weekly_flights * cargo_tons_per_flt:.1f} tonnes)")
    print(f"  • Average Cargo Value:         ${cargo_val_per_kg:,.2f} per kg")
    print(f"  • Economic Value Facilitated:  ${weekly_cargo_value:,.2f} per week")
    print(f"  • Annual Supply Chain Value:   ${annual_cargo_value:,.2f} per year")
    print(f"    -> Demonstrates why air freight represents <1% of physical volume but >35% of global trade value.")

    # 3. Air Connectivity Index (ACI)
    # Formula: (Weekly Seats / sqrt(Flight Time)) * Hub Multiplier
    connectivity_score = (weekly_seats / math.sqrt(flight_time_hrs)) * hub_multiplier

    print(f"\n[3] AIR CONNECTIVITY INDEX (ACI):")
    print(f"  • Formula: (Weekly Seats / √Flight Time) × Hub Multiplier")
    print(f"  • Calculation: ({weekly_seats:,.0f} / √{flight_time_hrs:.2f}) × {hub_multiplier:.1f}")
    print(f"  • Weighted Connectivity Score: {connectivity_score:,.1f} points")
    if connectivity_score > 8000:
        conn_tier = "Tier-1 Strategic Global Highway (Massive Network Feeder)"
    elif connectivity_score > 2500:
        conn_tier = "Tier-2 Regional Economic Backbone"
    else:
        conn_tier = "Tier-3 Local Lifeline / Essential Feeder"
    print(f"  • Connectivity Classification: {conn_tier}")

    # 4. Regional Catalytic Multiplier & Public Service Economics
    # Direct aviation generates a standard catalytic multiplier of ~1.8 to 2.4x across GDP
    catalytic_factor = 2.15
    total_economic_impact_annual = annual_ticket_rev * catalytic_factor + (annual_cargo_value * 0.05)

    print(f"\n[4] BROADER ECONOMIC & PUBLIC SERVICE IMPACT:")
    print(f"  • Catalytic GDP Multiplier:    {catalytic_factor:.2f}x (Direct, indirect, and induced economic activity)")
    print(f"  • Estimated Regional GDP Contribution: ${total_economic_impact_annual:,.2f} annually")

    if is_pso:
        # Operating cost benchmark for regional turboprop: approx $2,800/block hour
        hourly_op_cost = 2800.0
        weekly_block_hrs = weekly_flights * flight_time_hrs
        weekly_op_cost = weekly_block_hrs * hourly_op_cost
        weekly_margin = weekly_ticket_rev - weekly_op_cost
        annual_subsidy_required = abs(weekly_margin * 52.0) if weekly_margin < 0 else 0.0

        print(f"\n  [PSO REGULATORY ECONOMIC EVALUATION]")
        print(f"  • Aircraft Operating Cost:     ${hourly_op_cost:,.2f} per block hour")
        print(f"  • Weekly Route Operating Cost: ${weekly_op_cost:,.2f} ({weekly_block_hrs:.1f} block hours)")
        print(f"  • Weekly Net Commercial Balance: {'-$' if weekly_margin < 0 else '+$'}{abs(weekly_margin):,.2f}")
        if weekly_margin < 0:
            print(f"  • Required State PSO Subsidy:  ${annual_subsidy_required:,.2f} per year (Justified by hospital transfers & supplies)")
        else:
            print(f"  • Commercial Viability:       Self-sustaining without statutory subsidy.")

    # 5. Adversarial Break-It Stress Test: 7-Day Airspace Closure
    print("\n" + "=" * 76)
    print("  BREAK-IT STRESS TEST: SIMULATING A 7-DAY COMPLETE AIRSPACE SHUTDOWN")
    print("  Scenario: Volcanic ash cloud, severe winter blizzard, or ATC radar failure")
    print("=" * 76)
    
    stranded_pax = weekly_pax
    halted_cargo_kg = weekly_cargo_kg
    halted_cargo_val = weekly_cargo_value
    lost_revenue = weekly_ticket_rev

    print(f"  [!] Direct Airline Revenue Lost:      -${lost_revenue:,.2f}")
    print(f"  [!] Stranded Passenger Disruption:    {stranded_pax:,.0f} travelers requiring accommodation/rebooking")
    print(f"  [!] Stranded Time-Critical Cargo:     {halted_cargo_kg:,.0f} kg (${halted_cargo_val:,.2f} in halted trade)")
    if is_pso:
        print(f"  [CRITICAL PUBLIC IMPACT]: Island cut off from urgent hospital transfers and perishable food supply.")
    else:
        print(f"  [SUPPLY CHAIN IMPACT]: Just-in-Time factory lines stalled due to missing high-tech components.")

    t_elapsed = (time.perf_counter() - t_start) * 1000.0
    print("-" * 76)
    print(f"  ✓ Simulation completed successfully in {t_elapsed:.2f} ms (Clean Exit Code 0)")
    print("=" * 76)

if __name__ == '__main__':
    run_experiment()
