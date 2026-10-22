# Research Hypotheses & Causal Models

This investigation formulates four *a priori*, falsifiable empirical hypotheses regarding violent crime suspect data (BKA PKS Offense Key 892000, 2023) and criminological darkfield surveys, establishing explicit causal pathways and quantitative falsification criteria prior to econometric modeling:

---

### Hypothesis 1 (Denominator Matching & Residency Sensitivity)
> **$H_1$**: A substantial proportion of non-German suspects registered in the PKS does not belong to the permanent resident population (*Wohnbevölkerung*). Because official population denominators published by Destatis count strictly registered residents on a fixed reporting date, this numerator-denominator mismatch (*Nennerproblem*) mechanically inflates the crude non-German rate.
* **Operationalization**: Quantitative calculation of residence-stratified suspect rates (TVBZ per 100,000) using BKA PKS Table 29 (*Tatort-Wohnsitz der Tatverdächtigen*):
  - *Tier 0 (Unadjusted Total)*: All registered suspects.
  - *Tier 1 (Territorial Exclusion)*: Suspects excluding non-residents living abroad (*Wohnsitz im Ausland*).
  - *Tier 2 (Permanent Resident Core)*: Suspects excluding foreign residents and individuals without fixed/known residence (*ohne festen / unbekannten Wohnsitz*).
* **Falsification Criterion**: If the proportion of non-resident suspects in Offense Key 892000 is below 3.0%, or if the Tier 2 rate ratio does not differ from the crude ratio by at least 5%, the denominator mismatch hypothesis $H_1$ is deemed refuted.

---

### Hypothesis 2 (Demographic Age and Sex Standardization)
> **$H_2$**: Disparities in crude suspect rates are heavily confounded by differing demographic population structures—specifically the aging inverted "urn" shape of the German population (34.7% of males 14+ aged 60+, where violent delinquency is < 50 per 100k) versus the young adult concentration of non-Germans (31.2% aged 14–30 vs. 15.9% German, a 1.96× youth overhang), compounded by higher male shares in young immigrant cohorts.
* **Operationalization**: Direct age-and-sex standardization ($w_{a,s}$) to the joint resident population aged 14+ using official administrative age bands (BKA BV-01/BV-02, Destatis Genesis `12411-0006`, AZR `12521-04`).
* **Falsification Criterion**: If the directly age-standardized disparity ratio is statistically indistinguishable from the crude disparity ratio (overlapping 95% Poisson confidence intervals) or yields a relative reduction of less than 5.0%, $H_2$ is refuted. *(Note: Broad source age bands, e.g. 21–60, represent a documented conservative lower bound of the true demographic age effect).*

---

### Hypothesis 3 (Socioeconomic Status as a Causal Mediator)
> **$H_3$**: Income poverty, labor market barriers, welfare dependency, and institutional housing precarity act primarily as **endogenous mediators** along the causal pathway between legal immigrant/citizenship status and delinquency risk ($X \to M \to Y$). Under equivalent socioeconomic living conditions, the residual disparity decreases substantially toward parity.
* **Operationalization**: Integration with representative criminological microdata surveys and longitudinal panels (KFN Research Reports FB 107 and FB 109, Destatis Mikrozensus EU-SILC, CRIMOC panel) measuring socioeconomic indicators, school tracks, and parental socialization at the individual level.
* **Equivalence Testing & Falsification Criterion**:
  - *Refutation Threshold*: If representative microdata surveys demonstrate that the disparity remains substantially elevated after full controls for socioeconomic status, school track, and family context ($\text{Odds Ratio } \text{OR} > 1.30, p < 0.05$), $H_3$ is refuted.
  - *Equivalence Evaluation*: Compatibility with parity is assessed via Two One-Sided Tests (TOST) against an equivalence boundary of $\pm 30\%$ ($\text{OR} \in [0.77, 1.30]$).
  - *Scope Boundary*: Because person-level socioeconomic microdata is available primarily for youth school cohorts (ages 14–16), findings are reported as Controlled Direct Effects (CDE) within youth darkfield cohorts rather than extrapolated as hard subtractions onto the entire adult police register.

---

### Hypothesis 4 (Darkfield Research & Reporting Bias)
> **$H_4$**: Criminological victim and self-report surveys document systematically higher reporting propensities (*Anzeigebereitschaft*) when offenses involve strangers or perceived ethnic outgroup members, introducing reporting asymmetries into police workload statistics.
* **Operationalization**: Empirical sensitivity evaluation based on published representative victim surveys:
  - *Dyadic Ethnic Gap* (Baier et al. 2009 / KFN FB 107, p. 11): 29.3% reporting rate for German victims facing migrant youth vs. 19.5% for German perpetrators (factor 1.50×).
  - *Stranger vs. Acquaintance Gap* (Pfeiffer et al. 2018, p. 75, Abb. 19): 29.5% reporting rate for unknown/stranger perpetrators vs. 12.7% for known acquaintances (factor 2.32×).
* **Falsification Criterion**: If victim surveys demonstrate that violent offenses are reported to the police with equal probability regardless of perpetrator acquaintance or outgroup status (reporting disparity factor $\le 1.05$), $H_4$ is refuted.
