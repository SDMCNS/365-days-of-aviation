# Day 015 — Technical Walkthrough: European Aviation Governance Architecture & Competence Division

[← Return to Lesson Guide](README.md) | [System Topology Canvas](architecture.mermaid) | [Run Python Simulator](experiment.py)

---

## 1. The Institutional Quadrilateral of European Civil Aviation

Unlike the United States—where a single federal agency (the Federal Aviation Administration, FAA) writes rules, inspects aircraft, licenses pilots, operates air traffic control, and certifies airports—the European Union distributes civil aviation governance across four distinct institutional levels:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                 EUROPEAN PARLIAMENT & COUNCIL OF THE EU                 │
│         Primary Legislation: EASA Basic Regulation (EU) 2018/1139       │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (Empowerment / TFEU Art. 290 & 291)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    EUROPEAN COMMISSION (DG MOVE)                        │
│     Adopts Hard Law: Delegated & Implementing Regulations (e.g. Part-CAT)│
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (Opinions & Technical Support)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│            EASA — EUROPEAN UNION AVIATION SAFETY AGENCY (Cologne)       │
│  • Rulemaking Opinions & CS / AMC / GM (Soft Law)                       │
│  • Direct Competence: Aircraft Type Certification (TC/STC, Part-21)     │
│  • Direct Competence: Design Organisations (DOA) & Third Country Ops    │
│  • Standardisation Oversight: Audits NCAs of all 27 EU Member States    │
└──────────────────┬───────────────────────────────────▲──────────────────┘
                   │                                   │ (Audits & SCI)
                   │ (Directives & Standardised Rules) │
                   ▼                                   │
┌──────────────────────────────────────────────────────┴──────────────────┐
│             NATIONAL COMPETENT AUTHORITIES (NCAs / NAAs)                │
│    (e.g., DGAC France, LBA Germany, ENAC Italy, AESA Spain)             │
│  • Operations: Issue & Oversee Air Operator Certificates (AOC)          │
│  • Maintenance: Certify Part-145 Repair Stations & Part-CAMO            │
│  • Personnel: Issue Flight Crew Licenses (Part-FCL) & ATO Approvals     │
│  • Aerodromes: Certify Commercial Airports (ADR) & National ANSPs       │
└─────────────────────────────────────────────────────────────────────────┘
```

The foundational statutory anchor is **Regulation (EU) 2018/1139 (The EASA Basic Regulation)**.

---

## 2. Division of Competence: Direct Agency vs National Authority

A critical operational distinction in European aviation law is determining **who holds competent authority** for a given entity:

| Domain | Competent Authority | Governing EU Implementing Regulation | Legal Nature |
| :--- | :--- | :--- | :--- |
| **Aircraft Design & Type Certificates** | **EASA (Direct)** | Regulation (EU) 748/2012 (Part-21) | Direct Certification |
| **Design Organisation Approvals (DOA)** | **EASA (Direct)** | Regulation (EU) 748/2012 Subpart J | Direct Oversight |
| **Air Operator Certificates (AOC)** | **NCA (National)** | Regulation (EU) 965/2012 (Air Ops) | National Oversight |
| **Continuing Airworthiness (CAMO/145)** | **NCA (National)** | Regulation (EU) 1321/2014 (Part-M/145)| National Oversight |
| **Flight Crew Licensing (FCL)** | **NCA (National)** | Regulation (EU) 1178/2011 (Part-FCL) | National Oversight |
| **Third-Country Operators (TCO)** | **EASA (Direct)** | Regulation (EU) 452/2014 (Part-TCO) | Direct Authorization |
| **Major Commercial Aerodromes** | **NCA (National)** | Regulation (EU) 139/2014 (ADR) | National Oversight |
| **Pan-European ANSPs (e.g. MUAC)** | **EASA (Direct)** | Regulation (EU) 2018/1139 Art. 62 | Direct Oversight |

---

## 3. Quantitative & Analytical Formulation: EASA Standardisation

Under **Commission Implementing Regulation (EU) No 628/2013**, EASA conducts periodic **Standardisation Inspections** of every National Competent Authority (NCA) to ensure that EU aviation regulations are interpreted and enforced uniformly across all Member States.

### 1. Classification of Findings
Findings identified during an NCA inspection are classified by severity:
- **Class C (Observation)**: Numerical observation or procedural imperfection that does not constitute a non-compliance with EU law.
- **Class D (Non-Compliance)**: Direct failure to comply with an EU regulation or standard. Requires an agreed **Corrective Action Plan (CAP)** submitted within $\le 90$ days.
- **Class G (Immediate Safety Finding)**: Severe non-compliance posing an immediate and direct risk to aviation safety. Requires immediate provisional safety measures within $\le 15$ days.

### 2. Standardisation Compliance Index ($SCI$)
The performance of a National Competent Authority is evaluated via a weighted compliance metric:

$$SCI = 100\% - \left[ \frac{w_C N_C + w_D N_D + w_G N_G}{N_{\text{domain\_checkpoints}}} \times 100\% \right]$$

where typical audit penalty weights are:
- $w_C = 0.05$ (Observation)
- $w_D = 0.30$ (Standard Non-Compliance)
- $w_G = 1.00$ (Immediate Safety Finding)

### 3. The Article 70 Safeguard Clause Threshold
Under **Articles 67 and 70 of Regulation (EU) 2018/1139**, certificates issued by any EU NCA are granted automatic **mutual recognition** across the other 26 Member States.

However, if an NCA's $SCI$ drops below a critical threshold ($\tau_{\text{safeguard}} = 70\%$) or has unmitigated Class G findings:
$$\text{Safeguard Trigger} = \mathbb{I}\left( SCI < 70\% \lor N_{G,\text{unresolved}} > 0 \right)$$

If triggered, the European Commission, upon EASA's recommendation, initiates **Infringement Procedures under Article 258 TFEU** and may suspend mutual recognition of certificates issued by that national authority.

---

## 4. Step-by-Step Worked Numerical Example: Auditing an NCA

Consider a Standardisation Inspection conducted by EASA on the **Civil Aviation Authority of Member State X**:
- Total Audit Checkpoints Evaluated: $N_{\text{checkpoints}} = 120$ across Air Operations (OPS) and Airworthiness (AIR).
- Findings Recorded:
  - Class C (Observations): $N_C = 8$
  - Class D (Non-Compliances): $N_D = 6$ (e.g., flight time limitation oversight intervals exceeded)
  - Class G (Urgent Safety Findings): $N_G = 1$ (e.g., an airline operating under an unapproved MEL revision)

### 1. Calculation of Penalty & SCI
- Total Weighted Penalty:
  $$\text{Penalty} = (0.05 \times 8) + (0.30 \times 6) + (1.00 \times 1) = 0.40 + 1.80 + 1.00 = 3.20$$
- Standardisation Compliance Index:
  $$SCI = 100\% - \left( \frac{3.20}{120} \times 100\% \right) = 100\% - 2.67\% = 97.33\%$$

### 2. Operational Decision & Timeline
- Although the overall $SCI = 97.33\%$ is high, the presence of **$N_G = 1$** triggers the urgent safeguard clock:
  - **15-Day Limit**: NCA must issue an emergency operational directive grounding the affected operation or enforcing the correct MEL.
  - **90-Day Limit**: NCA must submit a comprehensive root-cause analysis and CAP for the 6 Class D findings.
- If the NCA rectifies the Class G finding within 15 days, mutual recognition under Article 67 remains intact.
