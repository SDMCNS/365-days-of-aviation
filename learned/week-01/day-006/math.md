# Day 006 — Operational & Quantitative Analysis: Balancing Commercial Revenue Against Operational, Technical & Regulatory Constraints

[← Return to Lesson Guide](README.md) | [System Topology Canvas](architecture.mermaid) | [Run Python Simulator](experiment.py)

---

## 1. The Commercial-Operational Tension in Airline Systems

A commercial airline exists to generate sustainable operating margin by providing safe air transport. Commercial objectives (maximizing revenue per available seat kilometre, aircraft daily utilization, and cargo belly yield) are in continuous tension with operational, technical, and regulatory constraints.

$$\text{Operating Profit } \Pi = \sum_{\text{flights}} \left[ \text{Revenue}(\text{Pax, Cargo}) - \text{Direct Operating Costs}(\text{DOC}) \right]$$

Every commercial decision is bound by non-negotiable physical and legal constraints:
1. **Structural Weight Limits**: Maximum Zero Fuel Mass (MZFM), Maximum Take-Off Mass (MTOM), and Maximum Landing Mass (MLM) certified under CS-25.
2. **Operational Fuel Policies**: Mandatory statutory fuel reserves under ICAO Annex 6 / EASA CAT.OP.MPA.181 (carrying less fuel is illegal; carrying excessive fuel burns extra fuel).
3. **Crew Legal Workload**: Maximum Flight Duty Periods (FDP) under EASA Part-ORO.FTL.
4. **Airport Environmental Curfews**: Night-time operating restrictions (e.g., London Heathrow, Frankfurt) penalizing late arrivals with mandatory diversions and fines.
5. **Passenger Rights Regulations**: Statutory delay compensation (e.g., Regulation (EC) 261/2004) transforming minor schedule delays into major financial losses.

---

## 2. Quantitative Formulation

### 1. Payload-Range Trade-off & Structural Envelopes
An aircraft's Take-Off Mass ($M_{\text{TOM}}$) is governed by three independent structural boundaries:

$$M_{\text{TOM}} = M_{\text{OEW}} + M_{\text{Payload}} + M_{\text{Fuel}}$$

$$\begin{cases}
M_{\text{TOM}} \le M_{\text{MTOM}} & (\text{Maximum Take-Off Mass - structural \& runway limit}) \\
M_{\text{OEW}} + M_{\text{Payload}} \le M_{\text{ZFM}} & (\text{Maximum Zero Fuel Mass - wing root bending moment}) \\
M_{\text{TOM}} - M_{\text{TripFuel}} \le M_{\text{MLM}} & (\text{Maximum Landing Mass - landing gear energy limit})
\end{cases}$$

When flight range requires high fuel load, commercial payload must be capped:
$$\text{Max Allowed Payload} = \min\left(M_{\text{ZFM}} - M_{\text{OEW}}, \; M_{\text{MTOM}} - M_{\text{OEW}} - M_{\text{Fuel}}\right)$$

### 2. Economic Optimization vs Weight Penalty: The Fuel Tankering Model
Airlines frequently attempt **economic fuel tankering** (uploading excess fuel at origin to avoid buying expensive fuel at an outstation destination).
However, carrying excess mass increases fuel consumption ("cost of carry"):

$$\Delta \text{Burn} = \Delta M_{\text{Tankered}} \times k_{\text{carry}} \times t_{\text{flight}}$$
Where $k_{\text{carry}} \approx 3.5\% \text{ to } 4.0\%\text{ per hour}$ for modern narrowbodies (A320/B737).

The economic net benefit of tankering $\Delta M$ kilograms is:
$$\text{Net Savings } S = \Delta M \times \left( P_{\text{dest}} - P_{\text{orig}} \right) - \left( \Delta \text{Burn} \times P_{\text{orig}} \right) - C_{\text{weight\_penalties}}$$

**Break-even Price Differential ($\Delta P_{\text{crit}}$)**:
Tankering is only economically profitable if:
$$\frac{P_{\text{dest}}}{P_{\text{orig}}} > 1 + (k_{\text{carry}} \times t_{\text{flight}})$$

Furthermore, tankered fuel directly reduces available belly cargo capacity if $M_{\text{TOM}} \to M_{\text{MTOM}}$ or $M_{\text{LM}} \to M_{\text{MLM}}$.

---

## 3. Step-by-Step Worked Numerical Example

Consider an Airbus A320 operating **Frankfurt (EDDF) to Madrid (LEMD)**:
- Operating Empty Weight ($M_{\text{OEW}}$): $42,600\text{ kg}$
- Structural Limits: $M_{\text{MZFM}} = 62,500\text{ kg}$, $M_{\text{MTOM}} = 77,000\text{ kg}$, $M_{\text{MLM}} = 66,000\text{ kg}$.
- Flight Time: $2.5\text{ hours}$. Mission Trip Fuel: $5,200\text{ kg}$.
- Mandatory Minimum Reserve Fuel: $2,100\text{ kg}$.
- Standard Minimum Ramp Fuel: $7,300\text{ kg}$.
- Commercial Demand: 168 passengers ($168 \times 84\text{ kg} = 14,112\text{ kg}$) + $4,500\text{ kg}$ high-yield cargo.
  $$\text{Target Commercial Payload} = 14,112 + 4,500 = \mathbf{18,612\text{ kg}}$$

### 1. Zero Fuel Weight Verification
$$M_{\text{ZFW}} = M_{\text{OEW}} + \text{Payload} = 42,600 + 18,612 = \mathbf{61,212\text{ kg}} \le 62,500\text{ kg} \quad \text{[LEGAL]}$$

### 2. Fuel Tankering Decision
- Fuel price at Frankfurt ($P_{\text{orig}}$): €0.80 / kg.
- Fuel price at Madrid ($P_{\text{dest}}$): €0.95 / kg (Price differential = +€0.15/kg, or +18.75%).
- Outbound Dispatch considers tankering $3,000\text{ kg}$ of return fuel for Madrid $\to$ Frankfurt.
- Cost of carry coefficient $k_{\text{carry}} = 3.8\% / \text{hr}$.
- Flight time = $2.5\text{ hr}$.
$$\text{Extra Burn Incurred} = 3,000\text{ kg} \times 0.038 \times 2.5 = \mathbf{285\text{ kg}}$$
$$\text{Gross Fuel Savings} = 3,000\text{ kg} \times (€0.95 - €0.80) = \mathbf{€450.00}$$
$$\text{Cost of Extra Burn} = 285\text{ kg} \times €0.80 = \mathbf{€228.00}$$
$$\text{Net Economic Benefit} = €450 - €228 = \mathbf{+€222.00}$$

### 3. Operational & Structural Feasibility Check
With $3,000\text{ kg}$ tankered fuel added to ramp fuel ($7,300 + 3,000 = 10,300\text{ kg}$):
$$M_{\text{TOM}} = M_{\text{ZFW}} + M_{\text{RampFuel}} = 61,212 + 10,300 = \mathbf{71,512\text{ kg}} \le 77,000\text{ kg} \quad \text{[LEGAL]}$$
Landing weight at Madrid:
$$M_{\text{Landing}} = M_{\text{TOM}} - M_{\text{TripFuel}} = 71,512 - (5,200 + 285) = \mathbf{66,027\text{ kg}}$$

$$\mathbf{M_{\text{Landing}} = 66,027\text{ kg} > M_{\text{MLM}} (66,000\text{ kg}) \implies \text{STRUCTURAL EXCEEDANCE BY 27 kg!}}$$

**The Operational Resolution**:
Even though tankering yields $+€222$ net profit, the flight will exceed Maximum Landing Mass at Madrid unless $27\text{ kg}$ of commercial cargo is offloaded, or tankering is reduced to $2,950\text{ kg}$.
This illustrates how regulatory structural limits dictate commercial optimization.
