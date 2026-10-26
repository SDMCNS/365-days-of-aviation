# Day 091 — Mathematical & Analytical Walkthrough: Deliver the flight lifecycle model, including roles, decisions, data and failure points.

[← Return to Lesson Document](README.md) | [Architecture Diagram](architecture.mermaid)

---

## 1. Mathematical Executive Summary: Flight Dispatch, Weight & Balance, Fuel Planning & Crew FTL

Day 091 establishes the analytical equations, mathematical physics, and quantitative metrics governing **Deliver the flight lifecycle model, including roles, decisions, data and failure points.**.


### 1. Mass & Balance: Center of Gravity (CG) and %MAC
Total mass and longitudinal moment summation about the reference datum:
$$M_{\text{total}} = \sum_{i=1}^n m_i, \quad x_{\text{CG}} = \frac{\sum_{i=1}^n (m_i \cdot x_i)}{M_{\text{total}}}$$
Center of gravity position expressed as percentage of Mean Aerodynamic Chord (%MAC):
$$\% \text{MAC} = \frac{x_{\text{CG}} - x_{\text{LEMAC}}}{\text{MAC}} \times 100\%$$
Where $x_{\text{LEMAC}}$ is the datum distance to the Leading Edge of the MAC.

### 2. Operational Fuel Scheme (EASA CAT.OP.MPA.181)
Ramp fuel requirement satisfies regulatory partitioning:
$$M_{\text{Ramp}} = M_{\text{Taxi}} + M_{\text{Trip}} + M_{\text{Contingency}} + M_{\text{Alternate}} + M_{\text{FinalReserve}} + M_{\text{Extra}}$$
Where:
- $M_{\text{Contingency}} = \max\left(0.05 \times M_{\text{Trip}}, M_{5\min\text{ holding}}\right)$
- $M_{\text{FinalReserve}} = \text{Fuel required to hold for 30 minutes at } 1500\text{ ft above alternate at ISA}$


---

## 2. Step-by-Step Numerical Verification & Sensitivity Trace


### Worked Numerical Example
- Dry Operating Mass $\text{DOM} = 42{,}500\text{ kg}$ at $x = 17.20\text{ m}$.
- Traffic Load (Pax + Cargo) $= 16{,}200\text{ kg}$ at $x = 16.85\text{ m}$.
- Zero Fuel Mass $\text{ZFM} = 58{,}700\text{ kg}$.
  $$x_{\text{ZFM}} = \frac{(42{,}500 \times 17.20) + (16{,}200 \times 16.85)}{58{,}700} = \frac{731{,}000 + 272{,}970}{58{,}700} = 17.103\text{ m}$$
- Takeoff fuel $= 8{,}400\text{ kg}$ at wing tank centroid $x = 17.50\text{ m}$.
- Takeoff Mass $\text{TOM} = 67{,}100\text{ kg}$.
  $$x_{\text{TOM}} = \frac{(58{,}700 \times 17.103) + (8{,}400 \times 17.50)}{67{,}100} = \frac{1{,}003{,}946 + 147{,}000}{67{,}100} = 17.153\text{ m}$$
- Given $\text{LEMAC} = 16.20\text{ m}$ and $\text{MAC} = 4.20\text{ m}$:
  $$\% \text{MAC} = \frac{17.153 - 16.20}{4.20} \times 100\% = \frac{0.953}{4.20} \times 100\% = 22.69\% \text{ MAC}$$
- Verification: $22.69\% \in [18.0\%, 32.0\%]$ operational forward/aft envelope limit $\implies$ SAFE FOR DISPATCH.


---

## 3. Operational & Regulatory Boundary Sensitivities

1. **Upper Critical Threshold**: Parameters that trigger mandatory regulatory interventions (e.g., maximum takeoff mass exceeding structural limit, flight duty period exceeding EASA FTL limit, or crosswind exceeding aircraft flight manual limit).
2. **Lower Critical Threshold**: Parameters below which operations become impermissible or economically unviable (e.g., fuel reserve below 30-minute final reserve, runway braking friction below minimum, or passenger load factor below break-even).
3. **Cross-Domain Ripple Factor**: How variance in this day's mathematical metric cascades into upstream airline planning or downstream air traffic management flow slots.
