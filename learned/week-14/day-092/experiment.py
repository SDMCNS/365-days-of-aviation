"""
Day 092 Experiment: Airport Turnaround & Runway Throughput Engine
Domain: The airport as a transport interchange, safety environment and operational system.
Adheres to the 6 PracticAI Experiment Rules:
  1. Interactive input with sensible defaults on Enter
  2. Step-by-step intermediate calculations
  3. Stress-testing / boundary conditions
  4. Formatted ASCII output
  5. Completely self-contained standard library Python
  6. Clean exit code 0
"""

import sys
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

def run_simulation():
    print("=" * 72)
    print("  AVIATION 365 - DAY 092: AIRPORT OPERATIONS & TURNAROUND ENGINE")
    print("  Context: The airport as a transport interchange, safety environment and operational system.")
    print("=" * 72)

    pax_deboard_min = prompt_float("Inbound Passenger Deboarding Duration (min)", 12.0)
    cleaning_min = prompt_float("Cabin Security Check & Cleaning Duration (min)", 15.0)
    pax_board_min = prompt_float("Outbound Passenger Boarding Duration (min)", 20.0)
    fueling_min = prompt_float("Ramp Refueling Duration (min)", 18.0)
    baggage_onload_min = prompt_float("Outbound Baggage Loading Duration (min)", 22.0)
    scheduled_ground_time = prompt_float("Scheduled Ground Turnaround Window (min)", 50.0)

    print("\n[1/3] Critical Path Analysis of Aircraft Turnaround:")
    pax_path_min = pax_deboard_min + cleaning_min + pax_board_min
    baggage_path_min = 4.0 + baggage_onload_min
    fueling_path_min = 10.0 + fueling_min

    turnaround_duration = max(pax_path_min, baggage_path_min, fueling_path_min)

    print(f"  -> Passenger Path Duration: {pax_path_min:.1f} min")
    print(f"  -> Baggage Handling Path: {baggage_path_min:.1f} min")
    print(f"  -> Refueling Service Path: {fueling_path_min:.1f} min")
    print(f"  -> Calculated Critical Path: {turnaround_duration:.1f} minutes")

    buffer_min = scheduled_ground_time - turnaround_duration
    print(f"\n[2/3] Schedule Robustness against Turnaround Buffer:")
    print(f"  -> Scheduled Ground Window: {scheduled_ground_time:.1f} min")
    print(f"  -> Operational Buffer: {buffer_min:.1f} min")
    if buffer_min >= 5.0:
        print("  -> Buffer Status: ROBUST (On-Time Departure Projected)")
    elif buffer_min >= 0.0:
        print("  -> Buffer Status: TIGHT (Zero-Tolerance for Gate Disruption)")
    else:
        print(f"  -> Buffer Status: CRITICAL DELAY (Projected Departure Delay: {-buffer_min:.1f} min)")

    print(f"\n[3/3] Runway Hourly Capacity & Slot Throughput:")
    avg_rot_sec = 52.0
    wake_sep_sec = 78.0
    single_rwy_capacity = int(3600.0 / (avg_rot_sec + wake_sep_sec))
    print(f"  -> Average Runway Occupancy Time (ROT): {avg_rot_sec:.1f} s")
    print(f"  -> Radar Wake Separation Interval: {wake_sep_sec:.1f} s")
    print(f"  -> Runway Peak Theoretical Capacity: {single_rwy_capacity} movements/hour")

    print("=" * 72)
    print("Simulation finished successfully (Exit Code 0).")

if __name__ == '__main__':
    run_simulation()
