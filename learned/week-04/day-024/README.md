# Day 024 — Operational Guide: Constructing a Searchable Regulatory Source Register & Compliance Inventory

[← Return to Lesson Plan](../../../lessons/week-04/day-024.md) | [Technical & Mathematical Walkthrough](analysis.md) | [System Topology Canvas](architecture.mermaid) | [Run Python Simulator](experiment.py)

---

## 1. Executive Summary & Operational Context

In commercial aviation, claiming that your operations are compliant is insufficient; you must be able to **prove compliance instantly upon demand**. Whether facing an annual oversight audit from a National Aviation Authority (NAA), an ICAO Universal Safety Oversight Audit Programme (USOAP) mission, an IATA Operational Safety Audit (IOSA), or a surprise SAFA ramp inspection, an aviation organisation must present a living, controlled **Regulatory Source Register (Legal Compliance Register)**.

Under **EASA Part-ORO (`ORO.GEN.200(a)(2)`)**, the Compliance Monitoring Manager is legally accountable for ensuring that every operational procedure in company manuals traces directly back to an active statutory requirement. Operating without an updated register guarantees Level 1 audit findings and risks the suspension of the Air Operator Certificate (AOC) or Part-145 maintenance approval.

---

## 2. The 6 Mandatory Data Attributes of a Professional Source Register

Every entry in an enterprise aviation regulatory register must be indexed by six standardized attributes:

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                   THE 6 PILLARS OF A CONTROLLED REGULATORY REGISTER ENTRY                        │
├───────────────────┬───────────────────┬───────────────────┬───────────────────┬──────────────────┤
│ 1. DOCUMENT TITLE │ 2. IDENTIFIER     │ 3. AMENDMENT / VER│ 4. STATUS & DATES │ 5. APPLICABILITY │
│    & SUBJECT      │    (LEGAL CITATION)│    (OJ REFERENCE) │    (IN-FORCE/EXP) │    & SCOPE       │
└───────────────────┴───────────────────┴───────────────────┴───────────────────┴──────────────────┘
                                                │
                                                ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│ 6. ORGANISATIONAL LINKAGE: Company Manual Reference (OM-A, CAME, MOE), Postholder, Audit Cycle  │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
```

1. **Document Title**: The formal, unambiguous title of the legislative or guidance instrument (e.g., *Air Operations — Commercial Air Transport Operations*).
2. **Identifier**: The precise legal citation, enabling retrieval from official repositories like Eur-Lex or the ICAO portal (e.g., *Commission Regulation (EU) No 965/2012 Annex IV (Part-CAT)*).
3. **Version / Amendment State**: The specific consolidated edition, including recent amending acts published in the Official Journal (e.g., *Amended by Regulation (EU) 2021/1296 on Fuel Schemes*).
4. **Effective Dates & Transition Timetable**:
   - Date of publication in the Official Journal.
   - Date of entry into force.
   - Date of mandatory implementation (transition period expiration).
5. **Regulatory Status**:
   - `Active`: Currently applicable and audited.
   - `In-Transition`: Promulgated, with voluntary adoption permitted, pending mandatory deadline.
   - `Superseded`: Replaced by a newer act; retained only for historical audit records.
   - `Revoked`: Expired or repealed by legislative act.
6. **Operational Scope & Internal Linkage**:
   - Target fleet and operation types (e.g., *Airbus A320 fleet, EASA AOC passenger operations*).
   - The specific company manual chapter implementing the rule (e.g., *OM-A Chapter 8.1 Fuel Policy*).
   - The responsible Nominated Person (e.g., *Nominated Person Flight Operations*).
   - Scheduled audit verification frequency (e.g., *Annual internal compliance audit*).

---

## 3. Regulatory Change Lifecycle: Managing the Transition Window

Aviation regulations change constantly. When EASA publishes a new Implementing Rule or Executive Director Decision, the organization enters a time-critical workflow:

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    REGULATORY CHANGE LIFECYCLE WORKFLOW                         │
├─────────────────────────────────────────────────────────────────────────────────┤
│ 1. DETECTION    │ Monitor EASA Rulemaking notices and Official Journal (OJ).    │
├─────────────────┼───────────────────────────────────────────────────────────────┤
│ 2. GAP ANALYSIS │ Compare new requirements against existing OM/CAME procedures. │
├─────────────────┼───────────────────────────────────────────────────────────────┤
│ 3. MOC PROCESS  │ Trigger Safety Management of Change (MOC) under SMS.          │
├─────────────────┼───────────────────────────────────────────────────────────────┤
│ 4. REVISION     │ Draft temporary or permanent revisions to company manuals.    │
├─────────────────┼───────────────────────────────────────────────────────────────┤
│ 5. NAA APPROVAL │ Submit revised manual to NAA if prior approval is required.   │
├─────────────────┼───────────────────────────────────────────────────────────────┤
│ 6. TRAINING     │ Conduct crew / dispatcher / engineer differences training.    │
├─────────────────┼───────────────────────────────────────────────────────────────┤
│ 7. GO-LIVE      │ Activate new procedure on or before mandatory deadline.       │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### The Transition Gap Risk:
If the mandatory implementation date arrives and the company's manuals or flight planning software still use the superseded standard, the airline is operating in **illegal non-compliance**. In the event of an incident, the operator's legal defenses collapse, and insurance coverage may be repudiated.

---

## 4. Practical Hands-On Exercise & Verification

Launch the interactive Python Regulatory Source Register and Change Management Simulator:
```bash
python learned/week-04/day-024/experiment.py
```

The script allows you to:
1. Search and query an authentic multi-domain aviation regulatory inventory.
2. Filter regulations by domain, status, or keyword (e.g., `Fuel`, `FTL`, `Airworthiness`, `CAT`).
3. Calculate the **Enterprise Regulatory Risk Index (ERRI)** based on pending transition deadlines.
4. Run an adversarial stress test simulating an expired fuel regulation transition leading to flight grounding.
