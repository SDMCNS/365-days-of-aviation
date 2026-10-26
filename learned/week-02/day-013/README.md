# Day 013 — From Global Standards to Cockpit Action: Certificates, OpSpecs, and Local Procedures

[← Return to Lesson Plan](../../../lessons/week-02/day-013.md) | [📊 Technical Walkthrough](analysis.md) | [System Topology Canvas](architecture.mermaid) | [Run Python Simulator](experiment.py)

---

## 1. Executive Summary & The Operational Translation Spine

When an international treaty like the **Chicago Convention** establishes global standards in Montreal, it creates legal duties for sovereign governments—not for an airline captain flaring an airliner over an icy runway in thick fog. 

How does an international Standard adopted in **ICAO Annex 6 (Operation of Aircraft)** or **Annex 8 (Airworthiness)** actually control the throttles, autopilots, and decisions on a commercial flight deck?

It does so through a strict, multi-tiered **Operational Translation Spine**:

```
┌─────────────────────────────────────────────────────────────┐
│                 ICAO CHICAGO CONVENTION                     │
│       Annex 6 (Flight Operations) & Annex 8 (Airworthiness) │
└──────────────────────────────┬──────────────────────────────┘
                               │ (Transposition into Law)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│              REGIONAL / NATIONAL REGULATION                 │
│      EASA Air Ops (Part-CAT / Part-SPA) or FAA 14 CFR       │
└──────────────────────────────┬──────────────────────────────┘
                               │ (Oversight & Certification)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│             AIR OPERATOR CERTIFICATE (AOC)                  │
│       Operations Specifications (OpSpecs / Part-SPA)        │
│   • ETOPS / EDTO  • Low Visibility (CAT II/III)  • RVSM     │
└──────────────┬───────────────────────────────┬──────────────┘
               │                               │
               ▼                               ▼
┌─────────────────────────────┐ ┌─────────────────────────────┐
│     AIRCRAFT READINESS      │ │      CREW QUALIFICATION     │
│ • Cert of Airworthiness     │ │ • Type Rating on Aircraft   │
│ • AFM Limits & STCs         │ │ • Recurrent Sim Evaluation  │
│ • Minimum Equipment List    │ │ • Recent Experience Checks │
└──────────────┬──────────────┘ └──────────────┬──────────────┘
               │                               │
               └───────────────┬───────────────┘
                               │ (Flight Execution)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│              LOCAL AERODROME SAFEGUARDS (AIP)               │
│ • Low Visibility Procedures (LVP) Active                    │
│ • ILS Critical & Sensitive Areas Protected                  │
│ • CAT II/III Hold Short Lines Enforced                      │
└─────────────────────────────────────────────────────────────┘
```

Without every single link in this chain intact, an airline cannot legally or safely conduct high-consequence operations.

---

## 2. The Core Legal Instruments

### 1. The Air Operator Certificate (AOC)
Issued by the National Aviation Authority (State of the Operator) under ICAO Annex 6, Chapter 4. The AOC certifies that the operator has the organization, staffing, flight operations structure, maintenance system, and safety management system (SMS) necessary for safe commercial air transport.

### 2. Operations Specifications (OpSpecs)
The AOC is only half the story. Attached directly to the AOC is the **Operations Specifications (OpSpecs)**. The OpSpecs is the regulatory passport of the airline, explicitly listing what the airline is permitted to do, and under what conditions:
- **Low Visibility Operations (LVO)**: Specific authorization to conduct Category II, Category IIIa, or Category IIIb instrument approaches with decision heights below 100 feet.
- **Extended Diversion Time Operations (EDTO / ETOPS)**: Specific authorization for twin-engine aircraft to fly 120, 180, 240, or 370 minutes away from an alternate airport.
- **Reduced Vertical Separation Minimum (RVSM)**: Specific authorization to fly between Flight Level 290 and 410 with 1,000 feet vertical separation instead of 2,000 feet.
- **Performance-Based Navigation (PBN)**: RNP 4 (oceanic), RNP 1 (terminal airspace), and RNP AR APCH (Authorisation Required curved approaches down to 0.1 NM).
- **Dangerous Goods**: Authorization to carry classified hazardous cargo under ICAO Annex 18 and Technical Instructions (Doc 9284).

### 3. The 4-Pillar Operational Authorization Rule
For any specialized flight operation (e.g. landing in zero visibility or crossing the Pacific on two engines), **four simultaneous pillars** must be verified:

$$\text{Operational Clearance} = \text{Airline OpSpec} \times \text{Aircraft AFM/MEL} \times \text{Flight Crew Qualification} \times \text{Local Aerodrome Safeguards}$$

If any single element is missing (value = 0), the operation is **strictly prohibited by law**:
1. **The Airline**: Does the OpSpec explicitly authorize this specific category?
2. **The Aircraft**: Is this specific tail number airworthy, certified in the Aircraft Flight Manual (AFM), and free from disqualifying Minimum Equipment List (MEL) defects (e.g. both autopilot servos working)?
3. **The Flight Crew**: Are both pilots qualified, simulator-checked within the last 6 months, and current for low-visibility autolands?
4. **The Local Aerodrome**: Has the airport declared **Low Visibility Procedures (LVP)** in force via ATIS, protected the ILS sensitive area from taxiing aircraft, and activated secondary backup power generators?

---

## 3. Real-World Case Study: CAT IIIb Autoland at Paris Charles de Gaulle

Imagine flight AF007 arriving over Paris CDG in freezing fog:
- **Weather Report (METAR)**: Wind calm, visibility 75 meters, Runway 26L RVR 125m / 100m / 100m, vertical visibility 50 feet.
- **The Challenge**: A standard Category I approach requires at least 550 meters RVR and a 200 ft decision height. Looking out the window, the crew will see nothing until 10 feet above the ground.
- **The Legal & Technical Chain**:
  1. *OpSpec Check*: Air France holds EASA Part-SPA.LVO authorization for CAT IIIb with no decision height and RVR down to 75m. (Valid)
  2. *Aircraft Status*: Airbus A350-900 AFM permits autoland. Both autopilot channels (AP1 + AP2) engaged in `DUAL` mode. Dual radio altimeters active. Auto-rollout guidance active. (Valid)
  3. *Crew Currency*: Both Captain and First Officer completed recurrent simulator CAT III checks 4 months ago. (Valid)
  4. *Airport Procedure*: Paris ATC issues clearance: *"Air France 007, cleared ILS Runway 26L, Low Visibility Procedures are in force, wind calm, RVR 125 meters"*. (Valid)
- **The Result**: At 50 feet, the pilots see only fog. The aircraft automatically tracks the localizer centerline, retards throttles, flares onto the runway, applies autobrakes, and steers down the centerline using nosewheel guidance until rolling to a stop safely.

---

## 4. Adversarial Failure Mode: Loss of Ground or Aircraft Safeguards

What happens if one pillar fails during the final approach?

```
[Inbound on ILS at 600 ft AGL] ─── (Tug crosses ILS Sensitive Area OR Autopilot fails) ───┐
                                                                                         ▼
┌──────────────────────────────────────────────┐        ┌───────────────────────────────┐
│        GROUND SAFEGUARD COMPROMISED          │        │       AIRBORNE FAILURE        │
│ • ILS signal beam fluctuates                 │        │ • Autopilot channel drops     │
│ • LVP protections breached                   │        │ • Autoland degraded to Cat I  │
│ • Aerodrome pillar = 0                       │        │ • Aircraft pillar = 0         │
└──────────────────────┬───────────────────────┘        └───────────────┬───────────────┘
                       │                                                │
                       └───────────────────────┬────────────────────────┘
                                               │
                                               ▼
                              ┌──────────────────────────────────┐
                              │  MANDATORY MISSED APPROACH (GO)  │
                              │ • Immediate climb to missed altitude│
                              │ • RVR 125m < Cat I minimum (550m)│
                              │ • Divert to planned alternate    │
                              └──────────────────────────────────┘
```

If an airport tug wanders past the CAT II/III holding point onto the ILS sensitive area, or if Autopilot 2 disconnects at 400 ft:
- The legal operational envelope collapses instantaneously.
- The captain cannot "take a look" or attempt a visual landing.
- Aviation law and Standard Operating Procedures (SOP) mandate an immediate **Go-Around** and diversion to an alternate airport where weather exceeds standard minima.

---

## 5. Practical Deliverable & Verification

Run the interactive Python simulation script for Day 013 to evaluate operational approvals, compute ETOPS diversion circles, verify CAT IIIb autoland criteria, and stress-test in-flight system degradations:

```bash
python learned/week-02/day-013/experiment.py
```
