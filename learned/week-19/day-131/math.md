# Day 131 — Mathematical & Analytical Walkthrough: Trace a fictional bag from check-in through transfer to final delivery.

[← Return to Lesson Document](README.md) | [Architecture Diagram](architecture.mermaid)

---

## 1. Mathematical Executive Summary: Passenger Terminal Flow, Baggage Sorting & Cargo Mass Modeling

Day 131 establishes the analytical equations, mathematical physics, and quantitative metrics governing **Trace a fictional bag from check-in through transfer to final delivery.**.


### 1. Terminal Queuing: Kendall M/M/s System Dynamics
Arrival rate $\lambda$ (pax/min) and service rate $\mu$ per lane across $s$ security checkpoints:
$$\text{Traffic Intensity } \rho = \frac{\lambda}{s \mu} < 1$$
Probability of zero passengers in queue $P_0$:
$$P_0 = \left[ \sum_{n=0}^{s-1} \frac{(s \rho)^n}{n!} + \frac{(s \rho)^s}{s!(1 - \rho)} \right]^{-1}$$
Average queue wait time $W_q$ (Erlang-C formulation):
$$P_{\text{wait}} = \frac{(s \rho)^s}{s!(1 - \rho)} P_0, \quad W_q = \frac{P_{\text{wait}}}{s \mu - \lambda}$$

### 2. Baggage Sortation Throughput & Missed Bag Rate
For $N$ connecting bags with transfer window $\Delta t$, sorting transit velocity $v$, and scan error $\epsilon$:
$$P(\text{Mishandled}) = 1 - \Phi\left(\frac{\Delta t - \mu_{\text{transfer}}}{\sigma_{\text{transfer}}}\right) + \epsilon$$


---

## 2. Step-by-Step Numerical Verification & Sensitivity Trace


### Worked Numerical Example
- Terminal peak hour passenger arrival rate $\lambda = 1200\text{ pax/hour} = 20\text{ pax/min}$.
- Security lane throughput $\mu = 3.2\text{ pax/min}$ per x-ray line.
- Number of active lanes $s = 8$.
- Utilization factor:
  $$\rho = \frac{20}{8 \times 3.2} = \frac{20}{25.6} = 0.78125 \quad (78.1\%)$$
- Calculated average wait in security queue:
  $$W_q \approx 1.84\text{ minutes}$$
- If 2 lanes close ($s = 6$): $\rho = 20 / 19.2 = 1.0417 > 1.0 \implies$ Queue becomes unstable and expands at $0.8\text{ pax/minute}$ without bound.


---

## 3. Operational & Regulatory Boundary Sensitivities

1. **Upper Critical Threshold**: Parameters that trigger mandatory regulatory interventions (e.g., maximum takeoff mass exceeding structural limit, flight duty period exceeding EASA FTL limit, or crosswind exceeding aircraft flight manual limit).
2. **Lower Critical Threshold**: Parameters below which operations become impermissible or economically unviable (e.g., fuel reserve below 30-minute final reserve, runway braking friction below minimum, or passenger load factor below break-even).
3. **Cross-Domain Ripple Factor**: How variance in this day's mathematical metric cascades into upstream airline planning or downstream air traffic management flow slots.
