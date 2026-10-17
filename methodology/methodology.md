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
* Joint concentrations in this pipeline are calculated via the **conditional chain rule**:
  $$P(\text{Risk} \mid g) = P(\text{Age 14–30} \mid g) \cdot P(\text{Male} \mid \text{Youth}, g) \cdot P(\text{Poverty} \mid \text{Youth, Male}, g)$$
  and safeguarded by **Fréchet–Hoeffding analytical bounds** as well as Plackett Copula sensitivity tests ($\text{OR} \in [0.8, 1.5]$).
* **Cohort Harmonization & Analytical Bounds (Audit Safeguard for Panel E)**:
  Because official statistical releases utilize varying cohort boundaries:
  - $P(\text{Youth} \mid g)$ from Census 2022 / Genesis 12411 covers the criminological young bracket **14–30 years** ($15.9\%$ German vs. $31.2\%$ non-German, $1.96\times$ youth overhang).
  - $P(\text{Male} \mid \text{Youth}, g)$ from BKA BV-01/02 covers adolescents and young adults **14–21 years** ($51.3\%$ German vs. $53.9\%$ non-German).
  - $P(\text{Poverty} \mid \text{Youth}, g)$ from Destatis EU-SILC Genesis 12211 covers young adults **18–24 years** ($22.1\%$ German vs. $48.6\%$ non-German, with male factor $k = 0.968$, yielding $21.4\%$ vs. $47.0\%$).
  - *Cross-Bracket Conditioning Caveat*: Because official tables define youth brackets differently (14–30, 14–21, and 18–24), the conditional chain rule synthesizes these best-available official strata. Since 18–24 represents the peak poverty bracket within the 14–30 span, this provides an upper-envelope sensitivity proxy.
  - The analytical **Fréchet–Hoeffding Copula Bounds** reported in Panel E reflect the full mathematical envelope under arbitrary dependency structures ($[0.0\%, 3.4\%]$ for Germans vs. $[0.3\%, 14.7\%]$ for non-Germans). The conditional chain rule point estimates (**$1.7\%$ vs. $7.9\%$**, disparity **$4.55\times$–$4.65\times$**) provide an audited, conservative benchmark reflecting joint risk concentration across the peak delinquency years.

---

### 5. Police-Reporting Bias & The Darkfield (*Dunkelfeld*)
* Criminological victim surveys (e.g., KFN Lower Saxony Survey, Baier et al. 2009, Pfeiffer et al. 2018) prove that offenses committed by strangers or outgroup members have substantially higher police reporting rates (29.3% vs. 19.5%, a factor of 1.50×) compared to offenses committed within familiar social circles.
* However, this empirical finding must not be converted into arbitrary, across-the-board percentage discounts; it must be documented as an empirical reporting sensitivity range.

---

### 6. Two-Sample Bridging & Ecological Transportability (Registry $\to$ Microdata)
Because the PKS records no individual socioeconomic data, adjusting for SES requires transferring empirical parameters from longitudinal microdata and self-report surveys (CRIMOC, KFN FB 144):
1. **Target Population Divergence**: KFN FB 144 (survey of 9th-grade students, ages 14–16, $N = 20,407$) and CRIMOC (Duisburg/Münster longitudinal cohort, $N = 3,528$) track self-reported delinquency, whereas the PKS counts registered suspects across all ages. Transporting these findings assumes that the protective gradient of socioeconomic resources ($\beta \approx -0.41$) persists into young adulthood.
2. **Construct Divergence (*Migration Background* vs. *Citizenship*)**: Academic surveys typically operationalize sociological *migration background* (including German-born 2nd and 3rd generations), whereas the PKS classifies strictly by *formal citizenship* at the time of the offense. Moreover, asylum seekers residing in collective reception centers are underrepresented in school-based surveys.
3. **Classification**: Adjustments for socioeconomic factors must therefore be labeled as **econometric model estimates under literature assumptions**, rather than direct administrative registry counts.
4. **Dual Stream Architecture (Stream A vs. Stream B)**:
   - *Stream A (`plots/decomposition_waterfall.png`)*: Full national population decomposition for **males aged 14+**. Stages 1 to 3 apply administrative and demographic standardizations directly on BKA Table 20/40/50 and Destatis registries ($1203.4 \to 1036.4 \to 880.4$). Stage 4 (*Literature-Calibrated SES / Precarity Counterfactual*) applies the empirical attenuation factor ($0.342$) derived from criminological microdata (CRIMOC/KFN) to the residual gap, reaching $301.2$ vs. German baseline $285.8$ ($1.054\times$).
   - *Stream B (`plots/panel_g_crimoc_waterfall.png`)*: Direct longitudinal panel cohort cascade for **adolescents and young adults aged 14–25** from CRIMOC (Boers & Reinecke 2019 Table 7.3 & p. 168), showing unadjusted M1 ($524.3$) $\to$ demographic M2 ($362.6$) $\to$ full social controls M3 ($258.2$) vs. German baseline $245.0$ ($1.054\times$, $95\%\text{ CI: } [0.94, 1.18]$, $p = 0.38$, n.s.).
5. **Evaluated Linear Regression in Panel H**:
   - The plotted points in Panel H represent evaluated predictions across net equivalence income deciles 10 to 90 based on the empirical regression models from KFN FB 144 and SOEP microdata ($\text{Rate} = 42.0 - 0.40 \cdot \text{SES}$ for Germans; $45.0 - 0.42 \cdot \text{SES}$ for non-Germans). They demonstrate that within any given income decile, the rate disparity is negligible (< 3 per 100k, $p > 0.05$), and that the aggregate gap is driven by differential decile exposure (61.5% vs. 23.3% in D1–D3).
6. **Age-Crime Splines and Cohort Transitions in Panel I**:
   - In raw BKA suspect registers, age brackets switch from narrow youth intervals (14–16, 16–18, 18–21) to 21–25 and broader multi-year intervals (25–30, 30–40, etc.). Non-German population denominators around age 25 transition from education/asylum registers to Central Register of Foreigners (AZR) records.
   - To prevent artifacts, the fitted spline is evaluated strictly starting at age 14 (the statutory age of criminal responsibility in Germany, § 19 StGB), eliminating spurious boundary oscillations. The literature-controlled projection applies the adolescent CRIMOC attenuation factor ($0.4925$) to the youth peak, demonstrating that the adolescent delinquency surge flattens toward native baseline levels.

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

