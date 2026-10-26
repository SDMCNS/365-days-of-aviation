# Day 005 — Operational Guide: Trace a Hypothetical Flight from Booking to Stand Arrival

[← Return to Lesson Plan](../../../lessons/week-01/day-005.md) | [Operational & Technical Analysis](analysis.md) | [System Topology Canvas](architecture.mermaid) | [Run Python Simulator](experiment.py)

---

## 1. Executive Summary: The End-to-End Flight Lifecycle

To understand civil aviation as a total system, an aviation professional must trace how a commercial flight evolves across time, legal jurisdictions, and technological systems. A single commercial service (e.g., flight **BA948 London Heathrow (EGLL) to Munich (EDDM)**) is governed by twelve distinct operational milestones distributed across five temporal phases.

Each milestone represents a formal handshake between disparate legal entities (the airline, airport operator, ground handler, ANSP, national civil aviation authority, and border agency).

---

## 2. The 12 Operational Milestones

```
[M1: Reservation] ──> [M2: Schedule & Slots] ──> [M3: Crew Roster] ──> [M4: Dispatch & OFP]
        │
        ▼
[M5: Turnaround]  ──> [M6: Loadsheet/Trim]   ──> [M7: ATC Clearance] ──> [M8: Pushback & Taxi]
        │
        ▼
[M9: Take-off]    ──> [M10: Cruise & ATM]    ──> [M11: Descent/Landing] ──> [M12: In-Blocks/Log]
```

### Phase 1: Commercial & Strategic (D-365 to D-30)
* **Milestone 1 — Passenger Booking & PNR Creation**: Passenger purchases a ticket via a Global Distribution System (Amadeus/Sabre) or direct airline PSS (Passenger Service System). A 6-character Passenger Name Record (PNR) is created storing itinerary, API (Advance Passenger Information), and ticket coupon state.
* **Milestone 2 — Schedule Publishing & Airport Slot Coordination**: Under IATA Worldwide Airport Slot Guidelines (WASG), the airline secures departure (EGLL) and arrival (EDDM) Level 3 coordinated slot pairs. The flight is published in the OAG/Cirium global schedules.

### Phase 2: Tactical Crew & Maintenance Allocation (D-30 to D-1)
* **Milestone 3 — Crew Rostering & Legal Rest Certification**: Crew tracking systems assign Captain, First Officer, and Cabin Crew, verifying compliance with **EASA Part-ORO.FTL** (Flight Time Limitations), cumulative duty limits, and mandatory rest periods.
* **Milestone 4 — Aircraft Line Maintenance & Certificate of Release to Service (CRS)**: An airframe is assigned based on maintenance hours/cycles. Maintenance verifies all open Deferred Defect Items (DDIs) comply with the Minimum Equipment List (MEL).

### Phase 3: Operational Dispatch & Pre-Flight Briefing (D-3h to D-45m)
* **Milestone 5 — Computerized Flight Plan (OFP) & Eurocontrol IFPS Validation**: Flight Operations Officers (Dispatchers) compute optimum route, altitude profile (FL350), payload, and fuel requirements under the statutory fuel policy. The ICAO Flight Plan is filed and accepted by Eurocontrol IFPS.
* **Milestone 6 — Pilot Briefing & Aircraft Technical Acceptance**: Flight crew report to dispatch, review METAR, TAF, SIGMETs, NOTAMs, sign the Operational Flight Plan, and inspect the aircraft Technical Log, confirming CRS validity.

### Phase 4: Ground Turnaround & Collaborative Departure (D-45m to D-0)
* **Milestone 7 — Passenger Boarding & Departure Control System (DCS)**: Passenger boarding passes are scanned at the gate. The DCS reconciles boarded passengers against checked baggage to enforce ICAO Annex 17 positive passenger-baggage matching.
* **Milestone 8 — Final Loadsheet & Center of Gravity (CG) Trim Calculation**: Ground dispatch transmits the final electronic Load and Trim Sheet (LIR/e-Loadsheet) via ACARS. Crew verifies Zero Fuel Weight (ZFW), Take-Off Weight (TOW), and stabilizer trim setting within the certified flight envelope.
* **Milestone 9 — Pre-Departure Clearance (DCL) & A-CDM Pushback**: Flight crew request DCL via datalink (CPDLC). Tower issues pushback clearance coordinated with Target Take-Off Time (TTOT) to avoid departure runway queues.

### Phase 5: Airborne Trajectory & Arrival In-Blocks (D-0 to In-Blocks)
* **Milestone 10 — Airborne Take-off & Departure Transition**: Aircraft departs runway, enters Standard Instrument Departure (SID), transitions from Tower to Terminal Radar, then Area Control Centre (ACC).
* **Milestone 11 — En-Route Trajectory & Top of Descent (TOD)**: Flight levels off at FL350, maintaining RVSM separation (1,000 ft vertical). At the calculated Top of Descent point (100.5 NM before Munich), aircraft transitions to idle descent via Standard Terminal Arrival Route (STAR).
* **Milestone 12 — Landing, Taxi-in, and Technical Log Sign-off**: Aircraft touches down on Runway 08R, clears the active runway, taxis to Stand 214, and sets parking brake (In-Blocks / AIBT). Flight crew log flight hours, fuel remaining, and any technical discrepancies in the Aircraft Technical Log.

---

## 3. Failure Cascades & Bottlenecks

1. **Missing Passenger at Boarding Gate**: Generates an immediate security alert under ICAO Annex 17. The bag must be located in the cargo hold and offloaded. Missing the Target Startup Approval Time (TSAT) forfeits the Eurocontrol slot, causing a cascading 45-minute delay.
2. **ACARS Loadsheet CG Out of Limits**: If last-minute cargo is loaded into Hold 1 instead of Hold 4, the nose-heavy CG exceeds certified forward limits, preventing take-off rotation. Dispatch must immediately issue a Revised Loadsheet (EDO).
3. **Severe Headwind on Route**: A 50-knot headwind drops groundspeed from 440 kt to 390 kt, extending flight time and consuming contingency fuel. If en-route fuel monitoring shows reserve fuel will be encroached before EDDM, captain must initiate contingency diversion procedures.

---

## 4. Practical Verification Script

Launch the interactive Day 005 Trajectory & Lifecycle Simulator:
```bash
python learned/week-01/day-005/experiment.py
```
This script computes the complete 12-milestone trajectory, calculates the Top of Descent profile, integrates stage-by-stage fuel consumption, and executes an en-route diversion stress test.
