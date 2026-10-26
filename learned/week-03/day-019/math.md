# Day 019 — Technical Walkthrough: Tracing an Operational Requirement from EU Law to Cockpit Action

[← Return to Lesson Guide](README.md) | [System Topology Canvas](architecture.mermaid) | [Run Python Simulator](experiment.py)

---

## 1. The Traceability Case Study: Flight Time Limitations & Commander's Discretion

To understand how high-level European law translates into real-time operational decisions, we trace a concrete, high-stakes operational requirement: **Flight Time Limitations (FTL) and the Commander's Discretion Procedure**.

Fatigue is one of the most insidious hazards in commercial aviation. If a flight crew exceeds legal duty hours, their cognitive response time and situational awareness degrade to levels equivalent to alcohol intoxication. Consequently, European law strictly bounds how long pilots can remain on duty, while providing an emergency legal mechanism for unexpected disruptions.

The legal journey from Brussels to the cockpit follows a five-step hierarchy:
$$\text{Basic Regulation (EU) 2018/1139} \longrightarrow \text{Implementing Reg (EU) 965/2012 Part-ORO} \longrightarrow \text{EASA Decision CS-FTL.1} \longrightarrow \text{Airline OM-A Section 7} \longrightarrow \text{Cockpit SOP \& Form 104}$$

---

## 2. Quantitative & Analytical Formulation of FTL Limits

### 1. Maximum Daily Flight Duty Period Calculation (`CS-FTL.1.205`)
Under European Certification Specifications, the maximum permissible daily Flight Duty Period ($\text{FDP}_{\text{max}}$) for an un-augmented crew is determined by the **Report Time** ($t_{\text{report}}$) and the **Number of Sectors** ($S$) planned:

$$\text{FDP}_{\text{max}} = f(t_{\text{report}}, S)$$

For an acclimatized crew reporting in the morning peak (06:00 to 13:29 local time):

| Sectors ($S$) | Maximum Permissible FDP ($\text{FDP}_{\text{max}}$) | WOCL Encroachment Deduction |
| :---: | :---: | :---: |
| **1 to 2 Sectors** | **13.00 hours** ($13\text{h }00\text{m}$) | $-100\%$ of encroachment time if report 05:00–05:59 |
| **3 Sectors** | **12.50 hours** ($12\text{h }30\text{m}$) | $-100\%$ of encroachment time if report 05:00–05:59 |
| **4 Sectors** | **12.00 hours** ($12\text{h }00\text{m}$) | $-100\%$ of encroachment time if report 05:00–05:59 |
| **5 Sectors** | **11.50 hours** ($11\text{h }30\text{m}$) | $-100\%$ of encroachment time if report 05:00–05:59 |
| **6 Sectors** | **11.00 hours** ($11\text{h }00\text{m}$) | $-100\%$ of encroachment time if report 05:00–05:59 |

If reporting between 17:00 and 04:59 (night operations encroaching on the **Window of Circadian Low - WOCL**), $\text{FDP}_{\text{max}}$ is compressed to between **9.00 and 11.00 hours**.

### 2. Commander's Discretion Boundary Condition (`ORO.FTL.205(f)`)
During actual flight operations, unforeseen delays (e.g. weather diversions, slot delays, minor mechanical fixes) occur. Under European Hard Law, the aircraft commander possesses a statutory power to extend the maximum FDP:

$$\text{FDP}_{\text{actual}} \le \text{FDP}_{\text{max}} + \Delta t_{\text{discretion}}$$

where:
- For an un-augmented crew, the absolute statutory limit is:
  $$\Delta t_{\text{discretion}} \le 2.0\text{ hours} \quad (120\text{ minutes})$$
- For an augmented crew with in-flight bunk rest facilities:
  $$\Delta t_{\text{discretion}} \le 3.0\text{ hours} \quad (180\text{ minutes})$$

### 3. Mandatory Safety Conditions for Discretion:
Before exercising discretion under `ORO.FTL.205(f)`:
1. **Unforeseen Nature**: The delay must have occurred *after* crew reporting (cannot be planned in advance by scheduling).
2. **Crew Consultation**: The Commander must formally consult all flight and cabin crew members regarding their physical fatigue state.
3. **Rest Compensation**: The subsequent minimum rest period must be increased by an amount equal to the discretion exercised:
   $$\text{Rest}_{\text{subsequent}} \ge \text{Rest}_{\text{nominal}} + \Delta t_{\text{discretion}}$$
4. **Authority Notification**: If $\Delta t_{\text{discretion}} > 1.0\text{ hour}$, the airline must submit the Commander's Discretion Report to the National Competent Authority within **28 days**.

---

## 3. Step-by-Step Worked Numerical Example: Frankfurt Multi-Sector Delay

Consider a European commercial crew operating a Boeing 737-800 on a 4-sector daily schedule:
- **Sector 1**: Frankfurt (EDDF) $\to$ Vienna (LOWW)
- **Sector 2**: Vienna (LOWW) $\to$ Frankfurt (EDDF)
- **Sector 3**: Frankfurt (EDDF) $\to$ Palma de Mallorca (LEPA)
- **Sector 4**: Palma de Mallorca (LEPA) $\to$ Frankfurt (EDDF)

### 1. Initial Planned FDP
- Crew Report Time: **06:30 local** at Frankfurt Base.
- Planned Sectors: $S = 4$.
- Looking up `CS-FTL.1.205`: For 06:30 report with 4 sectors:
  $$\text{FDP}_{\text{max}} = 12.00\text{ hours} \quad (720\text{ minutes})$$
- Latest legal shutdown time (without discretion):
  $$t_{\text{shutdown\_max}} = 06:30 + 12:00 = \mathbf{18:30\ \text{local}}$$

### 2. The Operational Delay Event
- While turning around in Palma de Mallorca for Sector 4, a major thunderstorm line closes the Palma departure corridor for 1 hour 45 minutes.
- Estimated Sector 4 flight time: 2 hours 10 minutes.
- Projected arrival and engine shutdown at Frankfurt: **19:40 local**.
- Projected FDP duration:
  $$\text{FDP}_{\text{projected}} = 19:40 - 06:30 = 13\text{ hours } 10\text{ minutes} = 13.17\text{ hours}$$
- Deficit vs Base FDP:
  $$\Delta t_{\text{overrun}} = 13\text{h }10\text{m} - 12\text{h }00\text{m} = \mathbf{1\text{ hour } 10\text{ minutes}}$$

### 3. Legal Analysis & Decision
1. Is $\Delta t_{\text{overrun}} \le 2.0\text{ hours}$? Yes ($1\text{h }10\text{m} \le 2\text{h }00\text{m}$).
2. Captain conducts formal crew briefing in the cockpit: all crew confirm they feel alert and fit to operate.
3. Captain signs the **Commander's Discretion Authorization** in the Aircraft Technical Logbook.
4. Flight departs at 17:25, lands safely at Frankfurt at 19:35 local.
5. Because $\Delta t = 70\text{ min} > 60\text{ min}$, Captain completes **Form FTL-104** within 24 hours; airline Safety Office logs the event and submits a copy to the German LBA within 28 days.

---

## 4. The Illegal Command: Dispatch Pressure vs Commander Authority

What happens if the ground delay in Palma lasted 2 hours 45 minutes?
- Projected FDP would be $14\text{ hours } 45\text{ minutes}$.
- Overrun would be $2\text{ hours } 45\text{ minutes}$, which **exceeds the 2-hour legal limit**.
- Under **`CAT.GEN.MPA.105` (Responsibilities of the Commander)**:
  > The Captain has the non-negotiable legal obligation to refuse the flight.
- If an airline operations controller orders the crew to fly anyway, the controller is ordering an illegal flight. If the Captain takes off, the flight is uninsured, and both the Captain and Accountable Manager face criminal sanctions under national aviation law.
