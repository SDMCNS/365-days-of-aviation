# Day 224 — Mathematical & Analytical Walkthrough: Explain the difference between a communication technology and the service delivered using it.

[← Return to Lesson Document](README.md) | [Architecture Diagram](architecture.mermaid)

---

## 1. Mathematical Executive Summary: CNS Link Budgets, GNSS Dilution of Precision & ADS-B Coverage

Day 224 establishes the analytical equations, mathematical physics, and quantitative metrics governing **Explain the difference between a communication technology and the service delivered using it.**.


### 1. Free Space Path Loss & Radio Link Budget
Aeronautical VHF/UHF propagation loss over distance $d$ at carrier frequency $f$:
$$\text{FSPL (dB)} = 20 \log_{10}(d) + 20 \log_{10}(f) + 20 \log_{10}\left(\frac{4 \pi}{c}\right) = 32.44 + 20 \log_{10}(d_{\text{km}}) + 20 \log_{10}(f_{\text{MHz}})$$
Received power:
$$P_{\text{rx}} = P_{\text{tx}} + G_{\text{tx}} + G_{\text{rx}} - \text{FSPL} - L_{\text{cable}} \ge S_{\text{receiver sensitivity}}$$

### 2. GNSS Geometric Dilution of Precision (GDOP)
With pseudorange error covariance $\mathbf{Q} = (\mathbf{G}^T \mathbf{G})^{-1}$, where $\mathbf{G}$ is the geometry matrix:
$$\text{GDOP} = \sqrt{\text{trace}(\mathbf{Q})} = \sqrt{\sigma_x^2 + \sigma_y^2 + \sigma_z^2 + \sigma_t^2}$$
Total positioning error: $\sigma_{\text{pos}} = \text{PDOP} \times \text{UERE}$.


---

## 2. Step-by-Step Numerical Verification & Sensitivity Trace


### Worked Numerical Example
- Aeronautical VHF communication: $f = 128.5\text{ MHz}$, Distance $d = 100\text{ NM} = 185.2\text{ km}$.
- Free Space Path Loss:
  $$\text{FSPL} = 32.44 + 20 \log_{10}(185.2) + 20 \log_{10}(128.5) = 32.44 + 45.35 + 42.18 = 119.97\text{ dB}$$
- Transmitter power: $P_{\text{tx}} = 25\text{ W} = +44.0\text{ dBm}$.
- Antenna gains: $G_{\text{tx}} = +3.0\text{ dBi}$, $G_{\text{rx}} = +2.0\text{ dBi}$. Cable loss: $L_{\text{loss}} = 2.5\text{ dB}$.
- Received signal strength:
  $$P_{\text{rx}} = 44.0 + 3.0 + 2.0 - 119.97 - 2.5 = -73.47\text{ dBm}$$
- Receiver squelch threshold is $-98.0\text{ dBm}$.
- Link margin: $\text{Margin} = -73.47 - (-98.0) = +24.53\text{ dB} \implies$ EXCELLENT AUDIO SIGNAL QUALITY.


---

## 3. Operational & Regulatory Boundary Sensitivities

1. **Upper Critical Threshold**: Parameters that trigger mandatory regulatory interventions (e.g., maximum takeoff mass exceeding structural limit, flight duty period exceeding EASA FTL limit, or crosswind exceeding aircraft flight manual limit).
2. **Lower Critical Threshold**: Parameters below which operations become impermissible or economically unviable (e.g., fuel reserve below 30-minute final reserve, runway braking friction below minimum, or passenger load factor below break-even).
3. **Cross-Domain Ripple Factor**: How variance in this day's mathematical metric cascades into upstream airline planning or downstream air traffic management flow slots.
