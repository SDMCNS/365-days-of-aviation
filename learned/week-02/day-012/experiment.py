"""
Day 012 Experiment: Multi-State Flight Legal Interface & Oceanic Clearance Simulator
Domain: Trace a hypothetical international flight across several States and identify the applicable legal interfaces.

Adheres to PracticAI Core Standards:
  1. Interactive input with sensible defaults on Enter
  2. Step-by-step transparent intermediate calculations
  3. Adversarial boundary & stress-testing
  4. Clean, formatted ASCII tables
  5. Standard library Python only
  6. Clean exit code 0
"""

import sys
import math

# UTF-8 stdout configuration for Windows compatibility
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


def prompt_str(prompt_text, default_val):
    sys.stdout.write(f"{prompt_text} [default: {default_val}]: ")
    sys.stdout.flush()
    val = sys.stdin.readline().strip()
    return val if val else default_val


def run_simulation():
    print("=" * 76)
    print("  AVIATION 365 - DAY 012: MULTI-JURISDICTIONAL FLIGHT LEGAL INTERFACE")
    print("  Trajectory: London Heathrow (EGLL) -> New York JFK (KJFK)")
    print("  Governing Law: ICAO Doc 7300 Articles 1, 5, 6, 12, 16, 17, 31, 33")
    print("=" * 76)

    # User-configurable parameters
    mtom_tonnes = prompt_float("Aircraft Maximum Takeoff Mass (MTOM in metric tonnes)", 319.0)
    planned_mach = prompt_float("Planned Oceanic Cruise Speed (Mach)", 0.85)
    planned_fl = int(prompt_float("Planned Oceanic Flight Level (FL)", 380))
    clearance_lead_min = prompt_float("Oceanic Clearance Request Lead Time prior to OEP (minutes)", 42.0)
    actual_entry_dev_min = prompt_float("Actual OEP Entry Time Deviation vs Cleared Time (+/- minutes)", 1.5)
    safa_defect_count = int(prompt_float("Foreign Ramp Inspection (SAFA) Minor Defects (Cat 1)", 1))
    safa_cat3_count = int(prompt_float("Foreign Ramp Inspection Major Safety Violations (Cat 3)", 0))

    print("\n" + "-" * 76)
    print("PHASE 1: PRE-FLIGHT LEGAL ATTRIBUTION & DEPARTURE JURISDICTION")
    print("-" * 76)
    print(f"  • Operator Jurisdiction : United Kingdom (UK CAA Air Operator Certificate)")
    print(f"  • Aircraft Registration : G-XWBF (State of Registry: United Kingdom)")
    print(f"  • Sovereign Law Anchor  : UK Air Navigation Order & UK Retained Reg (EU) 965/2012")
    print(f"  • Article 1 Sovereignty : United Kingdom exercises complete and exclusive territorial sovereignty.")
    print(f"  • Departure Airport     : London Heathrow (EGLL) - Ramp & Terminal under UK jurisdiction.")

    print("\n" + "-" * 76)
    print("PHASE 2: EN-ROUTE SOVEREIGN AIRSPACE & OVERFLIGHT CHARGES")
    print("-" * 76)
    uk_distance_km = 620.0
    uk_unit_rate = 74.20  # EUR per service unit
    weight_factor = math.sqrt(mtom_tonnes / 50.0)
    service_units = (uk_distance_km / 100.0) * weight_factor
    uk_route_charge = service_units * uk_unit_rate

    print(f"  • Domestic Transit Distance : {uk_distance_km:.1f} km across UK FIR (NATS Area Control)")
    print(f"  • Aircraft Weight Factor    : sqrt({mtom_tonnes:.1f} / 50) = {weight_factor:.4f}")
    print(f"  • Eurocontrol Service Units : {service_units:.2f} SU")
    print(f"  • En-Route Navigation Fee   : €{uk_route_charge:,.2f} payable to UK NATS via Eurocontrol CRCO")

    print("\n" + "-" * 76)
    print("PHASE 3: OCEANIC ENTRY & ARTICLE 12 HIGH SEAS JURISDICTION")
    print("-" * 76)
    oep_waypoint = "GOMUP (54°N 015°W)"
    req_lead_min = 40.0
    lead_ok = clearance_lead_min >= req_lead_min
    time_window_ok = abs(actual_entry_dev_min) <= 3.0

    print(f"  • Oceanic Entry Point (OEP) : {oep_waypoint}")
    print(f"  • Governing Jurisdiction    : HIGH SEAS (International Waters)")
    print(f"  • Statutory Rulebook        : ICAO Doc 7300 Article 12 (Rules of the Air - Annex 2)")
    print(f"                                (Zero national deviations permitted over High Seas)")
    print(f"  • Oceanic ATC Provider      : Shanwick Oceanic (EGGX) - Delegated ICAO Service Provider")
    print(f"  • Clearance Lead Time       : {clearance_lead_min:.1f} min before OEP (ICAO Min: {req_lead_min:.1f} min)")
    print(f"    -> Oceanic Request Timing : {'[LEGAL & COMPLIANT]' if lead_ok else '[NON-COMPLIANT - RISK OF HOLDING]'}")
    print(f"  • Cleared Cruise Profile    : FL{planned_fl}, Mach {planned_mach:.2f}")
    print(f"  • OEP Entry Timing Window   : Deviation {actual_entry_dev_min:+.1f} min (ICAO Limit: +/- 3.0 min)")
    print(f"    -> Track Adherence Check  : {'[WITHIN TOLERANCE]' if time_window_ok else '[TIMING VIOLATION - ATC SANCTION]'}")

    print("\n" + "-" * 76)
    print("PHASE 4: DESTINATION SOVEREIGN ENTRY & FOREIGN RAMP AUDIT (SAFA)")
    print("-" * 76)
    print(f"  • Destination Airspace      : United States (FAA Boston ARTCC / New York TRACON)")
    print(f"  • Governing Law             : 14 CFR Part 129 (Operations: Foreign Air Carriers)")
    print(f"  • Bilateral Traffic Rights  : US-UK Air Transport Agreement (3rd & 4th Freedoms)")
    print(f"  • Destination Airport       : New York JFK (KJFK) Terminal 7 Stand")
    print(f"  • Sovereign Inspection Right: Chicago Convention Article 16 (Right of Search)")

    # Foreign ramp check evaluation
    print("\n[Audit Evaluation: FAA / SAFA Foreign Ramp Inspection]")
    print(f"  • Category 1 (Minor) Findings     : {safa_defect_count}")
    print(f"  • Category 3 (Major) Safety Risks : {safa_cat3_count}")

    if safa_cat3_count > 0:
        flight_status = "AIRCRAFT GROUNDED BY DESTINATION STATE (Article 16 / SAFA Action)"
        legal_remedy = "Defect must be rectified before next flight, or ferry permit negotiated with FAA & UK CAA."
    elif safa_defect_count > 2:
        flight_status = "RELEASED WITH OPERATOR WARNING (Corrective Action Required within 15 Days)"
        legal_remedy = "Operator SMS must record finding and file root-cause closure report to EASA SAFA database."
    else:
        flight_status = "UNRESTRICTED RELEASE FOR RETURN FLIGHT (BA178 KJFK-EGLL)"
        legal_remedy = "Full mutual recognition under Chicago Convention Article 33."

    print(f"  • Ramp Inspection Decision        : {flight_status}")
    print(f"  • Regulatory Consequence          : {legal_remedy}")

    print("\n" + "=" * 76)
    print("ADVERSARIAL STRESS TEST: MID-OCEAN UNPLANNED EMERGENCY DIVERSION")
    print("=" * 76)
    print("Scenario: Severe uncontained engine oil leak at 57°N 030°W (Mid-Atlantic).")
    print("Action  : Captain declares 'MAYDAY' and executes 180° turn toward Reykjavik (BIRK), Iceland.")
    print("\nEvaluating Cross-Border Legal Handshakes under Article 25 (Aircraft in Distress):")
    print("  1. Airspace Entry without Prior Overflight Permit:")
    print("     -> Article 25 mandates contracting States to provide all practicable assistance.")
    print("     -> Emergency squawk 7700 grants immediate priority clearance over normal traffic.")
    print("  2. Customs & Border Security (ICAO Annex 9 Facilitation):")
    print("     -> Passengers & crew accommodated in bonded airport transit area without visa requirement.")
    print("     -> Critical medical patient disembarked directly to Icelandic national hospital.")
    print("  3. Article 7 Cabotage Constraint:")
    print("     -> British carrier strictly PROHIBITED from picking up domestic passengers in Reykjavik")
    print("        to transport to Akureyri (domestic cabotage reserved for Icelandic carriers).")
    print("=" * 76)
    print("Simulation completed successfully (Exit Code 0).")


if __name__ == "__main__":
    run_simulation()
