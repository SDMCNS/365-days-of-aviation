# Day 029 — Technical Walkthrough: Aircraft types, configurations, categories and intended operations.

[← Return to Lesson Guide](README.md) | [System Topology Canvas](architecture.mermaid) | [Run Python Simulator](experiment.py)

---

## 1. Quantitative Modeling & Physical/Operational Principles
To establish compliance with ICAO Annex 8 and CS-25 Subpart B, aircraft configurations must adhere to strict mass and balance limits. The structural operating envelopes are governed by the following core equations:

1. **Zero Fuel Mass (ZFM) Constraint:**
   $$\text{DOM} + \text{Passenger Payload} + \text{Cargo Payload} \le \text{MZFM}$$
   Where $\text{DOM}$ is Dry Operating Mass, and $\text{MZFM}$ is Maximum Zero Fuel Mass.

2. **Takeoff Mass (TOM) Constraint:**
   $$\text{TOM} = \text{ZFM} + \text{Takeoff Fuel Mass} \le \text{MTOM}$$
   Where $\text{MTOM}$ is Maximum Takeoff Mass governed by structural limits, field length performance, and climb gradient requirements.

3. **Center of Gravity (CG) Position Calculation:**
   $$\bar{c} = \frac{\sum (m_i \cdot x_i)}{\sum m_i}$$
   Expressed as a percentage of the Mean Aerodynamic Chord ($\% \text{MAC}$):
   $$\% \text{MAC} = \frac{\text{CG}_{\text{arm}} - \text{LEMAC}}{\text{MAC}} \times 100$$
   Where $\text{LEMAC}$ is the Leading Edge of the Mean Aerodynamic Chord.

## 2. Step-by-Step Worked Numerical Trace
Let us trace a transport category aircraft preparation under standard operating conditions:
- **Aircraft Type / Category:** CS-25 Twin-Jet Transport
- **Dry Operating Mass ($\text{DOM}$):** $41,500\text{ kg}$
- **Maximum Zero Fuel Mass ($\text{MZFM}$):** $62,500\text{ kg}$
- **Maximum Takeoff Mass ($\text{MTOM}$):** $79,000\text{ kg}$
- **Planned Passenger Load:** $160 \text{ passengers} \times 88\text{ kg}$ (standard adult average including carry-on) = $14,080\text{ kg}$
- **Planned Cargo Load:** $3,500\text{ kg}$
- **Ramp / Takeoff Fuel:** $8,200\text{ kg}$

**Step 1: Compute Zero Fuel Mass (ZFM)**
$$\text{ZFM} = 41,500 + 14,080 + 3,500 = 59,080\text{ kg}$$
*Check against MZFM:* $59,080\text{ kg} \le 62,500\text{ kg}$ $\rightarrow$ **PASS** ($3,420\text{ kg}$ structural margin remaining).

**Step 2: Compute Takeoff Mass (TOM)**
$$\text{TOM} = 59,080 + 8,200 = 67,280\text{ kg}$$
*Check against MTOM:* $67,280\text{ kg} \le 79,000\text{ kg}$ $\rightarrow$ **PASS** ($11,720\text{ kg}$ structural margin remaining).

**Step 3: Center of Gravity Verification**
- Calculated CG index moment: $1,482,500\text{ kg}\cdot\text{m}$
- Total Mass: $67,280\text{ kg}$
- $\text{CG}_{\text{arm}} = \frac{1,482,500}{67,280} = 22.03\text{ m aft of datum}$
- If $\text{LEMAC} = 20.50\text{ m}$ and $\text{MAC} = 4.20\text{ m}$:
  $$\% \text{MAC} = \frac{22.03 - 20.50}{4.20} \times 100 = 36.43\%$$
*Check against CS-25 Subpart B forward and aft stability limits (e.g., $15\% \text{to } 42\% \text{ MAC}$):* $\rightarrow$ **PASS**.

## 3. Regulatory Boundaries & Critical Thresholds
- **ICAO Annex 8:** Mandates that every aircraft holding a Certificate of Airworthiness must be maintained in conformity with its approved Type Design. Any unauthorized configuration change invalidates airworthiness.
- **CS-25 Subpart B:** Requires explicit demonstration of longitudinal, directional, and lateral stability across all operational configurations (flaps up, landing gear down, takeoff config).
- **MEL & Configuration Deviation List (CDL):** Defines exact operational tolerances permitted when secondary structural items or cabin configuration elements are missing or inoperative.