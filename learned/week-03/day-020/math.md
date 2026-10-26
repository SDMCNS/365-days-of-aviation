# Day 020 — Technical Walkthrough: Integrating International Standards, European Law, and Local Aerodrome Operating Arrangements

[← Return to Lesson Guide](README.md) | [System Topology Canvas](architecture.mermaid) | [Run Python Simulator](experiment.py)

---

## 1. The Tripartite Regulatory Stack

A commercial flight is never governed by a single monolithic rulebook. Instead, every operational decision represents the intersection of three distinct layers of legal authority:

$$\text{International Baseline (ICAO)} \quad \subset \quad \text{Regional Harmonisation (EASA / EU)} \quad \subset \quad \text{Local Operating Arrangements (AIP / ADR)}$$

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    TIER 1: INTERNATIONAL BASELINE (ICAO)                │
│   • ICAO Doc 7300 & Annexes 1-19 (Diplomatic Consensus & SARPs)         │
│   • Establishes universal minimums: airspace sovereignty, ICAO phrase-  │
│     ology, altimetry, basic aircraft airworthiness passports.           │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                 TIER 2: REGIONAL HARMONISATION (EASA / EU)              │
│   • Reg (EU) 2018/1139 & Reg (EU) 965/2012 (Directly Applicable Hard Law)│
│   • Single European Aviation Market: Standardised FTL, Part-CAT,         │
│     EU 261 passenger rights, EASA Part-21 Type Certification.           │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│              TIER 3: LOCAL OPERATING ARRANGEMENTS (AIP / ADR)           │
│   • Aeronautical Information Publication (AIP Section AD 2)             │
│   • Site-specific constraints: Airport night flight curfews, steep       │
│     approaches (e.g. London City 5.5°), noise abatement corridors,      │
│     local runway friction limits, and stand taxiing restrictions.       │
└─────────────────────────────────────────────────────────────────────────┘
```

An operation is legally permissible if and only if it satisfies all three tiers simultaneously. A flight that complies with ICAO and EASA regulations will still be grounded or fined if it violates a local municipal noise curfew or aerodrome obstacle limitation.

---

## 2. Comparative Matrix: The Three Regulatory Tiers

| Feature | Tier 1: International (ICAO) | Tier 2: European Union (EASA) | Tier 3: Local Aerodrome (AIP AD 2) |
| :--- | :--- | :--- | :--- |
| **Jurisdictional Scope** | Global (193 Member States) | Regional (27 EU States + EFTA) | Local (Single Airport / FIR sector) |
| **Legal Nature** | Non-self-executing SARPs | Directly applicable Hard Law | Binding via Aerodrome Conditions of Use |
| **Rulebook Example** | ICAO Annex 6 (Operation of Aircraft) | Regulation (EU) 965/2012 (Air Ops) | AIP UK AD 2.EGLC (London City) |
| **Approach Minimums** | Standard ILS Cat I (200 ft / 550 m) | Part-SPA.LVO (Cat IIIb / 75 m) | Steep Approach 5.5° glidepath required |
| **Noise Constraints** | ICAO Annex 16 Chapter 4 / 14 | Regulation (EU) 598/2014 | Strict Night Curfew (23:00–05:00) |
| **Enforcement Body** | Sovereign States via Article 33 | European Commission & National NCAs| Aerodrome Operator & Local Police / Courts |

---

## 3. Quantitative & Analytical Formulations

### 1. Multi-Tier Feasibility Intersection
Let an operational parameter profile be vector $\mathbf{x} = [t_{\text{arrival}}, \text{LDA}, \theta_{\text{glidepath}}, L_{\text{noise}}]$. The flight is authorized if:

$$\mathbf{x} \in \mathcal{C}_{\text{ICAO}} \cap \mathcal{C}_{\text{EASA}} \cap \mathcal{C}_{\text{Local}}$$

where:
- $\mathcal{C}_{\text{ICAO}}$: Basic airworthiness, crew licensing, and international dispatch.
- $\mathcal{C}_{\text{EASA}}$: Required runway landing distance factor:
  $$\text{LDA} \ge \text{ALDR} \times 1.67 \quad (\text{Dry Turbojet Factor under CAT.POL.A.230})$$
- $\mathcal{C}_{\text{Local}}$: Site-specific restrictions:
  - Curfew window: $t_{\text{arrival}} \notin [t_{\text{curfew\_start}}, t_{\text{curfew\_end}}]$
  - Noise quota: $L_{\text{noise}} \le L_{\text{max\_EPNdB}}$
  - Approach slope: $\theta_{\text{approach}} = \theta_{\text{published}}$

### 2. Steep Approach Performance Penalty Formulation (London City EGLC)
At a standard aerodrome, the ILS glidepath is $\theta_0 = 3.0^\circ$. At obstacle-restricted aerodromes like London City (EGLC), the published glidepath is $\theta = 5.5^\circ$.

Under **EASA Part-SPA.SPA.100 (Steep Approach Operations)**, aircraft must hold special AFM certification and flight crews must complete specialized simulator training. The steeper descent angle increases the vertical descent rate ($V_z = V_{\text{TAS}} \sin \theta$), requiring a prolonged aerodynamic flare and increasing the required landing distance:

$$\text{LDA}_{\text{required}} = \text{Unfactored Landing Dist} \times 1.67 \times \left[ 1 + \kappa_{\text{steep}} (\theta - 3.0^\circ) \right]$$

where $\kappa_{\text{steep}} \approx 0.08\text{ per degree}$ of glidepath increase.

---

## 4. Step-by-Step Worked Numerical Example: Geneva (LSGG) to London City (EGLC)

Consider an Airbus A220-100 operating Swiss flight LX466 from Geneva to London City:
- **Aircraft Data**:
  - Unfactored Dry Landing Distance: $820\text{ m}$
  - Approach Speed: $V_{\text{APP}} = 125\text{ KIAS}$
  - Noise Rating: Flyover 82.4 EPNdB (ICAO Annex 16 Chapter 14 compliant)
- **Destination Data (London City AIP AD 2.EGLC)**:
  - Landing Distance Available (Runway 27): $\text{LDA} = 1,199\text{ m}$
  - Published Glidepath: $\theta = 5.5^\circ$
  - Saturday Operational Curfew: Airport closes strictly at **12:30 UTC** until Sunday 12:30 UTC.

### 1. Performance & Clearance Trace across the 3 Tiers
1. **Tier 1 (ICAO)**: Aircraft holds valid Certificate of Airworthiness; crew holds ICAO Annex 1 licenses; noise satisfies Annex 16 $\implies \mathbf{ICAO\ Compliant}$.
2. **Tier 2 (EASA)**:
   - Steep approach factor: $1 + 0.08 \times (5.5 - 3.0) = 1 + (0.08 \times 2.5) = 1.20$.
   - Required factored landing distance:
     $$\text{LDA}_{\text{required}} = 820\text{ m} \times 1.67 \times 1.20 = 1,369.4 \times 1.20 = 1,164.3\text{ m}$$
   - Margin check: $\text{LDA}_{\text{available}} (1,199\text{ m}) - \text{LDA}_{\text{required}} (1,164.3\text{ m}) = +34.7\text{ m} \implies \mathbf{EASA\ Compliant}$.
   - Airline holds EASA Specific Approval `SPA.SPA.100` for London City steep approach.
3. **Tier 3 (Local Operating Arrangement)**:
   - Scheduled Arrival: 12:05 UTC.
   - Delay accrued in cruise: +15 minutes $\implies$ Estimated touchdown: **12:20 UTC**.
   - Curfew limit: $12:20\text{ UTC} < 12:30\text{ UTC} \implies \mathbf{Local\ Curfew\ Satisfied}$.
   - Outcome: **Cleared for landing on Runway 27**.

---

## 5. Adversarial Curfew Breach: Frankfurt Night Curfew

What happens if a Lufthansa flight to Frankfurt is delayed by 30 minutes, arriving at the final approach fix at **23:04 local**?
- Frankfurt operates a strict municipal ban on scheduled flights between **23:00 and 05:00 local**, established under German administrative court rulings and published in AIP Germany `EDDF AD 2.21`.
- The flight crew cannot plead that the aircraft is airworthy (ICAO) or that the crew has legal duty hours remaining (EASA).
- Frankfurt Tower **refuses landing clearance**.
- Mandatory Action: Aircraft must immediately break off approach and divert to Cologne/Bonn (EDDK) or Hannover, costing the airline over €65,000 in hotel accommodation, repositioning ferry flights, and municipal violation fines.
