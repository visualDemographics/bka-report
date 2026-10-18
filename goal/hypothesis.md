# Research Hypotheses & Causal Models

This project formulates four pre-registered, falsifiable hypotheses regarding BKA violent crime suspect data (Offense Key 892000):

---

### Hypothesis 1 (Denominator Matching & Residency Sensitivity)
> **$H_1$**: A substantial proportion of non-German suspects in the PKS does not reside permanently in Germany. Because official Destatis population denominators count exclusively registered residents, this numerator-denominator mismatch generates an artificial arithmetic inflation of the non-German crude rate by at least 10–30%.
* **Operationalization**: Computation of residence-adjusted suspect rates (TVBZ) using BKA PKS Table 29 (*Tatort-Wohnsitz*). Stratified exclusion of suspects residing abroad as well as persons without fixed or known residence.
* **Falsification Criterion**: If the proportion of non-resident suspects in Offense Key 892000 is below 3%, the denominator mismatch effect is deemed negligible.

---

### Hypothesis 2 (Demographic Age and Sex Standardization)
> **$H_2$**: Disparities in violent crime suspect rates are significantly driven by differing population age pyramids (an aging inverted "urn" shape among Germans vs. an asymmetric young adult overhang among non-Germans) and a higher male share in young immigrant cohorts.
* **Operationalization**: Direct standardization of rates to the shared total population aged 14+ using official administrative age bands (BKA BV-01/BV-02, Destatis Genesis `12411-0006`).
* **Falsification Criterion**: If the directly age-standardized disparity ratio does not differ significantly from the crude disparity ratio (reduction < 5%), $H_2$ is refuted.

---

### Hypothesis 3 (Socioeconomic Status as a Causal Mediator)
> **$H_3$**: Income poverty, labor market restrictions, and living in institutionalized precarity act primarily as **mediators** along the causal pathway between legal immigrant status and delinquency risk. Under equivalent socioeconomic conditions, the residual disparity decreases substantially toward parity.
* **Operationalization**: Integration with representative darkfield surveys and longitudinal panels (KFN FB 107/109, SOEP, Boers & Reinecke) that measure individual socioeconomic status (SES) at the person level.
* **Falsification Criterion**: If longitudinal panel studies demonstrate that the disparity remains substantially elevated after full controls for SES, school track, and family context (Odds Ratio $\text{OR} > 1.30, p < 0.05$), $H_3$ is refuted.

---

### Hypothesis 4 (Darkfield Research & Reporting Bias)
> **$H_4$**: Criminological victim and self-report surveys document a systematically higher propensity to report offenses committed by strangers or perceived ethnic outgroup members to the police. This asymmetry accounts for an additional fraction of the residual disparity observed in police registers.
* **Operationalization**: Sensitivity analysis incorporating published differential reporting rates from KFN victim surveys.
* **Falsification Criterion**: If victim surveys demonstrate that offenses committed by Germans and non-Germans are reported to the police with identical probability across all dyadic constellations, $H_4$ is refuted.
