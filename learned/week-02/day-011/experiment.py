"""
Day 011 Operational Experiment: Harmonisation vs National Requirements Friction Diagnostic
Domain: What happens when international harmonisation meets national requirements?

Adheres to Aviation 365 Tool Principles:
  1. Authentic aviation calculations (FAR 129 vs ICAO Annex 1 hours, EU261 statutory compensation)
  2. Interactive input with sensible defaults on Enter
  3. Step-by-step intermediate operational traces
  4. Adversarial stress-testing (Extraterritorial EU261 liability & Article 7 cabotage violation)
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

def run_simulation():
    print("=" * 76)
    print("  AVIATION 365 - DAY 011: HARMONISATION VS NATIONAL REGULATION DIAGNOSTIC")
    print("  Context: ICAO Annexes vs US FAR Part 129 / EASA Regulation (EC) 261/2004")
    print("=" * 76)
    print("This tool evaluates the operational, crew, and legal liability friction when")
    print("international flights cross sovereign regulatory boundaries.")
    print("-" * 76)

    pax_count = prompt_int("Booked Passenger Count on International Sector", 220)
    fo_hours = prompt_float("First Officer Total Flight Experience Hours", 650.0)
    delay_hours = prompt_float("Technical Departure Delay at Origin (hours)", 4.0)
    ticket_fare_eur = prompt_float("Average One-Way Ticket Fare (€)", 450.0)

    print("\n" + "=" * 76)
    print("  PHASE I: CREW QUALIFICATION JURISDICTIONAL CONFLICT")
    print("=" * 76)

    icao_min_hours = 250.0   # ICAO Annex 1 CPL/IR baseline
    faa_min_hours = 1500.0   # US Airline First Officer Rule (FAR 61.159)

    print(f"[1/3] Pilot Certification Across Borders:")
    print(f"      First Officer Total Time     : {fo_hours:.0f} flight hours")
    print(f"      ICAO Annex 1 International Standard: {icao_min_hours:.0f} hours minimum")
    print(f"      US FAA Domestic Airline Standard   : {faa_min_hours:.0f} hours minimum (FAR Part 121)")

    icao_compliant = fo_hours >= icao_min_hours
    faa_compliant = fo_hours >= faa_min_hours

    print(f"\n      Legal Status:")
    print(f"      • ICAO Annex 1 Compliance : {'LEGAL (Meets Global SARP)' if icao_compliant else 'NON-COMPLIANT'}")
    print(f"      • Under Chicago Art. 33   : Foreign States must recognize license for sovereign overflight.")
    if not faa_compliant:
        print(f"      • US Domestic Codeshare   : RESTRICTED! First Officer cannot fly as Part 121 crew.")
        print(f"                                  Permitted ONLY as foreign carrier under Part 129 OpSpecs.")

    print("\n" + "=" * 76)
    print("  PHASE II: EXTRATERRITORIAL CONSUMER COMPENSATION (EU261)")
    print("=" * 76)

    # Route > 3,500 km delay > 3 hours = €600 / passenger
    eu261_rate = 600.0 if delay_hours >= 3.0 else 0.0
    total_statutory_comp = pax_count * eu261_rate
    duty_of_care_per_pax = 150.0 if delay_hours >= 2.0 else 0.0
    total_duty_of_care = pax_count * duty_of_care_per_pax
    total_passenger_liability = total_statutory_comp + total_duty_of_care

    gross_ticket_revenue = pax_count * ticket_fare_eur
    net_flight_margin = gross_ticket_revenue - total_passenger_liability

    print(f"[2/3] Extraterritorial Jurisdiction at Frankfurt Departure:")
    print(f"      Flight Delay Incurred     : {delay_hours:.1f} hours (Technical APU defect)")
    print(f"      Gross Sector Ticket Sales : €{gross_ticket_revenue:,.2f} ({pax_count} pax @ €{ticket_fare_eur:.0f})")
    print(f"      Statutory EU261 Comp Rate : €{eu261_rate:.0f} per passenger (>3,500 km, delay >= 3h)")
    print(f"      Total Statutory Cash Comp : €{total_statutory_comp:,.2f}")
    print(f"      Mandatory Duty of Care    : €{total_duty_of_care:,.2f} (Hotel & meal vouchers)")
    print(f"      ----------------------------------------------------------------------")
    print(f"      Total Extraterritorial Cost: €{total_passenger_liability:,.2f}")
    print(f"      Net Sector Financial Balance: €{net_flight_margin:,.2f}")

    if net_flight_margin < 0:
        print(f"      RESULT: SECTOR OPERATES AT SEVERE NET LOSS (-€{abs(net_flight_margin):,.2f})")
    else:
        print(f"      RESULT: SURVIVES LIABILITY WITH MARGIN (+€{net_flight_margin:,.2f})")

    print("\n" + "=" * 76)
    print("  PHASE III: ADVERSARIAL STRESS TEST (ARTICLE 7 CABOTAGE INFRINGEMENT)")
    print("=" * 76)
    print("Injecting Legal Infringement Scenario:")
    print("  - Flight routes Frankfurt -> New York JFK -> Chicago O'Hare.")
    print("  - Commercial revenue management mistakenly sells 35 domestic tickets solely for JFK -> ORD.")
    print("  - US Customs & Border Protection (CBP) and FAA audit manifest upon JFK landing.")

    time.sleep(0.05)
    cabotage_fine_per_pax = 5000.0
    total_cabotage_fine = 35 * cabotage_fine_per_pax
    print(f"\n  Article 7 Cabotage Violation Audit:")
    print(f"    - Treaty Article: Chicago Convention Article 7 (Reservation of Cabotage)")
    print(f"    - Violation: Foreign airline carried 35 revenue passengers solely between two US domestic points.")
    print(f"    - Federal Civil Penalty: €{total_cabotage_fine:,.2f} ($5,000 / passenger)")
    print(f"    - Regulatory Sanction  : Immediate revocation of US Part 129 Foreign Carrier Permit.")
    print(f"    - Passengers offloaded and rebooked on domestic carrier at operator's expense.")

    print(f"\n  Harmonisation vs National Reality Takeaway:")
    print(f"    International treaties provide the baseline, but national laws dictate market access,")
    print(f"    crew restrictions, and catastrophic financial liabilities.")

    print("\n" + "=" * 76)
    print("  SIMULATION COMPLETE (Exit Code 0)")
    print("=" * 76)

if __name__ == "__main__":
    run_simulation()
