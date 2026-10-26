# Day 024 — Technical Walkthrough: Engineering an Aviation Regulatory Source Register & Compliance Inventory

[← Return to Lesson Guide](README.md) | [System Topology Canvas](architecture.mermaid) | [Run Python Simulator](experiment.py)

---

## 1. Statutory Mandate for an Enterprise Regulatory Register

Under **EASA Part-ORO (`ORO.GEN.200(a)(2)`)**, **Part-145 (`145.A.65`)**, and **Part-ADR (`ADR.OR.D.005`)**, every certified aviation organisation must establish, implement, and maintain a compliance monitoring management system that includes:

> *"A process to monitor compliance of the organisation with the relevant requirements and to monitor that operational procedures and policies comply with all applicable legal standards."*

An organisation cannot demonstrate compliance to a National Aviation Authority (NAA) or EASA standardisation team without a structured, searchable **Regulatory Source Register (Legal Register / Master Compliance Inventory)**. 

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                   ENTERPRISE REGULATORY SOURCE REGISTER ARCHITECTURE                             │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                │
         ┌──────────────────┬───────────────────┼───────────────────┬──────────────────┐
         ▼                  ▼                   ▼                   ▼                  ▼
┌─────────────────┐┌─────────────────┐┌─────────────────┐┌─────────────────┐┌─────────────────┐
│  FIELD 1:       ││  FIELD 2:       ││  FIELD 3:       ││  FIELD 4:       ││  FIELD 5 & 6:   │
│  DOCUMENT TITLE ││  IDENTIFIER     ││  AMENDMENT      ││  STATUS & DATES ││  SCOPE & MANUAL │
│  • Official     ││  • Treaty /     ││  • Consolidated ││  • Active /     ││  • Applicability│
│    Legal Title  ││    Regulation / ││    Amendment No ││    Transition / ││  • Linked OM/CAME│
│  • Subject Area ││    ED Decision  ││  • OJ Reference ││    Superseded   ││  • Postholder   │
└─────────────────┘└─────────────────┘└─────────────────┘└─────────────────┘└─────────────────┘
```

---

## 2. The 6 Core Attributes of a Controlled Regulatory Entry

To withstand safety audits and ISO 9001 / IOSA assessments, each register record must contain six immutable fields:

| Field # | Attribute | Definition & Verification Requirement | Aviation Example |
| :---: | :--- | :--- | :--- |
| **1** | **Document Title** | Formal name of the legislative or technical act. | *Air Operations — Commercial Air Transport Operations* |
| **2** | **Legal Identifier** | Precise statutory reference, including year and enacting series. | *Commission Regulation (EU) No 965/2012, Annex IV (Part-CAT)* |
| **3** | **Version / Amendment** | Current consolidated amendment and latest amending act in the Official Journal. | *Consolidated Edition 2023 / Amended by Reg (EU) 2021/1296 (Fuel Scheme)* |
| **4** | **Effective Dates** | Publication date, Entry into force date, and Mandatory transition deadline. | *In Force: 30 Oct 2022 / Transition End: 25 Mar 2023* |
| **5** | **Regulatory Status** | Operational state: `Active`, `In-Transition`, `Superseded`, or `Revoked`. | *Active (Fully implemented)* |
| **6** | **Operational Scope** | Target aircraft fleet, operational domain, linked company manual, and nominated owner. | *Scope: A320 Fleet CAT ops<br/>Manual: OM-A Chapter 8 (Fuel Planning)<br/>Owner: Nominated Person Flight Operations* |

---

## 3. Mathematical & Algorithmic Formulation: Regulatory Change Currency & Risk Index

A compliance register is not a static database; it is a dynamic monitoring engine.

### 1. Transition Window Metric
When an amending regulation or EASA ED Decision is promulgated, the transition lead time $\Delta t_{\text{trans}}$ is:

$$\Delta t_{\text{trans}} = t_{\text{enforcement}} - t_{\text{current}} \quad \text{[days]}$$

- If $\Delta t_{\text{trans}} > 180\text{ days}$: **Normal Planning Phase** (Safety Management of Change MOC initiated).
- If $60 < \Delta t_{\text{trans}} \le 180\text{ days}$: **Implementation Phase** (Manuals revised, crew training scheduled).
- If $0 \le \Delta t_{\text{trans}} \le 60\text{ days}$: **Critical Readiness Window** (NAA submission and approval).
- If $\Delta t_{\text{trans}} < 0$: **REGULATORY BREACH (Non-Compliance Level 1/2)**.

### 2. Enterprise Regulatory Risk Index (ERRI)
Let the organisation track $N$ regulatory instruments in its register. For each instrument $i$, let:
- $w_i \in [1, 5]$ be the operational criticality weight (e.g. Part-CAT Fuel Planning = 5, Aerodrome Badge Issuance = 1).
- $S_i \in \{0, 1\}$ represent implementation currency ($S_i = 1$ if company manuals match the latest version, $0$ if outdated).
- $D_i$ be the days elapsed past the mandatory transition date (clamped to 0 if not overdue).

$$\text{ERRI} = \sum_{i=1}^{N} w_i \cdot \left[ (1 - S_i) + \min\left(10, \frac{D_i}{30}\right) \right]$$

A healthy airline maintains $\text{ERRI} = 0.0$. An $\text{ERRI} > 5.0$ indicates systemic failure of the compliance monitoring system, triggering a mandatory NAA audit finding under `ARO.GEN.350`.

---

## 4. Step-by-Step Worked Numerical Example: The EASA Fuel Scheme Transition

Consider an airline operating 25 Boeing 737-800 aircraft. EASA introduced **Regulation (EU) 2021/1296** overhauling fuel and energy management schemes (replacing generic 5% contingency fuel with Individual Fuel Schemes / Fuel Schemes with statistical monitoring).

### Baseline Register State:
- **Identifier**: `CAT.OP.MPA.180` & `AMC1 CAT.OP.MPA.180`
- **Old Standard**: Standard 5% contingency fuel or 20-minute planning minimum.
- **New Standard**: Basic Fuel Scheme / Fuel Scheme with Operational Variations requiring historical fuel consumption data collection across $\ge 2$ years.
- **Criticality Weight**: $w_{\text{fuel}} = 5.0$ (Primary safety factor).

### Transition Scenario Evaluation:
1. **Promulgation Date**: 16 December 2021.
2. **Mandatory Effective Date**: 30 October 2022 ($t_{\text{mand}} = 318\text{ days}$).
3. **Manual Updates Required**:
   - Operations Manual Part A (OM-A), Section 8.1.7 (Fuel Policy).
   - Operations Manual Part D (OM-D), Dispatcher & Pilot Training Syllabus.
   - Flight Planning System (Lido/mFlight) algorithm update.
4. **Audit Findings Analysis**:
   - If on 01 November 2022 the company manual still specifies the pre-2021 fuel calculation rules, $S_{\text{fuel}} = 0$ and $D = 2\text{ days}$:
     $$\text{ERRI} = 5.0 \times \left[ (1 - 0) + \frac{2}{30} \right] = 5.0 \times 1.067 = 5.33$$
   - **Result**: Immediate Level 1 Audit Finding. The airline cannot dispatch flights legally until emergency OM-A temporary revisions are approved by the NAA.

---

## 5. Summary & Operational Takeaway

An aviation regulatory register is the cornerstone of organizational legality. Without a verified register:
- Engineers cannot prove they are using the latest airworthiness directives or Part-145 procedures.
- Dispatchers risk computing legal fuel reserves using superseded formulas.
- Flight crews risk violating updated flight duty limits.
- Audits result in grounding findings rather than clean certifications.
