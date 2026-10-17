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
> 3. **Pipeline Reproducibility:** All 16 CSV files are generated deterministically by [`src/data_preparation.py`](../src/data_preparation.py) with automated integrity assertions.

---

## 1. Comprehensive Synopsis of Active Datasets (16 Files)

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
| [`panel_g_age_crime_curve.csv`](./panel_g_age_crime_curve.csv) | **Panel I** (Universal Age-Crime Curves) | Age-specific crime suspect rates for males (crude German/non-German from T40/T50 ÷ BV-01/02/AZR; controlled = Raw Non-German × CRIMOC 0.493 for 14–25 y.). | BKA PKS T40/T50; BV-01/02; Destatis 12521-04; Boers & Reinecke (2019) | German male peak: 1164.6 per 100k (ages 14–18); Crude disparity 2.5×–3.4×; controlled series isolates Nennerproblem in adulthood. |
| [`panel_h_ses_regression_deciles.csv`](./panel_h_ses_regression_deciles.csv) | **Panel H** (SES Regression) | Econometric regression rates of violent delinquency across income deciles with empirical standard errors (Ages 14–16). | KFN Research Report No. 144; SOEP v38; Walburg (2014) | Slope $\beta \approx -0.41$; rate difference per decile $< 3$ per 100k ($p > 0.05$, statistically indistinguishable). |
| [`young_male_share_by_nationality.csv`](./young_male_share_by_nationality.csv) | **Panel E / Demographics** | Empirical sex and age proportions of young cohorts (14–21 yrs) from BKA BV-01 and BV-02 for exact conditional probability $P(M \mid Y, g)$. | BKA BV-01 & BV-02 (2023) | Young male share (14–21 yrs): 51.3% (German) vs. 53.9% (non-German). |
| [`literature_empirical_benchmarks.csv`](./literature_empirical_benchmarks.csv) | **Empirical Benchmarks** | Auditable literature and register benchmarks including Moffitt (1993) maturity gap, Sampson/Laub (1993) desistance, CRIMOC (2019), and EU-SILC poverty rates. | Moffitt (1993); Sampson & Laub (1993); Destatis; BA; KFN; CRIMOC | 79 parameters with exact citations, table numbers, quotes, and DOIs. |

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
  * Controlled series: Rather than multiplying the German series by $1.054$, the pipeline directly controls the empirical Raw Non-German series using the CRIMOC multivariate attenuation factor ($\text{factor} = 1.054 / 2.14 = 0.4925$, a $-50.7\%$ reduction) bounded within the 14–25 survey window (`Raw Non-German (14–25 J. CRIMOC-bereinigt)`). This flattens the adolescent peak toward the German baseline and leaves the adult residual as an administrative *Nennerproblem* artifact.
* **Limitations:** AZR population for ages 60+ is ~27% higher than the derived resident denominator, making crude rates conservative for older brackets. The controlled series represents a literature-based benchmark of complete covariate adjustment.

---

### 2.5 [`panel_h_ses_regression_deciles.csv`](./panel_h_ses_regression_deciles.csv)
* **Purpose:** Provides income decile violent delinquency rates and standard errors from KFN FB 144 ($N = 20,407$) for econometric regression without synthetic jitter (Ages 14–16).
* **Variables:** `ses_dezil`, `dezil_bezeichnung`, `perzentil_bereich`, `ses_dezil_perzentil`, `rate_deutsche_maenner_pro_100k`, `standardfehler_deutsche`, `rate_nichtdeutsche_maenner_pro_100k`, `standardfehler_nichtdeutsche`, `differenz_faelle_pro_100k`, `relatives_risiko_ratio`, `steigung_beta_de`, `steigung_beta_nde`, `statistische_signifikanz`, `quelle`.
* **Empirical Finding:** Socioeconomic protective gradients run parallel ($\beta_{\text{DE}} = -0.41$, $\beta_{\text{NDE}} = -0.42$). In every income decile, the rate difference between German and non-German youth is small ($< 3$ per 100,000) and statistically non-significant ($p > 0.05$).

---

## 3. Data Pipeline & Modeling Integration in [`src/modeling.py`](../src/modeling.py)

1. **Single Source of Truth:** All inferential statistical modeling, sensitivity testing, and figure rendering are performed in [`src/modeling.py`](../src/modeling.py).
2. **Panel E Joint Risk Calculation:**
   * Computed via the official **conditional chain rule**:
     $$P(\text{Risk} \mid g) = P(Y \mid g) \cdot P(M \mid Y, g) \cdot P(\text{Pov} \mid Y, M, g)$$
   * German: $15.9\% \times 51.3\% \times 21.4\% = \mathbf{1.7\%}$
   * Non-German: $31.2\% \times 53.9\% \times 47.0\% = \mathbf{7.9\%}$
   * Disparity ratio: **4.55×–4.65×**, bounded by Fréchet–Hoeffding analytical bounds ($[0.0\%, 3.4\%]$ vs. $[0.3\%, 14.7\%]$).
3. **Panel G Multivariate Decomposition:**
   * **v1 Matrix:** Displays the static 2-bar controlled benchmark from CRIMOC ($245.0$ vs. $258.2$ per 100k, $\text{OR} = 1.054$, $p > 0.05$).
   * **v2 Matrix:** Implements the authentic CRIMOC 5-bar waterfall (Boers & Reinecke 2019 Table 7.3, youth ages 14–25):
     * German baseline: $245.0$
     * Non-German crude: $524.3$ ($\text{OR} = 2.140$)
     * After SES & school track: $362.6$ ($\text{OR} = 1.480$)
     * After peer group & deviance: $258.2$ ($\text{OR} = 1.054$)
     * Residual difference: $+13.2$ per 1,000 ($p = 0.38$, statistically indistinguishable).
4. **Panel I Universal Age-Crime Curves (Conclusion of the Storyline):**
   * Serves as the ultimate synthesis across the entire life course (ages 14–80, starting at legal criminal responsibility), bringing together official police registry curves with empirical longitudinal controls.
   * Applying the CRIMOC attenuation factor ($0.4925$) to the empirical Raw Non-German suspect rate within the survey window (ages 14–25) flattens the adolescent spike, clearly isolating the administrative denominator problem (*Nennerproblem*) in adult ages.


