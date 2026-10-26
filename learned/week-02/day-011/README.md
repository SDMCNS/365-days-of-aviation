# Day 011 — Operational Guide: When International Harmonisation Meets National Requirements

[← Return to Master Syllabus](../../lessons/README.md) | [Technical Walkthrough](analysis.md) | [System Topology Canvas](architecture.mermaid) | [Run Python Simulator](experiment.py)

---

## 1. Executive Summary: The Sovereignty Friction Point

The dream of aviation pioneers was a borderless, seamless sky operating under a single universal rulebook. The reality of modern civil aviation is a continuous collision between **international harmonisation (ICAO SARPs)** and **national sovereign requirements**.

Under the Chicago Convention:
- States agree to harmonize regulations under Article 37.
- But sovereign States retain supreme authority under Article 1 to impose stricter standards, restrict market access, and protect domestic industries.

When an airline flies internationally, it crosses invisible legal frontiers where rules on pilot qualifications, passenger delay rights, maintenance standards, and carbon taxes change dramatically mid-flight.

---

## 2. Key Battlegrounds of Regulatory Divergence

### 1. Crew Licensing & The "1,500-Hour Rule"
- **ICAO Baseline**: Annex 1 permits a co-pilot to fly commercial passenger transport with a Commercial Pilot License (CPL) requiring 250 flight hours (or 200 hours in an approved integrated course).
- **US National Requirement**: Following the Colgan Air crash (2009), the US Congress passed Public Law 111-216, mandating that all Part 121 airline first officers hold an Airline Transport Pilot (ATP) certificate requiring **1,500 flight hours**.
- **The Clash**: European and Asian airlines operate long-haul widebody aircraft with 300-hour first officers into US airports under foreign operating specifications (FAR Part 129), while US airlines cannot hire first officers without 1,500 hours, creating massive training cost and labor supply differentials.

### 2. Extraterritorial Consumer Protection (EU261)
- **International Standard**: The Montreal Convention 1999 caps airline delay liability to proven out-of-pocket economic damages (capped in Special Drawing Rights).
- **EU National/Regional Requirement**: Regulation (EC) 261/2004 mandates fixed, non-fault cash compensation (€250, €400, or €600 per passenger) for delays over 3 hours.
- **The Clash**: The European Union enforces this regulation on **all foreign carriers departing EU airports**. A US, Japanese, or Brazilian airline departing Paris or Frankfurt is subject to EU consumer law, even if their home nation has no such laws.

### 3. Cabotage Protection (Article 7)
- **The Rule**: Each contracting State has the right to refuse permission to foreign aircraft to take on passengers or cargo destined for another point within its territory (cabotage).
- **Operational Reality**: British Airways cannot sell tickets to carry passengers solely from New York to Los Angeles. United Airlines cannot carry passengers solely from Paris to Nice. Nations strictly protect their domestic commercial markets.

---

## 3. Practical Implementation Reference

Launch the interactive Day 011 Harmonisation vs National Requirements Friction Diagnostic:
```bash
python learned/week-02/day-011/experiment.py
```
This tool:
1. Evaluates cross-jurisdictional compliance across pilot qualification, cabotage, and consumer compensation.
2. Models the financial impact of extraterritorial consumer regulations (EU261 vs US DOT rules).
3. Analyzes foreign ramp inspection (SAFA) risks when national rules conflict.
4. Stress-tests a wet-lease transatlantic passenger flight under FAR Part 129 and EU261 liabilities.
