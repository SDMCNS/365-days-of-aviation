"""
Day 007 Operational Experiment: Aviation Operational Decoder & Irregular Operations Simulator
Domain: Explain the aviation system without relying on unexplained acronyms.

Adheres to Aviation 365 Tool Principles:
  1. Plain-English translation of technical systems & regulatory mandates
  2. Interactive input with sensible defaults on Enter
  3. Step-by-step intermediate operational traces
  4. Adversarial stress-testing (Winter IRROPS snowstorm delay cascade & EU261 compensation)
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

def prompt_str(prompt_text, default_val):
    sys.stdout.write(f"{prompt_text} [default: {default_val}]: ")
    sys.stdout.flush()
    val = sys.stdin.readline().strip()
    return val if val else default_val

ACRONYM_DB = {
    "AOC": {
        "term": "Air Operator Certificate",
        "plain": "The official government license allowing an airline to safely carry paying passengers.",
        "rule": "ICAO Annex 6 / EASA Part-ORO",
        "failure": "Without an AOC, the entire airline is grounded immediately."
    },
    "A-CDM": {
        "term": "Airport Collaborative Decision Making",
        "plain": "A shared computer network between airlines, airport staff, and air traffic controllers to coordinate ground boarding and reduce runway taxi queues.",
        "rule": "Eurocontrol / ICAO Doc 9884",
        "failure": "Planes sit idling on the apron, wasting tons of fuel and causing terminal gridlock."
    },
    "MEL": {
        "term": "Minimum Equipment List",
        "plain": "A certified safety rulebook listing minor broken parts (like a reading lamp or coffee maker) that an aircraft is legally allowed to fly with for a few days.",
        "rule": "EASA CS-MMEL / Part-ORO.MLR",
        "failure": "A flight is cancelled for an inoperative passenger seat or cabin light."
    },
    "NOTAM": {
        "term": "Notice to Airmen",
        "plain": "Urgent safety bulletins warning pilots about unexpected hazards like closed runways, unlit towers, or military exercises.",
        "rule": "ICAO Annex 15 (Aeronautical Info)",
        "failure": "Pilots land on a closed runway or fly into live fireworks/military firing zones."
    },
    "METAR": {
        "term": "Meteorological Aerodrome Report",
        "plain": "A weather report updated every 30 minutes stating actual temperature, wind, rain, snow, and cloud height at an airport.",
        "rule": "ICAO Annex 3 (Meteorology)",
        "failure": "Pilots attempt landing in severe weather beyond certified safety limits."
    },
    "RVR": {
        "term": "Runway Visual Range",
        "plain": "The exact distance in meters a pilot can see runway lights through fog or snow while looking out the cockpit window.",
        "rule": "ICAO Annex 14 / EASA Part-CAT",
        "failure": "Aircraft attempts landing blind below visibility minimums, risking runway excursions."
    },
    "FTL": {
        "term": "Flight Time Limitations",
        "plain": "Mandatory legal limits on pilot working hours and required sleep periods to prevent deadly fatigue accidents.",
        "rule": "EASA Part-ORO.FTL / FAA FAR 117",
        "failure": "Exhausted pilots make critical judgment errors leading to fatal accidents."
    },
    "CTOT": {
        "term": "Calculated Take-Off Time",
        "plain": "An exact departure appointment time (within 10 minutes) assigned by air traffic control to prevent airborne traffic jams.",
        "rule": "Regulation (EU) 255/2010",
        "failure": "Missed slot forces the flight to the back of the European queue, adding 1-2 hours of delay."
    }
}

def run_simulation():
    print("=" * 76)
    print("  AVIATION 365 - DAY 007: PLAIN-LANGUAGE AVIATION DECODER & IRROPS SIMULATOR")
    print("  Goal: Deconstruct aviation technical complexity into clear operational reality.")
    print("=" * 76)

    print("\n[PART 1: INTERACTIVE ACRONYM TRANSLATION MATRIX]")
    query = prompt_str("Enter an aviation acronym to decode (or press Enter to view all)", "ALL").upper()

    if query in ACRONYM_DB:
        data = ACRONYM_DB[query]
        print(f"\n  ACRONYM       : {query}")
        print(f"  FORMAL TERM   : {data['term']}")
        print(f"  PLAIN ENGLISH : {data['plain']}")
        print(f"  LEGAL ANCHOR  : {data['rule']}")
        print(f"  FAILURE MODE  : {data['failure']}")
    else:
        print(f"\n  {'ACRONYM':<8} | {'FORMAL MEANING':<32} | {'LEGAL BASIS':<24}")
        print("  " + "-" * 72)
        for acr, d in ACRONYM_DB.items():
            print(f"  {acr:<8} | {d['term']:<32} | {d['rule']:<24}")
        print("  " + "-" * 72)

    print("\n" + "=" * 76)
    print("  [PART 2: WINTER IRREGULAR OPERATIONS (IRROPS) DISRUPTION TRACE]")
    print("=" * 76)
    print("Scenario: An A320 flight from Munich (EDDM) to London Heathrow (EGLL).")
    print("A heavy winter blizzard hits Munich at 18:00 local.")
    print("-" * 76)

    deice_delay_min = prompt_float("De-icing Apron Wait Delay (minutes)", 45.0)
    slot_delay_min = prompt_float("Air Traffic Control Flow Slot Delay - CTOT (minutes)", 50.0)
    crew_fDP_remain_min = prompt_float("Flight Crew Remaining Duty Allowance (minutes)", 195.0)
    pax_count = int(prompt_float("Number of Passengers on Board", 164.0))

    flight_duration_min = 105.0  # 1 hr 45 min
    post_flight_duty_min = 15.0

    print("\n" + "=" * 76)
    print("  CHRONOLOGICAL DUAL-TRACK TRACE: JARGON VS PLAIN ENGLISH")
    print("=" * 76)

    events = [
        ("Step 1", "18:00",
         "A-CDM reports target pushback delayed. Remote de-icing pad queue.",
         "Our plane is ready at the gate, but trucks are spraying special heated glycol fluid to melt ice and snow from the wings so they can safely generate lift."),
        ("Step 2", "18:45",
         "De-icing completed. Holdover time active. Eurocontrol IFPS issues revised CTOT.",
         "The wings are clean, but because planes are landing slower in the snow, European Air Traffic Control gave us a takeoff appointment time 50 minutes from now to prevent airborne traffic jams."),
        ("Step 3", "19:35",
         "Total ground delay: 95 min. Crew legal FTL calculation initiated under Part-ORO.",
         "Our pilots check their legal duty timer. To protect passenger safety, aviation law strictly limits how many hours pilots can work before fatigue sets in.")
    ]

    for step, t_stamp, tech, plain in events:
        time.sleep(0.04)
        print(f"\n[{step} | {t_stamp}]")
        print(f"  Technical Dispatch Log : {tech}")
        print(f"  Captain's Announcement : \"{plain}\"")

    total_ground_delay = deice_delay_min + slot_delay_min
    total_required_duty = total_ground_delay + flight_duration_min + post_flight_duty_min

    print("\n" + "=" * 76)
    print("  PHASE III: SAFETY & REGULATORY GATE VERIFICATION")
    print("=" * 76)
    print(f"  Initial Scheduled Departure : 18:00 Local")
    print(f"  De-icing Delay Incurred     : +{deice_delay_min:.0f} minutes")
    print(f"  ATC Flow Slot Delay Incurred: +{slot_delay_min:.0f} minutes")
    print(f"  Total Ground Delay          : {total_ground_delay:.0f} minutes")
    print(f"  Total Required Crew Duty    : {total_required_duty:.0f} minutes (Ground {total_ground_delay:.0f}m + Flight {flight_duration_min:.0f}m + Post {post_flight_duty_min:.0f}m)")
    print(f"  Crew Available Legal Duty   : {crew_fDP_remain_min:.0f} minutes")

    ftl_legal = total_required_duty <= crew_fDP_remain_min

    if ftl_legal:
        margin = crew_fDP_remain_min - total_required_duty
        print(f"\n  [DISPATCH LEGAL] Crew within legal duty limits (Margin: +{margin:.0f} minutes).")
        print(f"  Flight departs Munich at 19:35 and arrives Heathrow safely at 20:20.")
    else:
        overage = total_required_duty - crew_fDP_remain_min
        print(f"\n  [SAFETY STOP - FTL EXCEEDED] Pilot duty period exceeded by {overage:.0f} minutes!")
        print(f"  Law: Under EASA Part-ORO.FTL, it is a criminal safety violation to takeoff.")
        print(f"  Resolution: The flight must be cancelled or wait 60 minutes for a standby relief crew.")

    print("\n" + "=" * 76)
    print("  PHASE IV: ADVERSARIAL STRESS TEST & FINANCIAL IMPACT AUDIT")
    print("=" * 76)

    # Cost breakdown of cancellation
    delay_cost_per_min = 45.0  # Eurocontrol standard narrowbody ground delay cost (€45/min)
    ground_delay_cost = total_ground_delay * delay_cost_per_min
    eu261_comp_per_pax = 250.0 # flights under 1500 km delayed >3 hrs or cancelled
    hotel_cost_per_pax = 150.0

    total_eu261 = pax_count * eu261_comp_per_pax
    total_hotel = pax_count * hotel_cost_per_pax
    total_financial_loss = ground_delay_cost + total_eu261 + total_hotel

    print(f"  Financial & Consumer Impact of Today's Single Disruption:")
    print(f"    - Aircraft Ground Idle Cost (Fuel, Crew, Handling): €{ground_delay_cost:,.2f}")
    if not ftl_legal:
        print(f"    - Passenger Hotel & Meal Accommodation ({pax_count} pax): €{total_hotel:,.2f}")
        print(f"    - Statutory EU261 Delay Compensation ({pax_count} pax @ €250): €{total_eu261:,.2f}")
        print(f"    ----------------------------------------------------------------------")
        print(f"    - Total Irregularity Cost to Airline             : €{total_financial_loss:,.2f}")
        print(f"\n  Plain English Takeaway:")
        print(f"    A 45-minute de-icing wait combined with a 50-minute ATC slot triggered a pilot fatigue")
        print(f"    safety law, costing the airline over €{total_financial_loss:,.0f} and stranding {pax_count} people.")
        print(f"    This is why aviation is a connected system where weather, physics, law, and business collide.")
    else:
        print(f"    - Total Delay Cost (No cancellation): €{ground_delay_cost:,.2f}")

    print("\n" + "=" * 76)
    print("  SIMULATION COMPLETE (Exit Code 0)")
    print("=" * 76)

if __name__ == "__main__":
    run_simulation()
