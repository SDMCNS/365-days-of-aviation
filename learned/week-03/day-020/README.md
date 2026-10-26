# Day 020 — The Three-Tier Reality: International Standards, European Law, and Local Aerodrome Rules

[← Return to Lesson Plan](../../../lessons/week-03/day-020.md) | [📊 Technical Walkthrough](analysis.md) | [System Topology Canvas](architecture.mermaid) | [Run Python Simulator](experiment.py)

---

## 1. Executive Summary: The Tripartite Regulatory Stack

When a flight dispatcher plans a flight or an airline captain sets the flaps for landing, they are navigating a multi-layered legal puzzle. No single document contains all the rules. Instead, every commercial flight operates at the intersection of three distinct tiers of aviation governance:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    TIER 1: INTERNATIONAL BASELINE (ICAO)                │
│   • Universal global baseline negotiated by 193 nations in Montreal     │
│   • Airspace sovereignty, standard phraseology, basic airworthiness     │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                 TIER 2: REGIONAL HARMONISATION (EASA / EU)              │
│   • Directly applicable hard law across the Single European Sky         │
│   • Part-CAT commercial air transport rules, FTL, EU 261 passenger rights│
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│              TIER 3: LOCAL OPERATING ARRANGEMENTS (AIP / ADR)           │
│   • Site-specific operational reality published in AIP Section AD 2     │
│   • Night curfews, 5.5° steep approaches, noise fines, runway limits    │
└─────────────────────────────────────────────────────────────────────────┘
```

The golden rule of aviation operations is **simultaneous intersection**:
> An aircraft cannot operate simply because it complies with ICAO and EASA rules. It must also comply with the local bylaws, runway physics, and noise curfews of the specific municipal airport where it intends to land.

---

## 2. Real-World Case Studies: When Local Rules Dominate

### 1. London City Airport (EGLC): The Steep Approach Challenge
- **International Baseline (ICAO)**: Recommends standard 3.0° instrument approach glidepaths.
- **European Regulation (EASA)**: Mandates dry runway landing distance factoring of $1.67\times$ under `CAT.POL.A.230` and requires a Specific Approval (`SPA.SPA.100`) for non-standard approaches.
- **Local Operating Arrangement (AIP UK AD 2.EGLC)**:
  - Due to skyscrapers in Canary Wharf and the Docklands, London City requires a **5.5° glidepath**—nearly double the standard angle.
  - Aircraft must possess specialized fly-by-wire or spoiler flight control certification to maintain a safe descent rate without accelerating.
  - The runway is only $1,199\text{ meters}$ long.
  - **Weekend Curfew**: The airport strictly shuts down from Saturday 12:30 UTC to Sunday 12:30 UTC to preserve quality of life for local residents. A flight arriving at 12:31 UTC will be turned away.

### 2. Frankfurt Airport (EDDF): The Absolute Night Curfew
- **European Regulation (EASA)**: Allows flight crews with remaining duty hours to operate flights around the clock.
- **Local Operating Arrangement (AIP Germany EDDF AD 2.21)**:
  - German administrative courts instituted a zero-tolerance ban on scheduled jet operations between **23:00 and 05:00 local time**.
  - If a flight is delayed and touches down at 23:01, it violates municipal environmental law.
  - Frankfurt Tower will actively **refuse landing clearance** to delayed flights approaching at 23:02, forcing immediate diversions to Cologne/Bonn or Hannover at massive operational expense.

---

## 3. Comparative Summary: The Three Legal Tiers

| Attribute | Tier 1: ICAO Baseline | Tier 2: EASA / EU Law | Tier 3: Local Aerodrome Arrangement |
| :--- | :--- | :--- | :--- |
| **Geographic Scope** | Worldwide (193 States) | 27 EU States + EFTA | Single Aerodrome / City |
| **Primary Document** | ICAO Annexes (e.g. Annex 6, 14, 16) | Regulation (EU) 965/2012 (Air Ops) | National AIP Section AD 2 |
| **Enforcement Mechanism** | Bilateral recognition / Article 33 | NCA audits & European Court of Justice| Airport Operating License & Local Courts |
| **Flexibility** | High (State Differences Art. 38) | Medium (AltMoC under ORO.GEN.120) | Low (Strict municipal curfews / physical terrain) |

---

## 4. The Practical Integration: Dispatching Under All Three Layers

When an airline dispatcher prepares an Operational Flight Plan (OFP):
1. **ICAO Check**: Verify that the destination state has not filed Article 38 differences that invalidate equipment (e.g. 8.33 kHz radio channel spacing).
2. **EASA Check**: Verify that the airline holds the required Specific Approvals (e.g. `SPA.LVO` or `SPA.SPA.100`), crew duty hours are compliant under `ORO.FTL`, and runway performance margins satisfy Part-CAT.
3. **Local AIP Check**: Verify current NOTAMs, active Low Visibility Procedures, noise quota points (Quota Count QC system), and ensure arrival ETA clears the local airport curfew by at least 30 minutes.

---

## 5. Practical Deliverable & Verification

Run the interactive Python simulation script for Day 020 to evaluate multi-tier compliance, calculate steep approach landing distances, check noise quotas, and stress-test a night curfew breach:

```bash
python learned/week-03/day-020/experiment.py
```
