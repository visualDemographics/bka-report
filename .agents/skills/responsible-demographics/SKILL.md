---
name: responsible-demographics
description: >-
  Domain-specific operational protocol and standard operating procedure for responsible demographic analysis, population standardization, and causal inference on sensitive social, criminological, and population registries (e.g., BKA PKS crime registers, census cohorts, microcensus socio-economics). Use whenever standardizing demographic cohorts (age, sex, residency), resolving numerator-denominator mismatches (Nennerproblem), replacing synthetic Gaussian age assumptions with empirical population pyramids, computing joint risk distributions vs. marginals, or separating demographic confounders from socio-economic mediators.
---

# Responsible Demographics Protocol
## Standard Operating Procedure for Demographic Standardization, Registry Denominators, and Causal Disparity Analysis

This skill defines the mandatory repository structure, data pipeline standards, statistical safeguards, and a complete domain framework for **Responsible Demographics** when working with population registries, crime statistics, and sensitive social disparity indicators (extending the general [`responsible-research`](../responsible-research/SKILL.md) protocol).

---

## 1. Expected Repository Structure

Every empirical research project must maintain a modular, auditable directory structure that guarantees complete traceability from primary sources to published findings:

```text
/
├── goal/
│   ├── description.md       # Precise definition of research questions and scope
│   └── hypothesis.md        # Falsifiable hypotheses with expected causal directions
├── literature/
│   ├── literature.md        # Structured table of references with DOIs, URLs, and summaries
│   └── [NAME].pdf           # Primary research reports, working papers, and legal bases
├── rawdata/                 # (or raw/) Unmodified primary source files exactly as downloaded
│   ├── [NAME].csv           # Original register / survey exports
│   ├── [NAME].xlsx          # Official statistical releases (e.g., Destatis, BKA PKS)
│   └── rawdata.md           # Manifest table with source URLs, download timestamps, and SHA-256 hashes
├── datasets/                # Cleaned, structured, and auditable data derived exclusively from rawdata/
│   ├── [NAME].csv           # Reproducible datasets ready for analysis
│   └── datasets.md          # Data dictionary: columns, units, derivations, and limitations
├── src/
│   ├── data_preparation.py  # Fully automated, deterministic pipeline: rawdata -> datasets
│   └── modeling.py          # Fits statistical models to empirical data AND generates all plots
├── plots/
│   ├── [NAME].png           # High-resolution figures generated deterministically by modeling.py
│   └── plot.md              # Documentation of each individual plot with detailed explanation of validity
└── methodology/
    └── methodology.md       # Explicit documentation of assumptions, confounders, and limitations
```

---

## 2. Research Pipeline

Every empirical investigation must strictly follow this sequential, closed-loop pipeline:

$$\text{goal} \longrightarrow \text{literature} \longrightarrow \text{rawdata} \longrightarrow \text{datasets} \longrightarrow \text{src} \longrightarrow \text{plots} \longrightarrow \text{methodology} \longrightarrow \text{goal}$$

1. **Goal**: Formulate the empirical question without predetermining outcomes.
2. **Literature**: Map existing evidence, theoretical frameworks, and established empirical consensus.
3. **Rawdata**: Secure unmodified register extracts or microdata with verified provenance.
4. **Datasets**: Compute cleaned, standardized tables via automated scripts with integrity assertions (`assert`).
5. **Src (`modeling.py`)**: Fit models to empirical datasets and generate all publication-ready plots. `modeling.py` serves as the single source of truth for both inferential calculations and visual outputs.
6. **Plots (`plot.md`)**: Save generated figures in `/plots/`. Maintain `plots/plot.md` documenting every individual plot with its data provenance, statistical validity, model assumptions, and limitations.
7. **Methodology**: Audit the results against potential confounders, mediation paths, and known limitations.
8. **Goal Re-Evaluation**: Check whether hypotheses are supported, refuted, or require refined models.

---

## 3. Bad Practices to Avoid

### Bad Research Practices:
* **Cherry-picking literature**: Citing only studies that confirm the favored narrative while omitting contrary peer-reviewed evidence.
* **Cherry-picking data**: Filtering time windows, offense categories, or subgroups without pre-registered criteria.
* **Overstating results**: Presenting cross-sectional correlations or ecological associations as definitive causal proof.
* **Hiding limitations**: Omitting known measurement errors, administrative changes, or sample attrition.
* **Citing unverified sources**: Misattributing study authors, publication years, or referencing incorrect table numbers (e.g., citing BKA Table 62 for residency status instead of Table 29).
* **Concealing assumptions**: Presenting model projections or literature transfers as directly measured empirical facts.

### Bad Statistical Practices:
* **P-hacking & HARKing**: Testing multiple ad-hoc combinations until a significant p-value appears, or hypothesizing after results are known.
* **The Null-Hypothesis Parity Fallacy (Absence of Evidence $\neq$ Evidence of Absence)**: Never claim that group disparities "disappear" or "reach exact parity" under controls merely because $p > 0.05$. In representative microdata surveys, a non-significant odds ratio only fails to reject the null hypothesis; it does not prove zero difference. Conduct formal **Two One-Sided Tests (TOST)** against explicit equivalence bounds ($\pm \Delta$).
* **Building joint distributions from single marginals**: Assuming independence ($P(A \cap B \cap C) = P(A) \cdot P(B) \cdot P(C)$) when covariates (e.g., age, sex, income) are inherently correlated. If microdata is partially unobserved, formulate an illustrative baseline model ($M_{\text{ind}}$) strictly bounded by analytical Fréchet–Hoeffding limits and Plackett copula sensitivity.
* **Conflating descriptive and inferential statistics**:
  - *Descriptive statistics* must come directly from `/datasets` and reflect audited raw facts.
  - *Inferential statistics* must be produced by `/src/modeling.py`, displaying model parameters, standard errors, and confidence intervals.
* **Asserting statistical insignificance without tests**: Claiming two rates are "not significantly different" without calculating confidence intervals, standard errors, or hypothesis tests.
* **Conflating mediators with confounders**: Treating intermediate mechanisms on the causal pathway as if they were pre-treatment baseline confounders.

### Bad Code Practices (Strict AST Contract):
* **Uncommented, opaque code**: Writing scripts without docstrings, type hints, or explanatory comments.
* **Hardcoded guessed parameters**: Guessing statistical parameters ($\lambda, \mu, \sigma$, weights) and pasting them into source code.
* **Silent dictionary lookup fallbacks**: Never use `.get(key, <numeric_literal>)` in demographic or criminological pipelines. Always use direct lookups (`df.loc[key]` or `dict[key]`) so missing categories raise an immediate `KeyError`.
* **Conditional ternary fallbacks & domain float defaults**: Never write `x if cond else <domain_float>` or declare domain floats in function signatures (e.g., `precarity_rr=2.54`). Ingest parameters dynamically from `/datasets` or `literature_empirical_benchmarks.csv`.
* **Hardcoded empirical numbers in equality assertions**: Never write `assert count == 111517` with magic numbers. Assert against structural identities (`assert T20 == T40 + T50`) or benchmark lookups.
* **Generating synthetic data for inferential claims**: Never use `scipy.stats.norm.rvs(size=...)` to manufacture artificial observations and present them as empirical findings. Use `scipy.stats.<dist>.fit(...)` or empirical non-parametric density estimation (KDE/histograms) fitted to actual data.
* **Missing pipeline assertions**: Omitting integrity checks (e.g., `assert T20 == T40 + T50`, verifying that subgroup sums equal the grand total; verifying male + female equals total).
* **Interpolating unobservable denominator brackets**: When official register brackets do not align (e.g., BV-02 groups 21–60 while AZR groups 20–25, leaving 21–25 non-German males unobservable), retain `NaN` explicitly. Never invent an interpolated cell.
* **Misleading plot aesthetics**: Prioritizing artificial smoothness over data accuracy (e.g., drawing smooth parametric bell curves over distinctly bimodal or skewed distributions).
* **Decoupled or ad-hoc plotting**: Hardcoding values into standalone plotting scripts instead of having `src/modeling.py` fit models to empirical data from `/datasets` and generate all output plots.
* **Missing plot validity documentation**: Generating visual figures without maintaining `plots/plot.md` documenting the data provenance, statistical validity, and boundaries of each individual plot.

---

## 4. Responsible Demographics Framework

When analyzing population subgroups, demographic cohorts, and disparity indicators, researchers must adhere to these seven core pillars:

```text
                       RESPONSIBLE DEMOGRAPHICS FRAMEWORK
                                        │
    ┌───────────────────┬───────────────┴───────────────┬───────────────────┐
    ▼                   ▼                               ▼                   ▼
1. Denominator      2. Empirical                    3. Joint Risk       4. Causal DAGs:
   Matching            Cohorts vs. Normal              vs. Marginals       Mediators vs.
   (Nennerproblem)     Distributions                   (Mikrozensus)       Confounders
```

### Pillar 1: Population Demarcation & Denominator Matching (*Das Nennerproblem*)
1. **The Numerator-Denominator Mismatch**:
   * Official police registries (e.g., BKA PKS) count **registered suspects** apprehended within national territory during the calendar year.
   * Statistical offices (e.g., Destatis) count the **registered resident population** (*Wohnbevölkerung*) on a fixed reporting date.
   * The suspect numerator includes individuals absent from the resident denominator: tourists, cross-border commuters, business travelers, transit passengers, stationed military personnel, and individuals with irregular/unauthorized stay.
2. **Official Statistical Directives**:
   * Official statistical offices (such as the BKA in its *IMK-Bericht*, p. 41 & 50) intentionally refrain from publishing crime rates (TVBZ) for non-citizens because dividing a resident denominator into an open numerator creates an artificial mathematical distortion.
   * Any rate derived by researchers for non-citizens must be clearly designated as an **upper-bound estimate**, not an official registry rate.
3. **Mandatory Residence Sensitivity Tiers (PKS Table 29)**:
   * Use **BKA Table 29** (*Tatort-Wohnsitz der Tatverdächtigen*) to evaluate residency status:
     - **Tier 0 (Unadjusted Total)**: All registered suspects ($4.34\times$ for males 14+; $3.83\times$ across all ages).
     - **Tier 1 (Territorial Exclusion)**: Suspects excluding those residing abroad (*Wohnsitz im Ausland*, $4.21\times$ for males 14+).
     - **Tier 2 (Permanent Resident Core)**: Suspects excluding both foreign residents and those without fixed/known residence (*ohne festen / unbekannten Wohnsitz*, $3.74\times$ for males 14+).
4. **Table Verification**:
   * Do not cite Table 62 for residency status (Table 62 lists specific *nationalities*). Table 29 records *Tatort-Wohnsitz*. Table 61 records *Aufenthaltsanlass*.

### Pillar 2: Empirical Age Pyramids, Life-Course Onset & Unobservable Brackets
1. **Strict Prohibition of Normal Distributions for Age**:
   * Human populations are rarely normally distributed. In aging societies, assuming Gaussian normality (`Normal(47, 15)`) severely distorts demographic reality.
2. **The German Demography is an "Urnenform"**:
   * The German resident population features a massive Baby-Boomer cohort (ages 56–66) and a narrow base of young individuals (< 30).
   * Over 34% of German males aged 14+ are 60 years or older (a demographic bracket with violent crime rates < 50 per 100,000). This aging effect mechanically pulls the overall German rate down.
3. **The Non-German Population Has a High-Risk Age Peak**:
   * Foreign resident populations are disproportionately concentrated in young adulthood (ages 18–35), with only ~13% aged 60+.
   * Because delinquency universally peaks between 16 and 25 years (*Age-Crime Curve*), this demographic structure inflates the crude rate even if age-specific rates were identical.
4. **Direct Age-and-Sex Standardization**:
   * Calculate age- and sex-specific rates:
     $$\text{Rate}_{a,s}^{(g)} = \frac{\text{Suspects}_{a,s}^{(g)}}{\text{Population}_{a,s}^{(g)}} \times 100{,}000$$
   * Standardize using the total population as the reference standard:
     $$\text{Rate}_{\text{std}}^{(g)} = \sum_{a \in A, s \in S} w_{a,s} \cdot \text{Rate}_{a,s}^{(g)}, \quad \text{where } w_{a,s} = \frac{N^{\text{reference}}_{a,s}}{\sum N^{\text{reference}}}$$
5. **Document Coarse Band Aggregation Bias (Conservative Lower Bound)**:
   * If source tables provide broad adult age bands (e.g., `21–60`), document that non-Germans inside this band cluster between 21 and 35, whereas Germans cluster between 45 and 58. Standardization over broad bands represents a **conservative lower bound** of the true demographic age effect.
6. **Universal Life-Course Formulation across Ages 0–80**:
   * Model the continuous life-course Age-Crime curve via a dual-process formulation with a statutory juvenile onset sigmoid (§ 19 StGB criminal responsibility at age 14):
     $$\text{onset}(a) = \frac{1}{1 + \exp(-k_{\text{on}} (a - x_{\text{on}}))}$$
     $$A(a) = \text{onset}(a) \left[ a_{\text{peak}} \exp\left(-\frac{(a - \mu)^2}{2\sigma^2}\right) + a_{\text{adult}} \exp(-a / \tau) \right]$$
7. **Explicit NaN Rule for Incompatible Administrative Denominators**:
   * When administrative tables differ in cohort cuts (e.g., BKA BV-02 reports `21–60` while Destatis AZR 12521-04 reports `20–25`, leaving the non-German male `21–25` denominator unobservable), **preserve `NaN` explicitly**; never interpolate or guess. Anchor non-linear curve knots to discrete observed midpoints (e.g., age 16 for 14–18) to avoid artificial peak inflation between discrete cohorts.

### Pillar 3: Joint-Risk Distributions, Cohort Harmonization ($14\text{--}30$) & Copula Bounds
1. **The Independence Fallacy**:
   * Never estimate multi-variable risk concentrations by multiplying single marginal probabilities:
     $$P(\text{Male} \cap \text{Age 14–30} \cap \text{Poverty}) \neq P(\text{Male}) \cdot P(\text{Age 14–30}) \cdot P(\text{Poverty})$$
2. **Harmonized 14–30 Conditioning Window**:
   * Harmonize all terms in the conditional chain rule to share the exact criminological high-risk window (ages 14–30):
     $$P(\text{Risk} \mid g) = P(\text{Youth 14–30} \mid g) \cdot P(\text{Male} \mid \text{Youth 14–30}, g) \cdot P(\text{Poverty} \mid \text{Youth 14–30, Male}, g)$$
   * Compute $P(\text{Poverty} \mid \text{Youth}, g)$ as the population-weighted composite across microcensus sub-cohorts (14–17, 18–24, 25–29), scaled by the gender-specific poverty factor $k$.
3. **Illustrative Baseline Framing ($M_{\text{ind}}$) & Bounds**:
   * Explicitly label the point estimate as an **illustrative baseline model under conditional independence ($M_{\text{ind}}$)**. Never claim "zero marginals were multiplied".
   * Accompany with **analytical Fréchet–Hoeffding bounds** $[P_{\min}, P_{\max}]$ and **Plackett copula sensitivity** ($\text{OR} \in [0.8, 1.5]$) to confirm stability against dependency violations.

### Pillar 4: Causal Inference — Mediators vs. Confounders & Shapley Decomposition
1. **Confounders (Exogenous Demographics)**:
   * Biological sex and age cohort exist prior to migration or nationality status. Adjusting for them eliminates demographic composition artifacts.
2. **Mediators (Socio-Economic Conditions & Housing)**:
   * Factors like poverty, unemployment, lack of work permits, or living in shared reception facilities lie on the causal pathway between legal status and delinquency:
     $$\text{Status / Origin} \longrightarrow \text{Poverty / Housing (Mediator)} \longrightarrow \text{Delinquency}$$
   * Adjusting for socio-economic status isolates the **Controlled Direct Effect (CDE)**. Both total and direct effects must be transparently reported.
3. **Path-Independent Shapley Value Decomposition**:
   * In sequential waterfall decompositions, ordering alters individual bar steps. Evaluate all $K!$ permutations and report Shapley attribution values ($\phi_j$). In the BKA 14+ register decomposition, Shapley attribution confirms that demographic age structure ($52.2\%$) and denominator non-resident adjustments ($47.8\%$) contribute in roughly equal proportions.
4. **Epidemiological Compositional Standardization ($\text{CF}_{\text{SES}}$) & Symmetric Invariance**:
   * Standardizing an outcome for precarity prevalence ($p_{\text{NDE}}$ vs. $p_{\text{DE}}$) with relative risk $RR$ requires Rothman's population confounding factor:
     $$\text{CF}_{\text{SES}} = \frac{1 + p_{\text{NDE}} (RR - 1)}{1 + p_{\text{DE}} (RR - 1)}$$
   * Standardizing against the observed German baseline exposure produces identically the same relative disparity ratio as setting poverty to zero in both populations (**Symmetric Zero-Poverty Invariance**).

### Pillar 5: Measurement Boundaries of Registry Data vs. Microdata & Sibling Attenuation
1. **No Individual SES in Police Registries**:
   * Official police registries (PKS) record zero indicators for income, schooling, employment, wealth, or housing quality.
2. **Avoid Ecological Fallacies**:
   * Aggregate cross-referencing between PKS suspect counts and Mikrozensus poverty rates is an **ecological comparison**, not an individual-level regression.
3. **Macro-Observational Gradients vs. Discordant Sibling Fixed-Effects**:
   * Population-level register gradients ($RR / HR \approx 2.4\text{--}3.1\times$) reflect clustered structural disadvantage (neighborhood disorder, segregated schooling, family stress). In within-family discordant sibling models (Sariaslan et al. 2014, 2021), income hazard ratios attenuate to near unity ($HR \approx 1.10$). Thus, income is an empirical index of compound social disadvantage, not an isolated cash lever.
4. **Two One-Sided Tests (TOST) for Survey Parity Claims**:
   * In microdata surveys (e.g., KFN FB 107), when group odds ratios reach $p > 0.05$ under controls, do not claim "disparities are proven zero". Conduct TOST equivalence testing against explicit bounds ($\pm 30\%$ vs. $\pm 50\%$).

### Pillar 6: Darkfield Research & Reporting Bias (*Anzeigeverhalten*)
1. **Dual Verified Reporting Biases**:
   * **Dyadic Inter-Ethnic Reporting Differential** (Baier et al. 2009 / KFN FB 107): Offenses against German victims by migrant youths have a $29.3\%$ reporting rate vs. $19.5\%$ for German perpetrators (**$1.50\times$ factor**).
   * **Stranger vs. Acquaintance Reporting Differential** (Pfeiffer et al. 2018): Offenses by strangers or unknown refugees have a $29.5\%$ reporting rate vs. $12.7\%$ for known acquaintances (**$2.32\times$ factor**).
2. **Prohibition of Arbitrary Multipliers**:
   * Never subtract darkfield reporting factors as arbitrary additive deductions from official adult police registries. Report them as qualitative limitations explaining why police registers overstate outgroup disparities compared to representative darkfield surveys.

### Pillar 7: Demographic Identity & Generational Operationalization
1. **Formal Nationality vs. Migration Background**:
   * Official police registers classify individuals strictly by **formal citizenship** at the time of the offense.
   * The "German" baseline aggregates native-born citizens with multi-generational ancestry, naturalized citizens, and second/third-generation immigrants.
2. **Document Baseline Heterogeneity**:
   * Always state clearly whether an analysis compares citizenship (legal status) or migration background (sociological background), as the two concepts have distinct baselines and causal implications.

---

## 5. Handling Scraped Demographic Data, PDF Reports & Literature Benchmarks

When working with demographic tables scraped from official statistical portals (Destatis Genesis-Online, AZR) or extracted from criminological and sociological PDF monographs (KFN surveys, CRIMOC panel, BKA reports):

### 1. Ingestion Protocol:
* **Preserve Untouched Originals**: Store original Excel/CSV registers and downloaded PDFs in `raw/` (or `literature/`).
* **Cryptographic Provenance**: Record the download URL, timestamp, and SHA-256 hash in `rawdata.md` or `raw/MANIFEST.csv`.
* **Zero Hardcoded Magic Numbers**: Never paste odds ratios (e.g. $1.054$), poverty rates (e.g. $35.4\%$), or reporting multipliers (e.g. $2.32\times$) into `src/modeling.py`.
* **The Central Demographic Catalog (`literature_empirical_benchmarks.csv`)**: Any empirical microdata parameter or literature transfer value must be recorded in `datasets/literature_empirical_benchmarks.csv` with exact page numbers, table coordinates, and verbatim quotation.

### 2. Standard Schema & Sample Lines: `literature_empirical_benchmarks.csv`
```csv
parameter_id,themenbereich,indikator,gruppe,wert,einheit,intervall_95_ki,signifikanz_p,stichprobe_n,quelle_autor_institution,quelle_titel,jahr,fundstelle_seite_tabelle,exakte_zeile_fundstelle,exakter_quelltext_zitat,doi_url,lokale_datei,methodischer_status
DESTATIS_ARMUT_DE,Soziooekonomie,Armutsgefaehrdungsquote (Nettoaequivalenzeinkommen < 60% Median),deutsch,12.2,Prozent,,,N > 100.000,Statistisches Bundesamt (Destatis),Mikrozensus EU-SILC: Einkommen und Lebensbedingungen in Deutschland,2023,Pressemitteilung Nr. 419 Tabelle 1,"Tabelle 1, Zeile 2 'Personen ohne Migrationshintergrund'","Personen ohne Migrationshintergrund: 12,2 % (Erhebung EU-SILC 2022/2023)",https://www.destatis.de,literature/citations.md#L44,Amtliche_Repraesentativstatistik
DESTATIS_ARMUT_NDE,Soziooekonomie,Armutsgefaehrdungsquote Auslaender (Nichtdeutsche),nichtdeutsch,35.4,Prozent,,,N > 100.000,Statistisches Bundesamt (Destatis),Mikrozensus EU-SILC: Einkommen und Lebensbedingungen in Deutschland,2023,Pressemitteilung Nr. 419 Tabelle 1,"Tabelle 1, Zeile 5 'Personen mit ausländischer Staatsangehörigkeit'","Ausländerinnen und Ausländer: 35,4 % (mehr als doppelt so häufig von Armut bedroht)",https://www.destatis.de,literature/citations.md#L44,Amtliche_Repraesentativstatistik
CRIMOC_OR_UNADJUSTED,Multivariate_Kohorte,Unbereinigte Odds Ratio Nationalitaet auf Gewaltkriminalitaet,nichtdeutsch_vs_deutsch,2.14,Odds_Ratio,[1.62; 2.83],p < 0.001,N = 3.528,"Boers Klaus, Jost Reinecke (CRIMOC)",Delinquenz im Altersverlauf,2019,Tabelle 7.3 Modell 1 S. 142,"Tabelle 7.3, Seite 142, Modell 1 (bivariate Baseline), Zeile 'Nichtdeutsche Staatsangehörigkeit'","Modell 1: Nichtdeutsch OR = 2,14 (95%-KI: [1,62; 2,83], p < 0,001, Nagelkerke R² = 0,042)",https://www.waxmann.com/buch3966,literature/citations.md#L68-L70,Laengsschnitt_Panelstudie
CRIMOC_OR_CONTROLLED,Multivariate_Kohorte,Vollstaendig kontrollierte Odds Ratio (SES Peergroups Familie Schule),nichtdeutsch_vs_deutsch,1.054,Odds_Ratio,[0.94; 1.18],p = 0.38 (n.s.),N = 3.528,"Boers Klaus, Jost Reinecke (CRIMOC)",Delinquenz im Altersverlauf,2019,Tabelle 7.3 Modell 3 S. 145,"Tabelle 7.3, Seite 145, Modell 3 (Vollständige Kontrolle), Zeile 'Nichtdeutsche Staatsangehörigkeit'","Modell 3: Nichtdeutsch OR = 1,054 (95%-KI: [0,94; 1,18], p = 0,38 n.s.)",https://www.waxmann.com/buch3966,literature/citations.md#L69-L70,Laengsschnitt_Panelstudie
KFN_REGRESSION_SLOPE,Soziooekonomie,Regressionsgradient Gewaltdelinquenz ueber Einkommens-/SES-Dezile,alle,-0.41,Regressionskoeffizient,[-0.49; -0.33],p < 0.001,N = 20.407,"Bergmann et al. (KFN)",Jugendliche in Niedersachsen (Forschungsbericht Nr. 144),2019,Tabelle 4.8 S. 92,"Tabelle 4.8, Seite 92, Zeile 'SES-Dezil', Spalte 'B'","Tabelle 4.8: B = -0,41 (SE = 0,04, Beta = -0,18, p < 0,001)",https://kfn.de/wp-content/uploads/Forschungsberichte/FB_144.pdf,literature/Pfeiffer_Baier_Kliem_2018_FB144.pdf#page=92,Dunkelfeld_Repraesentativsurvey
PFEIFFER_REPORTING_BIAS,Dunkelfeld_Anzeigeverhalten,Doppelter Anzeigeeffekt (Fremde vs. Bekannte Taeter),disparitaet,2.32,Faktor,,,N = 1.250,"Pfeiffer Christian, Dirk Baier, Soeren Kliem (ZHAW & KFN)",Zur Entwicklung der Gewalt in Deutschland,2018,Kapitel 5.2.4 S. 75,"Seite 75, Absatz 2, Zeilen 25-28","S. 75: '...wird eine Gewalttat mehr als doppelt so häufig angezeigt (29,5 % zu 12,7 %, Faktor 2,32)...'",https://doi.org/10.21256/zhaw-2746,literature/Pfeiffer_Baier_Kliem_2018_Gewaltbericht.pdf#page=75,Dunkelfeld_Opfersurvey
```

### 3. Minimum Snippet: `src/data_preparation.py`
Ingests demographic tables, audits benchmark parameters, and enforces demographic accounting identities (`assert`):
```python
import csv, os

def audit_and_prepare_demographics(raw_benchmarks_path, raw_rates_path, out_datasets_path):
    # 1. Audit benchmarks from PDF literature
    benchmarks = {}
    with open(raw_benchmarks_path, "r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            pid = r["parameter_id"].strip()
            val = float(r["wert"])
            assert len(r["exakter_quelltext_zitat"].strip()) > 5, f"Missing quote for {pid}"
            benchmarks[pid] = val

    # 2. Ingest register rates and verify demographic integrity
    cleaned = []
    with open(raw_rates_path, "r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            suspects = float(r["tatverdaechtige"])
            population = float(r["bevoelkerung"])
            assert population > 0, "Denominator cannot be zero!"
            rate_per_100k = round((suspects / population) * 100_000.0, 1)
            cleaned.append({
                "geschlecht": r["geschlecht"],
                "altersband": r["altersband"],
                "tvbz_pro_100k": rate_per_100k
            })

    # 3. Export to datasets/
    with open(out_datasets_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["geschlecht", "altersband", "tvbz_pro_100k"])
        writer.writeheader()
        writer.writerows(cleaned)
    print(f"✓ Audited {len(benchmarks)} benchmarks and exported {len(cleaned)} cohort records.")
```

### 4. Minimum Snippet: `src/modeling.py`
Dynamically accesses demographic benchmark values and fits empirical age curves without synthetic Gaussian data:
```python
import csv, os, matplotlib
matplotlib.use("Agg")  # Non-interactive headless backend
import matplotlib.pyplot as plt, numpy as np
from scipy.optimize import curve_fit

def run_demographic_modeling(dataset_path, benchmarks_path, plot_path):
    # 1. Load benchmarks dynamically (NO hardcoded numbers!)
    benchmarks = {}
    with open(benchmarks_path, "r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            benchmarks[r["parameter_id"].strip()] = float(r["wert"])

    # 2. Ingest empirical rates
    ages, rates = [], []
    with open(dataset_path, "r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            ages.append(float(r["altersmitte"])), rates.append(float(r["tvbz_pro_100k"]))
    ages, rates = np.array(ages), np.array(rates)

    # 3. Fit parametric model to empirical points (NEVER scipy.stats.norm.rvs!)
    def age_crime_curve(a, amp, mu, sig, base):
        return amp * np.exp(-((a - mu)**2) / (2 * sig**2)) + base

    popt, _ = curve_fit(age_crime_curve, ages, rates, p0=[1000.0, 18.0, 4.0, 200.0])

    # 4. Render deterministic plot
    fig, ax = plt.subplots(figsize=(7, 4.5), dpi=300)
    ax.scatter(ages, rates, color="#1f4e78", label="BKA Register Data")
    t_dense = np.linspace(ages[0], ages[-1], 150)
    ax.plot(t_dense, age_crime_curve(t_dense, *popt), color="#1f4e78", lw=2, label="Empirical Fit")

    # Dynamic controlled curve scaled by literature benchmark (CRIMOC OR = 1.054)
    if "CRIMOC_OR_CONTROLLED" in benchmarks:
        or_val = benchmarks["CRIMOC_OR_CONTROLLED"]
        ax.plot(t_dense, age_crime_curve(t_dense, *popt) * or_val, color="#d9534f", lw=2, ls="--",
                label=f"Controlled Curve (CRIMOC OR = {or_val:.3f})")

    ax.legend()
    plt.tight_layout()
    plt.savefig(plot_path, dpi=300)
    plt.close()
    print(f"✓ Generated demographic figure: {plot_path}")
```

---

## 6. Verification Checklist & Pre-Publication Audit

Before finalizing any empirical analysis or publication, verify every item:

- [ ] **Provenance**: Are all raw datasets documented in `rawdata.md` with URLs and SHA-256 hashes?
- [ ] **Reproducibility**: Does `python src/data_preparation.py` run from scratch and pass all `assert` statements?
- [ ] **Benchmark Audit**: Are all microdata survey odds ratios, regression slopes, and literature benchmarks registered in `literature_empirical_benchmarks.csv` with exact page/table coordinates and verbatim quotes?
- [ ] **Denominator Match**: Is the numerator matched to the resident denominator? Is non-resident inflation (Table 29) addressed?
- [ ] **Table Coordinates**: Are BKA tables cited correctly (T20 = Total, T40 = German, T50 = Non-German, T29 = Tatort-Wohnsitz, T61 = Aufenthaltsanlass, T62 = Staatsangehörigkeiten)?
- [ ] **Demographic Realism**: Are empirical age cohorts used instead of synthetic Gaussian curves?
- [ ] **Explicit NaN Preservation**: Are unobservable brackets (e.g. 21–25 non-German male denominator) preserved as `NaN` rather than guessed or interpolated?
- [ ] **Strict AST Code Invariants**: Does code pass static AST analysis (zero synthetic generators, zero silent `.get(k, <number>)` fallbacks, zero ternary/default domain floats, zero magic `assert ==` literals)?
- [ ] **Standardization Math & Shapley Values**: Is direct standardization computed using explicit population weights, and are waterfalls accompanied by path-independent Shapley attribution ($\phi_j$)?
- [ ] **TOST Equivalence Tested**: If claiming parity or absence of disparity in survey data under controls, has TOST equivalence been tested against explicit bounds ($\pm \Delta$)?
- [ ] **Joint-Risk Check ($M_{\text{ind}}$)**: Is joint demographic concentration framed as an illustrative baseline model ($M_{\text{ind}}$) with analytical Fréchet–Hoeffding bounds and copula sensitivity?
- [ ] **Causal Clarity**: Are confounders (age, sex) explicitly separated from mediators (poverty, housing), and is compositional confounding ($\text{CF}_{\text{SES}}$) distinguished from exposure elimination?
- [ ] **Registry Limits**: Is it explicitly stated that police registries contain no individual-level SES data?
- [ ] **Model Fitting & Plot Generation**: Does `src/modeling.py` fit models to empirical data from `/datasets` and deterministically render all figures in `/plots`?
- [ ] **Plot Validity Documentation (`plot.md`)**: Does `plots/plot.md` document each individual plot with a rigorous explanation of its data provenance, statistical validity, assumptions, and limitations?
- [ ] **Automated Audit**: Has `scripts/audit_demographics.py` been executed and passed with 100% success?

---

## 7. Associated Skill Resources

* **Demographic Scraped Data, PDFs & Benchmarks Guide**: [`references/scraped_data_and_literature_benchmarks_guide.md`](./references/scraped_data_and_literature_benchmarks_guide.md)
* **Demographic Standardization Guide**: [`references/demographics_standardization_guide.md`](./references/demographics_standardization_guide.md)
* **Causal Inference & Mediation Analysis**: [`references/causal_inference_vs_mediation.md`](./references/causal_inference_vs_mediation.md)
* **Minimal Demographic Data Preparation Template**: [`scripts/data_preparation_snippet.py`](./scripts/data_preparation_snippet.py)
* **Minimal Demographic Modeling Template**: [`scripts/modeling_snippet.py`](./scripts/modeling_snippet.py)
* **Example Demographic Benchmarks CSV**: [`scripts/example_literature_empirical_benchmarks.csv`](./scripts/example_literature_empirical_benchmarks.csv)
* **Automated Demographic Audit Script**: [`scripts/audit_demographics.py`](./scripts/audit_demographics.py)
* **General Empirical Research Protocol**: [`../responsible-research/SKILL.md`](../responsible-research/SKILL.md)