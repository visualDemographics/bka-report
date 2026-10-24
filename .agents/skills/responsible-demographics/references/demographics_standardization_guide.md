# Methodological Guide: Demographic Standardization & Age Adjustment

This guide documents mathematical and methodological standards for age and sex standardization of crime and demographic statistics.

---

## 1. Mathematical Foundations of Direct Standardization

Direct standardization eliminates structural demographic differences (such as the aging urn shape of the native population or the high concentration of young adults among immigrants) by applying group-specific cohort rates to a shared **standard reference population**.

### Formulas

Let:
* $a \in A$: Age cohort (e.g., 14–18, 18–21, 21–60, 60+)
* $s \in S$: Sex (male, female)
* $N_{a,s}^{(g)}$: Absolute number of suspects in group $g \in \{\text{German}, \text{Non-German}\}$
* $P_{a,s}^{(g)}$: Resident population in group $g$
* $R_{a,s}^{(g)} = \frac{N_{a,s}^{(g)}}{P_{a,s}^{(g)}} \times 100{,}000$: Specific suspect rate (TVBZ) per cohort
* $P_{a,s}^{(\text{std})}$: Reference / standard population (e.g., total resident population aged 14+)

The cohort weight $w_{a,s}$ in the standard population is:
$$w_{a,s} = \frac{P_{a,s}^{(\text{std})}}{\sum_{a' \in A, s' \in S} P_{a',s'}^{(\text{std})}}$$

The directly standardized rate $\bar{R}^{(g)}_{\text{std}}$ is calculated as:
$$\bar{R}^{(g)}_{\text{std}} = \sum_{a \in A} \sum_{s \in S} w_{a,s} \cdot R_{a,s}^{(g)}$$

---

## 2. Real-World Population Pyramids in Germany: Inverted Urn vs. Migration Peak

### German Resident Population
* **Demographic Type**: Shrinking inverted urn shape with a pronounced Baby-Boomer peak.
* **Peak Cohorts**: Birth cohorts 1958–1968 (aged 55 to 65 at the time of the 2023 reporting period).
* **Share Aged 60+**: Over 37% of the population aged 14+ (34.7% among males).
* **Impact on Crude Rates**: Because older adults commit violent offenses at extremely low rates (TVBZ < 35 per 100,000), this demographic pensioner surplus mechanically pulls the overall German rate downward.

### Non-German Resident Population
* **Demographic Type**: Young labor and humanitarian migration pyramid.
* **Peak Cohorts**: Young adults aged 18 to 35.
* **Share Aged 60+**: Only ~13.2% of males aged 14+.
* **Impact on Crude Rates**: The demographic overhang in the peak-delinquency age window (ages 14–30) mechanically inflates the crude rate, even if age-specific offending propensities within each cohort were identical.

---

## 3. Aggregation Bias in Coarse Age Brackets

In official BKA overview tables (e.g., Tables BV-01, BV-02), population denominators for Germans and non-Germans are published in four standardized age bands:
1. `14–18 years` (Juveniles)
2. `18–21 years` (Young adults)
3. `21–60 years` (Working-age adults)
4. `60+ years` (Seniors)

### The Wide 21–60 Bracket Problem:
* Within the broad interval `21–60`, the age distributions of Germans and non-Germans are **not homogeneous**:
  - Germans within this band cluster between ages 45 and 58.
  - Non-Germans within this band cluster between ages 22 and 34.
* Because violent crime rates decline steeply throughout the 20s and 30s, standardizing across the coarse `21–60` band underestimates the true demographic age effect.
* **Methodological Implication**: A 4-band standardization represents a **conservative lower bound** of the demographic age effect. Finer 5-year cohorts (from Destatis Genesis 12411-0006) capture the age effect even more completely.

---

## 4. Sensitivity Analysis for Non-Resident Suspects (PKS Table 29)

Because suspects without permanent residence in Germany (tourists, transit travelers, cross-border commuters, undocumented individuals) are recorded in the PKS suspect numerator but excluded from the Destatis residential population denominator, a sensitivity analysis is mandatory:

$$\text{Adjusted TVBZ}_{\text{Tier 1}} = \frac{N_{\text{total}} - N_{\text{residence abroad}}}{P_{\text{resident population}}} \times 100{,}000$$

$$\text{Adjusted TVBZ}_{\text{Tier 2}} = \frac{N_{\text{total}} - N_{\text{residence abroad}} - N_{\text{no fixed/unknown residence}}}{P_{\text{resident population}}} \times 100{,}000$$

Both tiers must be reported transparently alongside the unadjusted crude rate:
* **Tier 0 (Unadjusted Total)**: Baseline registry quotient ($4.34\times$ for males 14+; $3.83\times$ total population).
* **Tier 1 (Territorial Exclusion)**: Removes suspects residing abroad ($4.21\times$ for males 14+).
* **Tier 2 (Permanent Resident Core)**: Additionally removes suspects lacking fixed/known residency ($3.74\times$ for males 14+).

---

## 5. Path-Independent Shapley Value Decomposition for Waterfalls

Sequential waterfall charts are sensitive to execution order:
* **Sequence 1 (Residence Adjustment $\to$ Age Standardization)**:
  - Step 1 (Residence Adjustment, BKA T29 Tier 2): $1{,}203.4 \to 1{,}036.4$ ($\Delta_{\text{res}}^{(1)} = -167.0\text{ per 100k}$, ratio drops to $3.74\times$).
  - Step 2 (Direct Age Standardization): $1{,}036.4 \to 880.3$ ($\Delta_{\text{age}}^{(1)} = -156.1\text{ per 100k}$, ratio drops to $3.08\times$ vs. German baseline $285.8$).
* **Sequence 2 (Age Standardization $\to$ Residence Adjustment)**:
  - Step 1 (Direct Age Standardization): $1{,}203.4 \to 1{,}022.3$ ($\Delta_{\text{age}}^{(2)} = -181.1\text{ per 100k}$, ratio drops to $3.58\times$).
  - Step 2 (Residence Adjustment): $1{,}022.3 \to 880.4$ ($\Delta_{\text{res}}^{(2)} = -141.9\text{ per 100k}$, ratio drops to $3.08\times$).

### Shapley Attribution:
To eliminate ordering artifacts, compute the mean marginal contribution across all $K! = 2$ permutations:
$$\phi_{\text{Demography/Age}} = \frac{-156.1 + (-181.1)}{2} = \mathbf{-168.6 \text{ per 100,000}} \quad (52.2\% \text{ of register gap reduction})$$
$$\phi_{\text{Residence/Nenner}} = \frac{-167.0 + (-141.9)}{2} = \mathbf{-154.5 \text{ per 100,000}} \quad (47.8\% \text{ of register gap reduction})$$
Both factors contribute in nearly equal measure to narrowing the register disparity from $4.34\times$ to $3.08\times$.

---

## 6. Epidemiological Compositional Standardization ($\text{CF}_{\text{SES}}$)

When adjusting for socio-economic precarity without individual register data, researchers often commit the fallacy of dividing by the full relative risk $RR$ (which falsely assumes 100% of non-Germans are precarious and 0% of Germans are precarious).

Standardization requires **Rothman's Population Confounding Factor**:
$$\text{CF}_{\text{SES}} = \frac{1 + p_{\text{NDE}} (RR - 1)}{1 + p_{\text{DE}} (RR - 1)}$$
Where $p_{\text{NDE}} = 61.5\%$ and $p_{\text{DE}} = 23.3\%$ in Destatis Microcensus deciles D1–D3, and $RR = 2.54$ (OECD meta-regression):
$$\text{CF}_{\text{SES}} = \frac{1 + 0.615 \times 1.54}{1 + 0.233 \times 1.54} = \frac{1.947}{1.359} \approx \mathbf{1.432}$$
Standardizing against the observed German baseline lowers the residence-adjusted youth peak from $3{,}392$ to **$2{,}367\text{ per 100k}$** (disparity drops to $2.03\times$).

### Symmetric Zero-Poverty Theorem:
Hypothetically setting poverty to $0\%$ in both populations scales down the German baseline ($1{,}165 \to 858$) and the non-German rate ($3{,}392 \to 1{,}745$) by the identical factor $1.359$, yielding the exact same residual disparity ratio:
$$\frac{1{,}745}{858} \equiv \frac{2{,}367}{1{,}165} = \mathbf{2.03\times}$$
Standardizing to the German observed baseline preserves real-world administrative reference grounding without altering the mathematical conclusion.

---

## 7. Unobservable Brackets & Non-Linear Life-Course Modeling

When combining tables with non-overlapping cohort cuts (e.g., BKA BV-02 reports `21–60` while AZR reports `20–25`, leaving non-German males aged `21–25` unobservable):
1. **Preserve `NaN`**: Never fabricate an interpolated estimate.
2. **Anchor Parameter Knots**: When fitting universal parametric models:
   $$\text{onset}(a) = \frac{1}{1 + \exp(-k_{\text{on}}(a - x_{\text{on}}))}, \quad A(a) = \text{onset}(a) \cdot \left[ a_{\text{peak}} \exp\left(-\frac{(a - \mu)^2}{2\sigma^2}\right) + a_{\text{adult}} \exp(-a / \tau) \right]$$
   Fix the peak knot $\mu$ to the empirical observed youth midpoint (e.g., age 16.0 for 14–18) to prevent artificial spline overshoot in the missing interval.
3. **Clip External Interventions**: Restrict external literature sensitivity bands strictly to the empirical age window of the studies (e.g., ages 14–30).
