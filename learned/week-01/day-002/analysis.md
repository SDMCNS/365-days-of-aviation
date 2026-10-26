# Day 002 — Operational & Quantitative Analysis: Aircraft Turnaround Critical Path & Stakeholder Interface Cascades

[← Return to Lesson Guide](README.md) | [System Topology Canvas](architecture.mermaid) | [Run Python Simulator](experiment.py)

---

## 1. The Ecosystem Interface Reality

An aircraft produces economic value only when flying. On the ground, it incurs capital amortization, parking fees, handling charges, and maintenance wear. The primary operational interface where all aviation stakeholders physically collide is the **aircraft turnaround** on the aerodrome ramp.

Under Airport Collaborative Decision Making (**A-CDM**, ICAO Doc 9971 / Eurocontrol A-CDM Manual), an aircraft turnaround is not treated as a black box. It is tracked as a synchronized sequence of discrete milestone events shared between the **Airline OCC**, the **Aerodrome Operator**, **Ground Handlers**, and **Air Traffic Control (ATC)**.

---

## 2. Quantitative Model: Turnaround Critical Path & Delay Cascades

The total turnaround duration is determined not by the sum of all tasks, but by the **Critical Path**—the longest sequence of dependent activities that cannot be performed in parallel.

### 1. Parallel & Sequential Activity Vectors
Let a standard 40-minute narrowbody turnaround (e.g., Airbus A320 or Boeing 737) be partitioned into parallel sub-systems:

$$\text{Subsystem 1 (Passenger Flow): } t_{\text{deboard}} \longrightarrow t_{\text{cabin\_clean}} \longrightarrow t_{\text{boarding}} \longrightarrow t_{\text{doors\_closed}}$$
$$\text{Subsystem 2 (Baggage / Cargo Flow): } t_{\text{bag\_offload}} \longrightarrow t_{\text{hold\_inspect}} \longrightarrow t_{\text{bag\_load}} \longrightarrow t_{\text{hold\_doors\_closed}}$$
$$\text{Subsystem 3 (Technical & Fueling): } t_{\text{ground\_power}} \longrightarrow t_{\text{fueling}} \longrightarrow t_{\text{tech\_log\_signoff}}$$
$$\text{Subsystem 4 (Catering & Servicing): } t_{\text{potable\_water/lavatory}} \parallel t_{\text{catering\_truck}}$$

### 2. Operational Interlocks & Safety Constraints
- **Fueling Safety Rule (EASA CAT.OP.MPA.195)**: Aircraft fueling while passengers are embarking or disembarking is legally permissible *only* if designated cabin exits are clear, ground fire lanes are unobstructed, and a qualified two-way communication link is maintained between the flight crew and fueling operator.
- **Hold Closure Interlock**: Under international security regulations (ICAO Annex 17), if a checked passenger fails to board (no-show), that passenger's baggage **must be identified and offloaded** before departure clearance can be granted.
- **Loadsheet Calculation**: The final weight & balance trim sheet can only be computed and signed by the Pilot-in-Command (PIC) after actual passenger numbers and final baggage counts are locked.

### 3. Critical Path Duration Formulation
$$\text{Duration}_{\text{critical}} = \max\left( T_{\text{passenger\_chain}}, T_{\text{baggage\_chain}}, T_{\text{fueling\_chain}} \right)$$

$$\text{Actual Off-Block Time (AOBT)} = \max\left( \text{Chocks-On} + \text{Duration}_{\text{critical}}, \text{ATC TSAT} \right)$$

Where **TSAT** is the Target Start-Up Approval Time issued by ATC based on airspace flow constraints (ATFM).

---

## 3. Step-by-Step Worked Numerical Example

Consider an Airbus A320 arriving at Stand 14 with scheduled turnaround $T_{\text{sched}} = 40\text{ minutes}$.

- Inbound Chocks-On: `12:00 UTC`
- Scheduled Off-Block Time (SOBT): `12:40 UTC`
- ATFM Slot Calculated Take-Off Time (CTOT): `12:55 UTC` (with $\pm 5$ min slot tolerance: `12:50 - 13:00 UTC`). Estimated taxi time = 12 minutes. Thus, pushback must occur no later than `12:43 UTC` to hit the slot.

### Baseline Durations (Minutes)
1. Passenger Chain: Deboard (10m) + Cleaning (10m) + Boarding (16m) = **36 minutes**
2. Baggage Chain: Offload (12m) + Loading (16m) = **28 minutes**
3. Fueling: Setup (4m) + Fuel Uplift 6,000 kg @ 800 kg/min (7.5m) + Disconnect (3m) = **14.5 minutes**

$$\text{Nominal Turnaround} = \max(36, 28, 14.5) = 36\text{ minutes} \longrightarrow \text{Ready at 12:36 UTC (4 min buffer)}.$$

### Disruption Scenario: No-Show Passenger Baggage Search
At `12:34 UTC` (2 minutes before planned ready time), Passenger Seat 14B fails to board.
- Gate closes; reconciliation shows 1 bag in Bulk Aft Hold.
- Ground handler must open Aft Hold, scan luggage tags, locate bag, and offload: $+12\text{ minutes}$.
- Revised Baggage Chain Completion: $28 + 12 = \mathbf{40\text{ minutes}}$.
- Revised Passenger Chain: Recalculate revised loadsheet and trim: $+4\text{ minutes}$ from `12:36` = `12:40 UTC`.
- New Target Off-Block Time (TOBT): `12:48 UTC`.
- Add 12 min taxi time $\longrightarrow$ Estimated Take-Off Time = `13:00 UTC`.
- **Result**: The aircraft hits the very last minute of the CTOT slot window (`12:50 - 13:00 UTC`). If the baggage offload had taken 13 minutes instead of 12, the slot would be **missed**, triggering an ATFM slot suspension and a new delay penalty of 45–90 minutes.

---

## 4. Operational & Regulatory Boundary Sensitivities

1. **Reactionary (Downstream) Delay Ripple**: Narrowbody airliners typically fly 4 to 6 sectors per day. A 15-minute delay on Sector 1 cascades into every downstream flight, often terminating in night curfew violations or crew flight duty period (FTL) exceedances on Sector 5.
2. **A-CDM Milestone Accuracy**: If an airline OCC fails to update TOBT accurately within 5 minutes of projected readiness, Eurocontrol's Network Manager cancels the aircraft's pre-departure sequencing, placing it at the back of the departure queue.
3. **Stand Obstruction**: A grounded aircraft on stand blocks incoming arriving flights, forcing inbound aircraft to hold on taxiways with engines running, burning excess fuel and emitting unnecessary $\text{CO}_2$.
