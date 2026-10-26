# Day 028 — Month 01 Capstone Project: Master Aviation Ecosystem Map & Regulatory Reference Guide

[← Return to Lesson Plan](../../../lessons/week-04/day-028.md) | [Technical & Mathematical Walkthrough](analysis.md) | [System Topology Canvas](architecture.mermaid) | [Run Python Simulator](experiment.py)

---

## 1. Executive Summary & Capstone Deliverable

Welcome to the **Month 01 Capstone Project** of the 365 Days of Aviation curriculum. 

Over the past four weeks, you have progressed systematically through the foundational architecture of civil aviation:
- **Week 01**: *The Global Air Transport System* (Airports, Airlines, ANSPs, Handlers, Fleet Economics, and Turnaround Critical Paths).
- **Week 02**: *International Aviation Law & Sovereign Airspace* (Chicago Convention Doc 7300, 19 Annexes, SARPs vs Differences, Freedoms of the Air, and USOAP).
- **Week 03**: *European & National Governance* (TFEU Art 288 direct applicability, EASA Basic Reg 2018/1139, Division of Competence, Level 1 Findings, and Commander's Authority).
- **Week 04**: *The Aviation Regulatory Library* (PANS Series Doc 8168/4444, the 7 EASA Domains, Easy Access Rules, Regulatory Registers, and the Quad-Link Traceability Architecture).

Today's capstone synthesizes these four pillars into a unified operational artifact: **The Master Aviation Ecosystem Map and Regulatory Reference Guide**.

---

## 2. The Master Aviation Ecosystem Architecture

Civil aviation functions as a tightly coupled, multi-tiered hierarchy. Power, legal authority, and operational data cascade down through five distinct layers:

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                   THE 5-TIER AVIATION ECOSYSTEM TOPOLOGY                                         │
├──────────────────────────────────────────────────────────────────────────────────────────────────┤
│ TIER 1: GLOBAL PUBLIC INTERNATIONAL LAW (ICAO)                                                   │
│ • Chicago Convention (Doc 7300): Airspace Sovereignty (Art 1), Overflight Rights, Treaties       │
│ • 19 ICAO Annexes: SARPs (Standards: Shall / Recommended Practices: Should)                      │
│ • PANS Series: PANS-OPS (Doc 8168), PANS-ATM (Doc 4444), PANS-ADR (Doc 9981)                      │
│ • Global Plans: GASP (Doc 10004 Safety), GANP (Doc 9750 Modernization / ASBU Blocks)             │
├──────────────────────────────────────────────────────────────────────────────────────────────────┤
│ TIER 2: SUPRANATIONAL & REGIONAL LEGISLATION (EUROPEAN UNION & EASA)                             │
│ • Treaty Foundation: TFEU Article 288 (Regulations have direct applicability and primacy)       │
│ • Basic Regulation (EU) 2018/1139: EASA competence over Design, Type Certification, Foreign Ops  │
│ • The 7 Domains: Part-21, Part-M/145/CAMO, Part-CAT/SPA/NCC/NCO, Part-FCL, Part-ADR, ATM/ANS, UAS│
│ • Easy Access Rules (EAR): Hard Law (IR) vs Soft Law (CS, AMC Presumption of Conformity, GM)     │
├──────────────────────────────────────────────────────────────────────────────────────────────────┤
│ TIER 3: NATIONAL OVERSIGHT & STATE REGULATIONS (NAAS & LOCAL AIP)                                │
│ • National Authorities: CAA/DGAC issuing AOCs, Part-145 approvals, and Pilot Licenses            │
│ • Aeronautical Information Publications (AIP): GEN 1.7 State Differences, Local Curfews & Noise │
│ • State Safety Programmes (SSP): National safety targets under ICAO Annex 19                     │
├──────────────────────────────────────────────────────────────────────────────────────────────────┤
│ TIER 4: CERTIFIED OPERATIONAL ORGANISATIONS (THE INDUSTRY OPERATORS)                             │
│ • Airlines (AOC Holders under Part-CAT & Part-ORO): Accountable Manager (ORO.GEN.210)            │
│ • Maintenance & Engineering: CAMO airworthiness management & Part-145 MRO base/line stations     │
│ • Aerodrome Operators: Certified under Part-ADR (Runway surface friction GRF, RFFS categories)   │
│ • Air Navigation Service Providers (ANSPs): Certified under Reg (EU) 2017/373 (Separation & CNS) │
├──────────────────────────────────────────────────────────────────────────────────────────────────┤
│ TIER 5: CLOSED-LOOP EVIDENCE & REAL-TIME EXECUTION (THE COCKPIT & RAMP)                          │
│ • The Quad-Link: Rule -> Postholder -> Frontline SOP -> Safety Metric (SPI) -> Indestructible Proof│
│ • Aircraft Technical Log: Certificate of Release to Service (CRS) under Part-145.A.50             │
│ • Operational Flight Plan (OFP): Certified Fuel Reserves under Regulation (EU) 2021/1296         │
│ • Flight Data Monitoring (FDM): Black box telemetry verifying flight stability and safety limits  │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. The Master Regulatory Reference Guide (Quick-Lookup)

| Operational Subject | Governing ICAO Annex / Doc | Governing EU / EASA Regulation | Company Manual Reference | Mandatory Audit Evidence Record |
| :--- | :--- | :--- | :--- | :--- |
| **Airspace Sovereignty** | Doc 7300 Arts 1, 5, 6, 12 | Standardised European Rules of the Air (SERA Reg 923/2012) | OM-A Section 8 (En-Route Navigation) | Diplomatic Overflight Permits & ATC Flight Plans |
| **Commercial Air Transport** | ICAO Annex 6 (Operation of Aircraft) | Regulation (EU) No 965/2012 Annex IV (Part-CAT) | Operations Manual Parts A, B, C, D | Air Operator Certificate (AOC) & Operations Specifications |
| **Fuel & Energy Planning** | Annex 6 Part I (Fuel Policy) | Regulation (EU) 2021/1296 (EASA Fuel Scheme) | OM-A Chapter 8.1.7 (Fuel Policy) | OFP with Trip, Cont, Alternate & 30-min Final Reserve |
| **Flight Crew Fatigue (FTL)** | Annex 6 Part I Chapter 4 | Reg (EU) 965/2012 Subpart ORO.FTL & CS-FTL.1 | OM-A Chapter 7 (Flight Time Limitations) | Digital Crew Sign-in Timestamps & Form FTL-104 |
| **Continuing Airworthiness** | ICAO Annex 8 (Airworthiness) | Regulation (EU) No 1321/2014 (Part-M & Part-CAMO) | Continuing Airworthiness Mgmt Exposition (CAME) | Airworthiness Review Certificate (ARC Form 15) |
| **Maintenance Release** | Annex 6 & Annex 8 | Regulation (EU) No 1321/2014 Annex II (Part-145) | Maintenance Organisation Exposition (MOE) | Signed Certificate of Release to Service (CRS) in Tech Log |
| **Pilot Licensing & Medical** | ICAO Annex 1 (Personnel Licensing) | Regulation (EU) No 1178/2011 (Part-FCL & Part-MED) | OM-D (Crew Training Records) | EASA Pilot License, Type Rating Endorsement, Class 1 Med |
| **Aerodrome Safety & RFFS** | ICAO Annex 14 (Aerodromes) | Regulation (EU) No 139/2014 (Part-ADR.OPS) | Aerodrome Manual (ADR Manual) | Runway Condition Report (RCR via GRF) & RFFS Cat log |
| **Dangerous Goods & PEDs** | ICAO Doc 9284 & Annex 18 | Reg 965/2012 CAT.GEN.MPA.140 / 200 & SIB 2017-01 | OM-A Chapter 9.2 (Dangerous Goods) | Passenger DG Check-in Declarations & Cabin Containment SOP |

---

## 4. Capstone Interactive Simulation & Ecosystem Auditor

To demonstrate mastery of Month 01, launch the comprehensive Capstone Simulator:
```bash
python learned/week-04/day-028/experiment.py
```

The capstone script allows you to:
1. Query the comprehensive Month 01 Master Regulatory Reference Guide.
2. Conduct an end-to-end multi-domain compliance audit for a real-world transatlantic flight (London Heathrow EGLL to New York JFK KJFK).
3. Evaluate the 4-gate Systemic Feasibility Model ($\mathcal{G}_{\text{Ecosystem}} \times \mathcal{G}_{\text{Airspace}} \times \mathcal{G}_{\text{Governance}} \times \mathcal{G}_{\text{Traceability}}$).
4. Run a compounding multi-system stress test simulating simultaneous airspace closure, superseded fuel policy, and an unrecorded maintenance defect to observe the regulatory failsafes that protect civil aviation from disaster.
