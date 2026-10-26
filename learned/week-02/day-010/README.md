# Day 010 — Operational Guide: The Hierarchy Map of Conventions, Annexes, PANS & State Regulations

[← Return to Master Syllabus](../../lessons/README.md) | [Technical Walkthrough](analysis.md) | [System Topology Canvas](architecture.mermaid) | [Run Python Simulator](experiment.py)

---

## 1. Executive Summary: The Structural Spine of Aviation Law

A commercial aircraft in flight is governed by hundreds of technical specifications simultaneously: how thick the cockpit windshield must be, how many fire extinguishers are required, what phraseology air traffic control uses, and how flight hours are logged.

Where do these rules come from, and which document wins when two sources disagree?

To answer this, an aviation professional must master the **5-Tier Hierarchy of Aviation Material**:
1. **Tier 1 — The Convention**: The primary international treaty (Chicago 1944, Doc 7300), signed and ratified by sovereign nations.
2. **Tier 2 — The 19 Annexes**: Technical Standards and Recommended Practices (SARPs) adopted by the ICAO Council.
3. **Tier 3 — PANS (Procedures for Air Navigation Services)**: Detailed worldwide operational instructions (Doc 4444 ATM, Doc 8168 OPS) approved by ICAO Council.
4. **Tier 4 — ICAO Guidance Manuals**: Non-binding technical guidance manuals (Doc 9859 SMS, Doc 9640 De-icing) published under Secretary General authority.
5. **Tier 5 — National Law & Operator Procedures**: Sovereign legislation (EASA regulations, FAA FARs, national AIPs) and airline Operations Manuals (OM-A/B/C/D).

---

## 2. Navigating the 5 Tiers

| Tier | Document Type | Legal Authority | Binding Force on Operators | Example |
| :--- | :--- | :--- | :--- | :--- |
| **Tier 1** | **International Treaty** | Chicago Convention 1944 (Doc 7300) | Binding on sovereign States; not directly self-executing on airlines. | Article 1 (Sovereignty), Article 12 (Rules of the Air), Article 33 (Mutual Recognition). |
| **Tier 2** | **ICAO Annexes (SARPs)** | Adopted by ICAO Council under Art. 37 & 54(l) | Mandatory on States unless Article 38 difference filed. | Annex 6 (Operation of Aircraft), Annex 8 (Airworthiness), Annex 14 (Aerodromes). |
| **Tier 3** | **PANS Documents** | Approved by ICAO Council for worldwide use | Operational baseline; incorporated into State AIPs. | Doc 4444 (PANS-ATM), Doc 8168 (PANS-OPS Aircraft Operations). |
| **Tier 4** | **ICAO Manuals & Circulars** | Published under ICAO Secretary General | Advisory; provides "how-to" guidance, but cannot create law. | Doc 9859 (Safety Management Manual), Doc 9976 (Flight Planning & Fuel). |
| **Tier 5** | **National Acts & Operator SOPs** | Sovereign Parliaments, NAAs, and Airlines | Directly legally enforceable on pilots and airlines with criminal penalties. | Regulation (EU) 2018/1139, EASA Part-CAT, Airline Operations Manual (OM-A). |

---

## 3. The Golden Rule of Legal Precedence

> **The Higher Tier Always Overrules the Lower Tier.**
> If an operator manual (Tier 5) contradicts a national regulation (Tier 5), the national regulation wins.
> If a national regulation contradicts an ICAO standard (Tier 2), the State is in breach of international law unless it has formally filed an Article 38 difference in its AIP.
> If an ICAO manual (Tier 4) contains advice that contradicts an Annex standard (Tier 2), the Annex standard prevails.

---

## 4. Practical Implementation Reference

Launch the interactive Day 010 Regulatory Hierarchy Navigator:
```bash
python learned/week-02/day-010/experiment.py
```
This tool:
1. Traces regulatory lineage from the Chicago Convention down to cockpit checklists across 5 operational domains.
2. Resolves legal precedence when operational conflicts occur.
3. Validates regulatory compliance chains (checking for broken links or unapproved procedures).
4. Simulates a regulatory audit finding where an unauthorized company procedure violates Tier 2/5 standards.
