# Day 005 — Operational & Quantitative Analysis: The 12-Milestone Flight Lifecycle & Trajectory Burn

[← Return to Lesson Guide](README.md) | [System Topology Canvas](architecture.mermaid) | [Run Python Simulator](experiment.py)

---

## 1. The Temporal Architecture of a Flight

A commercial flight is not a two-hour event; it is an operational progression spanning up to 365 days of commercial scheduling, weeks of crew rostering, hours of pre-flight preparation, and post-flight maintenance reconciliation.

Under the ICAO and IATA Operational Framework, this lifecycle is structured into five distinct operational horizons:
1. **Strategic Planning Horizon (D-365 to D-30)**: Schedule creation, IATA Worldwide Airport Slot coordination, and fleet allocation.
2. **Tactical Planning Horizon (D-30 to D-1)**: Crew roster publication under EASA Part-ORO.FTL, aircraft maintenance check allocation (EASA Part-M), and preliminary commercial passenger booking curve lock.
3. **Operational Dispatch Horizon (D-3h to D-1h)**: Meteorological briefing, NOTAM assessment, computerized flight plan (CFP/OFP) calculation, fuel loading determination, and ICAO FPL filing to Eurocontrol IFPS.
4. **Pre-Departure Horizon (D-45m to D-0)**: Aircraft physical turnaround, passenger boarding, fueling, loadsheet/trim calculation, ATC pre-departure clearance (DCL), pushback, and taxi.
5. **In-Flight & Turnaround Horizon (D-0 to In-Blocks)**: Take-off, climb, en-route ATM separation, descent profile, landing, taxi-in, and Technical Log entry.

---

## 2. Quantitative Model: Flight Trajectory Fuel-Burn Integration

The physical flight profile is segmented into discrete flight phases with distinct aerodynamic fuel burn rates:

### Trajectory Fuel Consumption Formulation
$$\text{Total Mission Trip Fuel } M_{\text{trip}} = M_{\text{climb}} + M_{\text{cruise}} + M_{\text{descent}} + M_{\text{approach}}$$

1. **Climb Phase**: High thrust, changing air density ($\rho$), transitioning from ground to Cruising Flight Level (e.g., FL350):
   $$M_{\text{climb}} = \int_{0}^{t_{\text{TOC}}} \dot{m}_{\text{climb}}(h, V) \, dt \quad \approx 850 - 1,050 \text{ kg (A320, 18-22 min)}$$
2. **Cruise Phase**: Constant altitude or step climb at optimum Mach number ($M = 0.78$):
   $$\text{Ground Speed } V_g = \text{TAS} \pm V_{\text{wind}}$$
   $$M_{\text{cruise}} = \left( \frac{\text{Distance}_{\text{cruise}}}{V_g} \right) \times \text{SFC} \times \text{Thrust}_{\text{req}} \quad \approx 2,100 - 2,400 \text{ kg/hr}$$
3. **Descent Phase**: Flight Idle descent profile following the operational "3-to-1 Rule" (3 NM per 1,000 ft altitude drop):
   $$\text{Top of Descent (TOD) Distance (NM)} = \frac{\text{Cruising Altitude (ft)} - \text{Field Elevation (ft)}}{1000} \times 3$$
   At flight idle, fuel burn drops to nominal levels ($\approx 250 - 350\text{ kg total descent}$).
4. **Approach & Landing**: Flap deployment, landing gear extension (increased parasite drag), and thrust reversers ($\approx 150 - 200\text{ kg}$).

---

## 3. Step-by-Step Worked Numerical Example

Consider an Airbus A320 flying **London Heathrow (EGLL)** to **Munich (EDDM)**:
- Ground Track Distance: 520 NM
- Cruising Level: FL350 (35,000 ft)
- Average True Airspeed (TAS): 440 knots
- Headwind Component: 25 knots $\longrightarrow$ Ground Speed $V_g = 440 - 25 = 415\text{ knots}$.

### 1. Top of Descent (TOD) Calculation
Munich field elevation is $1,487\text{ ft} \approx 1,500\text{ ft}$.
$$\text{Altitude to lose} = 35,000 - 1,500 = 33,500\text{ ft}$$
$$\text{TOD Distance before Munich} = \frac{33,500}{1,000} \times 3 = \mathbf{100.5\text{ NM}}$$

### 2. Phase Breakdown & Mission Fuel
- **Climb**: 70 NM covered in 20 minutes; Fuel burn = **920 kg**.
- **Descent**: 100 NM covered in 22 minutes (idle); Fuel burn = **280 kg**.
- **Cruise Distance**: $520 - (70 + 100) = \mathbf{350\text{ NM}}$.
  $$\text{Cruise Time} = \frac{350\text{ NM}}{415\text{ kt}} = 0.843\text{ hours} \approx \mathbf{50.6\text{ minutes}}.$$
  $$\text{Cruise Fuel} = 0.843\text{ hr} \times 2,300\text{ kg/hr} = \mathbf{1,939\text{ kg}}.$$
- **Approach & Landing**: **180 kg**.

$$\text{Total Trip Fuel} = 920 + 1,939 + 280 + 180 = \mathbf{3,319\text{ kg}}$$

### 3. Total Ramp Fuel Plan (EASA Fuel Scheme)
- **Taxi Fuel**: $150\text{ kg}$
- **Trip Fuel**: $3,319\text{ kg}$
- **Contingency Fuel (5%)**: $0.05 \times 3,319 = 166\text{ kg}$
- **Alternate Fuel (Nuremberg - EDDN, 90 NM)**: $750\text{ kg}$
- **Final Reserve (30 min hold at 1,500 ft)**: $1,100\text{ kg}$

$$\mathbf{\text{Total Block Fuel Required}} = 150 + 3,319 + 166 + 750 + 1,100 = \mathbf{5,485\text{ kg}}$$
