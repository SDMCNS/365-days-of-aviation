# Day 023 — Operational Guide: How to Navigate the EASA Regulatory Structure & Identify the Correct Regulatory Domain

[← Return to Lesson Plan](../../../lessons/week-04/day-023.md) | [Technical & Mathematical Walkthrough](analysis.md) | [System Topology Canvas](architecture.mermaid) | [Run Python Simulator](experiment.py)

---

## 1. Executive Summary & Operational Context

A primary reason aviation professionals struggle with European aviation law is the misconception that "regulations" are a single monolithic body of rules. In reality, the European Union Aviation Safety Agency (EASA) system is divided into **seven distinct regulatory domains**, each established by a dedicated European Commission Implementing Regulation under the overarching authority of the **Basic Regulation (EU) 2018/1139**.

When an airline pilot, maintenance engineer, safety officer, or corporate flight department encounters an operational question, the first and most critical step is **deriving the correct regulatory domain**. Looking up a rule in the wrong domain (for example, applying commercial airline Part-CAT rules to a corporate business jet operating under Part-NCC) leads to erroneous compliance procedures, wasted capital, or severe regulatory non-compliance findings.

---

## 2. The 7 Core EASA Regulatory Domains

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 BASIC REGULATION (EU) 2018/1139                                  │
│             Constitutional foundation enacted by European Parliament and Council of the EU       │
└───────────────────────────────────────────────┬──────────────────────────────────────────────────┘
                                                │
         ┌──────────────────┬───────────────────┼───────────────────┬──────────────────┐
         ▼                  ▼                   ▼                   ▼                  ▼
┌─────────────────┐┌─────────────────┐┌─────────────────┐┌─────────────────┐┌─────────────────┐
│   DOMAIN 1:     ││   DOMAIN 2:     ││   DOMAIN 3:     ││   DOMAIN 4:     ││   DOMAIN 5:     │
│    INITIAL      ││   CONTINUING    ││  AIR OPERATIONS ││    AIRCREW &    ││   AERODROMES    │
│  AIRWORTHINESS  ││  AIRWORTHINESS  ││    (AIR OPS)    ││    LICENSING    ││   & GROUND OPS  │
│  Reg 748/2012   ││  Reg 1321/2014  ││   Reg 965/2012  ││  Reg 1178/2011  ││   Reg 139/2014  │
│                 ││                 ││                 ││                 ││                 │
│ • Design (DOA)  ││ • CAMO / CAO    ││ • Part-ARO (NAA)││ • Part-FCL      ││ • Part-ADR.AR   │
│ • Type Certs    ││ • Part-M (Mgmt) ││ • Part-ORO (Org)││ • Part-MED      ││ • Part-ADR.OR   │
│ • STC & Mods    ││ • Part-ML (GA)  ││ • Part-CAT (AOC)││ • Part-CC (Cabin││ • Part-ADR.OPS  │
│ • Production    ││ • Part-145(MRO) ││ • Part-SPA(LVO) ││ • Part-DTO/ATO  ││ • RFFS & GRF    │
│   (POA)         ││ • Part-66 / 147 ││ • Part-NCC/NCO  ││ • FSTD (Sims)   ││ • Safeguarding  │
└─────────────────┘└─────────────────┘└─────────────────┘└─────────────────┘└─────────────────┘
                                                │
                                 ┌──────────────┴──────────────┐
                                 ▼                             ▼
                        ┌─────────────────┐           ┌─────────────────┐
                        │   DOMAIN 6:     │           │   DOMAIN 7:     │
                        │    ATM / ANS    │           │    DRONES &     │
                        │  Reg 2017/373   │           │      UAS        │
                        │                 │           │ Reg 2019/947    │
                        │ • ATS / ATC     │           │ • Open Category │
                        │ • CNS Providers │           │ • Specific (SORA│
                        │ • AIS / MET     │           │ • Certified Cat │
                        │ • Network Mgr   │           │ Reg 2019/945(CE)│
                        │ • Airspace(AUR) │           │ • Drone Design  │
                        └─────────────────┘           └─────────────────┘
```

### Domain Breakdown:
1. **Initial Airworthiness (Regulation (EU) No 748/2012 — Part-21)**: Governs the design and manufacturing of aircraft, engines, and parts. Defines Design Organisation Approvals (DOA), Production Organisation Approvals (POA), Type Certificates (TC), Supplemental Type Certificates (STC), and Airworthiness Directives (AD).
2. **Continuing Airworthiness (Regulation (EU) No 1321/2014 — Part-M / Part-145 / Part-CAMO)**: Governs keeping certified aircraft in an airworthy condition. Sets rules for Continuing Airworthiness Management Organisations (CAMO), Maintenance Organisations (Part-145), Certifying Staff (Part-66), and Maintenance Training (Part-147).
3. **Air Operations (Regulation (EU) No 965/2012 — Air Ops)**: Governs flight operations. Divided into sub-parts based on operation type:
   - **Part-ARO**: Authority Requirements (Oversight by NAAs)
   - **Part-ORO**: Organisation Requirements (Management systems, FTL, manuals)
   - **Part-CAT**: Commercial Air Transport (Passenger and cargo airlines)
   - **Part-SPA**: Specific Approvals (LVO, ETOPS, PBN, Dangerous Goods)
   - **Part-NCC**: Non-Commercial operations with Complex Motor-Powered Aircraft (Corporate jets)
   - **Part-NCO**: Non-Commercial operations with Other-than-complex aircraft (General aviation)
   - **Part-SPO**: Specialised Operations (Aerial photography, crop dusting, survey, skydiving)
4. **Aircrew & Licensing (Regulation (EU) No 1178/2011 — Aircrew)**: Governs flight crew licensing (Part-FCL), medical certificates (Part-MED), cabin crew attestations (Part-CC), and pilot training organisations (Part-DTO / Part-ATO).
5. **Aerodromes & Ground Operations (Regulation (EU) No 139/2014 — ADR)**: Governs airports, runway maintenance, rescue and firefighting services (RFFS), and global reporting format (GRF) for runway friction.
6. **Air Traffic Management & Navigation Services (Regulation (EU) 2017/373 — ATM/ANS)**: Governs air traffic control (ATC), communication, navigation, surveillance (CNS), aeronautical information (AIS), and weather services (MET).
7. **Unmanned Aircraft Systems (Regulations (EU) 2019/947 & 2019/945 — UAS)**: Governs drones and eVTOL operations across Open, Specific, and Certified categories.

---

## 3. The Easy Access Rules (EAR) Architecture: Hard Law vs Soft Law

EASA consolidates legislation into **Easy Access Rules (EAR)** books. Every page of an EAR document integrates four legal layers:

```
┌────────────────────────────────────────────────────────────────────────┐
│ 1. IMPLEMENTING RULE (IR) - HARD LAW                                   │
│    • Commission Regulation (e.g., CAT.OP.MPA.110)                      │
│    • Must be complied with directly. Legally binding in all 27 States. │
├────────────────────────────────────────────────────────────────────────┤
│ 2. CERTIFICATION SPECIFICATIONS (CS)                                   │
│    • EASA ED Decisions (e.g., CS-25, CS-AWO)                           │
│    • Technical standard showing design or operational compliance.      │
├────────────────────────────────────────────────────────────────────────┤
│ 3. ACCEPTABLE MEANS OF COMPLIANCE (AMC) - SOFT LAW                     │
│    • EASA ED Decision (e.g., AMC1 CAT.OP.MPA.110(a))                   │
│    • Grants "presumption of conformity". Deviation requires AltMoC.    │
├────────────────────────────────────────────────────────────────────────┤
│ 4. GUIDANCE MATERIAL (GM) - SOFT LAW                                   │
│    • EASA ED Decision (e.g., GM1 CAT.OP.MPA.110)                       │
│    • Illustrative, non-binding explanations and best practices.        │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Operational Derivation Protocol: Which Rule Governs Your Flight?

To determine the correct rule, apply this four-question derivation chain:

1. **Who is the actor?**
   - Individual pilot $\implies$ Part-FCL / Part-MED
   - Airline company $\implies$ Part-ORO & Part-CAT
   - Maintenance base $\implies$ Part-145
   - Design team $\implies$ Part-21 Subpart J (DOA)
2. **Is remuneration or hire involved?**
   - Yes $\implies$ Commercial Air Transport (`Part-CAT`) or Commercial Specialised Ops (`Part-SPO`).
   - No $\implies$ Non-Commercial (`Part-NCC` or `Part-NCO`).
3. **Is the aircraft a Complex Motor-Powered Aircraft (CMPA)?**
   - A complex aeroplane is defined under Basic Reg Article 3(9) as:
     - Maximum Takeoff Mass (MTOM) $> 5,700\text{ kg}$, or
     - Maximum Operational Passenger Seating Configuration (MOPSC) $> 19$, or
     - Certified for operation with a minimum crew of at least 2 pilots, or
     - Equipped with turbojet engine(s) or more than one turboprop engine.
   - If Non-Commercial + CMPA $\implies$ **Part-NCC** (Must implement an SMS and declare operations to the NAA).
   - If Non-Commercial + Non-CMPA (e.g., Cessna 172) $\implies$ **Part-NCO** (Simplified general aviation rules).
4. **Does the operation require a Specific Approval?**
   - Low Visibility (CAT II/III Autoland) $\implies$ **Part-SPA.LVO**
   - Extended Range Twin Engine Operations $\implies$ **Part-SPA.ETOPS**
   - Dangerous Goods $\implies$ **Part-SPA.DG**
   - Performance-Based Navigation $\implies$ **Part-SPA.PBN**

---

## 5. Practical Hands-On Exercise & Verification

Run the interactive Python domain classifier and compliance burden simulator:
```bash
python learned/week-04/day-023/experiment.py
```

Observe how:
1. Shifting an aircraft operation from private leisure (`Part-NCO`) to commercial passenger transport (`Part-CAT`) instantly multiplies the applicable regulatory provisions by over $300\%$.
2. Authorizing a cross-domain operation like Low Visibility Autoland (CAT IIIb) requires intersecting six EASA domains simultaneously.
3. Attempting to run a specialized commercial survey under Part-NCO triggers an illegal operation finding and grounding.
