# Day 302 — Mathematical & Analytical Walkthrough: Aviation security threats, threat assessment, access control and protection of critical assets.

[← Return to Lesson Document](README.md) | [Architecture Diagram](architecture.mermaid)

---

## 1. Mathematical Executive Summary: Safety Management Systems (SMS), 5x5 Risk Matrix & Cyber Vulnerability

Day 302 establishes the analytical equations, mathematical physics, and quantitative metrics governing **Aviation security threats, threat assessment, access control and protection of critical assets.**.


### 1. ICAO Doc 9859 Safety Risk Matrix Formulation
Risk Score $R$ as the product of Likelihood Index $L \in \{1, \dots, 5\}$ and Severity Index $S \in \{1, \dots, 5\}$:
$$R = L \times S, \quad \text{Risk Tolerability Classification:}$$
- $R \in [1, 4]$: Acceptable (Green)
- $R \in [5, 9]$: Tolerable with mitigation (Yellow)
- $R \in [10, 25]$: Intolerable (Red - Immediate operation shutdown)

### 2. Bow-Tie Barrier Probability & Hazard Occurrence Rate
For initiating threat frequency $\lambda_{\text{threat}}$ and independent protective safety barriers $b_1, \dots, b_k$ with failure probabilities $P(b_i)$:
$$\lambda_{\text{top event}} = \lambda_{\text{threat}} \times \prod_{i=1}^k P(b_i)$$
Mitigation effectiveness factor: $\eta_{\text{barrier}} = 1 - \prod P(b_i)$.


---

## 2. Step-by-Step Numerical Verification & Sensitivity Trace


### Worked Numerical Example
- Hazard: Unstabilized approach continuing to runway excursion.
- Historical frequency without barrier controls: $\lambda_{\text{threat}} = 1.2 \times 10^{-3}$ per approach.
- Safety Barriers implemented under SMS:
  1. Flight Data Monitoring (FDM) mandatory go-around policy ($P(b_1) = 0.15$ non-compliance rate).
  2. Enhanced Ground Proximity Warning System (EGPWS) callout ($P(b_2) = 0.04$ alert ignored).
  3. Runway Surface Grip & Grooving drainage ($P(b_3) = 0.10$ degraded braking coefficient).
- Resulting top event catastrophic excursion rate:
  $$\lambda_{\text{excursion}} = 1.2 \times 10^{-3} \times (0.15 \times 0.04 \times 0.10) = 1.2 \times 10^{-3} \times 0.0006 = 7.2 \times 10^{-7}\text{ per landing}$$
- Tolerability evaluation: Falls below catastrophic threshold $10^{-6} \implies$ ACCEPTABLE RISK UNDER SMS.


---

## 3. Operational & Regulatory Boundary Sensitivities

1. **Upper Critical Threshold**: Parameters that trigger mandatory regulatory interventions (e.g., maximum takeoff mass exceeding structural limit, flight duty period exceeding EASA FTL limit, or crosswind exceeding aircraft flight manual limit).
2. **Lower Critical Threshold**: Parameters below which operations become impermissible or economically unviable (e.g., fuel reserve below 30-minute final reserve, runway braking friction below minimum, or passenger load factor below break-even).
3. **Cross-Domain Ripple Factor**: How variance in this day's mathematical metric cascades into upstream airline planning or downstream air traffic management flow slots.
