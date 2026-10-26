# Day 026 — Operational Guide: Researching Requirements via Primary Sources & Documenting Exact Applicability

[← Return to Lesson Plan](../../../lessons/week-04/day-026.md) | [Technical & Mathematical Walkthrough](analysis.md) | [System Topology Canvas](architecture.mermaid) | [Run Python Simulator](experiment.py)

---

## 1. Executive Summary & Operational Context

In aviation operations and safety engineering, hearsay is unacceptable. An airline captain, compliance auditor, or aircraft maintenance engineer cannot justify an operational decision by saying *"I read it on a forum"* or *"That's how our competitor does it."* You must be able to cite the **primary legal source** — the specific article, paragraph, and subparagraph of an enacted European Union Regulation, ICAO Annex, or National Statutory Instrument.

Today's lesson demonstrates the end-to-end primary source research methodology by taking one critical, high-risk operational requirement — **the carriage and in-flight use of Portable Electronic Devices (PEDs) and Lithium Batteries (`CAT.GEN.MPA.140` & `CAT.GEN.MPA.200`)** — and documenting its exact legal applicability, technical scope, and operational boundaries.

---

## 2. The 4-Step Primary Source Research Protocol

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                 PRIMARY SOURCE RESEARCH METHODOLOGY                             │
├─────────────────────────────────────────────────────────────────────────────────┤
│ STEP 1: LOCATE THE ENACTED LEGISLATIVE INSTRUMENT                               │
│ Search Eur-Lex (Official Journal of the EU) for the parent regulation.          │
│ • Commission Regulation (EU) No 965/2012 Annex IV (Part-CAT)                    │
├─────────────────────────────────────────────────────────────────────────────────┤
│ STEP 2: CROSS-REFERENCE EASA SOFT LAW (AMC & GM)                                │
│ Retrieve the EASA Executive Director Decision establishing AMC & GM.            │
│ • AMC1 CAT.GEN.MPA.140 (EMI certification standards RTCA DO-363 / ED-239)       │
│ • AMC2 CAT.GEN.MPA.140 (Cabin crew firefighting & water cooling procedures)     │
├─────────────────────────────────────────────────────────────────────────────────┤
│ STEP 3: INTERSECT WITH SPECIALIZED TECHNICAL STANDARDS                          │
│ Consult ICAO Doc 9284 (Dangerous Goods Technical Instructions) & EASA SIBs.     │
│ • SIB 2017-01R1 (Smart luggage and lithium battery Watt-hour limits)            │
├─────────────────────────────────────────────────────────────────────────────────┤
│ STEP 4: DOCUMENT EXACT APPLICABILITY & INTERNAL MANUAL CITATIONS                │
│ Map the requirement into company Operations Manual (OM-A, OM-B Cabin Crew).     │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Dissecting the Lithium Battery Mandate: The Physics Behind the Rule

Why does European aviation law (`CAT.GEN.MPA.200` & ICAO Doc 9284) strictly permit spare power banks in the passenger cabin but **strictly prohibit them in checked baggage inside the cargo hold**?

1. **The Fire Suppression Paradox**:
   - The aircraft lower cargo hold is equipped with a **Halon 1301 fire suppression system**. Halon works by chemically inhibiting flame propagation, but it **cannot cool the internal chemistry** of a lithium-ion battery in thermal runaway.
   - If a lithium battery catches fire in a checked suitcase, the runaway reactions continue generating heat ($>600^\circ\text{C}$), producing combustible toxic gases that can over-pressurize the hold or defeat fire barriers.
2. **The Cabin Advantage**:
   - In the passenger cabin, cabin crew are trained under `AMC2 CAT.GEN.MPA.140` to immediately extinguish flames with Halon 1211, and then **douse the device with water or non-alcoholic liquid**.
   - Water absorbs the $1.4\text{ Megajoules}$ of chemical energy released through high latent heat of vaporization ($2,260\text{ kJ/kg}$), cooling the battery below the thermal runaway propagation threshold ($150^\circ\text{C}$). The device is then sealed in a fire containment bag.

---

## 4. Applicability Summary Table

| Regulatory Field | Precise Primary Citation | Applicable Scope | Exceptions & Thresholds |
| :--- | :--- | :--- | :--- |
| **In-Flight PED Usage** | `CAT.GEN.MPA.140` | All EASA CAT passenger aircraft | Permitted gate-to-gate only if aircraft has proven EMI tolerance (ED-239). |
| **Spare Power Banks** | ICAO Doc 9284 Part 8 / SIB 2017-01 | Commercial passengers & crew | Carry-on only. $\le 100\text{ Wh}$ allowed; $>100\text{ to }160\text{ Wh}$ requires airline approval; $>160\text{ Wh}$ forbidden. |
| **Smart Luggage** | EASA SIB 2017-01R1 | Baggage with integrated battery | If checked, battery **must be removed** and carried into the cabin. |

---

## 5. Practical Hands-On Exercise & Verification

Launch the interactive Python Primary Source Applicability and Battery Thermodynamics Simulator:
```bash
python learned/week-04/day-026/experiment.py
```

The simulator allows you to:
1. Conduct an interactive compliance check on passenger electronics and battery capacities.
2. Calculate the thermal runaway energy ($kJ$) and minimum water cooling volume required under `AMC2 CAT.GEN.MPA.140`.
3. Stress-test an illegal attempt to check a non-removable $160\text{ Wh}$ smart bag into the cargo hold, observing the automated gate refusal and regulatory safety intervention.
