# Documentation & Data Codebook (`/datasets`)
## Empirical Deconstruction of Crime Disparities (BKA PKS 2023, Destatis Census 2022, Microcensus & Longitudinal Studies)

---

### Overview & Methodological Focus

The [`/datasets`](./) directory contains all structured, auditable primary and derived datasets in CSV format that underpin the 9-panel visualization matrix ([`src/modeling.py`](../src/modeling.py)), the methodological architecture ([`methodology/methodology.md`](../methodology/methodology.md)), and the scientific audit ([`literature/citations.md`](../literature/citations.md)).

> [!IMPORTANT]
> **Complete Elimination of Guessed Distributions in Favor of Empirical Registers:**
> All legacy synthetic random simulations (such as arbitrary Gaussian GMMs for age in Panel B or beta random variables for SES in Panel C) have been strictly replaced by **empirical official register histograms and microdata cross-tabulations**:
> 1. **Panel B (Age Structure):** Based on single-year cohorts and 5-year brackets from **Destatis Census 2022 & Genesis 12411-0006** ([`panel_b_zensus_age_histogram.csv`](./panel_b_zensus_age_histogram.csv) and [`panel_b_age_distribution.csv`](./panel_b_age_distribution.csv)).
> 2. **Panel C (Socioeconomics):** Based on empirical net equivalised income deciles from the **Destatis Microcensus (EU-SILC) & SOEP v38** ([`panel_c_ses_histogram.csv`](./panel_c_ses_histogram.csv)).
> 3. **Pipeline Reproducibility:** All 17 CSV files are generated deterministically by [`src/data_preparation.py`](../src/data_preparation.py) with automated integrity assertions.

---

## 1. Comprehensive Synopsis of Active Datasets (17 Files)

| Dataset Filename | Associated Panel / Topic | Description & Core Content | Primary Source(s) | Key Metrics & Statistics |
| :--- | :--- | :--- | :--- | :--- |
| [`panel_a_raw_crime_rates.csv`](./panel_a_raw_crime_rates.csv) | **Panel A** (Crude Crime Rates) | Official violent crime figures (Key 892000), total resident population (Destatis update & Census 2022), and crude disparity ratios. | BKA PKS 2023 Tables 20, 40, 50; Destatis Genesis 12411-0006; Census 2022 | TVBZ: **152.4** (German) vs. **584.1** (non-German); Crude Disparity: **3.83×** (all ages, total population). Demonstrates numerator-denominator mismatch. |
| [`bka_tv_gewalt_892000_alter_geschlecht.csv`](./bka_tv_gewalt_892000_alter_geschlecht.csv) | **Panels A, D, I** (Primary Suspects) | Full breakdown of registered violent crime suspects by single age brackets, sex, and citizenship. Long format. | BKA PKS 2023 Tables 20, 40, 50 | Verified identity assertion: Total (T20) = German (T40) + Non-German (T50) across all age-sex cells. |
| [`bka_bevoelkerung_nenner_2023.csv`](./bka_bevoelkerung_nenner_2023.csv) | **Panels A, I / Standardization** | Official denominator population for criminally liable ages (14+) across 4 official BKA age brackets. | BKA Tables BV-01 (German) and BV-02 (Total) | Non-German denominator = Total − German. Reporting date 31.12.2022. |
| [`tvbz_alter_geschlecht_staatsangehoerigkeit.csv`](./tvbz_alter_geschlecht_staatsangehoerigkeit.csv) | **Demographic Rates** | Specific crime suspect rates per 100,000 by age band, sex, and nationality. | BKA Tables 40, 50, BV-01, BV-02 | Demonstrates age-sex specific suspect rates across 14–18, 18–21, 21–60, and 60+. |
| [`tvbz_roh_vs_altersstandardisiert.csv`](./tvbz_roh_vs_altersstandardisiert.csv) | **Standardization** | Direct age-standardization comparing crude rates (ages 14+) with demographically standardized rates. | BKA PKS 2023 & BV-01/02 | Direct standardization reduces the 14+ disparity from 4.31× to 3.48× using total population weights. |
| [`bka_t29_wohnsitz_nichtdeutsche.csv`](./bka_t29_wohnsitz_nichtdeutsche.csv) | **Residency Sensitivity** | Official crime scene and residence relationship of non-German suspects. | BKA PKS 2023 Table 29 (BU-TV-21-T29) | Total crime: 19.5% reside abroad, 18.5% without fixed/unknown residence. Violent crime: 9.3% reside abroad, 18.4% without fixed residence (~27.7% non-resident core). |
| [`tvbz_wohnsitz_sensitivitaet.csv`](./tvbz_wohnsitz_sensitivitaet.csv) | **Residency Sensitivity** | Multi-tier sensitivity analysis of non-German crime rates excluding non-resident categories. | BKA Tables 29, 50, BV-02 | Tier 0 (unadjusted) vs. Tier 1 (excl. foreign residents) vs. Tier 2 (resident core). |
| [`bka_t61_aufenthaltsanlass_gewalt.csv`](./bka_t61_aufenthaltsanlass_gewalt.csv) | **Context of Stay** | Non-German violent crime suspects classified by legal title / reason for stay. | BKA PKS 2023 Table 61 (BU-TV-23-T61) | Asylum seekers: 15.0%, recognized refugees: 8.8%, tolerated stay (Duldung): 6.5%, other lawful stay / EU: 67.4%. |
| [`bka_t62_staatsangehoerigkeiten_gewalt.csv`](./bka_t62_staatsangehoerigkeiten_gewalt.csv) | **Nationalities** | Breakdown of violent crime suspects by specific citizenship. | BKA PKS 2023 Table 62 (BU-TV-22-T62) | Syria (11,316), Turkey (6,880), Romania (5,262), Afghanistan (5,219), Poland (4,401), Iraq (3,569). |
| [`panel_b_age_distribution.csv`](./panel_b_age_distribution.csv) | **Panel B** (Demographic Cohorts) | Age structure of German vs. non-German resident population across 10 criminologically relevant cohorts. | Destatis Genesis 12411-0006; Census 2022 | Share aged 14–30: 15.9% (German) vs. 31.2% (non-German); Disparity ratio: 1.96×. |
| [`panel_b_zensus_age_histogram.csv`](./panel_b_zensus_age_histogram.csv) | **Panel B** (Census Histogram) | **Empirical 5-year histogram** of age distribution from Census 2022 and Genesis 12411 by citizenship. | Destatis Census 2022 Reports; Genesis 12411-0005 & AZR 12521-04 | 18 five-year cohorts (0–4 to 85+); demonstrates severe German demographic aging vs. young non-German peak. |
| [`panel_c_ses_histogram.csv`](./panel_c_ses_histogram.csv) | **Panel C** (Microcensus Histogram) | **Empirical decile histogram** of net equivalised disposable income / SES from Microcensus & SOEP. | Destatis Microcensus EU-SILC (Genesis 12211); SOEP v38 | 10 income deciles (D1–D10); D1–D3 (<= 30th percentile): 61.5% (non-German) vs. 23.3% (German, 2.64×); D1–D4 (< 40th percentile): 72.5% vs. 32.8% (2.21×). |
| [`panel_g_age_crime_curve.csv`](./panel_g_age_crime_curve.csv) | **Panel I** (Universal Age-Crime Curves) | Age-specific crime suspect rates for males (crude German/non-German from T40/T50 ÷ BV-01/02/AZR; residence-adjusted = BKA T29 Tier 3: –13.9%). | BKA PKS T40/T50; BV-01/02; Destatis 12521-04; BKA T29 | German male peak: 1164.6 per 100k (ages 14–18); Crude non-German peak: 3938.7 per 100k; residence-adjusted peak: ~3400 per 100k. |
| [`panel_h_kfn_lebensbedingungen.csv`](./panel_h_kfn_lebensbedingungen.csv) | **Panel H** (Living Conditions) | Authentic empirical youth violent delinquency across 3 living condition control stages ($N = 44,610$, ages 14–16). | KFN Research Report No. 107 (Baier et al. 2009, Abb. 5.24) | Unadjusted 11.5% vs. 20.3% / 22.1% drops under equal conditions (no welfare/Förderschule/abuse) to 6.4% vs. 5.9% / 5.7% ($p = 0.56$ n.s.). |
| [`young_male_share_by_nationality.csv`](./young_male_share_by_nationality.csv) | **Panel E / Demographics** | Empirical sex and age proportions of young cohorts (14–21 yrs) from BKA BV-01 and BV-02 for exact conditional probability $P(M \mid Y, g)$. | BKA BV-01 & BV-02 (2023) | Young male share (14–21 yrs): 51.3% (German) vs. 53.9% (non-German). |
| [`oecd_precarity_crime_meta.csv`](./oecd_precarity_crime_meta.csv) | **Panel J / OECD Meta-Regression** | Curated econometric cross-national dataset pairing empirical precarity disparity ratios ($X_i$) against violent crime effect ratios ($Y_i$) across 7 landmark longitudinal and total-population register studies from 6 OECD peer nations, strictly restricted to young adulthood violent offending (ages 14–33). | Sweden (LISA/BRÅ, Hällsten 2013, Sariaslan 2014), Netherlands (WODC 277, Jennissen 2009), Norway (SSB 728, Skardhamar 2012), US (Pittsburgh Youth Study, Loeber 2012), NZ (Dunedin, Moffitt 1993), Denmark (Mok 2018) | $N = 7$ international studies; WLS meta-regression $\ln(Y) = 0.408 + 0.517 \ln(X)$ ($R^2 = 0.32$); calibrates German precarity projection $\widehat{Y}_{\text{DE}} \in [2.26\times, 2.61\times]$, directly validating the Swedish benchmark ($2.41\times$) with zero circularity. |



---

## 2. Detailed Methodological Notes on Selected Datasets

### 2.1 [`panel_a_raw_crime_rates.csv`](./panel_a_raw_crime_rates.csv)
* **Purpose:** Forms the transparent baseline of the entire analysis (Panel A). Establishes the unadjusted registered suspect rates across the entire resident population.
* **Key Findings:**
  * German violent crime suspect rate: **152.4 per 100,000** (111,517 suspects / 73.15 million residents).
  * Non-German violent crime suspect rate: **584.1 per 100,000** (79,088 suspects / 13.54 million residents).
  * Crude Disparity Ratio: **3.83×** (rising to 4.08× if using the revised Census 2022 denominator).
* **Numerator-Denominator Mismatch (*Nennerproblem*):**
  * The non-German numerator includes tourists, transit passengers, cross-border commuters, and non-registered individuals (~27.7% non-resident share per BKA Table 29), while the denominator includes only registered residents.
  * Because of this distortion, the BKA explicitly refrains from calculating official crime suspect rates (TVBZ) for non-Germans (*IMK-Bericht*, p. 41).

---

### 2.2 [`panel_b_zensus_age_histogram.csv`](./panel_b_zensus_age_histogram.csv)
* **Purpose:** Provides the empirical 5-year binned age structure from the Census 2022 and Destatis Genesis 12411.
* **Variables:** `alterskohorte`, `alter_von`, `alter_bis`, `alter_mitte`, `bevoelkerung_deutsche`, `anteil_deutsche_pct`, `bevoelkerung_nichtdeutsche`, `anteil_nichtdeutsche_pct`, `ueberhang_faktor`, `in_hochrisikofenster`.
* **Empirical Reality:**
  * Non-Germans show a pronounced young-adult peak: ages 20–24 account for **6.74%** and ages 25–29 for **10.04%** (1.4× to 2.0× higher than Germans).
  * In contrast, the German population features a massive Baby-Boomer cohort (ages 55–64: **8.59%** and **8.36%**), where violent crime rates drop below 50 per 100,000. This demographic aging mechanically depresses the German crude baseline.

---

### 2.3 [`panel_c_ses_histogram.csv`](./panel_c_ses_histogram.csv)
* **Purpose:** Provides the empirical income decile distribution from Destatis Microcensus EU-SILC and SOEP.
* **Variables:** `ses_dezil`, `dezil_bezeichnung`, `perzentil_bereich`, `anteil_deutsche_pct`, `anteil_nichtdeutsche_pct`, `ueberhang_faktor_nichtdeutsche`, `status_kategorie`, `risiko_zone_unter_40`.
* **Empirical Reality:**
  * In the lowest income decile D1 (acute poverty), non-Germans are represented at **28.5%**, compared to only **6.5%** of Germans (**4.38× overrepresentation**).
  * Across deciles D1–D3 (cumulative $\le 30$th percentile), **61.5%** of non-Germans reside, compared to **23.3%** of Germans ($2.64\times$ overrepresentation). Across deciles D1–D4 ($\text{SES} < 40$), **72.5%** of non-Germans reside compared to **32.8%** of Germans ($2.21\times$).

---

### 2.4 [`panel_g_age_crime_curve.csv`](./panel_g_age_crime_curve.csv) (Panel I Universal Age-Crime Curves)
* **Purpose:** Age-specific crime suspect rates for males across cohorts, computed directly from source files in `rawdata/` and visualized in Panel I.
* **Derivation:**
  * German male series: Suspects (`BU-TV-12-T40`) / Population (`BKA_BV_01`, 31.12.2022) $\times$ 100,000. Peak occurs at ages 14–18 (1164.6 per 100k) and ages 18–21 (1040.7 per 100k).
  * Non-German male series (crude): Suspects (`BU-TV-17-T50`) / Denominator (`BV-02 − BV-01` for ages 14–21; AZR 12521 for ages 25+). Peak at 14–18 (3467.5 per 100k).
  * Residence-adjusted series: Evaluates BKA Table 29 Tier 3 correction ($-13.88\%$ non-residents / no fixed abode) across age bands (`tvbz_nichtdeutsche_maenner_wohnsitzbereinigt`), lowering the peak to $\sim 3,400$ per 100k.
  * Controlled series (`tvbz_nichtdeutsche_maenner_kontrolliert`): Evaluates full structural control benchmark via verified KFN FB 109 multilevel odds ratio ($\text{Exp}(B) = 1.003$ n.s.).
* **Limitations:** AZR population for ages 60+ is ~27% higher than the derived resident denominator, making crude rates conservative for older brackets.

---

### 2.5 [`panel_h_kfn_lebensbedingungen.csv`](./panel_h_kfn_lebensbedingungen.csv)
* **Purpose:** Provides verbatim empirical youth violent delinquency prevalence data across 3 progressive control conditions from the nationwide KFN youth survey (Forschungsbericht Nr. 107, Baier et al. 2009, Abbildung 5.24, p. 86, $N = 44,610$ 9th-graders aged 14–16). Also mirrored in `panel_h_ses_regression_deciles.csv` for pipeline compatibility.
* **Variables:** `stufe_id`, `stufe_name_de`, `stufe_name_en`, `herkunft_gruppe`, `herkunft_label_de`, `herkunft_label_en`, `n_stichprobe`, `gewalttaeter_praevalenz_pct`, `quelle`.
* **Empirical Finding:**
  * **Stage 1 (Unadjusted / All Adolescents)**: German: 11.5% ($N = 22,233$); Turkish origin: 20.3% ($N = 812$); Ex-Yugoslavia: 22.1% ($N = 267$).
  * **Stage 2 (Peer-Controlled, $\le 5$ delinquent peers)**: German: 7.7% ($N = 21,399$); Turkish: 11.9% ($N = 724$); Ex-Yugoslavia: 11.4% ($N = 228$).
  * **Stage 3 (Equal Living Conditions: no welfare dependency, no Förderschule, no severe parental physical abuse)**: German: 6.4% ($N = 17,318$); Turkish: 5.9% ($N = 505$); Ex-Yugoslavia: 5.7% ($N = 173$).
  * **Statistical Significance**: Differences in Stage 3 are statistically non-significant ($p = 0.56$ n.s., pooled $\text{OR} = 0.909$ $[0.66; 1.26]$). When living conditions are equalized, violent delinquency drops symmetrically across all groups, with immigrant youth exhibiting rates slightly below the German baseline.

---

## 3. Data Pipeline & Modeling Integration in [`src/modeling.py`](../src/modeling.py)

1. **Single Source of Truth:** All inferential statistical modeling, sensitivity testing, and figure rendering are performed in [`src/modeling.py`](../src/modeling.py).
2. **Panel E Joint Risk Calculation:**
   * Computed via the official **conditional chain rule across the harmonized 14–30 window**:
     $$P(\text{Risk} \mid g) = P(Y \mid g) \cdot P(M \mid Y, g) \cdot P(\text{Pov} \mid Y, M, g)$$
   * German: $15.9\% \times 51.2\% \times 16.32\% = \mathbf{1.3\%}$
   * Non-German: $31.2\% \times 55.0\% \times 39.05\% = \mathbf{6.7\%}$
   * Disparity ratio: **5.04×**, bounded by Fréchet–Hoeffding analytical bounds ($[0.0\%, 2.6\%]$ vs. $[0.0\%, 12.2\%]$) and Plackett copula sensitivity ($4.81\times$ to $5.21\times$).
3. **Panel G Official BKA Register Decomposition (Waterfall):**
   * Implements the 3 empirical register stages for males 14+:
     * 1. Raw PKS Rate: **1,203.4** per 100k ($4.34\times$ vs. German raw 277.5)
     * 2. Residence Adjustment (BKA T29 Tier 3: $-13.9\%$): **1,036.4** per 100k ($3.74\times$)
     * 3. Direct Age Standardization (Destatis): **880.3** per 100k ($3.08\times$ vs. German baseline **285.8**)
   * Documents the boundary of register data (PKS records neither SES nor reporting bias).
4. **Panel I Universal Age-Crime Curves (Ages 14–80):**
   * Serves as the ultimate synthesis across the entire life course (ages 14–80, starting at statutory criminal responsibility § 19 StGB).
   * Compares German baseline (T40 / BV-01), Raw Non-German (T50 / AZR), and Residence-Adjusted Non-German (T29 Tier 3: $-13.9\%$) without synthetic survey attenuation multipliers.
5. **Panel F Bivariate Delinquency Model (Age × SES Surface):**
   * Evaluates the continuous bivariate delinquency surface across ages 14–80 and SES percentiles 0–100.
   * Parameterizes the precarity gradient using the Swedish linked population registry relative risk ($RR = 2.41\times$, Hällsten et al. 2013 Table 1 p. 45, key `SWEDEN_LISA_REGISTER_PRECARITY_RR`) centered at $\text{SES} < 40$.
   * Enforces exact mathematical marginal conservation: $\int_0^{100} R(a, s) \frac{ds}{100} \equiv A_{\text{PKS}}(a)$ identically across all $a \in [14, 80]$ (drift $< 10^{-10}$).
   * In line with the Responsible Demographics Protocol, model surface points remain strictly in-memory for visualization and are never mixed with raw descriptive registers in `datasets/`.



