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
