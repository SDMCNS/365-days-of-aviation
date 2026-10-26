# Day 015 — European Aviation Governance: The Commission, EASA, and National Competent Authorities

[← Return to Lesson Plan](../../../lessons/week-03/day-015.md) | [📊 Technical Walkthrough](analysis.md) | [System Topology Canvas](architecture.mermaid) | [Run Python Simulator](experiment.py)

---

## 1. Executive Summary: The Multi-Layered European Governance Model

In civil aviation, students often ask: *"Is EASA the European FAA?"*

The answer is **both yes and no**. While EASA (European Union Aviation Safety Agency, based in Cologne, Germany) performs many functions analogous to the US FAA, Europe's regulatory model is fundamentally distinct. 

In the United States, a single federal agency—the FAA—handles everything: writing federal aviation regulations, inspecting Boeing's factories, issuing airline operating certificates (Part 121), licensing every private and commercial pilot, and operating the nation's air traffic control towers.

In the European Union, aviation governance is split between **centralized European bodies** and **sovereign National Competent Authorities (NCAs)** across 27 Member States (plus Switzerland, Norway, and Iceland):
- **Political & Legislative Power**: Resides with the **European Parliament & Council** and the **European Commission (DG MOVE)**.
- **Technical & Design Competence**: Resides with **EASA**. EASA directly certifies all aircraft types (Airbus, Boeing, Embraer) and design organisations (DOA).
- **Operational & Day-to-Day Enforcement**: Resides with **National Competent Authorities** (e.g. DGAC in France, LBA in Germany, AESA in Spain, ENAC in Italy). The NCAs issue Air Operator Certificates to airlines, license pilots, certify mechanics, and inspect airports.

The overarching constitutional charter of this system is **Regulation (EU) 2018/1139**, known throughout the industry as the **EASA Basic Regulation**.

---

## 2. The Four Pillars of European Aviation Governance

```
┌─────────────────────────────────────────────────────────────────────────┐
│               1. LEGISLATIVE: PARLIAMENT & COUNCIL OF THE EU            │
│  • Enacts the Basic Regulation (EU) 2018/1139 under TFEU Article 100(2) │
│  • Establishes EASA's legal mandate, budget, and scope of competence    │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                 2. EXECUTIVE: EUROPEAN COMMISSION (DG MOVE)             │
│  • Adopts legally binding Delegated and Implementing Regulations        │
│  • Manages the EU Air Safety List (Blacklist)                           │
│  • Launches infringement proceedings against non-compliant Member States│
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│            3. TECHNICAL SPECIALIST: EASA (COLOGNE, GERMANY)             │
│  • Drafts technical rules ("Opinions") for the Commission               │
│  • Issues non-binding Soft Law: AMC, Guidance Material, and CS          │
│  • Direct Certification: Aircraft Type Certificates & Part-21 DOA       │
│  • Standardisation Oversight: Audits all national aviation authorities  │
└──────────────────┬───────────────────────────────────▲──────────────────┘
                   │                                   │ (Audits & SCI)
                   │ (Technical Rules & Standards)     │
                   ▼                                   │
┌──────────────────────────────────────────────────────┴──────────────────┐
│      4. OPERATIONAL ENFORCERS: NATIONAL COMPETENT AUTHORITIES (NCAs)    │
│  • DGAC (France), LBA (Germany), AESA (Spain), ENAC (Italy), etc.       │
│  • Issues Air Operator Certificates (AOC) to national airlines          │
│  • Issues Flight Crew Licenses (Part-FCL) and Maintenance Approvals     │
│  • Certifies commercial aerodromes (ADR) and national ANSPs             │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Division of Competence: Who Does What?

To navigate European aviation, you must understand the jurisdictional boundary between EASA and the NCAs:

### 1. Direct EASA Competence (Centralized in Cologne)
- **Airworthiness Type Certification (Part-21)**: EASA directly certifies every aircraft type flown in the EU (e.g. Airbus A321neo, Boeing 787, Dassault Falcon). The Type Certificate belongs to EASA, not France or Germany.
- **Design Organisation Approvals (DOA)**: EASA directly audits and certifies manufacturers who design aircraft or major modifications (Airbus, Rolls-Royce, Safran).
- **Third-Country Operators (Part-TCO)**: Any non-EU airline wishing to fly commercial passengers into EU airspace (e.g. Delta, Emirates, Singapore Airlines) must obtain an operational safety authorization directly from EASA.

### 2. National Competent Authority Competence (Decentralized to Member States)
- **Air Operator Certificates (AOC)**: Air France is certified and audited by the French DGAC; Lufthansa by the German LBA; Iberia by the Spanish AESA.
- **Continuing Airworthiness (Part-CAMO & Part-145)**: Airline maintenance management and line/base maintenance repair stations are certified by their national authority.
- **Flight Crew Licensing (Part-FCL)**: Pilots hold national licenses issued under European rules by their home NCA.
- **Aerodrome Certification (ADR)**: Physical airports (Paris CDG, Frankfurt, Madrid Barajas) are certified and supervised by the national authority of the territory where they reside.

---

## 4. EASA Standardisation: Auditing the Regulators

If 27 separate national authorities issue AOCs and licenses, what prevents one country from becoming a "flag of convenience" with lax safety oversight to attract airlines?

The answer is **EASA Standardisation Inspections** under **Commission Implementing Regulation (EU) No 628/2013**:
1. **Auditing the Authority**: EASA inspectors visit national CAAs unannounced, reviewing inspector files, audit logs, and certification decisions.
2. **Standardisation Findings**:
   - **Class C (Observation)**: Minor clerical or administrative suggestions.
   - **Class D (Non-Compliance)**: Violation of an EU implementing rule. The NCA must produce an agreed **Corrective Action Plan (CAP)** within 90 days.
   - **Class G (Urgent Safety Finding)**: A systemic failure that poses an immediate threat to safety. The NCA must execute provisional safety measures within 15 days.
3. **The Ultimate Sanction**: If a Member State refuses or fails to rectify deficiencies, EASA informs the European Commission. The Commission can suspend **mutual recognition (Article 70)** of that country's certificates across Europe, grounding its airlines' international flights until compliance is restored.

---

## 5. Practical Deliverable & Verification

Run the interactive Python simulation script for Day 015 to explore the European competence division router, simulate an EASA Standardisation Inspection of a National Competent Authority, and calculate the Standardisation Compliance Index:

```bash
python learned/week-03/day-015/experiment.py
```
