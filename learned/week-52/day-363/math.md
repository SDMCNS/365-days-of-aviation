# Day 363 — Mathematical & Analytical Walkthrough: Explain how a change in one domain can propagate across the whole aviation ecosystem.

[← Return to Lesson Document](README.md) | [Architecture Diagram](architecture.mermaid)

---

## 1. Mathematical Executive Summary: Airline Unit Economics, Network Propagation & Whole-System Capstone

Day 363 establishes the analytical equations, mathematical physics, and quantitative metrics governing **Explain how a change in one domain can propagate across the whole aviation ecosystem.**.


### 1. Airline Unit Economics: CASM, RASM & Break-Even Load Factor
Available Seat Kilometers (ASK) for fleet flying $N$ flights of distance $D_i$ with $S_i$ seats:
$$\text{ASK} = \sum_{i=1}^N S_i \times D_i, \quad \text{RPK (Revenue Pax Km)} = \sum_{i=1}^N \text{Pax}_i \times D_i$$
Cost per Available Seat Kilometer (CASM) and Revenue per ASK (RASM):
$$\text{CASM} = \frac{\text{Total Operating Costs}}{\text{ASK}}, \quad \text{RASM} = \frac{\text{Total Revenue}}{\text{ASK}} = \text{Yield} \times \text{Load Factor}$$
Break-Even Passenger Load Factor $\text{LF}_{\text{BE}}$:
$$\text{LF}_{\text{BE}} = \frac{\text{CASM}}{\text{Yield}} = \frac{\text{Cost} / \text{ASK}}{\text{Revenue} / \text{RPK}}$$

### 2. Network Delay Contagion & System Capstone Coupling
Propagation of upstream arrival delay $\Delta t_{\text{arr}}$ through aircraft turnaround buffer $B_{\text{turn}}$ to downstream flight:
$$\Delta t_{\text{dep, next}} = \max\left(0, \Delta t_{\text{arr}} - B_{\text{turn}}\right) + \Delta t_{\text{crew}} + \Delta t_{\text{ATC}}$$


---

## 2. Step-by-Step Numerical Verification & Sensitivity Trace


### Worked Numerical Example
- Route: Paris CDG to Rome FCO ($D = 1100\text{ km}$), A320 with $S = 180\text{ seats}$.
- $\text{ASK} = 180 \times 1100 = 198{,}000\text{ seat-km}$.
- Operating Costs for the flight: Fuel (€3400), Crew (€1800), Airport Charges (€2400), Maintenance & Lease (€2200), Navigation Charges (€900) $\implies \text{Total Cost} = \text{€}10{,}700$.
- Unit Cost:
  $$\text{CASM} = \frac{10{,}700}{198{,}000} = \text{€}0.05404 \text{ per ASK } (5.40\text{ cents/ASK})$$
- Average Passenger Fare booked $= \text{€}92.00 \implies$ Passenger Yield:
  $$\text{Yield} = \frac{92.00}{1100} = \text{€}0.08364 \text{ per RPK } (8.36\text{ cents/RPK})$$
- Break-Even Load Factor:
  $$\text{LF}_{\text{BE}} = \frac{0.05404}{0.08364} = 64.6\% \quad (116.3 \text{ passengers})$$
- Actual passengers on board $= 152 \implies \text{Actual Load Factor} = 152 / 180 = 84.4\%$.
- Flight Operating Profit $= (152 \times 92.00) - 10{,}700 = 13{,}984 - 10{,}700 = +\text{€}3{,}284$.


---

## 3. Operational & Regulatory Boundary Sensitivities

1. **Upper Critical Threshold**: Parameters that trigger mandatory regulatory interventions (e.g., maximum takeoff mass exceeding structural limit, flight duty period exceeding EASA FTL limit, or crosswind exceeding aircraft flight manual limit).
2. **Lower Critical Threshold**: Parameters below which operations become impermissible or economically unviable (e.g., fuel reserve below 30-minute final reserve, runway braking friction below minimum, or passenger load factor below break-even).
3. **Cross-Domain Ripple Factor**: How variance in this day's mathematical metric cascades into upstream airline planning or downstream air traffic management flow slots.
