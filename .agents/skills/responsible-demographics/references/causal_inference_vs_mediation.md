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
