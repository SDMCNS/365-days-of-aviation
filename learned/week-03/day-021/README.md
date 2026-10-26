# Day 021 — The Aviation Ecosystem Blueprint: Who Makes Rules, Who Oversees Compliance, and Who Operates Services

[← Return to Lesson Plan](../../../lessons/week-03/day-021.md) | [📊 Technical Walkthrough](analysis.md) | [System Topology Canvas](architecture.mermaid) | [Run Python Simulator](experiment.py)

---

## 1. Executive Summary: The Three Pillars of Civil Aviation

To master the aviation regulatory ecosystem, every organisation, official, and technician can be placed into one of three essential functional pillars:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           1. WHO MAKES RULES?                           │
│                     (The Rulemakers / Legislators)                      │
│   • ICAO: 193 States adopt global SARPs (Annexes 1 to 19)               │
│   • European Parliament & Council: Enacts Basic Regulation (EU) 2018/1139│
│   • European Commission (DG MOVE): Enacts Implementing Regulations     │
│   • EASA: Prepares technical opinions, CS, AMC, and GM                  │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (Enacts Laws & Technical Standards)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                       2. WHO OVERSEES COMPLIANCE?                       │
│                     (The Regulators / Inspectors)                       │
│   • EASA: Direct certification for aircraft designs (TC), DOA, and TCO; │
│           audits national authorities via Standardisation.              │
│   • National Competent Authorities (NCAs / NAAs):                       │
│     (DGAC France, LBA Germany, AESA Spain, ENAC Italy, UK CAA)          │
│     Issues AOCs to airlines, licenses pilots, audits Part-145 MROs,     │
│     certifies commercial airports (ADR).                                │
│   • Eurocontrol: Manages air traffic flow (ATFM slots) and route charges│
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (Certificates, Audits & Enforces)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         3. WHO OPERATES SERVICES?                       │
│                     (The Industry / Service Providers)                  │
│   • Airlines / Air Operators (AOC holders under Part-CAT)               │
│   • Aerodrome Operators (ADR certified airport authorities)             │
│   • Air Navigation Service Providers (ANSPs: DFS, DSNA, NATS, ENAIRE)   │
│   • Maintenance Organisations (Part-145 MRO & Part-CAMO)                │
│   • Flight Training Organisations (Approved Training Orgs - ATOs)       │
│   • Ground Handling & Ramp Service Providers                            │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. The One-Page Master Governance Matrix

| Aviation Domain | 1. Who Makes the Rules? | 2. Who Oversees Compliance? | 3. Who Operates the Service? | Operating Certificate / License |
| :--- | :--- | :--- | :--- | :--- |
| **Aircraft Design & Production** | EU Commission / EASA | **EASA (Direct Centralized)** | Manufacturers (Airbus, Rolls-Royce, Dassault) | Design Organisation Approval (DOA / Part-21) & Type Certificate |
| **Airline Flight Operations** | EU Commission (Air Ops) / EASA | **National Authority (NCA)** | Airlines (Lufthansa, Air France, Ryanair) | Air Operator Certificate (AOC) & Operations Specifications |
| **Aircraft Maintenance (MRO)** | EU Commission (Part-M/145) | **National Authority (NCA)** | Maintenance Repair Stations & CAMOs | Part-145 Approval & Part-CAMO Certificate |
| **Pilot Training & Licensing** | EU Commission (Part-FCL) | **National Authority (NCA)** | Commercial Pilots & Flight Schools (ATOs) | Flight Crew License (ATPL/CPL) & ATO Certificate |
| **Commercial Aerodromes** | EU Commission (Part-ADR) | **National Competent Authority** | Airport Authorities (Fraport, ADP, AENA) | Aerodrome Operator Certificate (ADR) |
| **Air Traffic Management** | EU Commission (Single Sky) | **National Supervisory Authority** | Air Traffic Providers (DFS, NATS, DSNA) | Air Navigation Service Certificate (ANSP) |
| **Foreign Carriers Flying to EU**| EU Commission (Part-TCO) | **EASA (Direct Centralized)** | Non-EU Airlines (Delta, Emirates, Qatar) | Third-Country Operator (TCO) Authorization |

---

## 3. The 30-Minute Operational Dispatch Handshake

Every time a commercial flight takes off, the three pillars synchronize in real-time:
1. **The Aircraft (EASA + MRO)**: The airliner flies under a Type Certificate issued by **EASA**. At the gate, a licensed technician from a **Part-145 MRO** inspects the airplane and signs the Certificate of Release to Service (CRS).
2. **The Airline (NCA + Dispatch)**: The flight is dispatched under the airline's Air Operator Certificate (AOC) issued by the **National Competent Authority** (e.g. LBA or DGAC). The dispatcher calculates fuel complying with `CAT.OP.MPA.181`.
3. **The Airport (NCA + ADR Operator)**: The airport operator manages the runway friction, taxiway lighting, and fire services under an **ADR certificate**.
4. **The Airspace (Eurocontrol + ANSP)**: The aircraft pushes back within its allocated slot issued by **Eurocontrol (Network Manager)** and climbs into controlled airspace directed by the national **ANSP**.

---

## 4. Week 03 Synthesis: European & National Governance

| Day | Theme | Key Learning Point & Regulatory Anchor |
| :---: | :--- | :--- |
| **015** | **Understand** | Institutional Quadrilateral: Parliament $\to$ Commission $\to$ EASA $\to$ NCAs (Reg 2018/1139). |
| **016** | **Derive** | Direct Applicability (TFEU 288), Part-ARO oversight, Part-ORO Accountable Manager, finding escalation. |
| **017** | **Build** | Constructing a 5-Point Traceability Table (Requirement $\to$ Source $\to$ Authority $\to$ Org $\to$ Evidence). |
| **018** | **Challenge** | The Hierarchy of Norms: Hard Law vs CS vs AMC (Presumption of Conformity / AltMoC) vs GM vs SOP. |
| **019** | **Apply** | Live operational trace: Flight Time Limitations (`ORO.FTL.205`) & Commander's Discretion limits. |
| **020** | **Integrate** | The Tripartite Stack: ICAO Global Baseline $\cap$ EASA Regional Law $\cap$ Local Aerodrome AIP. |
| **021** | **Consolidate** | The One-Page Ecosystem Blueprint: Who makes rules, who oversees compliance, who operates services. |

---

## 5. Practical Deliverable & Verification

Run the interactive Python simulation script for Day 021 to query the complete aviation ecosystem governance router, trace the multi-actor dispatch handshake, and stress-test an emerging technology regulatory vacuum:

```bash
python learned/week-03/day-021/experiment.py
```
