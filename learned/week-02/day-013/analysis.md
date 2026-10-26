# Day 013 — Technical Walkthrough: Connecting International Standards to Certificates, Operational Approvals, and Local Procedures

[← Return to Lesson Guide](README.md) | [System Topology Canvas](architecture.mermaid) | [Run Python Simulator](experiment.py)

---

## 1. The Operational Translation Spine

International civil aviation standards established in Montreal by ICAO are neither self-executing nor directly enforceable on an airline captain sitting on a flight deck. For an ICAO Standard in **Annex 6 (Operation of Aircraft)** or **Annex 8 (Airworthiness)** to govern a flight, it must travel down a rigorous translation spine:

$$\text{ICAO Annexes (SARPs)} \longrightarrow \text{State Regulations (e.g. EASA Part-SPA / FAR 121)} \longrightarrow \text{AOC \& Operations Specifications (OpSpecs)} \longrightarrow \text{Aircraft AFM / MEL} \longrightarrow \text{Flight Operations Manual (OM-A/B/C/D)} \longrightarrow \text{Local AIP Procedures}$$

Every high-risk commercial operation requires a cascade of synchronized approvals:
1. **The Airline (AOC & OpSpecs)**: The civil aviation authority grants specific operational authorizations listed in the **Operations Specifications (OpSpecs)**.
2. **The Aircraft (Type Certificate, C of A, AFM)**: The specific tail number must be equipped, certified, and maintained under an approved maintenance program (e.g., dual autoland systems, cargo fire suppression).
3. **The Flight Crew (Licenses & Training)**: Pilots must hold current type ratings and recurrent training qualifications for that specific operational envelope (e.g. annual simulator autoland checks).
4. **The Local Aerodrome (AIP AD 2 & LVP)**: The ground infrastructure must support the operation (e.g., Cat III Instrument Landing System, Low Visibility Procedures declared active by ATC).

---

## 2. Quantitative & Analytical Formulations

### 1. Extended Diversion Time Operations (EDTO / ETOPS) Dispatch Envelope
Under ICAO Annex 6, twin-engine turbine airliners operating beyond the threshold time (typically 60 minutes from an adequate aerodrome at one-engine-inoperative cruise speed) must hold an **ETOPS / EDTO Specific Approval**.

The maximum permissible diversion distance $D_{\text{max}}$ from any point along the route to an en-route alternate is:

$$D_{\text{max}} = V_{\text{OEI}} \times \left( \frac{T_{\text{ETOPS}}}{60} \right)$$

where:
- $V_{\text{OEI}}$ is the approved One-Engine-Inoperative (OEI) true airspeed in standard atmosphere (KTAS).
- $T_{\text{ETOPS}}$ is the approved ETOPS diversion time limit in minutes (e.g. 120, 180, 240, 370 min).

For a flight plan to be legal under OpSpecs:
$$\forall P \in \text{Route}, \quad \min_{i \in \text{Alternates}} \text{Dist}(P, A_i) \le D_{\text{max}}$$

Furthermore, every nominated ETOPS alternate must forecast weather above **Dispatch Alternate Minima** at the estimated time of arrival (ETA $\pm 1$ hour).

### 2. All-Weather Operations: Low Visibility Operations (LVO / CAT III)
Under ICAO Annex 6 and national regulations (e.g. EASA Part-SPA.LVO), precision instrument approach categories dictate the minimum Decision Height (DH) and Runway Visual Range (RVR):

| Approach Category | Minimum Decision Height (DH) | Minimum Runway Visual Range (RVR) | Required Ground & Airborne Systems |
| :--- | :--- | :--- | :--- |
| **Category I** | $\ge 200\text{ ft}$ ($60\text{ m}$) | $\ge 550\text{ m}$ | Standard ILS, single-channel autopilot or manual flight |
| **Category II** | $100\text{ ft} \le \text{DH} < 200\text{ ft}$ | $\ge 300\text{ m}$ | Cat II ILS, fail-passive flight control, inner marker |
| **Category IIIa** | $50\text{ ft} \le \text{DH} < 100\text{ ft}$ | $\ge 175\text{ m}$ | Fail-passive autoland, dual radio altimeters |
| **Category IIIb** | $\text{DH} < 50\text{ ft}$ or No DH | $75\text{ m} \le \text{RVR} < 175\text{ m}$ | Fail-operational autoland with rollout control / guidance |
| **Category IIIc** | No DH | No RVR limitation (Zero-Zero) | Fully automatic landing and taxi guidance |

### 3. The 4-Pillar Operational Authorization Verification Matrix
For any specialized flight operation $\Omega \in \{\text{CAT IIIb}, \text{ETOPS 180}, \text{RVSM}, \text{RNP AR 0.1}\}$:

$$\Phi(\Omega) = \mathbf{1}_{\text{OpSpec}} \times \mathbf{1}_{\text{Aircraft}} \times \mathbf{1}_{\text{Crew}} \times \mathbf{1}_{\text{Facility}}$$

where each indicator $\mathbf{1} \in \{0, 1\}$ represents:
- $\mathbf{1}_{\text{OpSpec}} = 1$ if operator holds valid Specific Approval in AOC Operations Specifications.
- $\mathbf{1}_{\text{Aircraft}} = 1$ if aircraft tail number has AFM certification and no disqualifying MEL defects (e.g. dual autopilots serviceable).
- $\mathbf{1}_{\text{Crew}} = 1$ if both flight crew members have current recurrent check and line qualification.
- $\mathbf{1}_{\text{Facility}} = 1$ if local aerodrome has published procedure and active operational safeguards (e.g. ATC Low Visibility Procedures active, ILS critical sensitive areas protected).

If $\Phi(\Omega) = 0$, the flight crew **cannot legally execute the operation**.

---

## 3. Step-by-Step Worked Numerical Example: London to New York Diversion & CAT IIIb Autoland

Consider a twin-engine widebody (Airbus A350-900) operating transatlantic:

### 1. ETOPS 180 Dispatch Verification
- Approved OEI Speed: $V_{\text{OEI}} = 425\text{ KTAS}$.
- Operator OpSpec Limit: $T_{\text{ETOPS}} = 180\text{ minutes}$.
- Max diversion radius:
  $$D_{\text{max}} = 425 \times \left( \frac{180}{60} \right) = 425 \times 3.0 = 1,275\text{ NM}$$
- Route Point: Mid-Atlantic at 52°N 035°W.
- Nearest En-Route Alternates:
  - Shannon (EINN): 1,120 NM
  - Keflavik (BIKF): 890 NM
  - Gander (CYQX): 1,040 NM
- Since $\min(1120, 890, 1040) = 890\text{ NM} \le 1,275\text{ NM}$, the flight plan is **LEGAL for ETOPS 180**.

### 2. Destination Arrival & Low Visibility CAT IIIb Approach into Paris CDG (LFPG)
As the flight arrives, dense radiation fog covers Paris Charles de Gaulle:
- Reported Runway 26L Weather: METAR LFPG $\dots$ **RVR 125m / 100m / 100m, Vertical Visibility 50 ft**.
- Operational requirements for CAT IIIb:
  - Required RVR: $75\text{ m} \le 125\text{ m} \implies$ **RVR satisfies CAT IIIb criteria**.
- Verification of 4 Pillars:
  1. Airline OpSpec: EASA Part-SPA.LVO authorization active $\implies \mathbf{1}_{\text{OpSpec}} = 1$.
  2. Aircraft Serviceability: Both Autopilot channels (AP1 + AP2) engaged in `LAND` mode, dual radio altimeters operative, auto-thrust operative, no MEL restrictions $\implies \mathbf{1}_{\text{Aircraft}} = 1$.
  3. Flight Crew: Both Captain and First Officer hold valid CAT II/III annual simulator evaluations and 3 autolands logged in preceding 90 days $\implies \mathbf{1}_{\text{Crew}} = 1$.
  4. Aerodrome Safeguards: Paris CDG ATIS states: *"Low Visibility Procedures (LVP) are in force. Cat II/III hold points in use, secondary power supply on"* $\implies \mathbf{1}_{\text{Facility}} = 1$.

$$\Phi(\text{CAT IIIb}) = 1 \times 1 \times 1 \times 1 = 1 \implies \mathbf{CLEARED\ FOR\ CAT\ IIIb\ AUTOLAND}$$

---

## 4. Adversarial Degradation Trace: Autopilot Channel Loss

At 800 ft AGL on final approach:
- System Fault: Master Caution illuminates; `AUTO FLT AP 2 FAULT` messages appear on ECAM.
- Impact on Capability: Aircraft capability degrades from **Fail-Operational (CAT IIIb)** to **Fail-Passive (CAT IIIa)**.
- For CAT IIIa, minimum RVR required is **175 m**.
- Actual reported touchdown RVR is **125 m**.
- Decision:
  $$\text{Actual RVR } (125\text{ m}) < \text{Degraded Minimum RVR } (175\text{ m}) \implies \Phi(\text{CAT IIIa}) = 0$$
- Mandatory Action: Captain immediately disengages approach, calls **"GO AROUND, FLAPS"**, executes missed approach procedure, and diverts to alternate airport.
