# Day 023 — Technical Walkthrough: Navigating the EASA Regulatory Structure & Domain Derivation

[← Return to Lesson Guide](README.md) | [System Topology Canvas](architecture.mermaid) | [Run Python Simulator](experiment.py)

---

## 1. The 7 Pillars of the EASA Regulatory System

Under the **Basic Regulation (EU) 2018/1139**, the European Union Aviation Safety Agency (EASA) exercises unified regulatory jurisdiction across seven discrete operational domains. Navigating EASA regulations requires an engineer, safety manager, or flight operations specialist to pinpoint the governing domain before consulting specific implementing rules:

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                             BASIC REGULATION (EU) 2018/1139                                      │
│        (Enacted by European Parliament & Council — Supreme Primary Aviation Law in the EU)       │
└───────────────────────────────────────────────┬──────────────────────────────────────────────────┘
                                                │
         ┌──────────────────┬───────────────────┼───────────────────┬──────────────────┐
         ▼                  ▼                   ▼                   ▼                  ▼
┌─────────────────┐┌─────────────────┐┌─────────────────┐┌─────────────────┐┌─────────────────┐
│   DOMAIN 1:     ││   DOMAIN 2:     ││   DOMAIN 3:     ││   DOMAIN 4:     ││   DOMAIN 5:     │
│    INITIAL      ││   CONTINUING    ││  AIR OPERATIONS ││    AIRCREW &    ││   AERODROMES    │
│  AIRWORTHINESS  ││  AIRWORTHINESS  ││    (AIR OPS)    ││    LICENSING    ││   & GROUND OPS  │
│  Reg 748/2012   ││  Reg 1321/2014  ││   Reg 965/2012  ││  Reg 1178/2011  ││   Reg 139/2014  │
│ • Part-21 (DOA) ││ • Part-M (CAMO) ││ • Part-ARO / ORO││ • Part-FCL      ││ • Part-ADR.AR   │
│ • Type Cert(TC) ││ • Part-ML (GA)  ││ • Part-CAT (AOC)││ • Part-MED      ││ • Part-ADR.OR   │
│ • STC & Repairs ││ • Part-145(MRO) ││ • Part-SPA(LVO) ││ • Part-CC (Crew)││ • Part-ADR.OPS  │
│ • Part-21 (POA) ││ • Part-66 / 147 ││ • Part-NCC/NCO  ││ • Part-DTO/ATO  ││ • RFFS & GRF    │
└─────────────────┘└─────────────────┘└─────────────────┘└─────────────────┘└─────────────────┘
                                                │
                                 ┌──────────────┴──────────────┐
                                 ▼                             ▼
                        ┌─────────────────┐           ┌─────────────────┐
                        │   DOMAIN 6:     │           │   DOMAIN 7:     │
                        │    ATM / ANS    │           │    DRONES &     │
                        │  Reg 2017/373   │           │      UAS        │
                        │ • ATS / CNS     │           │ Reg 2019/947    │
                        │ • AIS / MET     │           │ • Open / Specific│
                        │ • Network Mgr   │           │ • Certified     │
                        │ • Airspace(AUR) │           │ Reg 2019/945(CE)│
                        └─────────────────┘           └─────────────────┘
```

---

## 2. Anatomy of the EASA "Easy Access Rules" (EAR)

Because European aviation law is published across dozens of amending Official Journals (OJ), EASA consolidates primary legislation, implementing acts, and soft law into **Easy Access Rules (EAR)**. Understanding the anatomy of an EAR provision is critical for legal traceability:

| Layer | Legal Form | Enacting Body | Nature & Binding Status | Example Identifier |
| :--- | :--- | :--- | :--- | :--- |
| **Basic Regulation** | Regulation | EU Parliament & Council | Hard Law (Directly applicable) | Reg (EU) 2018/1139 Art 30 |
| **Implementing Rule (IR)** | Commission Regulation | European Commission | Hard Law (Directly applicable) | `CAT.OP.MPA.110` (Aerodrome Operating Minima) |
| **Certification Specs (CS)** | EASA ED Decision | EASA Executive Director | Standard for Design/Ops | `CS-AWO.100` (All Weather Operations) |
| **Acceptable Means (AMC)** | EASA ED Decision | EASA Executive Director | Soft Law (Presumption of conformity) | `AMC1 CAT.OP.MPA.110(a)` |
| **Guidance Material (GM)** | EASA ED Decision | EASA Executive Director | Soft Law (Non-binding explanation) | `GM1 CAT.OP.MPA.110` |

### Key Rule of Interpretation:
- You cannot be prosecuted or fined for violating **GM**.
- You can deviate from **AMC** only if you submit an **Alternative Means of Compliance (AltMoC)** under `ORO.GEN.120` demonstrating equivalent safety, approved by your National Aviation Authority (NAA).
- You **cannot** deviate from an **Implementing Rule (IR)** without a formal Article 71 exemption granted by the European Commission.

---

## 3. Mathematical & Algorithmic Derivation: The EASA Domain Decision Function

To determine the governing regulatory domain for any operational or engineering question, we formulate the **Domain Classification Function**:

$$\mathcal{D}(A, T, C, S) \to \{\text{Part-21}, \text{Part-145}, \text{Part-CAMO}, \text{Part-CAT}, \text{Part-NCC}, \text{Part-NCO}, \text{Part-SPO}, \dots\}$$

Where:
- $A \in \{\text{Natural Person}, \text{Organisation}, \text{Manufacturer}, \text{Service Provider}\}$ (The Actor)
- $T \in \{\text{Commercial}, \text{Non-Commercial}, \text{Specialised Aerial Work}\}$ (The Operation Type)
- $C \in \{\text{Complex Motor-Powered Aircraft (CMPA)}, \text{Non-Complex Aircraft}, \text{UAS}\}$ (The Aircraft Class)
- $S \in \{\text{Design}, \text{Maintenance}, \text{Flight Operations}, \text{Licensing}, \text{Ground/Airspace}\}$ (The Subject Domain)

### Classification Rules Matrix:
1. **Air Operations Domain Selection**:
   $$\text{Rule}(T, C) = \begin{cases}
   \text{Part-CAT} & \text{if } T = \text{Commercial Air Transport} \\
   \text{Part-SPO} & \text{if } T = \text{Specialised Operations (Survey, Parachute, Towing)} \\
   \text{Part-NCC} & \text{if } T = \text{Non-Commercial} \land C = \text{CMPA} \\
   \text{Part-NCO} & \text{if } T = \text{Non-Commercial} \land C \neq \text{CMPA}
   \end{cases}$$

2. **Continuing Airworthiness Maintenance Assignment**:
   $$\text{MRO}(T, C) = \begin{cases}
   \text{Part-CAMO} + \text{Part-145} & \text{if } T = \text{Commercial} \lor C = \text{CMPA} \\
   \text{Part-CAO} \lor \text{Part-M Subpart F} & \text{if } T = \text{Non-Commercial} \land C = \text{Non-Complex (Part-ML)}
   \end{cases}$$

---

## 4. Multi-Domain Operational Trace: Low Visibility Operations (LVO)

When an airline decides to conduct **CAT IIIb autoland** operations in $75\text{ m}$ Runway Visual Range (RVR), the approval cuts across **six separate EASA domains simultaneously**. The regulatory compliance burden $\mathcal{B}_{\text{total}}$ is the sum of requirements across all intersected domains:

$$\mathcal{B}_{\text{total}} = \sum_{d \in \text{Domains}} \left( N_{\text{IR}, d} + N_{\text{AMC}, d} + N_{\text{CS}, d} \right)$$

### The 6-Domain Trace for CAT IIIb Operations:
1. **Initial Airworthiness (Part-21)**: Aircraft type certificate must include approval under **`CS-AWO` (Certification Specifications for All-Weather Operations)** for fail-operational autoland systems.
2. **Continuing Airworthiness (Part-145 / Part-CAMO)**: Aircraft must be maintained under a specific **Low Visibility Maintenance Programme** (`Part-M.A.302`), requiring daily sensor calibrations and CAT III status sign-off in the Aircraft Technical Log.
3. **Air Operations (Part-SPA)**: The airline must hold a Specific Approval for Low Visibility Operations issued under **`SPA.LVO.100`** and documented on its Air Operator Certificate (AOC) Operations Specifications.
4. **Air Operations General (Part-CAT)**: Cockpit procedures must comply with **`CAT.OP.MPA.110`** (Aerodrome operating minima) and **`CAT.OP.MPA.305`** (Commencement and continuation of approach).
5. **Aircrew & Licensing (Part-FCL)**: Both pilots must hold an instrument rating endorsed for CAT IIIb, with recurrent simulator training and Low Visibility line checks under **`Part-ORO.FC.200`** every 6 months.
6. **Aerodrome Operations (Part-ADR)**: The airport must declare Low Visibility Procedures (LVP) in force under **`ADR.OPS.B.045`**, guaranteeing CAT II/III ILS sensitive area protection and surface movement radar surveillance.

---

## 5. Worked Numerical Example: Multi-Domain Compliance Metric

An airline introducing a fleet of 10 new aircraft for CAT IIIb operations must conduct a formal gap analysis across the 6 domains:

| Domain | EASA Reference | Required IR Provisions | Required AMC Provisions | Target Verification Audit Days |
| :--- | :--- | :---: | :---: | :---: |
| Initial Airworthiness | CS-AWO / Part-21 | 14 | 22 | 5 |
| Continuing Airworthiness | Part-CAMO / Part-145 | 18 | 35 | 8 |
| Air Ops Specific Approvals | Part-SPA.LVO | 12 | 28 | 6 |
| Air Ops Commercial | Part-CAT & Part-ORO | 24 | 46 | 10 |
| Flight Crew Training | Part-FCL / Part-ORO.FC | 16 | 30 | 7 |
| Aerodrome Interface | Part-ADR.OPS | 8 | 12 | 3 |
| **TOTAL** | — | **92 IRs** | **173 AMCs** | **39 Audit Days** |

If the airline opts to create an **Alternative Means of Compliance (AltMoC)** for flight crew recurrent simulator intervals under `ORO.GEN.120`, the approval risk score $R_{\text{alt}}$ is:

$$R_{\text{alt}} = \text{Risk Baseline} \times \left(1 + \frac{\text{Deviation Severity}}{\text{Safety Margin}}\right) = 1.0 \times \left(1 + \frac{0.40}{0.80}\right) = 1.50$$

Requiring formal mathematical risk assessment, NAA evaluation, and notification to EASA within 30 days.

---

## 6. Summary & Key Takeaways

1. **Always classify by domain first**: Never jump into Part-CAT without checking if the aircraft is complex or if the operation is specialized aerial work.
2. **Know Hard Law from Soft Law**: Implementing Rules bind by law; AMC provides safe harbor; GM explains intent.
3. **Complex operations are cross-domain**: Advanced capabilities like CAT III autoland, ETOPS, or PBN are not just "pilot rules" — they require simultaneous airworthiness, maintenance, aerodrome, and operational certifications.
