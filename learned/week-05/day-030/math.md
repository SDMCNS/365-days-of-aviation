# Day 030 — Mathematical & Analytical Walkthrough: Lift, drag, thrust, weight, stability and control.

[← Return to Lesson Document](README.md) | [Architecture Diagram](architecture.mermaid)

---

## 1. Mathematical Executive Summary: Flight Physics, Aerodynamics, Propulsion & Airworthiness Lifecycles

Day 030 establishes the analytical equations, mathematical physics, and quantitative metrics governing **Lift, drag, thrust, weight, stability and control.**.


### 1. Aerodynamic Lift, Drag & Drag Polar
Subsonic aerodynamic forces acting upon wing surface area $S$ at true airspeed $V$ and air density $\rho$:
$$L = \frac{1}{2} \rho V^2 S C_L, \quad D = \frac{1}{2} \rho V^2 S C_D$$
The parabolic drag polar with zero-lift parasite drag $C_{D0}$ and Oswald efficiency $e$:
$$C_D = C_{D0} + \frac{C_L^2}{\pi e \text{AR}}, \quad \text{where aspect ratio } \text{AR} = \frac{b^2}{S}$$
Maximum Lift-to-Drag ratio $(L/D)_{\max}$ occurs at the speed where induced drag equals parasite drag:
$$\left(\frac{L}{D}\right)_{\max} = \frac{1}{2 \sqrt{C_{D0} / (\pi e \text{AR})}}$$

### 2. ISA Atmosphere & True Airspeed (TAS) Conversion
Temperature lapse rate $L = 0.0065\text{ K/m}$ up to the tropopause ($h_p = 11{,}000\text{ m}$):
$$T(h) = T_0 - L \cdot h, \quad P(h) = P_0 \left(1 - \frac{L h}{T_0}\right)^{\frac{g_0}{R L}}, \quad \rho(h) = \frac{P(h)}{R T(h)}$$
$$V_{\text{TAS}} = V_{\text{EAS}} \sqrt{\frac{\rho_0}{\rho}}, \quad M = \frac{V_{\text{TAS}}}{\sqrt{\gamma R T}}$$


---

## 2. Step-by-Step Numerical Verification & Sensitivity Trace


### Worked Numerical Example
- Aircraft: Twin-aisle airliner, Mass $m = 70{,}000\text{ kg}$, Wing area $S = 122.6\text{ m}^2$, $\text{AR} = 9.5$, $e = 0.85$, $C_{D0} = 0.020$.
- Atmospheric condition: Flight Level FL330 ($h = 10{,}060\text{ m}$, $T = 222.6\text{ K}$, $\rho = 0.380\text{ kg/m}^3$).
- Weight $W = m \cdot g = 70{,}000 \times 9.80665 = 686{,}465\text{ N}$.
- At cruise speed $M = 0.78$ ($a = \sqrt{1.4 \times 287.05 \times 222.6} = 299.1\text{ m/s}$):
  $$V_{\text{TAS}} = 0.78 \times 299.1 = 233.3\text{ m/s} \quad (453.5\text{ knots})$$
- Required lift coefficient:
  $$C_L = \frac{2 W}{\rho V_{\text{TAS}}^2 S} = \frac{2 \times 686{,}465}{0.380 \times (233.3)^2 \times 122.6} = 0.5416$$
- Induced drag coefficient:
  $$C_{Di} = \frac{(0.5416)^2}{\pi \times 0.85 \times 9.5} = \frac{0.2933}{25.368} = 0.01156$$
- Total drag coefficient $C_D = 0.020 + 0.01156 = 0.03156$.
- Lift-to-Drag ratio $L/D = 0.5416 / 0.03156 = 17.16$.
- Total cruise thrust required $T_{\text{req}} = W / (L/D) = 686{,}465 / 17.16 = 40{,}004\text{ N}$ ($20.0\text{ kN per engine}$).


---

## 3. Operational & Regulatory Boundary Sensitivities

1. **Upper Critical Threshold**: Parameters that trigger mandatory regulatory interventions (e.g., maximum takeoff mass exceeding structural limit, flight duty period exceeding EASA FTL limit, or crosswind exceeding aircraft flight manual limit).
2. **Lower Critical Threshold**: Parameters below which operations become impermissible or economically unviable (e.g., fuel reserve below 30-minute final reserve, runway braking friction below minimum, or passenger load factor below break-even).
3. **Cross-Domain Ripple Factor**: How variance in this day's mathematical metric cascades into upstream airline planning or downstream air traffic management flow slots.
