# Dataset Provenance (`/datasets`)

All CSV files at this directory level are computed deterministically by [`src/data_preparation.py`](../src/data_preparation.py) from source files in `rawdata/`.
Running `python src/data_preparation.py --download` re-fetches primary raw data files and regenerates `rawdata/MANIFEST.csv` (URL, date, SHA-256).
Running without `--download` verifies the SHA-256 checksums against the manifest and regenerates all datasets locally.

| CSV | Raw Source File(s) | Computation / Derivation |
|---|---|---|
| `panel_a_raw_crime_rates.csv` | BKA T20, T40, T50, Destatis Genesis 12411-0006, Zensus 2022 | Broadest crude crime suspect rates across all ages (total resident population: 152.4 German vs. 584.1 Non-German per 100k, $3.83\times$ crude disparity). Highlights the unadjusted starting point and the numerator-denominator mismatch (*Nennerproblem*). |
| `bka_tv_gewalt_892000_alter_geschlecht.csv` | T20, T40, T50 | Offense Key 892000 (Violent Crime), all age columns, long format. Integrity assertion: T20 = T40 + T50. |
| `bka_bevoelkerung_nenner_2023.csv` | BKA BV-01 (German), BKA BV-02 (Total) | Non-German = Total − German, ages 14+ across 4 official age bands. Reporting date 31.12.2022. |
| `tvbz_alter_geschlecht_staatsangehoerigkeit.csv` | Above two files | Suspects / Population $\times$ 100,000 per age-sex band. |
| `tvbz_roh_vs_altersstandardisiert.csv` | Above two files | Crude rates for ages 14+ and direct standardization against the total population 14+ (weights per band). |
| `bka_t29_wohnsitz_nichtdeutsche.csv` | T29 | Shares of suspects residing abroad or without fixed / with unknown residence. |
| `tvbz_wohnsitz_sensitivitaet.csv` | T29 + above | Non-German suspect rate excluding non-resident categories. Assumes uniform distribution across age bands. |
| `bka_t61_aufenthaltsanlass_gewalt.csv` | T61 | Rows for offense key 892000 (reasons for stay). |
| `bka_t62_staatsangehoerigkeiten_gewalt.csv` | T62 | Columns sorted by suspect volume. |
| `panel_b_age_distribution.csv` | Destatis Genesis 12411-0006, Zensus 2022, AZR 12521-04 | Age distribution across 9 criminological cohorts (0–13 to 65+) + 14–30 high-risk window with population counts and shares. |
| `panel_b_zensus_age_histogram.csv` | Destatis Genesis 12411-0005, Zensus 2022, AZR 12521-04 | 18 five-year age cohorts (0–4 to 85+) with absolute population counts and proportions. |
| `panel_c_ses_histogram.csv` | Destatis Microcensus EU-SILC (Genesis 12211) & SOEP v38 | 10 net equivalised income deciles (D1 to D10) by nationality and poverty risk zone (< 40%). |
| `panel_g_age_crime_curve.csv` | T40, T50, BV-01, BV-02, Destatis 12521-04 (AZR), BKA T29 Tier 3 | Male suspect rates across age bands (German baseline, raw Non-German, and residence-adjusted Non-German deducting 13.9% non-residents). Pure register data without synthetic multipliers. |
| `panel_h_kfn_lebensbedingungen.csv` | KFN FB 107 (Baier et al. 2009, Abb. 5.24 & Tab. 5.2) | Youth violent delinquency prevalence across 3 conditions (unadjusted, peer-controlled, and equal living conditions: no welfare, no Förderschule, no severe family violence) for German, Turkish, and Ex-Yugoslav youth ($N = 44,610$). |
| `panel_h_ses_regression_deciles.csv` | KFN FB 107 (Baier et al. 2009, Abb. 5.24) | Maintained for backward compatibility; contains identical empirical 3-stage living conditions data from KFN FB 107. |
| `young_male_share_by_nationality.csv` | BKA BV-01 (German), BKA BV-02 (Total) | Empirical male shares in young cohorts (14–18, 18–21, 14–21 combined) by nationality. |
| `literature_empirical_benchmarks.csv` | Destatis Microcensus EU-SILC, BA, KFN (FB 107, FB 109, Pfeiffer 2018), Moffitt (1993) | Fully auditable criminological literature and official register benchmarks with exact citations, table locations, DOIs, and URLs. |
| `oecd_precarity_crime_meta.csv` | Primary literature PDFs in `literature/` (Sweden LISA Hällsten/Sariaslan, Netherlands WODC 277, Norway SSB 728, US NIJ Loeber, NZ Moffitt, Denmark Mok) | Curated cross-national empirical dataset ($N=7$ studies, 6 OECD peer nations) pairing precarity disparity ratios ($X_i$) against violent crime effect ratios ($Y_i$), strictly restricted to young adulthood violent offending (ages 14–33). Analyzed via WLS meta-regression in `src/modeling.py` (Panel J). |


## Known Limitations

* Denominators in BKA tables are available in 4 broad age bands (14–18, 18–21, 21–60, 60+). The 21–60 band is especially wide. Non-Germans within this bracket cluster heavily between ages 21–35, whereas Germans cluster between 45–58. Standardization over broad bands therefore represents a conservative lower bound of the demographic age effect.
* The non-German resident population is derived by subtraction ($\text{Total} - \text{German}$). The BKA explicitly avoids publishing official crime suspect rates (TVBZ) for non-Germans due to denominator distortion (*IMK-Bericht*, p. 41).
* SES distributions and darkfield risk factor benchmarks are drawn from Microcensus EU-SILC and established criminological representative surveys (KFN FB 107, FB 109, Pfeiffer et al. 2018). All data is stored in `datasets/` and processed for statistical inference by `src/modeling.py`.


