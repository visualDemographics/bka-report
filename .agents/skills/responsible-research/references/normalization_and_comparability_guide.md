# Methodological Guide: Per-Capita Normalization, Accounting Boundaries & Cross-Domain Comparability

This guide establishes mathematical and accounting standards for normalizing empirical indicators across time, populations, currencies, and institutional boundaries.

---

## 1. Generalized Numerator-Denominator Alignment

Any empirical intensity or efficiency ratio takes the form:
$$R_{i,t} = \frac{Y_{i,t}}{D_{i,t}} \times k$$
where $Y_{i,t}$ is the aggregate output or resource flow for entity $i$ at time $t$, $D_{i,t}$ is the reference exposure denominator (population, full-time equivalent students, faculty count, land area), and $k$ is a scaling constant ($1$, $1{,}000$, or $100{,}000$).

### Core Rule of Boundary Equivalence:
The activity scope generating $Y_{i,t}$ must strictly equal the population scope counted in $D_{i,t}$:
$$\text{Scope}(Y_{i,t}) \equiv \text{Scope}(D_{i,t})$$

Whenever raw institutional or national aggregates include pass-through activities or non-resident outputs, researchers must define **Sensitivity & Boundary Tiers**:
* **Tier 0 (Raw Consolidated Quotient)**: Unadjusted headline total divided by headline denominator. (Must be labeled as unadjusted).
* **Tier 1 (Scope-Aligned Core)**: Removes external non-core pass-throughs (e.g., university teaching hospitals, federally managed defense labs, transit re-exports).
* **Tier 2 (Activity-Matched & PPP/Cohort Standardized)**: Matches specific functional budgets or outputs to specific active cohorts (e.g., instructional expenditure per FTE degree-seeking student, adjusted for PPP and disciplinary cost weights).

---

## 2. Case Study A: Cross-National University Benchmarking (TUM vs. MIT vs. ETH Zurich)

Comparing elite technical universities across Germany (TUM), the United States (MIT), and Switzerland (ETH Zurich) in terms of **student-facing budget per student** and **research quality** illustrates three classic methodological traps that must be corrected:

### Trap 1: Gross Consolidated Budget vs. Student-Facing Instructional Budget
* **TUM (Technical University of Munich)**:
  - State funding + third-party research (*Drittmittel*) + *Klinikum rechts der Isar* (university hospital).
  - Including clinical hospital patient care turnover ($>\text{€}1\text{B}$) in a university's budget per student artificially inflates resources available to engineering and science students.
  - Furthermore, TUM expanded rapidly to $>50{,}000$ enrolled students, creating a massive denominator shift relative to its fixed core state budget (*Grundfinanzierung*).
* **MIT (Massachusetts Institute of Technology)**:
  - Gross operating revenue ($>\$4.5\text{B}$) includes **MIT Lincoln Laboratory** ($\sim\$1.2\text{B}+$ federal DoD R&D contract), SMART (Singapore center), and auxiliary housing/dining enterprises.
  - However, MIT has a compact student body ($\sim 11{,}900$ total students: $\sim 4{,}600$ undergrads, $\sim 7{,}300$ grad students) and a massive endowment ($\sim\$23\text{B}+$) subsidizing campus instruction and student financial aid.
* **ETH Zurich**:
  - Financial reporting separates **ETH Zurich** ($\sim\text{CHF } 1.9\text{B}$ total budget, $\sim 25{,}000$ students) from the broader *ETH Domain* (which includes PSI, Empa, Eawag, WSL).
  - ETH enjoys a high proportion of stable federal core funding (*Trägerfinanzierung*, $\sim 70\%+$) that directly supports teaching infrastructure, laboratories, and assistantships, alongside competitive third-party funds (SNF, ERC).

### Harmonization Formula for Student-Facing Budget per FTE Student:
$$\text{Student-Facing Budget per FTE}_{u} = \frac{\text{Total Core Academic Budget}_{u} - \text{Hospital/Clinical}_{u} - \text{External National Labs}_{u} - \text{Non-Instructional Pure Research Pass-Through}_{u}}{\text{FTE Enrolled Students}_{u} \times \text{PPP Deflator}_{u}}$$

Breakdown into transparent tiers:
1. **Direct Instructional & Student Services Expenditure per FTE** (teaching staff salaries, lab courses, student support, libraries, teaching infrastructure).
2. **Research-Integrated Academic Expenditure per FTE** (adding departmental base budgets and doctoral/postdoc supervision that directly mentor Masters/Bachelor thesis students).
3. **Gross Total University Expenditure per Headcount** (reported only as Tier 0 baseline to illustrate the distortion of unadjusted rankings).

### Trap 2: Currency Exchange Rates vs. Academic Purchasing Power Parity (PPP)
* Converting CHF, EUR, and USD at spot FX overstates Swiss costs (due to strong nominal CHF and high Zurich salary levels) and ignores local purchasing power.
* Always report both **Nominal EUR/USD** and **OECD PPP-Adjusted USD/EUR**, and optionally normalize by **Academic Staff Cost Index** (e.g., "effective full-time teaching assistants or lab hours purchasable per student").

### Trap 3: Single-Metric Research Quality Gaming vs. Multi-Dimensional Quality Vector
* Volume metrics (total publications) favor large institutions with medical schools.
* Normalize research quality for scale and disciplinary mix:
  1. **Citation Excellence**: Share of publications in the **Top 1% and Top 10% most cited worldwide** (field-normalized, fractional counting via CWTS Leiden Ranking) and **Field-Weighted Citation Impact (FWCI)**.
  2. **Competitive Grant Density**: ERC Starting/Consolidator/Advanced Grants or NSF/DOE competitive awards **per 100 tenured/tenure-track faculty**.
  3. **Talent & Innovation Yield**: Deep-tech spin-offs, triadic patents, and highly cited researchers per $1{,}000$ academic staff.

---

## 3. Case Study B: Multi-Decade Per-Capita Commodity Output (Venezuela 50-Year Trajectory)

Analyzing declining production output per capita of key commodities over 50 years (e.g., 1975–2025 in Venezuela) requires rigorous time-series and demographic standardization:

### 1. Physical Units vs. Nominal Export Values
* Commodity price booms (e.g., 1979–1981 and 2004–2014 oil price spikes) mask severe physical production declines if output is measured in nominal USD revenue.
* **Mandatory Rule**: Track primary production in **intrinsic physical units per capita**:
  - **Crude Oil & Condensates**: Barrels per day per $1{,}000$ residents ($\text{bbl/d per 1k pop}$), or annual barrels per capita.
  - **Iron Ore & Crude Steel (SIDOR)**: Metric tons per $1{,}000$ residents.
  - **Primary Aluminum (ALCASA / VENALUM)**: Kilograms per capita.
  - **Electric Power Generation (Guri / SEN)**: Kilowatt-hours per capita ($\text{kWh/capita}$).
  - **Agricultural Staples (Corn/Maize, Coffee, Beef, Rice)**: Kilograms per capita ($\text{kg/capita}$).

### 2. Multi-Commodity Indexing ($\text{Base Year } t_0 = 100$)
* To compare decay rates across commodities with different physical units on a single synoptic panel, compute the normalized per-capita index relative to a transparent benchmark year $t_0$ (e.g., $1975 = 100$ or peak-decade average $= 100$):
  $$I_{c,t} = \left( \frac{Q_{c,t} / P_t}{Q_{c,t_0} / P_{t_0}} \right) \times 100$$
* To construct an aggregate **Composite Per-Capita Commodity Output Index**, weight each commodity $c$ using fixed constant-price international unit values $p_{c,\text{const}}$ (Laspeyres volume index per capita):
  $$I_{\text{composite}, t} = \frac{\sum_{c} p_{c,\text{const}} \cdot (Q_{c,t} / P_t)}{\sum_{c} p_{c,\text{const}} \cdot (Q_{c,t_0} / P_{t_0})} \times 100$$

### 3. Demographic Denominator Adjustments Under Mass Emigration
* Between 2015 and 2025, approximately $7.7\text{ million}$ Venezuelans emigrated ($\sim 25\%$ of the pre-crisis population).
* **Sensitivity Requirement**:
  - Using unrevised pre-2014 linear population projections ($>34\text{ million}$) artificially depresses post-2015 per-capita figures.
  - Using empirical migration-adjusted resident denominators (UN World Population Prospects 2024 revision / ENCOVI demographic reconstructions, $\sim 28\text{–}29\text{ million}$) yields the true domestic per-capita output—and reveals that even after accounting for a 20%+ smaller population denominator, per-capita physical output collapsed by $70\%\text{–}95\%$ across hydrocarbons, metallurgy, and agriculture.

### 4. Source Splicing & Concordance Under Statistical Censorship
* When domestic agencies (*Banco Central de Venezuela*, *Ministerio de Petróleo*, *INE*) delay or halt statistical series, splice time series using audited international registries:
  - Hydrocarbons: OPEC Annual Statistical Bulletin (distinguishing *Direct Communication* vs. *Secondary Sources*) and U.S. EIA / Energy Institute Statistical Review.
  - Metals & Minerals: USGS Minerals Yearbook & World Steel Association (*worldsteel*).
  - Agriculture: UN FAOSTAT production databases & USDA FAS.
  - Socio-Economic & Living Conditions: UCAB *ENCOVI* (*Encuesta Nacional de Condiciones de Vida*).
* Always verify overlap years (e.g., 1990–2013) to confirm that primary and secondary series match within $<2\%$ before splicing.

