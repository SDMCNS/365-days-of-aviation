# Day 026 — Technical Walkthrough: Primary Source Regulatory Research & Applicability Analysis

[← Return to Lesson Guide](README.md) | [System Topology Canvas](architecture.mermaid) | [Run Python Simulator](experiment.py)

---

## 1. The Primary Source Research Methodology in Civil Aviation

Aviation safety depends on absolute legal and technical precision. Secondary summaries, training handbooks, and internet articles are prone to truncation and outdated guidance. A professional aviation analyst or operations engineer must be able to locate, analyze, and document the exact applicability of a statutory requirement using **primary legal sources**.

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                   PRIMARY SOURCE REGULATORY RESEARCH METHODOLOGY                                 │
├───────────────────┬───────────────────┬───────────────────┬──────────────────────────────────────┤
│ STEP 1:           │ STEP 2:           │ STEP 3:           │ STEP 4:                              │
│ LOCATE PRIMARY    │ MAP STATUTORY     │ ANALYZE HARD VS   │ DOCUMENT EXACT                       │
│ INSTRUMENT        │ APPLICABILITY     │ SOFT PROVISIONS   │ OPERATIONAL APPLICABILITY            │
├───────────────────┼───────────────────┼───────────────────┼──────────────────────────────────────┤
│ Search Eur-Lex    │ Basic Reg Scope   │ Differentiate:    │ Define:                              │
│ Official Journal  │ • Aircraft Type   │ • IR (Hard Law)   │ • Fleet types covered                │
│ & EASA Repository │ • Commercial vs GA│ • CS (Tech Specs) │ • Operational phase                  │
│ for authentic act.│ • Territory/AOC   │ • AMC (Safe harbor│ • Exemptions / conditions            │
│                   │                   │ • GM (Explanations│ • Company manual citation            │
└───────────────────┴───────────────────┴───────────────────┴──────────────────────────────────────┘
```

---

## 2. In-Depth Case Study: Lithium Batteries & Passenger PEDs

To demonstrate primary source research, we dissect the rules governing **Portable Electronic Devices (PEDs) and Lithium Batteries in Commercial Aviation**.

### Primary Source Documents:
1. **Hard Law**: Commission Regulation (EU) No 965/2012, Annex IV (Part-CAT):
   - **`CAT.GEN.MPA.140`**: *Portable electronic devices (PEDs)*
   - **`CAT.GEN.MPA.200`**: *Transport of dangerous goods*
2. **Soft Law (Acceptable Means of Compliance)**: EASA ED Decision 2014/015/R (as amended):
   - **`AMC1 CAT.GEN.MPA.140`**: Technical conditions for permitting PEDs across all flight phases.
   - **`AMC2 CAT.GEN.MPA.140`**: Crew procedures and passenger briefing standards.
3. **Soft Law (Guidance Material)**:
   - **`GM1 CAT.GEN.MPA.140`**: Electromagnetic interference (EMI) risk assessment and back-fire protection.
4. **Safety Guidance & Standards**:
   - EASA **Safety Information Bulletin (SIB) 2017-01R1**: *Passenger baggage containing lithium batteries*.
   - ICAO **Doc 9284**: *Technical Instructions for the Safe Transport of Dangerous Goods by Air* (Part 8).

---

## 3. Statutory Deconstruction: Article-by-Article Analysis

### 1. `CAT.GEN.MPA.140` (The Implementing Rule — Hard Law)
> *(a) The operator shall not permit any person to use a portable electronic device (PED) on board an aircraft that could adversely affect the performance of the aircraft’s systems and equipment.*  
> *(b) The operator shall take all reasonable measures to ensure that passengers are informed of the conditions under which PEDs may be used.*

**Legal Nature**: Directly binding on all EASA Air Operator Certificate (AOC) holders. Failure to implement triggers an immediate non-compliance finding.

### 2. `AMC1 CAT.GEN.MPA.140` (Soft Law — Presumption of Conformity)
Defines how an airline proves non-interference:
- An operator may allow continuous use of lightweight handheld PEDs in all phases of flight (including taxi, takeoff, and landing) provided the aircraft type has demonstrated **front-door and back-door EMI tolerance** according to **`RTCA DO-363 / EUROCAE ED-239`** standards.
- If the aircraft is not certified PED-tolerant, PEDs must be switched off or placed in "Airplane Mode" during critical flight phases (takeoff, approach, landing).

### 3. ICAO Doc 9284 & EASA SIB 2017-01R1 (Lithium Battery Thresholds)
- **Lithium Metal (Non-rechargeable)**: Maximum $2\text{ grams}$ lithium content.
- **Lithium Ion (Rechargeable)**:
  - $\le 100\text{ Watt-hours (Wh)}$: Permitted in carry-on baggage without operator approval. Permitted in checked baggage *only if completely switched off and protected against inadvertent activation*.
  - **Spare Batteries & Power Banks**: **STRICTLY PROHIBITED IN CHECKED BAGGAGE**. Must be carried in the passenger cabin where thermal runaway can be fought immediately.
  - $> 100\text{ Wh to } 160\text{ Wh}$: Permitted in carry-on baggage with operator approval (maximum 2 spare batteries per passenger).
  - $> 160\text{ Wh}$: Completely forbidden for passenger transport (must be shipped as cargo under full dangerous goods regulations).

---

## 4. Quantitative & Analytical Physics: Battery Thermal Runaway Energy

When a lithium-ion cell experiences an internal short circuit (mechanical damage, manufacturing defect, or overcharging), it enters an uncontrollable **thermal runaway** reaction:

### 1. Electrochemical Energy Content
The electrical energy stored in a battery pack of capacity $C$ (Ampere-hours) and nominal voltage $V$ is:

$$E_{\text{elec}} = V \cdot C \quad [\text{Watt-hours}] = V \cdot C \times 3,600 \quad [\text{Joules}]$$

For a high-capacity laptop battery ($100\text{ Wh}$):
$$E_{\text{elec}} = 100 \times 3,600 = 360,000\text{ Joules } (360\text{ kJ})$$

### 2. Total Thermal Energy Release
During thermal runaway, the chemical energy released by decomposition of the cathode and organic electrolyte exceeds electrical storage by a factor of 3 to 5:

$$Q_{\text{thermal}} \approx 4.0 \cdot E_{\text{elec}} = 4.0 \times 360\text{ kJ} = 1,440\text{ kJ}$$

### 3. Extinguishment & Cooling Thermodynamics
Halon 1211 / 2402 extinguishers extinguish open flames but **cannot cool the internal battery cells**. If water is not applied, runaway propagates from cell to cell.

The minimum mass of water $m_w$ required to absorb $Q_{\text{thermal}}$ via sensible heating ($c_w = 4.184\text{ kJ/kg}\cdot^\circ\text{C}$, $\Delta T = 80^\circ\text{C}$) and vaporization ($L_v = 2,260\text{ kJ/kg}$):

$$Q_{\text{absorbed}} = m_w \cdot \left[ c_w \Delta T + L_v \right] = m_w \cdot [ (4.184 \times 80) + 2,260 ] = m_w \cdot 2,595\text{ kJ/kg}$$

$$m_w = \frac{1,440\text{ kJ}}{2,595\text{ kJ/kg}} \approx \mathbf{0.55\text{ kg } (0.55\text{ Litres of water})}$$

This physical reality directly justifies **`AMC2 CAT.GEN.MPA.140`**: Cabin crew must extinguish flames with Halon and then immediately douse the device with water or non-alcoholic liquid, storing it in a dedicated fire containment bag.

---

## 5. Worked Applicability Trace Table

| Dimension | Primary Legal Citation | Applicable Scope | Exemptions / Restrictions | Company Manual Citation |
| :--- | :--- | :--- | :--- | :--- |
| **Aircraft Operating Minima** | `CAT.OP.MPA.110` | EASA AOC Flights | None without Specific Approval | OM-A Section 8.4 |
| **Passenger PED Usage** | `CAT.GEN.MPA.140` | All EASA CAT aircraft | Non-transmitting only if uncertified | OM-A Section 8.3.1 |
| **Spare Lithium Batteries** | ICAO Doc 9284 / SIB 2017-01 | Passenger carry-on only | Prohibited in checked baggage | OM-A Section 9.2 (Dangerous Goods) |
| **Smart Luggage (Bags)** | EASA SIB 2017-01R1 | Luggage with power banks | Battery must be removable | Check-in & Gate Procedures |

---

## 6. Summary & Key Takeaways

1. **Trace to the Authentic Enacting Regulation**: Never rely on a company bullet point without verifying the exact paragraph in `CAT.GEN.MPA.140` or ICAO Doc 9284.
2. **Safety Rules are Grounded in Physics**: The ban on spare lithium batteries in the cargo hold exists because Halon cannot penetrate thermal runaway cells in checked baggage; in the cabin, crew can apply water.
3. **Document Exact Boundaries**: Always specify who is covered, who is exempt, what thresholds apply, and which internal company manual implements the law.
