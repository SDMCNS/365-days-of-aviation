# Day 093 — Mathematical & Analytical Walkthrough: Runways, taxiways, aprons, stands, terminals, rescue facilities and supporting infrastructure.

[← Return to Lesson Document](README.md) | [Architecture Diagram](architecture.mermaid)

---

## 1. Mathematical Executive Summary: Aerodrome Infrastructure, Turnaround Critical Path & Slot Throughput

Day 093 establishes the analytical equations, mathematical physics, and quantitative metrics governing **Runways, taxiways, aprons, stands, terminals, rescue facilities and supporting infrastructure.**.


### 1. Runway Declared Distances & Accelerate-Stop
Runway safety margins under ICAO Annex 14:
$$\text{TORA} = \text{Take-Off Run Available}$$
$$\text{TODA} = \text{TORA} + \text{Clearway}, \quad \text{ASDA} = \text{TORA} + \text{Stopway}, \quad \text{LDA} = \text{Landing Distance Available}$$
Balanced field length requires reject distance at decision speed $V_1$ to equal continue distance to screen height ($35\text{ ft}$):
$$\text{BFL}: D_{\text{accel}}(0 \to V_1) + D_{\text{stop}}(V_1 \to 0) = D_{\text{accel}}(0 \to V_1) + D_{\text{climb}}(V_1 \to V_2 \text{ at } 35\text{ ft})$$

### 2. Turnaround Critical Path Scheduling & Queuing
Turnaround critical path duration $T_{\text{turn}}$ with parallel servicing streams:
$$T_{\text{turn}} = \max_{p \in \mathcal{P}_{\text{paths}}} \sum_{i \in p} d_i$$
Runway slot capacity $C_{\text{runway}}$ under wake separation time $t_{\text{sep}}$ and runway occupancy time $\text{ROT}$:
$$C_{\text{runway}} = \left\lfloor \frac{3600}{\mathbb{E}[t_{\text{sep}}] + \mathbb{E}[\text{ROT}]} \right\rfloor \text{ movements/hour}$$


---

## 2. Step-by-Step Numerical Verification & Sensitivity Trace


### Worked Numerical Example
- Aircraft turnaround: Narrow-body A320.
- Parallel streams:
  1. Deboarding ($12\text{ min}$) $\to$ Cabin Cleaning ($15\text{ min}$) $\to$ Boarding ($20\text{ min}$) $= 47\text{ min}$.
  2. Baggage offload ($14\text{ min}$) $\to$ Baggage onload ($18\text{ min}$) $= 32\text{ min}$.
  3. Refueling ($16\text{ min}$) started after deboarding completion $= 12 + 16 = 28\text{ min}$.
  4. Catering service ($12\text{ min}$) concurrent with cleaning $= 12 + 12 = 24\text{ min}$.
- Critical Path Duration $= 12 + 15 + 20 = 47\text{ minutes}$.
- Buffer allowance $3\text{ min} \implies$ Minimum Scheduled Ground Time $= 50\text{ minutes}$.


---

## 3. Operational & Regulatory Boundary Sensitivities

1. **Upper Critical Threshold**: Parameters that trigger mandatory regulatory interventions (e.g., maximum takeoff mass exceeding structural limit, flight duty period exceeding EASA FTL limit, or crosswind exceeding aircraft flight manual limit).
2. **Lower Critical Threshold**: Parameters below which operations become impermissible or economically unviable (e.g., fuel reserve below 30-minute final reserve, runway braking friction below minimum, or passenger load factor below break-even).
3. **Cross-Domain Ripple Factor**: How variance in this day's mathematical metric cascades into upstream airline planning or downstream air traffic management flow slots.
