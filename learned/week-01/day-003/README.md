# Day 003 — Operational Guide: Aviation Information Flows, Aeronautical Telecommunications & System Maps

[← Return to Lesson Plan](../../../lessons/week-01/day-003.md) | [Operational & Technical Analysis](math.md) | [System Topology Canvas](architecture.mermaid) | [Run Python Simulator](experiment.py)

---

## 1. Executive Summary & Operational Context

In Days 001 and 002, we examined what aviation does and mapped its core stakeholders. Today, on **Day 3 (Build)**, we construct the nervous system of the entire aviation industry: the digital information flows, message routing protocols, and operational data pipelines that coordinate every aircraft movement.

- **Weekly Domain**: Week 01 — Aviation as a System
- **Stage in Learning Cycle**: Day 3 — Build
- **Regulatory Framework**: ICAO Annex 10 (Telecommunications), ICAO Annex 15 (Aeronautical Information Services), and ICAO Doc 4444 (PANS-ATM)
- **Monthly Project Link**: Aviation Ecosystem Map and Regulatory Hierarchy

---

## 2. The Core Aeronautical Information Pipeline

Before an aircraft can push back from the gate, four distinct categories of operational data must converge at the Airline Operations Control (OCC) and the Cockpit:

```
[ METAR / TAF / SIGMET ] (ICAO Annex 3)  ──┐
                                           │
[ NOTAMs & AIP Supplements ] (Annex 15)  ──┼──> [ Flight Dispatcher (OCC) ]
                                           │            │
[ Airline Commercial Schedule ] ───────────┘            ▼
                                                [ Operational Flight Plan (OFP) ]
                                                        │
                      ┌─────────────────────────────────┴────────────────────────┐
                      ▼                                                          ▼
         [ Eurocontrol IFPS / FAA ]                                    [ Aircraft Cockpit ]
          (AFTN/AMHS ICAO FPL filing)                                   (FMC Initialization)
                      │                                                          │
                      ▼                                                          ▼
             [ Local ATC Tower ] <═══════ Air-Ground DCL/CPDLC ════════> [ Flight Crew ]
```

### 1. ICAO Flight Plan (FPL)
Filed via AFTN/AMHS using strict ICAO Doc 4444 formatting. Specifies callsign, aircraft type, wake turbulence category, navigation equipment (PBN), cruising speed/flight level, route waypoints, destination, alternate aerodrome, and fuel endurance.

### 2. NOTAM (Notice to Air Missions)
Temporary alerts essential to flight operations: runway closures, out-of-service Instrument Landing Systems (ILS), crane obstacles, airshow airspace closures, or unserviceable aerodrome lighting.

### 3. Aeronautical Meteorology (METAR, TAF, SIGMET)
- **METAR**: Current observed weather at an aerodrome (wind direction/speed, runway visual range, cloud base, QNH altimeter setting).
- **TAF**: Terminal Aerodrome Forecast predicting conditions during the planned arrival window.
- **SIGMET**: Significant meteorological hazards en-route (severe turbulence, icing, volcanic ash, severe mountain waves).

### 4. A-CDM Milestone Telegrams
Standardized automated messages exchanged between airport stakeholders:
- **TOBT** (Target Off-Block Time): Estimated time when aircraft doors will be closed and passenger boarding bridge retracted.
- **TSAT** (Target Start-up Approval Time): Exact time ATC Tower expects the flight to commence pushback/start-up.
- **CTOT** (Calculated Take-Off Time): Eurocontrol flow management departure slot window ($\pm 5$ minutes).

---

## 3. Hands-On Practical Tool: Flight Plan Validator & Aeronautical Information Router

Today's interactive Python experiment allows you to construct, validate, and stress-test an authentic ICAO flight plan:

```bash
python learned/week-01/day-003/experiment.py
```

### What You Will Explore:
- Enter flight parameters: departure, destination, alternate, cruising level, and fuel loading.
- Generate an authentic **ICAO Doc 4444 FPL string**.
- Verify the mandatory statutory fuel reserves (Trip + 5% Contingency + Alternate + 30 min Final Reserve).
- Run the **Break-It Stress Test**: Inject an illegal waypoint or insufficient alternate fuel and observe how Eurocontrol's IFPS automated validation rejects the flight plan (`REJ`), halting flight release.
