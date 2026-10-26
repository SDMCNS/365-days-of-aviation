"""
Day 002 Experiment: Aircraft Turnaround Critical Path & Ecosystem Interface Simulator
Domain: Map the aviation ecosystem: passengers, airlines, airports, ANSPs, regulators, manufacturers and service providers.

Adheres to the Aviation Operational Experiment Principles:
  1. Direct Domain Support: Simulates the multi-stakeholder aircraft turnaround critical path and ATFM slot windows.
  2. Interactive parameter exploration with sensible defaults.
  3. Transparent intermediate operational mechanics ("Show the Working").
  4. Adversarial stress-testing: Simulates a last-minute security baggage offload with an active CTOT slot.
  5. Microsecond execution benchmarking using time.perf_counter().
  6. Self-contained standard library Python (zero external dependencies).
"""

import sys
import time

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
    print("  ✈️ AVIATION 365 — DAY 002: AIRCRAFT TURNAROUND CRITICAL PATH SIMULATOR")
    print("  Topic: Aviation Ecosystem Interfaces (Airline, Airport, Handler, ATC)")
    print("=" * 76)
    print("Scenario: An Airbus A320 narrowbody turnaround at a congested hub.")
    print("Scheduled Turnaround Time: 40 minutes (Chocks-On: 12:00 UTC | SOBT: 12:40 UTC)")
    print("ATFM Slot CTOT: 12:55 UTC (Taxi Time: 12 min -> Pushback must be <= 12:43 UTC)")
    print("-" * 76)

    # Operational Prompts for Turnaround Tasks
    deboard_time = prompt_param("1. Passenger Deboarding duration (min)", 10.0, float, 5.0, 30.0)
    clean_time = prompt_param("2. Cabin Cleaning & Security search duration (min)", 10.0, float, 4.0, 30.0)
    board_time = prompt_param("3. Passenger Boarding duration (min)", 16.0, float, 8.0, 45.0)
    bag_offload_time = prompt_param("4. Inbound Baggage Offload duration (min)", 12.0, float, 5.0, 35.0)
    bag_load_time = prompt_param("5. Outbound Baggage Loading duration (min)", 16.0, float, 5.0, 40.0)
    fuel_uplift_time = prompt_param("6. Refueling duration (hookup, pump, disconnect) (min)", 15.0, float, 5.0, 45.0)
    catering_time = prompt_param("7. Galley Catering truck servicing duration (min)", 12.0, float, 4.0, 30.0)
    loadsheet_time = prompt_param("8. Final Loadsheet & Trim calculation & PIC sign-off (min)", 4.0, float, 2.0, 15.0)

    print("\n" + "=" * 76)
    print("  PARALLEL PROCESS CHAINS & CRITICAL PATH EVALUATION")
    print("=" * 76)

    # Chain 1: Passenger Flow (Sequential)
    pax_chain_duration = deboard_time + clean_time + board_time
    print(f"\n[A] PASSENGER CHAIN (Cabin & Gate):")
    print(f"    Deboard ({deboard_time:.1f}m) + Clean ({clean_time:.1f}m) + Board ({board_time:.1f}m) = {pax_chain_duration:.1f} min")

    # Chain 2: Baggage / Cargo Flow (Ramp Handling)
    # Note: Loading starts after offload finishes or in parallel hold compartments
    bag_chain_duration = bag_offload_time + bag_load_time
    print(f"\n[B] BAGGAGE & RAMP CHAIN (Ground Handlers):")
    print(f"    Offload ({bag_offload_time:.1f}m) + Load ({bag_load_time:.1f}m) = {bag_chain_duration:.1f} min")

    # Chain 3: Fueling Chain (Fuel Supplier)
    # Starts once chocks are on and fuel truck connects
    fuel_chain_duration = fuel_uplift_time
    print(f"\n[C] FUELING CHAIN (Into-Plane Fuel Operator):")
    print(f"    Setup, uplift & disconnect = {fuel_chain_duration:.1f} min")

    # Chain 4: Catering Servicing (Catering Agent)
    catering_chain_duration = catering_time
    print(f"\n[D] CATERING CHAIN (Flight Kitchen Servicing):")
    print(f"    Galleys replenish = {catering_chain_duration:.1f} min")

    # Critical path is the max of the parallel physical readiness chains
    physical_readiness = max(pax_chain_duration, bag_chain_duration, fuel_chain_duration, catering_chain_duration)
    
    # Final loadsheet and dispatch release occur once passenger and cargo numbers are finalized
    total_turnaround_time = max(pax_chain_duration, bag_chain_duration) + loadsheet_time

    # Determine which stakeholder is the critical constraint
    chains = {
        "Passenger Boarding & Cabin Flow (Airline Gate & Cabin Crew)": pax_chain_duration,
        "Baggage Ramp Handling (Ground Handling Agent)": bag_chain_duration,
        "Aircraft Refueling (Into-Plane Fuel Supplier)": fuel_chain_duration,
        "Catering Delivery (In-flight Service Provider)": catering_chain_duration
    }
    critical_driver = max(chains, key=chains.get)

    print("-" * 76)
    print(f"CRITICAL PATH IDENTIFICATION:")
    print(f"  • Bottleneck Subsystem: {critical_driver} ({chains[critical_driver]:.1f} min)")
    print(f"  • Loadsheet Calculation: +{loadsheet_time:.1f} min (Post-headcount & bag lock)")
    print(f"  • Total Aircraft Ready Time: {total_turnaround_time:.1f} minutes from Chocks-On")

    # Departure & Slot Window Analysis
    scheduled_turnaround = 40.0
    latest_pushback_for_slot = 43.0 # 12:43 UTC for 12:55 CTOT with 12m taxi time
    on_time = total_turnaround_time <= scheduled_turnaround
    slot_met = total_turnaround_time <= latest_pushback_for_slot

    print("\n" + "=" * 76)
    print("  OPERATIONAL OUTCOME & ATFM SLOT COMPLIANCE")
    print("=" * 76)
    print(f"  • Scheduled Turnaround: {scheduled_turnaround:.1f} min (Off-block target: 12:40 UTC)")
    print(f"  • Actual Turnaround:    {total_turnaround_time:.1f} min (Off-block projected: 12:{int(total_turnaround_time):02d} UTC)")
    print(f"  • Slot Pushback Limit:  {latest_pushback_for_slot:.1f} min (Must push by 12:43 UTC to hit 12:55 CTOT)")

    if on_time:
        print("  STATUS: [ON-TIME DEPARTURE] (Buffer remaining: {:.1f} min)".format(scheduled_turnaround - total_turnaround_time))
    elif slot_met:
        delay = total_turnaround_time - scheduled_turnaround
        print(f"  STATUS: [SLIGHT DELAY (+{delay:.1f} min) - ATFM SLOT PRESERVED]")
        print("  Aircraft will make the CTOT slot window (12:50-13:00 UTC). No ATC flow penalty.")
    else:
        overdue = total_turnaround_time - latest_pushback_for_slot
        print(f"  STATUS: [CRITICAL FAILURE: ATFM SLOT MISSED (+{overdue:.1f} min past limit)]")
        print("  ATC CTOT slot expired. Aircraft must be re-sequenced by Eurocontrol NMOC.")
        print("  Projected Slot Delay Penalty: +45 to +90 minutes ground hold!")

    # Adversarial Break-It Stress Test: Security Bag Offload
    print("\n" + "=" * 76)
    print("  BREAK-IT STRESS TEST: LAST-MINUTE NO-SHOW BAGGAGE RECONCILIATION")
    print("  ICAO Annex 17 Security Mandate: Checked bag cannot fly without passenger!")
    print("=" * 76)
    bag_search_duration = 14.0 # 14 minutes to locate bag in aft cargo hold
    stress_turnaround = total_turnaround_time + bag_search_duration
    print(f"  [!] Passenger in Seat 22F fails to board at final call.")
    print(f"  [!] Hold doors reopened. Ground crew searching for bag tag #BA882914: +{bag_search_duration:.1f} min")
    print(f"  [!] Revised Aircraft Ready Time: {stress_turnaround:.1f} minutes")
    if stress_turnaround <= latest_pushback_for_slot:
        print(f"  Outcome: Slot barely maintained with {latest_pushback_for_slot - stress_turnaround:.1f} min margin!")
    else:
        slot_miss_min = stress_turnaround - latest_pushback_for_slot
        print(f"  Outcome: Slot MISSED by {slot_miss_min:.1f} min. Flight grounded awaiting new slot.")
        print(f"  Ripple Effect: Inbound aircraft holding on taxiway waiting for Stand 14 to clear.")

    t_elapsed = (time.perf_counter() - t_start) * 1000.0
    print("-" * 76)
    print(f"  ✓ Turnaround simulation completed in {t_elapsed:.2f} ms (Exit Code 0)")
    print("=" * 76)

if __name__ == '__main__':
    run_experiment()
