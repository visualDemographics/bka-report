# Causal Inference & Mediation Analysis in Demographic Disparities

## 1. Confounders vs. Mediators: Formal Definition

In epidemiological and criminological disparity research, distinguishing between confounders and mediators is fundamental to drawing valid inferences.

```
(A) Confounding (Alternative Explanation):
             Age, Sex, Cohort (Z)
                /            \
               /              \
              ▼                ▼
   Group / Nationality (X) ───► Delinquency (Y)

(B) Mediation (Causal Mechanism):
   Group / Nationality (X) ───► Poverty / Housing (M) ───► Delinquency (Y)
              \                                          ▲
               \────────────────────────────────────────/
                             Direct Effect
```

### Confounders ($Z$)
* **Definition**: A variable that causally influences both group membership (or demographic composition) and the outcome, but is not on the causal pathway from group membership to the outcome.
* **Examples**: Biological sex, age cohort.
* **Analytical Treatment**: Must be controlled for (via direct standardization or regression) to eliminate composition artifacts.

### Mediators ($M$)
* **Definition**: A variable that lies on the causal pathway between group status and the outcome.
* **Examples**:
  - Legal employment prohibitions or labor market restrictions.
  - Placement in overcrowded mass refugee accommodations.
  - Lower socio-economic status (SES), relative income deprivation, or lack of wealth buffer.
* **Analytical Treatment**:
  - Controlling for $M$ blocks the indirect pathway ($X \to M \to Y$).
  - What remains is the **direct effect** ($X \to Y$).
  - **Crucial Interpretation**: Demonstrating that the direct effect approaches zero does **not** mean the group disparity is fictitious or an artifact; it demonstrates that the disparity is **mediated by socio-economic conditions**.

---

## 2. The Ecological Fallacy in Aggregate Disparity Studies

### What is the Ecological Fallacy?
The ecological fallacy occurs when inferences about individual-level relationships are deduced solely from aggregate population statistics.

### Concrete Example in Crime Statistics:
* **Aggregate observation**: Group $A$ (non-Germans) has a higher national poverty rate (35.4% vs. 12.2%) and a higher aggregate crude crime rate (584.1 vs. 152.4 per 100k overall, or 710.9 vs. 165.0 for ages 14+).
* **Invalid deduction**: Concluding that individual suspects in Group $A$ offend because of poverty, or asserting that 60% of suspects have an individual SES percentile $< 40$, without measuring individual suspect incomes.
* **Scientific Standard**:
  - State clearly that the PKS is an administrative register lacking individual socio-economic data.
  - When referencing socio-economic gradients, rely on longitudinal microdata studies (e.g., CRIMOC panel, KFN surveys) where individual income, school performance, and family structure are measured at the person level.

---

## 3. Reporting Standards for Model Estimates

When reporting controlled results:
1. Specify the Baseline: Always state the raw disparity ratio alongside the controlled ratio.
2. Report the Decomposition Pathway: Use waterfall models to show the incremental change from:
   - Raw rate
   - Numerator correction (non-residents)
   - Demographic standardization (age & sex)
   - Socio-economic conditional analysis (mediator explanation)
3. Disclose Assumptions: Every model step must document whether it is an exact registry adjustment or a sensitivity projection derived from external surveys.

---

## 4. Macro-Observational Gradients vs. Discordant Sibling Fixed-Effects

A critical breakthrough in modern life-course criminology is distinguishing between **macro-observational population risk gradients** and **within-family causal identification**:

* **Observational Register Disparity ($RR / HR \approx 2.4\text{--}3.1\times$)**:
  In unadjusted population registers across Sweden, Norway, Denmark, and Finland, children raised in the lowest income quintile or welfare-dependent households exhibit more than double the risk of violent offending in young adulthood.
* **Discordant Sibling Attenuation (Sariaslan et al. 2014, 2021)**:
  When comparing biological siblings who grew up in the same family but experienced divergent family income during childhood (controlling for unobserved genetic and parental confounders via family fixed effects), the hazard ratio for income drops to **$HR \approx 1.10\text{--}1.12$** (virtually indistinguishable from unity).
* **Causal Interpretation**:
  This attenuation proves that monetary income is an **empirical index or proxy for clustered structural disadvantage** (housing segregation, peer delinquency, neighborhood disorder, school underfunding, parental conflict) rather than an isolated mechanical lever. Income transfers alone do not automatically eliminate delinquency without addressing the broader structural cluster.

---

## 5. Two One-Sided Tests (TOST) for Parity & Equivalence Claims

In survey microdata (e.g., KFN FB 107, Baier et al. 2009), controlling for living conditions and peer delinquency reduces the odds ratio for Turkish vs. German adolescents to $\text{OR} = 0.917$ with $p = 0.455$.
* **The Fallacy**: Reporting "disparities disappear" or "parity is proven" because $p > 0.05$.
* **The Methodological Remedy (TOST)**:
  Conduct Two One-Sided Tests against an explicit equivalence margin $\Delta$:
  $$z_1 = \frac{\ln(\text{OR}) - (-\Delta)}{\text{SE}_{\ln}}, \quad z_2 = \frac{\Delta - \ln(\text{OR})}{\text{SE}_{\ln}}$$
  $$p_{\text{TOST}} = \max(1 - \Phi(z_1), 1 - \Phi(z_2))$$
  - At a strict $\pm 30\%$ margin ($\Delta = \ln(1.30)$): $p_{\text{TOST}} = 0.065$ (borderline inconclusive).
  - At a standard $\pm 50\%$ margin ($\Delta = \ln(1.50)$): $p_{\text{TOST}} = 0.003$ (statistically significant equivalence).
  This establishes transparent scientific reporting: differences are bounded within $\pm 50\%$, while sampling uncertainty precludes claiming exact zero difference.

---

## 6. Cross-National Meta-Regression (REMR) as a Calibration Anchor

When national police statistics lack individual SES data, cross-national meta-regression (e.g., across 12 studies from 9 OECD peer nations) provides an empirical order of magnitude for socioeconomic confounding:
1. **DerSimonian–Laird Random Effects**: Rebalances weights $w_i^* = 1 / (\sigma_i^2 + \tau^2)$ so multi-million-person registries do not collapse variance.
2. **Knapp–Hartung Adjustment**: Adjusts standard errors for small study counts ($k = 12$).
3. **95% Confidence Intervals vs. Prediction Intervals**:
   - The 95% CI ($[2.23\times, 2.90\times]$) represents mean projection precision.
   - The 95% Prediction Interval ($[1.66\times, 3.89\times]$) reflects real-world institutional diversity in a new country.
4. **Jackknife Stability**: Verify that leave-one-country-out predictions remain stable (e.g., corridor $[2.48\times, 2.60\times]$).
