# Day 018 — The Hierarchy of Norms: Hard Law, AMC, GM, CS, and Company SOPs

[← Return to Lesson Plan](../../../lessons/week-03/day-018.md) | [📊 Technical Walkthrough](analysis.md) | [System Topology Canvas](architecture.mermaid) | [Run Python Simulator](experiment.py)

---

## 1. Executive Summary: The Trap of Treating All Rules Alike

In the complex world of aviation regulations, one of the most common—and expensive—mistakes made by engineers, airline managers, and even novice regulatory inspectors is assuming that **every sentence written in an EASA document is an inflexible statutory law**.

This misconception leads to two dangerous extremes:
1. **Blind Over-Compliance**: An airline spends millions of euros implementing cumbersome procedures because they mistakenly believed that an EASA *Guidance Material (GM)* note was a mandatory legal command.
2. **Unlawful Deviation**: An airline cuts corners on an *Implementing Rule (Hard Law)*, assuming it was merely a recommendation, resulting in immediate fleet grounding by the civil aviation authority.

To navigate aviation law with precision, you must master the **Five Tiers of European Aviation Norms**:

```
[TIER 1: HARD LAW] ────► [TIER 2: CS STANDARDS] ────► [TIER 3: AMC SOFT LAW] ────► [TIER 4: GM ADVISORY] ────► [TIER 5: COMPANY SOP]
  Directly Binding         Binding for Cert Basis     Presumption of Conformity    Purely Explanatory           Internally Binding
```

---

## 2. Deconstructing the Five Normative Tiers

### 1. Hard Law: Implementing Regulations (IRs)
- **Legal Source**: Enacted by the European Commission under the Basic Regulation (e.g. `CAT.OP.MPA.181`, `Part-145.A.50`).
- **Legal Status**: **Legally Binding in its entirety**.
- **Can you deviate?** No. Any deviation without a formal European Commission exemption under Article 71 is a direct statutory violation.

### 2. Certification Specifications (CS)
- **Legal Source**: Issued by EASA Decisions (e.g. `CS-25` for Large Aeroplanes, `CS-FTL.1` for Flight Time Limitations).
- **Legal Status**: **Binding once incorporated into the certification basis**.
- **Can you deviate?** Only via an **Equivalent Safety Finding (ESF)** approved during the aircraft type certification process.

### 3. Acceptable Means of Compliance (AMC)
- **Legal Source**: Issued by EASA Executive Director Decisions (e.g. `AMC1 CAT.OP.MPA.181(a)`).
- **Legal Status**: **Soft Law (Non-binding)**.
- **The Golden Rule**: AMCs illustrate *one approved way* to comply with the Hard Law. If you follow the AMC, you enjoy an automatic **Presumption of Conformity**—the regulator cannot reject your procedure.
- **Can you deviate?** **YES!** Under `ORO.GEN.120`, an airline can propose an **Alternative Means of Compliance (AltMoC)** that achieves the same safety goal through a different method, subject to prior authority approval.

### 4. Guidance Material (GM)
- **Legal Source**: Issued by EASA Decisions alongside AMCs.
- **Legal Status**: **Purely Advisory**.
- **The Auditor Trap**: GM contains explanatory text, definitions, and philosophy. **An auditor cannot legally issue a finding citing only a GM!** A finding must always cite an Implementing Rule (Hard Law).

### 5. Company Procedures (SOPs / OM / MOE)
- **Legal Source**: Written by the airline or MRO and accepted/approved by the National Competent Authority as part of the Air Operator Certificate.
- **Legal Status**: **Legally Binding on employees**.
- **The Internal Mandate**: If an airline's Operations Manual Part A requires a pilot to carry 45 minutes of reserve fuel (even though the law only requires 30 minutes), the pilot is legally bound by company SOP. Violating the SOP is grounds for license suspension or termination.

---

## 3. The Power of AltMoC: How Leading Airlines Innovate

Why does EASA allow Alternative Means of Compliance (AltMoC)?

Because technology evolves faster than legislation. When airlines wanted to replace heavy paper flight manuals with electronic iPads (Electronic Flight Bags), the existing AMC required complex physical containment boxes. Leading airlines engineered an **AltMoC under ORO.GEN.120**:
1. Conducted quantitative thermal runaway hazard risk assessments,
2. Proved that fire bags and flight deck telemetry achieved equal or superior safety margins,
3. Gained National Authority approval,
4. EASA reviewed the data and eventually adopted the airline's AltMoC as the new global standard!

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    THE ALTMOC APPROVAL PIPELINE                         │
│ 1. Airline Hazard & Quantitative Risk Assessment (ORO.GEN.200)          │
│ 2. Submit Safety Equivalence Dossier to National Competent Authority    │
│ 3. Authority Review & Formal Approval (ARO.GEN.120)                     │
│ 4. 30-Day Central Notification to EASA for Standardisation Harmonisation│
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Practical Deliverable & Verification

Run the interactive Python simulation script for Day 018 to classify regulatory text into the correct normative tier, simulate an AltMoC safety equivalence calculation, and test your defense against an invalid "GM audit finding":

```bash
python learned/week-03/day-018/experiment.py
```
