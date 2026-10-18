# Methodology, Assumptions & Analytical Boundaries (`/methodology`)
## Scientific Protocol for Responsible Demographics and Causal Inference on Police Registries

---

### 1. Administrative Nature of the Police Crime Statistics (PKS)
The Police Crime Statistics (PKS) published annually by the Federal Criminal Police Office (BKA) is an **investigative and administrative workload register of the police**, not a criminological census of all crime committed in society and not a judicial conviction register:
1. **Suspects $\neq$ Convicts**: The PKS registers police-identified suspects at the conclusion of police investigation and transmission of case files to the public prosecutor's office. The presumption of innocence applies; judicial dismissals, plea bargains, or acquittals are never reflected in the PKS.
2. **Registered Crime (*Hellfeld*) $\neq$ Total Delinquency**: Only offenses reported to or detected by police are registered. Offenses with low reporting propensity (darkfield / *Dunkelfeld*) distort official figures.
3. **Absence of Socioeconomic Indicators**: The PKS registers **no individual data on income, schooling, educational attainment, wealth, employment, or housing conditions** of suspects. Causal statements regarding individual socioeconomic pathways cannot be derived directly from the PKS alone.

---

### 2. The Numerator-Denominator Mismatch (*Das Nennerproblem*)
* **Numerator**: All suspects apprehended within German federal territory during the calendar year. This includes individuals who do not reside in Germany (tourists, cross-border commuters, transit travelers, foreign commercial syndicates) as well as individuals without fixed address or legal residence title.
* **Denominator**: Strictly the registered permanent resident population (*Wohnbevölkerung*) documented on a fixed reporting date by the Federal Statistical Office (Destatis).
* **Consequence**: Dividing an open suspect numerator by a closed resident denominator mechanically inflates the crime rate for non-Germans.
* **Official Statistical Directive**: In its *IMK Report* (p. 41 & 50), the BKA explicitly refrains from publishing crime suspect rates (TVBZ) for non-Germans due to this mathematical distortion. Any raw rate computed by dividing registered non-German suspects by resident population is an **arithmetic upper-bound estimate**, not a true population rate.
* **Residency Sensitivity Tiers (PKS Table 29 - *Tatort-Wohnsitz*)**:
  - **Tier 0 (Unadjusted Total)**: All registered suspects ($584.1$ vs. $152.4$ across all ages, $3.83\times$; or $1203.4$ vs. $277.5$ per 100k among males 14+, $4.34\times$).
  - **Tier 1 (Territorial Exclusion)**: Suspects excluding those residing abroad (*Wohnsitz im Ausland*, $4.21\times$ among males 14+).
  - **Tier 2 (Permanent Resident Core)**: Suspects excluding both foreign residents and those without fixed or with unknown residence (*ohne festen / unbekannten Wohnsitz*, $3.74\times$ among males 14+).
  - *Methodological Caveat*: Because some individuals without fixed residence may be unhoused local residents or asylum seekers in emergency reception facilities, Tier 1 marks the most defensible upper bound and Tier 2 marks the plausible lower bound of the residency denominator effect.

---

### 3. Confounders vs. Mediators: Causal Identification
A common flaw in crime disparity research is conflating exogenous confounders with intermediate mediators:

```text
(A) Demographic Confounders (Age, Biological Sex):
    Age / Biological Sex ────────► Delinquency Hazard
            │
            ▼
    Citizenship / Legal Status

(B) Socioeconomic Mediators (Poverty, Housing, Labor Market Integration):
    Immigration / Legal Status ──► Relative Poverty / Precarity ──► Delinquency Hazard
            │                                                              ▲
            └────────────────────── (Direct Effect) ───────────────────────┘
```

1. **Age and Biological Sex (Confounders)**: These are biologically and temporally established prior to migration or offending decisions, structurally distorting crude group comparisons. Direct demographic age-and-sex standardization against the total resident population is an indispensable baseline control.
2. **Poverty, Labor Market Access, Living Accommodations (Mediators)**: These lie **on the causal pathway** between immigration status and delinquency:
   - Adjusting for SES isolates the **Controlled Direct Effect (CDE)**, answering: *"Do immigrants and natives facing identical socioeconomic hardship offend at equal rates?"*
   - It does **not** prove that the overall group difference is non-existent in society; rather, it identifies the **causal mechanism** ($X \to M \to Y$) through which offending disparities are generated. Both the total disparity and the direct effect must be reported side-by-side.

---

### 4. The Joint-Risk Fallacy & Demographic Cohort Harmonization (Panel E)
* Multiplying single marginal probabilities ($P(\text{Male}) \times P(\text{Age 14–30}) \times P(\text{SES} < 40)$) under the assumption of statistical independence is **methodologically invalid**, as age, biological sex, and poverty are inherently correlated in real populations.
* Joint concentrations in this pipeline are calculated via the **conditional chain rule across the harmonized 14–30 window**:
  $$P(\text{Risk} \mid g) = P(\text{Age 14–30} \mid g) \cdot P(\text{Male} \mid \text{Youth 14–30}, g) \cdot P(\text{Poverty} \mid \text{Youth 14–30, Male}, g)$$
  and safeguarded by **Fréchet–Hoeffding analytical bounds** as well as Plackett Copula sensitivity tests ($\text{OR} \in [0.8, 1.5]$).
* **Cohort Harmonization & Analytical Bounds (Audit Safeguard for Panel E)**:
  - $P(\text{Youth} \mid g)$ from Census 2022 / Genesis 12411 covers the criminological young bracket **14–30 years** ($15.9\%$ German vs. $31.2\%$ non-German, $1.96\times$ youth overhang).
  - $P(\text{Male} \mid \text{Youth}, g)$ from Census 2022 & AZR 12521-04 covers the entire **14–30 years** bracket ($51.2\%$ German vs. $55.0\%$ non-German).
  - $P(\text{Poverty} \mid \text{Youth}, g)$ from Destatis EU-SILC Genesis 12211 is population-weighted across the sub-cohorts spanning 14–30 (14–17 at 14.8%/36.2%, 18–24 at 22.1%/48.6%, and 25–29 at 11.5%/31.8%), yielding a weighted youth poverty rate of $16.9\%$ vs. $40.4\%$. Applying the male factor $k = 0.968$ yields $16.32\%$ vs. $39.05\%$.
  - The analytical **Fréchet–Hoeffding Copula Bounds** reported in Panel E reflect the full mathematical envelope under arbitrary dependency structures ($[0.0\%, 2.6\%]$ for Germans vs. $[0.0\%, 12.2\%]$ for non-Germans). The conditional chain rule point estimates (**$1.3\%$ vs. $6.7\%$**, disparity **$5.04\times$**) provide an audited, mathematically harmonized benchmark reflecting joint risk concentration across the peak delinquency years. Plackett copula sensitivity ($\text{OR} \in [0.8, 1.5]$) demonstrates stability between $4.81\times$ and $5.21\times$.

---

### 5. Police-Reporting Bias & The Darkfield (*Dunkelfeld*)
* Criminological victim surveys (e.g., KFN Lower Saxony Survey, Baier et al. 2009, Pfeiffer et al. 2018) prove that offenses committed by strangers or outgroup members have substantially higher police reporting rates (29.3% vs. 19.5%, a factor of 1.50×) compared to offenses committed within familiar social circles.
* However, this empirical finding must not be converted into arbitrary, across-the-board percentage discounts; it must be documented as an empirical reporting sensitivity range.

---

### 6. Separation of Official Police Registers (Hellfeld) and Darkfield Surveys (Dunkelfeld)
Because the PKS records no individual socioeconomic or darkfield data, scientific integrity requires maintaining a strict separation between register counts and survey findings:
1. **Target Population Divergence**: KFN FB 107 (nationwide representative survey of 9th-grade students across 61 districts, ages 14–16, $N = 44,610$) tracks self-reported delinquency, whereas the PKS counts registered suspects across all ages (78.5% adults). Adolescent survey Odds Ratios are not extrapolated across adult men up to 80 years old as hard register deductions.
2. **Construct Divergence (*Migration Background* vs. *Citizenship*)**: Academic surveys typically operationalize sociological *migration background* (including German-born 2nd and 3rd generations), whereas the PKS classifies strictly by *formal citizenship* at the time of the offense. Moreover, asylum seekers residing in collective reception centers are underrepresented in school-based surveys.
3. **Register-Based Accounting in Panel G & Waterfall (`plots/decomposition_waterfall.png`)**:
   - Evaluates the national population decomposition for **males aged 14+** across 3 empirical register stages:
     - Stage 1: Raw PKS Suspect Rate: **1,203.4** per 100k ($4.34\times$ vs. German raw 277.5).
     - Stage 2: Residence Adjustment (BKA T29 Tier 3: $-13.9\%$ non-residents / no fixed abode): **1,036.4** per 100k ($3.74\times$).
     - Stage 3: Direct Age Standardization (Destatis Standard Population): **880.3** per 100k ($-156.1$, $3.08\times$ vs. German age-standardized baseline **285.8**).
   - *Scientific Boundary*: Official police registers stop at $3.08\times$. BKA PKS does not record socioeconomic status or reporting behavior.
4. **Empirical Living Conditions Decomposition in Panel H (KFN FB 107)**:
   - Rather than relying on synthetic continuous income deciles, Panel H displays directly measured empirical violent delinquency prevalence across 3 progressive control conditions from KFN Research Report No. 107 (Baier et al. 2009, Figure 5.24, p. 86, $N = 44,610$).
   - Demonstrates that under equalized living conditions (no state welfare receipt, attendance at standard schools rather than Förderschule, and absence of severe parental physical abuse), violent delinquency converges completely ($6.4\%$ German vs. $5.9\%$ Turkish and $5.7\%$ Ex-Yugoslav youth, pooled $\text{OR} = 0.909$ $[0.66; 1.26]$, $p = 0.56$ n.s.).
5. **Universal Age-Crime Curves in Panel I (Ages 14–80)**:
   - Evaluates the empirical BKA male curves across the entire life course (§ 19 StGB criminal responsibility starting at age 14): German baseline (T40 / BV-01), Raw Non-German (T50 / AZR), and Residence-Adjusted Non-German (T29 Tier 3: $-13.9\%$).
   - Concludes the storyline using authentic administrative data without synthetic survey attenuation multipliers.

---

### 7. Unobserved Confounders in Mediation Analysis
Formal standards of causal inference (e.g., VanderWeele 2015, Pearl 2009) dictate that identification of the Controlled Direct Effect (CDE) requires no unobserved confounding between mediator ($M$) and outcome ($Y$):
* **Urban Density / Spatial Opportunity Structure**: Non-German residents are disproportionately concentrated in densely populated metropolitan areas where crime rates are structurally higher across all demographics. A portion of the SES effect may correlate with urban opportunity structures.
* **Pre-Migration Trauma & Flight Experiences**: Among refugee subgroups, experiences of war, violence, and forced displacement can impede labor market integration while simultaneously increasing impulse control risks.

---

### 8. Responsible Demographics Verification Checklist
- [x] **No cherry-picking**: Complete side-by-side reporting of registered registry figures, demographic standardizations, and longitudinal survey evidence.
- [x] **No synthetic normal curves**: Empirical binned cohorts from Census 2022 and Microcensus EU-SILC replace artificial Gaussian simulations.
- [x] **Tested statistical significance**: All regression coefficients and differences report empirical standard errors, confidence intervals, and $p$-values.
- [x] **Traceable provenance**: All raw sources documented in `rawdata/MANIFEST.csv` with download URLs and SHA-256 checksums.
- [x] **Registry vs. model clarity**: Clear separation between administrative registry counts (Panels A–D) and econometric model projections (Panels E–I).

