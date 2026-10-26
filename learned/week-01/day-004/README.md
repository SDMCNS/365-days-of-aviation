# Day 004 — Operational Guide: Why a Serviceable Aircraft Can Still Be Grounded

[← Return to Lesson Plan](../../../lessons/week-01/day-004.md) | [Operational & Technical Analysis](math.md) | [System Topology Canvas](architecture.mermaid) | [Run Python Simulator](experiment.py)

---

## 1. Executive Summary & Operational Context

A fundamental mistake made by external observers of aviation is equating aircraft mechanical readiness with operational release. Today, on **Day 4 (Challenge)**, we stress-test the limits of the aviation system by analyzing how non-technical barriers—crew fatigue laws, aerodrome runway friction, airport curfews, overflight permits, and rescue service downgrades—can completely paralyze a flight even when the aircraft has zero technical defects.

- **Weekly Domain**: Week 01 — Aviation as a System
- **Stage in Learning Cycle**: Day 4 — Challenge
- **Regulatory Framework**: EASA Part-ORO.FTL (Crew Duty), EASA Part-CAT (Operational Minima), and ICAO Annex 14 (Aerodrome Emergency Services)
- **Monthly Project Link**: Aviation Ecosystem Map and Regulatory Hierarchy

---

## 2. The Non-Technical Failure Modes

```
                              [ Pristine Serviceable Aircraft ]
                                             │
      ┌─────────────────┬────────────────────┼───────────────────┬─────────────────┐
      ▼                 ▼                    ▼                   ▼                 ▼
[ Crew FTL ]      [ Aerodrome ]       [ Slot & Curfew ]   [ Overflight ]    [ Fire Service ]
Exceeded Duty     RVR below minima    Arrival after 23:00 Diplomatic permit Downgraded RFFS
 ceiling (hours)   or freezing rain    night curfew        denied across FIR  below aircraft Cat
      │                 │                    │                   │                 │
      ▼                 ▼                    ▼                   ▼                 ▼
  [ ❌ HALT ]       [ ❌ HALT ]          [ ❌ HALT ]         [ ❌ HALT ]       [ ❌ HALT ]
```

### 1. Crew Flight Time Limitations (FTL)
Under **EASA ORO.FTL**, fatigue is managed through strictly bounded legal limits. If an aircraft experiences ground delays that would cause the crew to exceed their maximum allowable Flight Duty Period (FDP) before landing, the crew cannot legally initiate the flight.

### 2. Aerodrome Weather & Runway Surface (GRF)
Even with Category III autoland capability, an aircraft requires adequate runway friction to decelerate safely during an aborted takeoff (RTO). Under the ICAO Global Reporting Format (GRF), if runway braking action is reported as RWYCC 1 (Poor) or contaminated with unplowed wet snow, operations may be suspended by the Pilot-in-Command or the aerodrome operator.

### 3. Night Flight Restrictions & Curfews
Major aerodromes (e.g. Frankfurt EDDF, London Heathrow EGLL, Sydney YSSY) enforce statutory noise curfews. Arriving 1 minute after the curfew cutoff results in severe legal fines and denial of landing clearance, forcing an airborne diversion.

### 4. Aerodrome Fire & Rescue Downgrades (RFFS)
ICAO Annex 14 requires commercial aircraft to land only at airports with an adequate Rescue and Firefighting Services (RFFS) rating (Category 1 to 10). If an airport's primary crash tender breaks down, the category drops; an A320 or B777 is legally prohibited from landing there until full fire cover is restored.

---

## 3. Hands-On Practical Tool: Multi-Gate Dispatch Diagnostic

Run today's interactive Python experiment to evaluate an aircraft dispatch release across all 6 operational gates:

```bash
python learned/week-01/day-004/experiment.py
```

### What You Will Explore:
- Evaluate a mechanically perfect aircraft against:
  - Elapsed crew duty hours vs legal limits.
  - Runway Visual Range (RVR) vs takeoff minima.
  - Destination ETA vs airport night curfew.
  - Airport RFFS fire protection rating.
- Observe how failure in any single non-technical gate blocks the dispatch release.
- Run the **Break-It Stress Test**: Introduce a minor 20-minute ground delay that triggers a compounding crew timeout, grounding the flight.
