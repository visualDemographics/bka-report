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
   - *Denominator Granularity & The 21–60 Conservative Lower-Bound Property*: Official BKA denominator tables (`BV-01` and `BV-02`) publish population counts across 4 statutory age brackets: 14–18, 18–21, 21–60, and 60+. Within the broad 21–60 band, the non-German resident population is heavily skewed toward peak delinquency ages (21–35, where migration influx is concentrated), whereas the German resident population is concentrated in late working age (40–59, where violent crime rates have fallen by over 70%). Because direct age standardization on the BKA's 4 official brackets cannot adjust for internal compositional variation within the 21–60 bracket, the reduction of the male 14+ disparity from $4.34\times$ to $3.58\times$ represents a **conservative lower-bound estimate** of demographic age confounding. When more granular 5-year census cohorts are evaluated (Panels B & G), the demographic age-correction is even more pronounced.
2. **Poverty, Labor Market Access, Living Accommodations (Mediators)**: These lie **on the causal pathway** between immigration status and delinquency:
   - Adjusting for SES isolates the **Controlled Direct Effect (CDE)**, answering: *"Do immigrants and natives facing identical socioeconomic hardship offend at equal rates?"*
   - It does **not** prove that the overall group difference is non-existent in society; rather, it identifies the **causal mechanism** ($X \to M \to Y$) through which offending disparities are generated. Both the total disparity and the direct effect must be reported side-by-side.

---

### 4. The Joint-Risk Fallacy & Demographic Cohort Harmonization (Panel E)
* Multiplying single marginal probabilities ($P(\text{Male}) \times P(\text{Age 14–30}) \times P(\text{SES} < 40)$) under the assumption of statistical independence is **methodologically invalid**, as age, biological sex, and poverty are inherently correlated in real populations.
* In accordance with Pillar 3 of Responsible Demographics, joint concentrations in this pipeline are calculated via the **conditional chain rule across the harmonized 14–30 window as an illustrative baseline model ($M_{\text{ind}}$)**:
  $$P(\text{Risk} \mid g) = P(\text{Age 14–30} \mid g) \cdot P(\text{Male} \mid \text{Youth 14–30}, g) \cdot P(\text{Poverty} \mid \text{Youth 14–30, Male}, g)$$
  and safeguarded by **Fréchet–Hoeffding analytical bounds** ($[P_{\min}, P_{\max}]$) as well as Plackett Copula sensitivity tests ($\text{OR} \in [0.8, 1.5]$).
* **Cohort Harmonization & Analytical Bounds (Audit Safeguard for Panel E)**:
  - $P(\text{Youth} \mid g)$ from Census 2022 / Genesis 12411 covers the criminological young bracket **14–30 years** ($15.9\%$ German vs. $31.2\%$ non-German, $1.96\times$ youth overhang).
  - $P(\text{Male} \mid \text{Youth}, g)$ from Census 2022 & AZR 12521-04 covers the entire **14–30 years** bracket ($51.2\%$ German vs. $55.0\%$ non-German).
  - $P(\text{Poverty} \mid \text{Youth}, g)$ from Destatis EU-SILC Genesis 12211 is population-weighted across the sub-cohorts spanning 14–30 (14–17 at 14.8%/36.2%, 18–24 at 22.1%/48.6%, and 25–29 at 11.5%/31.8%), yielding a weighted youth poverty rate of $16.9\%$ vs. $40.4\%$. Applying the male factor $k = 0.968$ yields $16.32\%$ vs. $39.05\%$.
  - The analytical **Fréchet–Hoeffding Copula Bounds** reported in Panel E reflect the full mathematical envelope under arbitrary dependency structures ($[0.0\%, 2.6\%]$ for Germans vs. $[0.0\%, 12.2\%]$ for non-Germans). The conditional chain rule point estimates (**$1.3\%$ vs. $6.7\%$**, disparity **$5.04\times$**) provide an audited baseline model ($M_{\text{ind}}$) reflecting joint risk concentration across the peak delinquency years under conditional independence. Plackett copula sensitivity ($\text{OR} \in [0.8, 1.5]$) demonstrates stability between $4.81\times$ and $5.21\times$. True empirical joint concentrations require dedicated microdata cross-tabulations.

---

### 5. Police-Reporting Bias & The Darkfield (*Dunkelfeld*)
Criminological victim surveys establish two distinct, empirically verified reporting asymmetries:
1. **Dyadic Ethnic Reporting Gap** (*Baier, Pfeiffer, Simonson & Rabold 2009 / KFN FB 107, p. 11*):
   - Offenses with German victims and German perpetrators have a police reporting rate of **19.5%**.
   - When a German victim is assaulted by a non-German/migrant youth, the reporting rate rises to **29.3%**, a **1.50× factor** ($+50\%$ higher probability of entering police registries).
2. **Stranger vs. Acquaintance Reporting Gap** (*Pfeiffer, Baier & Kliem 2018, Chapter 5.2.4, pp. 74–76, Abbildung 19*):
   - Violent offenses committed by acquaintances or ingroup members have a reporting rate of **12.7%**.
   - Offenses committed by strangers, unknown persons, or refugees have a reporting rate of **29.5%**, a **2.32× factor**.
3. **Methodological Restraint**:
   - Neither factor is converted into an arbitrary subtractive scalar discount on the official PKS register.
   - Reporting bias is documented as a qualitative darkfield limitation explaining why register-based counts overstate outgroup delinquency relative to representative darkfield self-reports.

---

### 6. Register Accounting, Shapley Decomposition & Darkfield Surveys
Because the PKS records no individual socioeconomic or darkfield data, scientific integrity requires maintaining a strict separation between register counts and survey findings:

#### A. Official Register Decomposition (Males Aged 14+) & Shapley Permutation Analysis
The official police register decomposition for males aged 14+ transitions from the crude rate to the standardized rate:
- **Baseline Raw Suspect Rate**: Non-German **1,203.4** vs. German **277.5** per 100k ($4.34\times$, 95% CI: $[4.29, 4.39]$).
- **Sequence 1 (Residence Adjustment $\to$ Age Standardization)**:
  - Step 1 (Residence Adjustment, BKA T29 Tier 2): Excludes foreign residents and individuals without fixed abode ($-13.9\%$), reducing the rate to **1,036.4** per 100k ($\Delta_{\text{res}}^{(1)} = -167.0$, $3.74\times$, 95% CI: $[3.69, 3.78]$).
  - Step 2 (Direct Age Standardization): Applying Destatis reference weights across administrative age bands reduces the rate to **880.3** per 100k ($\Delta_{\text{age}}^{(1)} = -156.1$, $3.08\times$ vs. German age-standardized baseline **285.8**, 95% CI: $[3.04, 3.12]$).
- **Sequence 2 (Age Standardization $\to$ Residence Adjustment)**:
  - Step 1 (Direct Age Standardization): Reduces raw non-German rate to **1,022.3** per 100k ($\Delta_{\text{age}}^{(2)} = -181.1$, $3.58\times$ vs. German age-standardized baseline 285.8).
  - Step 2 (Residence Adjustment): Applying the $-13.9\%$ residence factor ($0.8612$) reduces the rate to **880.4** per 100k ($\Delta_{\text{res}}^{(2)} = -141.9$, $3.08\times$).
- **Shapley Path-Independent Attribution**:
  - $\phi_{\text{res}} = \frac{-167.0 + (-141.9)}{2} = -154.5\text{ per 100,000}$ (**47.8%** of explainable register gap reduction).
  - $\phi_{\text{age}} = \frac{-156.1 + (-181.1)}{2} = -168.6\text{ per 100,000}$ (**52.2%** of explainable register gap reduction).
  - Total explainable reduction: $-323.1$ per 100k. The residual disparity of **3.08×** marks the boundary of official register data.

#### B. Representative Darkfield Survey Decomposition (KFN FB 107) & TOST Equivalence Analysis
- In KFN Research Report No. 107 (Baier et al. 2009, Figure 5.24, p. 86, $N = 44,610$), 12-month violent delinquency prevalence among 9th-grade students is evaluated across progressive control stages:
  - *Crude Unadjusted Prevalence*: German $11.5\%$, Turkish $20.3\%$ ($1.77\times$), Ex-Yugoslav $22.1\%$ ($1.92\times$).
  - *Peer & Violence Norm Controls*: German $9.8\%$, Turkish $11.3\%$ ($1.15\times$), Ex-Yugoslav $12.4\%$ ($1.27\times$).
  - *Fully Equalized Living Conditions* (no welfare receipt, standard school track, no severe parental physical abuse): German $6.4\%$, Turkish $5.9\%$, Ex-Yugoslav $5.7\%$.
- **Statistical Significance & Equivalence Testing**:
  - Turkish vs. German youth under identical living conditions: $\text{OR} = 0.917$ (95% CI: $[0.731, 1.151]$, standard null hypothesis $p = 0.455$ n.s.).
  - Pooled migrant youth: $\text{OR} = 0.909$ (95% CI: $[0.656, 1.258]$, $p = 0.56$ n.s.).
  - **Two One-Sided Tests (TOST)**:
    - Against a strict $\pm 30\%$ equivalence margin ($\text{OR} \in [0.77, 1.30]$): $p_{\text{TOST}} = 0.065$, indicating that while massive differences are ruled out, strict $\pm 30\%$ equivalence is borderline due to finite sub-sample size.
    - Against a moderate $\pm 50\%$ equivalence margin ($\text{OR} \in [0.67, 1.50]$): $p_{\text{TOST}} = 0.0030$ (statistically significant equivalence).
  - *Scientific Scope*: Statistical insignificance ($p = 0.56$) confirms that under equalized living conditions in this youth cohort, no residual disparity is detectable. However, sampling uncertainty does not constitute mathematical proof of zero difference, and school cohort findings cannot be extrapolated as hard subtractions onto the adult registered population.

---

### 7. Cross-National OECD Meta-Regression (REMR) & Heterogeneity Diagnostics
Panel F integrates a DerSimonian-Laird Random-Effects Meta-Regression (REMR) over 12 landmark empirical cohort studies across 9 OECD peer nations (Sweden, Norway, Finland, Denmark, Netherlands, United States, France, United Kingdom, Austria; total $N = 17,909,254$):
1. **Model Specification & Heterogeneity**:
   - Model: $\ln(Y_i) = \beta_0 + \beta_1 \ln(X_i) + u_i + \epsilon_i$, where $u_i \sim \mathcal{N}(0, \tau^2)$.
   - Cochran's $Q = 232.41$ ($df = 10, p < 0.0001$).
   - Between-study variance: $\tau^2 = 0.0328$ ($\tau = 0.1812$).
   - Higgins' Heterogeneity Index: $I^2 = 95.7\%$, confirming substantial between-country heterogeneity that warrants a random-effects framework over fixed-effects WLS.
   - Knapp-Hartung small-sample standard error adjustment applied to test statistics ($t_{\text{crit}} = 2.228$).
   - Model equation: $\ln(Y) = 0.5423 + 0.4030 \cdot \ln(X)$.
2. **Central Projection Corridor & Jackknife Sensitivity**:
   - For primary German income precarity ($D_1\text{--}D_3$, ratio $X = 2.64$), the central REMR prediction is $\hat{Y} = 2.54\times$ (mean prediction 95% CI: $[2.23\times, 2.90\times]$).
   - Microcensus SES $< 40$ ($X = 2.21$): $\hat{Y} = 2.37\times$ (95% CI: $[1.87\times, 3.00\times]$).
   - EU-SILC At-Risk-of-Poverty ($X = 2.90$): $\hat{Y} = 2.64\times$ (95% CI: $[2.32\times, 3.01\times]$).
   - Overall empirical German calibration corridor (95% CI): $[2.23\times, 2.90\times]$.
   - *Jackknife Leave-One-Country-Out Analysis across 9 Nations*:
     - Drop Sweden: $\hat{Y} = 2.48\times$
     - Drop Netherlands: $\hat{Y} = 2.53\times$
     - Drop Norway: $\hat{Y} = 2.58\times$
     - Drop United States: $\hat{Y} = 2.55\times$
     - Drop Denmark: $\hat{Y} = 2.53\times$
     - Drop Finland: $\hat{Y} = 2.55\times$
     - Drop France: $\hat{Y} = 2.49\times$
     - Drop United Kingdom: $\hat{Y} = 2.55\times$
     - Drop Austria: $\hat{Y} = 2.60\times$
     - Stability corridor across all exclusions: $[2.48\times, 2.60\times]$, confirming that the central precarity anchor is robust to any single country's inclusion.
3. **Prediction Interval & Methodological Boundaries**:
   - The 95% Prediction Interval incorporating between-country variance $\tau^2$ spans $[1.66\times, 3.89\times]$ across the German precarity range (and $[1.66\times, 3.89\times]$ at D1–D3), reflecting genuine institutional and welfare state differences across OECD nations.
   - *Construct Boundary & Epidemiological Interpretation*:
     - **Counterfactual Exposure Equalization ($Y / RR_{\text{precarity}}$)**: Applying the central relative risk ($RR = 2.54\times$, corridor $[2.23\times, 2.90\times]$) directly to the non-German suspect rate models the counterfactual outcome if the structural precarity penalty were entirely neutralized.
     - **Population Compositional Confounder ($\text{CF}_{\text{SES}}$)**: Under standard epidemiological standardization (Rothman 2008), differential exposure rates ($p_{\text{NDE}} = 61.5\%$ vs. $p_{\text{DE}} = 23.3\%$ in D1–D3) yield a compositional confounding factor $\text{CF}_{\text{SES}} = \frac{1 + p_{\text{NDE}}(RR - 1)}{1 + p_{\text{DE}}(RR - 1)} = \frac{1 + 0.615(1.543)}{1 + 0.233(1.543)} \approx \mathbf{1.43\times}$. Income precarity per se accounts for approximately 44% of the residence-adjusted youth peak disparity overhang, with remaining differences attributable to unobserved non-income structural factors (accommodation in collective reception centers, employment bans, trauma, peer networks, and differential darkfield reporting behavior).
4. **Causal Interpretation & Sibling Fixed-Effects Attenuation (Sariaslan et al. 2014, 2021)**:
   - The effect ratios $Y_i$ in the OECD meta-regression reflect **macro-observational population disparities** ($RR, HR, IRR \approx 2.34\text{--}3.10\times$). In Nordic register studies, children growing up in low-income or welfare-dependent households exhibit more than double the rate of subsequent registered violent crime in young adulthood.
   - However, rigorous sibling-comparison studies (notably Sariaslan et al. 2014 in Sweden and Sariaslan et al. 2021 in Finland) demonstrate that within-family discordant sibling models attenuate the hazard ratio for family income substantially (attenuating from $HR \approx 2.42\text{--}2.52$ at the population level to $HR \approx 1.10\text{--}1.12$, virtually indistinguishable from unity).
   - This vital distinction demonstrates that pure monetary income is an **empirical index/proxy of clustered structural disadvantage** (school segregation, labor market barriers, parental stress, neighborhood disorder, and discrimination) rather than an isolated mechanical lever that can be adjusted in isolation.
   - Accordingly, the OECD meta-regression models the **aggregate population risk gradient** associated with socioeconomic stratification, and must not be misinterpreted as an unconfounded guarantee that isolated income transfers alone would eliminate individual delinquency.

---

### 8. Structural Calibration of the Bivariate Risk Surface (Panel G)
Panel G calibrates a continuous bivariate delinquency hazard surface $R(\text{Age}, \text{SES})$ across the life course (ages 0 to 80 and SES percentiles 0 to 100):
1. **Mathematical Conservation of Empirical Marginals**:
   - Constrained such that the marginal integral over uniform SES percentiles identically reproduces the empirical BKA male Age-Crime curve across all age slices:
     $$\frac{1}{100} \int_0^{100} R(a, s) \, ds \equiv A_{\text{PKS}}(a) \quad \forall a \in [0, 80] \quad (\text{drift } < 10^{-10}).$$
2. **Developmental Calibration Parameters**:
   - Calibrated using the OECD precarity central anchor ($RR = 2.54\times$ across SES $< 40$, Atkinson 1987 logistic kernel $k = 0.12$), adolescent maturity gap weights ($w_{\text{gap}} = 0.35, w_{\text{depr}} = 0.65$, Moffitt 1993), and adult turning point persistence delay ($\tau = 25.0\text{ years}$, Sampson & Laub 1993, 2003).
3. **Explicit Methodological Status**:
   - Panel G is a **theoretical and structural response surface model** illustrating how developmental criminology and empirical precarity gradients interact over the life course. It is **not** an empirical 3D microdata cross-tabulation, as official police registers contain no socioeconomic microdata.

---

### 9. Universal Age-Crime Curves & Demographic SES Standardization (Panel I)
Panel I synthesizes the full life-course empirical trajectories (ages 14 to 80) and applies demographic SES standardization restricted strictly to the empirical adolescent and young adult high-risk window (ages 14–30):
1. **Three-Stage Causal Trajectory (Peak at Age 17.5)**:
   - **Stage 0 (Raw Registered Non-German Peak)**: $3,939\text{ per 100,000}$ (vs. German baseline $1,165\text{ per 100,000}$, raw disparity $3.38\times$).
   - **Stage 1 (Residence Adjustment, BKA Table 29 Tier 3: $-13.9\%$)**: Deducting non-residents residing abroad and individuals without permanent abode drops the peak to $3,392\text{ per 100,000}$ ($2.91\times$).
   - **Stage 2 (Demographic SES Standardization, $\text{CF}_{\text{SES}} = 1.43\times$)**: Plotted as the solid purple curve (`#8e44ad`). Standardizes the non-German cohort to the observed German poverty baseline (Destatis EU-SILC D1–D3: $61.5\%$ vs. $23.3\%$) via Rothman's population confounding factor:
     $$\text{CF}_{\text{SES}} = \frac{1 + p_{\text{NDE}}(RR - 1)}{1 + p_{\text{DE}}(RR - 1)} = \frac{1 + 0.615 \times 1.543}{1 + 0.233 \times 1.543} = \mathbf{1.434} \approx \mathbf{1.43\times}$$
     lowering the peak from $3,392$ to **$2,367\text{ per 100,000}$**, explaining **$44\%$** of the residence-adjusted peak gap without assuming unobserved individual counterfactuals.
   - **OECD SES Safety Band**: Shaded purple area reflecting the empirical 95% CI uncertainty corridor from the OECD REMR meta-regression ($RR \in [2.23\times, 2.90\times]$), propagating to an SES confounding factor corridor of $\text{CF}_{\text{SES}} \in [1.36\times, 1.50\times]$ and bracketing the standardized peak within **$[2,260, 2,490]\text{ per 100,000}$**.
2. **Reconciliation of Causal Dimensions & Symmetric Zero-Poverty Equivalence**:
   - The demographic SES standardization ($\text{CF} = 1.43\times$, peak $2,367$) models the observable effect of equalizing precarity to the German reference baseline ($23.3\%$), leaving a residual disparity of **$2.03\times$** ($2,367$ vs. $1,165$).
   - *Symmetric Zero-Poverty Theorem*: Hypothetically eradicating poverty to $0\%$ in both groups scales both curves down symmetrically by factor $1 + 0.233 \times 1.534 = 1.357\times$ ($1,165 \to 858$ and $3,392 \to 1,745$), maintaining identically the same residual disparity ratio ($\frac{1,745}{858} = \frac{2,367}{1,165} = \mathbf{2.03\times}$). The plotted trajectory standardizes against the empirical German baseline to preserve real-world administrative reference grounding.
   - The remaining gap ($2,367$ vs. $1,165$) is bridged by documented unobserved structural mediators (collective emergency shelter accommodation, legal work bans, language friction, trauma) and darkfield victim reporting asymmetries ($1.50\times$ to $2.32\times$, Pfeiffer et al. 2018).

---

### 10. Responsible Demographics Verification Summary
- [x] **No cherry-picking**: Side-by-side reporting of raw register rates, demographic standardizations, and longitudinal survey evidence.
- [x] **No synthetic normal curves**: Empirical age cohorts from Census 2022 and Microcensus EU-SILC replace artificial Gaussian simulations.
- [x] **Uncertainty & Equivalence**: Exact standard errors, confidence intervals, and TOST equivalence tests reported.
- [x] **Traceable provenance**: All raw sources documented in `rawdata/MANIFEST.csv` with SHA-256 checksums.
- [x] **Registry vs. model clarity**: Clear separation between administrative registry counts (Panels A–D, H), empirical darkfield surveys (Panel H), and econometric/theoretical model calibrations (Panels E, F, G, I).
