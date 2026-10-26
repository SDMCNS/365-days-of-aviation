"""
Day 019 Experiment: FTL & Commander's Discretion Traceability Engine
Domain: Trace an operational requirement from EU legislation to an operator's documented process.

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


def prompt_bool(prompt_text, default_val=True):
    default_str = "Y" if default_val else "N"
    sys.stdout.write(f"{prompt_text} (Y/N) [default: {default_str}]: ")
    sys.stdout.flush()
    val = sys.stdin.readline().strip().upper()
    if not val:
        return default_val
    return val.startswith("Y")


def get_base_fdp(report_hour, report_min, sectors):
    """EASA CS-FTL.1.205 Table 1 Maximum Daily FDP Look-up"""
    time_float = report_hour + (report_min / 60.0)
    
    # Standard day band: 06:00 - 13:29
    if 6.0 <= time_float < 13.5:
        if sectors <= 2: return 13.0
        elif sectors == 3: return 12.5
        elif sectors == 4: return 12.0
        elif sectors == 5: return 11.5
        else: return 11.0
    # Early morning WOCL encroachment: 05:00 - 05:59
    elif 5.0 <= time_float < 6.0:
        base = 12.0 if sectors <= 2 else 11.5
        encroachment = (6.0 - time_float)
        return max(9.0, base - encroachment)
    # Afternoon / Evening: 13:30 - 16:59
    elif 13.5 <= time_float < 17.0:
        if sectors <= 2: return 12.0
        elif sectors == 3: return 11.5
        elif sectors == 4: return 11.0
        else: return 10.5
    # Night operations / WOCL
    else:
        if sectors <= 2: return 11.0
        elif sectors == 3: return 10.0
        else: return 9.0


def run_simulation():
    print("=" * 76)
    print("  AVIATION 365 - DAY 019: OPERATIONAL TRACEABILITY & FTL DISCRETION")
    print("  Case: EU Law -> Part-ORO -> CS-FTL.1 -> OM-A Section 7 -> Cockpit Action")
    print("  Statutory Anchors: Reg (EU) 2018/1139, ORO.FTL.205(f), CS-FTL.1.205")
    print("=" * 76)

    # 1. Operational Inputs
    print("\n--- [MODULE 1: FLIGHT DUTY ROSTERING & SCHEDULE] ---")
    report_time_str = prompt_str("Crew Report Time at Base (HH:MM)", "06:30")
    try:
        r_hr, r_min = map(int, report_time_str.split(":"))
    except ValueError:
        r_hr, r_min = 6, 30

    sectors = prompt_int("Number of Planned Sectors in Duty", 4)
    final_sector_flight_min = prompt_int("Flight Time of Final Return Sector (minutes)", 130)
    unforeseen_delay_min = prompt_int("Unforeseen Turnaround Ground Delay Accrued (minutes)", 85)

    # Calculate Base FDP
    base_fdp_hours = get_base_fdp(r_hr, r_min, sectors)
    base_fdp_min = int(base_fdp_hours * 60)

    # Duty Timeline
    report_min_of_day = (r_hr * 60) + r_min
    max_shutdown_min_of_day = (report_min_of_day + base_fdp_min) % (24 * 60)
    max_shutdown_str = f"{max_shutdown_min_of_day // 60:02d}:{max_shutdown_min_of_day % 60:02d}"

    # Nominal Duty without delay
    nominal_duty_min = (base_fdp_min - 30)  # Planned 30 min buffer
    projected_fdp_min = nominal_duty_min + unforeseen_delay_min
    projected_shutdown_min_of_day = (report_min_of_day + projected_fdp_min) % (24 * 60)
    projected_shutdown_str = f"{projected_shutdown_min_of_day // 60:02d}:{projected_shutdown_min_of_day % 60:02d}"

    print("\n" + "-" * 76)
    print("STATUTORY FDP DERIVATION (CS-FTL.1.205 TABLE 1)")
    print("-" * 76)
    print(f"  • Crew Report Time             : {report_time_str} local (Base Acclimatized)")
    print(f"  • Number of Sectors            : {sectors} sectors")
    print(f"  • Maximum Permitted Base FDP   : {base_fdp_hours:.2f} hours ({base_fdp_min} minutes)")
    print(f"  • Latest Legal Base Shutdown   : {max_shutdown_str} local")
    print(f"  • Unforeseen Ground Delay      : {unforeseen_delay_min} minutes")
    print(f"  • Projected Engine Shutdown    : {projected_shutdown_str} local")
    print(f"  • Projected Total FDP          : {projected_fdp_min / 60.0:.2f} hours ({projected_fdp_min} minutes)")

    # 2. Commander's Discretion Analysis
    print("\n" + "-" * 76)
    print("COMMANDER'S DISCRETION EVALUATION (ORO.FTL.205(f))")
    print("-" * 76)
    overrun_min = projected_fdp_min - base_fdp_min
    max_allowed_discretion_min = 120  # 2.0 hours un-augmented crew

    if overrun_min <= 0:
        print("  • Discretion Status            : NOT REQUIRED")
        print("    Flight arrives within the baseline maximum Flight Duty Period.")
    else:
        print(f"  • Statutory FDP Overrun        : {overrun_min} minutes ({overrun_min / 60.0:.2f} hrs)")
        print(f"  • Statutory Discretion Ceiling : {max_allowed_discretion_min} minutes (2.0 hours un-augmented)")

        discretion_legal = overrun_min <= max_allowed_discretion_min
        print(f"  -> Discretion Authorization    : {'[LEGAL TO EXERCISE DISCRETION]' if discretion_legal else '[PROHIBITED - CEILING EXCEEDED]'}")

        if discretion_legal:
            all_crew_fit = prompt_bool("  • Mandatory Gate 1: Did all flight & cabin crew confirm fit for duty?", True)
            nca_report_required = overrun_min > 60

            print("\n[MANDATORY POST-DISCRETION ACTIONS]:")
            print(f"  1. Technical Log Sign-off      : Captain must enter '{overrun_min} min Discretion' in ATL.")
            print(f"  2. Rest Extension Mandate      : Subsequent rest must increase by +{overrun_min} min.")
            print(f"  3. Authority Reporting         : {'Form FTL-104 MUST be submitted to NCA in 28 days' if nca_report_required else 'Internal airline logging only (<= 60 min)'}")

    # 3. Adversarial Stress Test
    print("\n" + "=" * 76)
    print("ADVERSARIAL STRESS TEST: UNLAWFUL PRESSURE VS COMMANDER AUTHORITY")
    print("=" * 76)
    print("Scenario: Ground delay swells to 150 minutes (2.5 hours).")
    print("  • Projected Overrun : 150 minutes (Exceeds legal 120-minute cap by 30 min).")
    print("  • Dispatch Pressure : Airline Network Controller messages the cockpit via ACARS:")
    print("                        'Please accept discretion and depart to save flight connections.'")
    print("\nEvaluating Captain's Legal Duty under CAT.GEN.MPA.105:")
    print("  1. The Captain has the NON-NEGOTIABLE LEGAL DUTY to REFUSE DEPARTURE.")
    print("  2. Taking off beyond 2 hours discretion constitutes an ILLEGAL FLIGHT:")
    print("     -> Third-party aircraft hull & passenger liability insurance VOIDED.")
    print("     -> Captain's ATPL pilot license subject to immediate suspension by NCA.")
    print("     -> Accountable Manager liable for criminal safety non-compliance.")
    print("  3. Correct Operational Action:")
    print("     -> Captain announces flight cancellation, disembarks passengers to hotel,")
    print("        and places crew into mandatory 12-hour statutory rest.")
    print("=" * 76)
    print("Simulation completed successfully (Exit Code 0).")


if __name__ == "__main__":
    run_simulation()
