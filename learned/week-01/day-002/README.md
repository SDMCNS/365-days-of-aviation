# Day 002 — Operational Guide: Mapping the Aviation Ecosystem Stakeholders & Interfaces

[← Return to Lesson Plan](../../../lessons/week-01/day-002.md) | [Operational & Technical Analysis](math.md) | [System Topology Canvas](architecture.mermaid) | [Run Python Simulator](experiment.py)

---

## 1. Executive Summary & Operational Context

In Day 001, we established that aviation is a connected system of systems. Today, on **Day 2 (Derive)**, we map the exact operational boundaries, statutory roles, and real-time handshakes between the human, technical, and regulatory actors that make a commercial flight possible.

- **Weekly Domain**: Week 01 — Aviation as a System
- **Stage in Learning Cycle**: Day 2 — Derive
- **Regulatory Framework**: ICAO Annexes 1, 6, 8, 11, 14, 17 & Regulation (EU) 2018/1139
- **Monthly Project Link**: Aviation Ecosystem Map and Regulatory Hierarchy

---

## 2. The Seven Pillars of the Aviation Ecosystem

A civil flight is executed through the coordinated actions of seven distinct regulated entities:

```
[ Regulators: ICAO / EASA / National Aviation Authorities (NAAs) ]
                               │ (Certification & Safety Oversight)
       ┌───────────────────────┼────────────────────────┐
       ▼                       ▼                        ▼
[ AOC Airlines ]       [ Aerodrome Operators ]  [ ANSPs / ATC ]
 (Flight Crew, Dispatch, (Runways, Stands, RFFS, (Separation, Flow,
  CAMO, Maintenance)      Security, De-icing)     Airspace Routing)
       │                       │                        │
       └───────────────────────┼────────────────────────┘
                               ▼
               [ Ground Handling & Fueling (SGHA) ]
                               ▲
                               │
               [ OEM Manufacturers & Suppliers ]
               (Airframe, Engines, Avionics, Parts)
```

### 1. The Airline (AOC Holder)
- Governed by **ICAO Annex 6** and **EASA Part-CAT**.
- Holds the legal Air Operator Certificate (AOC).
- Responsible for operational control: flight crew duty compliance (FTL), flight planning, aircraft acceptance from maintenance, and passenger safety.

### 2. The Aerodrome Operator (ADR)
- Governed by **ICAO Annex 14** and **EASA Part-ADR**.
- Provides physical infrastructure: certified movement areas, runway friction assessment (Global Reporting Format - GRF), obstacle limitation surfaces (OLS), rescue and firefighting services (RFFS Category 1–10), and parking stand allocation.

### 3. The Air Navigation Service Provider (ANSP)
- Governed by **ICAO Annex 11** and **EASA Part-ATM/ANS**.
- Ensures the safe separation of aircraft in controlled airspace and provides Air Traffic Flow Management (ATFM) slots to prevent sector overcapacity.

### 4. Ground Handling & Ramp Services
- Governed under the **IATA Standard Ground Handling Agreement (SGHA)** and newly emerging EASA Ground Handling regulations.
- Executes marshalling, chocks, passenger boarding, baggage loading, aircraft pushback, and de-icing.

### 5. Continuing Airworthiness Management (CAMO / Part-145)
- Governed by **EASA Part-M / Part-CAMO / Part-145**.
- Certifies that the physical airframe, engines, and avionics comply with mandatory Airworthiness Directives (ADs) and Maintenance Steering Group (MSG-3) schedules.

### 6. The Manufacturer / OEM (Type Certificate Holder)
- Governed by **ICAO Annex 8** and **EASA Part-21**.
- Designs, tests, and certifies the aircraft type design (e.g. Airbus, Boeing) and issues the Aircraft Flight Manual (AFM) and Master Minimum Equipment List (MMEL).

### 7. Passengers and Cargo Shippers
- Governed by the **Montreal Convention 1999** (air carrier liability) and **ICAO Annex 17 / 18** (aviation security and safe transport of dangerous goods).

---

## 3. Hands-On Practical Tool: Aircraft Turnaround & Interface Delay Simulator

Launch today's interactive Python simulation to explore the critical path of an aircraft turnaround and test how a delay by a single stakeholder propagates through the airport network:

```bash
python learned/week-01/day-002/experiment.py
```

### What You Will Explore:
- Control durations for deboarding, cleaning, boarding, fueling, baggage loading, and ATC slot clearance.
- Identify which stakeholder is on the **Critical Path**.
- Run the **Break-It Stress Test**: Simulate a last-minute baggage offload for a no-show passenger with an imminent ATFM slot expiration.
