# Day 017 — The Architecture of Proof: Constructing a Regulatory Traceability Table

[← Return to Lesson Plan](../../../lessons/week-03/day-017.md) | [📊 Technical Walkthrough](analysis.md) | [System Topology Canvas](architecture.mermaid) | [Run Python Simulator](experiment.py)

---

## 1. Executive Summary: Why Aviation Requires Traceability

In commercial aviation, the statement *"Our airline always follows the rules"* is legally meaningless. 

When a National Competent Authority (such as the UK CAA, French DGAC, or German LBA) performs a certification audit on an airline, airport, or maintenance organisation, they do not take anyone's word for it. They operate on a strict evidentiary doctrine:

> **"If it is not written down, it does not exist. If there is no auditable evidence, it did not happen."**

A **Regulatory Traceability Table** (often referred to as a **Compliance Matrix** or **Statement of Compliance**) is the master blueprint that connects high-level European and international aviation laws to the everyday actions of flight crews, dispatchers, mechanics, and ramp handlers. It provides an unbroken chain of custody proving that every single sentence in the regulatory code has an assigned corporate owner, a documented procedure, and verifiable proof of execution.

---

## 2. The 5-Column Traceability Model

Every regulatory line item must be mapped across five mandatory structural dimensions:

```
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│  1. REQUIREMENT  │    │    2. SOURCE     │    │   3. AUTHORITY   │    │ 4. ORGANISATION  │    │   5. EVIDENCE    │
│  What must be    │───►│  Which statute   │───►│  Who oversees    │───►│  Who executes    │───►│  How do you      │
│  achieved?       │    │  mandates it?    │    │  and audits it?  │    │  the task?       │    │  prove it?       │
└──────────────────┘    └──────────────────┘    └──────────────────┘    └──────────────────┘    └──────────────────┘
```

1. **The Operational Requirement**: The plain-language technical rule and its mathematical thresholds (e.g., minimum reserve fuel, maximum duty hours, required runway friction).
2. **The Statutory Source**: The exact legal chapter, paragraph, and subparagraph (e.g. Regulation (EU) 965/2012 `CAT.OP.MPA.181`).
3. **The Responsible Authority**: The state or regional regulator empowered to enforce the rule (e.g. EASA or the National Competent Authority).
4. **The Regulated Organisation**: The entity holding the certificate (e.g. Part-CAT Airline, Part-145 MRO, or Aerodrome Operator).
5. **The Compliance Evidence Artifact**: The tangible physical or digital proof generated during operations (e.g. an Operational Flight Plan signed by the captain, an aircraft tech log entry, or a fire drill log).

---

## 3. Master Traceability Matrix: Six Core Operational Domains

```
   [EU HARD LAW]  ───────►  [NATIONAL REGULATOR]  ───────►  [OPERATOR MANUAL]  ───────►  [FLIGHT EVIDENCE]
   CAT.OP.MPA.181              French DGAC / LBA                 OM-A Section 8.1             Signed OFP & ATL
```

The table below illustrates the complete 5-point traceability chain across six foundational civil aviation domains:

| Domain | 1. Operational Requirement | 2. Statutory Source | 3. Responsible Authority | 4. Regulated Organisation | 5. Compliance Evidence Artifact |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Fuel Planning** | Every flight must carry taxi, trip, contingency (5%), alternate, and 30-min final reserve fuel. | Reg (EU) 965/2012 **CAT.OP.MPA.181** | National Competent Authority (NCA) | Commercial Air Transport Operator (Part-CAT) | Operational Flight Plan (OFP) signed by Captain & Dispatcher; fuel uplift receipts. |
| **Flight Time (FTL)** | Maximum Flight Duty Period (FDP) capped based on report time and sectors; mandatory rest periods. | Reg (EU) 965/2012 **ORO.FTL.205** | National Competent Authority (NCA) | Commercial Air Transport Operator (Part-CAT) | Crew Rostering System duty records; Commander's Discretion Report Form (if FDP extended). |
| **Maintenance Release** | Aircraft cannot be released to service without verification of certified maintenance completion. | Reg (EU) 1321/2014 **M.A.801 & 145.A.50** | NCA / EASA (for non-EU MROs) | Part-145 Maintenance Organisation / CAMO | Certificate of Release to Service (CRS) signed in Aircraft Technical Logbook (ATL). |
| **Low Visibility Ops** | Specific approval required for CAT II/III precision approaches; auto-rollout and DH limits. | Reg (EU) 965/2012 **SPA.LVO.100** | National Competent Authority (NCA) | Commercial Air Transport Operator (Part-CAT) | AOC Operations Specifications (OpSpecs); Pilot 6-month Sim Check Form; AFM autoland supplement. |
| **Aerodrome RFFS** | Aerodrome must maintain dedicated Rescue and Firefighting Category with $\le 3\text{ min}$ response time. | Reg (EU) 139/2014 **ADR.OPS.B.010** | National Competent Authority (NCA) | Certified Aerodrome Operator (ADR) | Daily RFFS Station Readiness Log; Annual Emergency Response Exercise Drill Records. |
| **Dangerous Goods** | Dangerous goods acceptance inspection, packaging checks, and formal written notification to pilot. | Reg (EU) 965/2012 **CAT.GEN.MPA.200** | National Competent Authority (NCA) | Commercial Air Transport Operator (Part-CAT) | Completed Dangerous Goods Acceptance Checklist; NOTOC (Notification to Captain) signed copy. |

---

## 4. The Dangerous Myth of "Compliance Blind Spots"

What happens if an airline performs a safe operation, but its traceability table has a missing link?

Consider an airline that carries adequate final reserve fuel on every single flight, but its Operations Manual fails to reference the newly updated **AMC1 CAT.OP.MPA.181**, or dispatchers do not archive signed paper or electronic copies of the OFP for 3 months:
- In the eyes of the regulator, this is a **Compliance Blind Spot**.
- The authority inspector will issue a formal **Level 2 finding** under **Part-ARO.GEN.350**.
- The airline will be forced into a 90-day corrective action cycle, requiring root-cause analysis, software updates, and staff retraining.

A complete regulatory traceability table is the shield that protects an airline's Air Operator Certificate from regulatory suspension.

---

## 5. Practical Deliverable & Verification

Run the interactive Python simulation script for Day 017 to explore the regulatory traceability database, execute forward and backward compliance traces across the 6 core aviation domains, and stress-test a simulated regulatory gap:

```bash
python learned/week-03/day-017/experiment.py
```
