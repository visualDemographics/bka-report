---
name: responsible-research
description: >-
  General operational protocol and standard operating procedure for rigorous empirical research, data pipeline reproducibility, per-capita and accounting normalization, causal inference, and publication-grade 3x3 synoptic matrix visualizations across economics, macro-historical time series, institutional benchmarking, science policy, and social sciences. Use whenever setting up an empirical research repository, building raw-to-dataset pipelines, normalizing metrics across populations/institutions/time (e.g., per-capita commodity output over decades, university student-facing budgets and research quality across TUM/MIT/ETH), distinguishing confounders from mediators, or generating 9-panel (3x3) synoptic analysis matrices and waterfall decompositions.
---

# Responsible Empirical Research Protocol
## Standard Operating Procedure for Scientific Rigor, Normalization, Causal Inference, and Synoptic Visualization

This skill defines the mandatory repository architecture, deterministic data pipeline standards, statistical and methodological safeguards, and synoptic visualization blueprints (**9-Panel $3 \times 3$ Matrix & Sequential Waterfall Decomposition**) for empirical research across any quantitative domain—such as macro-historical commodity trajectories, cross-national institutional comparisons, econometrics, public policy, and social data science.

*(For domain-specific rules on population registries, age-crime curves, BKA PKS tables, and demographic cohort standardization, use this skill in conjunction with [`responsible-demographics`](../responsible-demographics/SKILL.md)).*

---

## 1. Expected Repository Structure

Every empirical research project must maintain a modular, auditable directory structure that guarantees complete traceability from unmodified primary sources to published figures:

```text
/
├── goal/
│   ├── description.md       # Precise definition of research questions, entities, time horizon, and scope
│   └── hypothesis.md        # Falsifiable hypotheses with expected causal pathways and mechanisms
├── literature/
│   ├── literature.md        # Structured table of peer-reviewed references, reports, DOIs, and URLs
│   └── [NAME].pdf           # Primary research papers, institutional annual reports, statistical yearbooks
├── rawdata/                 # (or raw/) Unmodified primary source files exactly as downloaded
│   ├── [NAME].csv           # Original statistical releases, time-series extracts, financial tables
│   ├── [NAME].xlsx          # Official spreadsheets (e.g., World Bank, OPEC, EIA, FAO, ETH/MIT/TUM reports)
│   └── rawdata.md           # Manifest table with source URLs, retrieval dates, and SHA-256 hashes
├── datasets/                # Cleaned, harmonized, and auditable tables derived exclusively from rawdata/
│   ├── [NAME].csv           # Reproducible analysis-ready datasets (standardized units, PPP, per-capita)
│   └── datasets.md          # Data dictionary: column definitions, units, normalization formulas, caveats
├── src/
│   ├── data_preparation.py  # Automated, deterministic ETL pipeline: rawdata -> datasets (with assertions)
│   └── modeling.py          # Fits statistical/econometric models to datasets AND renders all plots
├── plots/
│   ├── panel_a_[NAME].png   # Individual high-resolution figures (Panels A through I)
│   ├── [NAME]_3x3_[LANG].png# Publication-ready 3x3 synoptic matrix combining Panels A–I
│   └── plot.md              # Systematic documentation of every plot: provenance, math, and validity
└── methodology/
    └── methodology.md       # Explicit documentation of accounting boundaries, confounders, and limitations
```

---

## 2. Closed-Loop Research Pipeline

Every empirical investigation must strictly follow this sequential, closed-loop workflow:

$$\text{goal} \longrightarrow \text{literature} \longrightarrow \text{rawdata} \longrightarrow \text{datasets} \longrightarrow \text{src} \longrightarrow \text{plots} \longrightarrow \text{methodology} \longrightarrow \text{goal}$$

1. **Goal**: Formulate the empirical question, comparison entities, and time horizon without predetermining outcomes.
2. **Literature**: Map existing peer-reviewed evidence, accounting standards, and established theoretical mechanisms.
3. **Rawdata**: Secure unmodified primary data (official registries, financial statements, international statistical series) with verified SHA-256 provenance.
4. **Datasets**: Harmonize units, currencies (PPP/inflation deflators), accounting boundaries, and denominators via automated scripts with strict integrity assertions (`assert`).
5. **Src (`modeling.py`)**: Fit statistical/econometric models to empirical datasets and deterministically generate all standalone panels and composite $3 \times 3$ matrices. `modeling.py` is the single source of truth for both inferential math and visual rendering.
6. **Plots (`plot.md`)**: Save generated figures in `/plots/`. Maintain `plots/plot.md` documenting every individual figure's data provenance, mathematical formulation, confidence intervals, and methodological boundaries.
7. **Methodology**: Audit findings against alternative explanations, structural breaks, accounting artifacts, confounders, and mediation paths.
8. **Goal Re-Evaluation**: Verify whether initial hypotheses are supported, refuted, or require refined parameterization.

---

## 3. Bad Practices to Avoid

### Bad Research Practices:
* **Cherry-picking literature**: Citing only studies or rankings that favor a predetermined narrative while omitting contrary evidence.
* **Cherry-picking time windows, commodities, or metrics**: Selecting arbitrary base years (e.g., starting a time series at a cyclical spike without disclosure), omitting key sectors, or picking a single institutional ranking metric that favors one entity.
* **Apples-to-oranges accounting boundaries**: Comparing gross institutional budgets that include university hospitals or external defense labs against core academic budgets without boundary adjustment, or comparing nominal budgets across countries without Purchasing Power Parity (PPP) and regional cost adjustments.
* **Overstating causal claims**: Presenting cross-sectional correlations, simple time trends, or ecological associations as definitive causal proof.
* **Hiding data censorship or regime breaks**: Failing to document when official statistical agencies change definitions, halt publication, or require splicing with secondary international series.
* **Concealing model assumptions**: Presenting literature transfers, interpolated gaps, or theoretical response surfaces as directly measured primary observations.

### Bad Statistical Practices:
* **P-hacking & HARKing**: Testing multiple ad-hoc covariate combinations or functional forms until a desired $p$-value or ratio appears.
* **The Null-Hypothesis Parity Fallacy (Absence of Evidence $\neq$ Evidence of Absence)**: Never claim that two groups or policies exhibit "no disparity", "identical outcomes", or "complete convergence" merely because a regression coefficient or group dummy has $p > 0.05$. A statistically non-significant result only fails to reject the null; it does not prove parity. Whenever claiming equivalence under controlled conditions, conduct formal **Two One-Sided Tests (TOST)** against explicit equivalence margins ($\pm \Delta$).
* **Building joint distributions from independent marginals**: Assuming $P(A \cap B \cap C) = P(A) \cdot P(B) \cdot P(C)$ when structural variables (e.g., capital investment, labor productivity, institutional scale, socio-economic factors) are correlated.
* **Fixed-Effects Dominance Fallacy in Cross-Entity Meta-Analysis**: When pooling effect sizes across jurisdictions or studies with sample sizes varying by orders of magnitude (e.g., $N = 10^3$ surveys alongside $N = 8 \cdot 10^6$ national registers), using Fixed-Effects inverse-variance weighting collapses between-entity heterogeneity ($\tau^2$) and allows a single massive register to consume $>90\%$ of the weight. Always evaluate Cochran's $Q$, estimate between-entity variance $\tau^2$ (DerSimonian–Laird Random Effects), apply small-sample adjustments (Knapp–Hartung), and report both 95% Confidence Intervals (mean projection) and 95% Prediction Intervals (new entity outcome).
* **Conflating descriptive and inferential statistics**:
  - *Descriptive statistics* must be computed directly from `/datasets` and reflect audited empirical observations.
  - *Inferential statistics* must be estimated in `/src/modeling.py`, reporting fitted parameters, standard errors, $R^2$, confidence intervals, or analytical bounds.
* **Asserting equivalence or difference without uncertainty quantification**: Claiming two trajectories, slopes, or institutional efficiencies are "identical" or "significantly different" without standard errors, confidence intervals, or hypothesis tests.
* **Conflating mediators with confounders**: Treating endogenous mechanisms on the causal pathway (e.g., capex collapse, institutional brain drain, funding allocation) as exogenous baseline confounders.

### Bad Code & Visualization Practices (Strict AST Contract):
* **Uncommented, opaque code**: Writing scripts without docstrings, clear variable names, or mathematical explanations.
* **Hardcoded guessed parameters**: Pasting invented distribution parameters ($\mu, \sigma, \lambda$, regression slopes) into scripts instead of fitting them to `/datasets`.
* **Silent dictionary lookup fallbacks**: Never use `.get(key, <numeric_literal>)` for empirical or domain parameters. Silent fallbacks mask missing data keys and allow corrupted data pipelines to proceed undetected. Use direct index lookups `df.loc[key]` or `dict[key]` so missing records trigger an immediate, fail-fast exception (`KeyError`).
* **Conditional ternary fallbacks & domain float defaults**: Never write `x if cond else <domain_float>` or declare domain floats in function signatures (e.g., `def fit_model(..., precarity_rr=2.54)`). All numerical parameters must be passed explicitly from audited datasets or literature catalogs.
* **Hardcoded empirical numbers in equality assertions**: Never write `assert value == 111517` with magic literals. Assert against structural accounting identities (`assert total == part_a + part_b`) or dynamic benchmark references (`assert value == benchmarks.loc[...]`).
* **Unreachable dead code**: Never leave dead code after `return` statements in data transformation or modeling modules.
* **Generating synthetic random data for empirical claims**: Never use `scipy.stats.norm.rvs(size=...)` or `np.random.normal(...)` to fabricate artificial observations and plot them as empirical distributions. Always plot empirical cohorts/series or fit parametric/non-parametric models (`scipy.optimize.curve_fit`, `scipy.stats.linregress`, KDE) to real data.
* **Missing pipeline assertions**: Omitting automated checks in `src/data_preparation.py` (e.g., verifying that sub-budgets sum to total budget, physical output / population = per-capita output, or index base year $= 100.0$).
* **Guessing or interpolating unobservable cells**: When administrative registers have non-overlapping reporting brackets that leave a cell denominator unobservable, preserve `NaN` (`None`) explicitly rather than fabricating an interpolated estimate.
* **Decoupled or ad-hoc plotting**: Hardcoding numbers inside standalone plotting scripts instead of having `src/modeling.py` ingest `/datasets`, fit models, and render all figures.
* **Missing plot validity documentation**: Rendering plots without updating `plots/plot.md` with provenance, equations, and limitations for every panel.

---

## 4. Seven Core Pillars of Responsible Empirical Research

```text
                      RESPONSIBLE EMPIRICAL RESEARCH FRAMEWORK
                                         │
     ┌───────────────────┬───────────────┴───────────────┬───────────────────┐
     ▼                   ▼                               ▼                   ▼
1. Accounting &     2. Empirical Data               3. Structural       4. Causal DAGs:
   Denominator         vs. Synthetic                   Standardization     Confounders,
   Alignment           Distributions                   (PPP, Per-Capita)   Mediators & Breaks
```

### Pillar 1: Scope Alignment & Numerator-Denominator Consistency
1. **Exact Boundary Matching**:
   * Every rate, per-capita indicator, or per-student ratio $\text{Rate} = \frac{\text{Numerator}}{\text{Denominator}}$ requires that the numerator and denominator share the exact same institutional, geographic, and temporal boundary.
2. **Explicit NaN Preservation for Incompatible Brackets**:
   * When cross-referencing administrative registers where sub-category brackets do not align (e.g., numerator reported for ages 21–25, but reference denominator available only for 20–25 or 21–60), **retain `NaN` explicitly** in analysis tables rather than inventing an interpolated value. In parametric curve fitting, anchor model knots to observed midpoints to prevent artificial overshoot between discrete cohorts.
3. **Institutional Accounting Harmonization (e.g., University Comparisons: TUM vs. MIT vs. ETH)**:
   * **Consolidated vs. Core Academic Budgets**: University financial statements differ vastly in scope. TUM’s consolidated figures often interface with the *Klinikum rechts der Isar* (medical center with massive clinical patient revenue/costs); MIT’s gross operating revenues include the federally funded *MIT Lincoln Laboratory* ($>\$1.2\text{B}$) and auxiliary dining/housing enterprises; ETH Domain figures distinguish between ETH Zurich proper and sister research institutes (PSI, Empa, Eawag, WSL).
   * **Student-Facing Budget Isolation**: To measure *student-facing budget per student*, researchers must strip non-academic clinical hospitals, external defense/national labs, and pure industrial contract pass-throughs, isolating **Instructional & Student-Facing Academic Expenditure** (core teaching budget + instructional share of central infrastructure and academic support) divided by **Full-Time Equivalent (FTE) enrolled students** (separating bachelor/master teaching loads from external doctoral employees).
4. **Longitudinal Denominator Integrity (e.g., Multi-Decade Per-Capita Output in Venezuela)**:
   * When computing per-capita production over 50 years ($\text{Output}_{c,t} / \text{Population}_t$), the population denominator must account for demographic regime shocks (such as the post-2014 emigration of $>7\text{ million}$ Venezuelans documented in UN WPP and ENCOVI revisions). Using unadjusted linear population projections overstates the denominator and distorts per-capita trajectories.

### Pillar 2: Empirical Distributions & Trajectories vs. Synthetic Fallacies
1. **Strict Prohibition of Guessed Distributions**:
   * Never represent empirical populations, budgets, citation counts, or production series using invented Gaussian distributions (`Normal(mu, sigma)`).
2. **Respect Skewness, Heavy Tails, and Structural Regimes**:
   * Bibliometric impact (citations per paper), departmental grant capture, and firm/commodity outputs follow skewed Pareto/log-normal distributions or piecewise regime shifts.
   * Always plot actual empirical deciles, cohorts, or historical time points alongside explicitly fitted curves (`scipy.optimize.curve_fit`, piecewise structural break models, or OLS/GLS regressions with standard error bands).

### Pillar 3: Structural Standardization, Deflation & Index Normalization
1. **Direct Compositional Standardization**:
   * When comparing entities with different internal compositions (e.g., universities with different STEM vs. humanities shares, or economies with shifting sectoral mixes), compute stratum-specific metrics $R_k^{(g)}$ and apply a common reference weight $w_k$:
     $$R_{\text{std}}^{(g)} = \sum_{k \in K} w_k \cdot R_k^{(g)}, \quad w_k = \frac{N_k^{(\text{ref})}}{\sum_{j} N_j^{(\text{ref})}}$$
2. **Epidemiological Compositional Confounding Factor ($\text{CF}$, Rothman 2008)**:
   * When standardizing a group disparity for a mediator/confounder with differential prevalence ($p_1$ vs. $p_0$) and relative risk $RR$, compute the exact population confounding factor:
     $$\text{CF} = \frac{1 + p_1 (RR - 1)}{1 + p_0 (RR - 1)}$$
   * **Symmetric Zero-Exposure Theorem**: Standardizing Group 1 to Group 0's baseline exposure level ($p_1 \to p_0$) produces identically the same relative disparity ratio as hypothetically setting exposure to zero ($p \to 0\%$) in both groups. Always standardize against the empirical reference baseline to preserve real-world administrative grounding.
3. **Currency, Inflation, and PPP Normalization**:
   * Cross-national monetary metrics (e.g., EUR in Munich, USD in Cambridge MA, CHF in Zurich) must be converted using **OECD / World Bank Purchasing Power Parity (PPP)** and adjusted for local academic cost structures (salary scales, living costs), always reporting both nominal exchange-rate equivalents and PPP-adjusted real values.
   * Multi-decade monetary series must be deflated to constant real base-year prices (or evaluated in physical units: barrels/day, metric tons, GWh per capita).
4. **Multi-Series Base-Year Indexing**:
   * When comparing heterogeneous physical commodities (e.g., crude oil in bbl/day, steel/aluminum in tons/capita, electricity in kWh/capita, cereals in kg/capita), normalize trajectories to a shared baseline index ($\text{Index}_{t_0} = 100$ at peak or initial year $t_0$) in comparative panels while preserving exact physical units in dedicated panels and tables.

### Pillar 4: Joint Distributions, Conditional Chain Rule, Fréchet Bounds & Copula Sensitivity
1. **Avoid the Independence Fallacy**:
   * When evaluating multi-factor intersections (e.g., probability that a student is in a small-cohort seminar $\cap$ taught by tenured faculty $\cap$ high-equipment lab, or a commodity sector experiencing simultaneous capex starvation $\cap$ skilled-labor exodus $\cap$ price controls), never multiply unconditional marginals without checking correlation.
2. **Conditional Chain Rule, Illustrative Baseline ($M_{\text{ind}}$) & Bounds**:
   * Express joint concentrations via empirical conditional probabilities:
     $$P(A \cap B \cap C) = P(A) \cdot P(B \mid A) \cdot P(C \mid A, B)$$
   * If individual microdata cross-tabulations are unobserved, label the estimate explicitly as an **illustrative baseline model under conditional independence ($M_{\text{ind}}$)** and provide:
     - **Analytical Fréchet–Hoeffding bounds** $[P_{\min}, P_{\max}]$ spanning all possible dependency structures:
       $$P_{\min} = P(A) \cdot \max(0, P(B \mid A) + P(C \mid A) - 1), \quad P_{\max} = P(A) \cdot \min(P(B \mid A), P(C \mid A))$$
     - **Parametric Copula Sensitivity** (e.g., Plackett copula varying odds ratio $\text{OR} \in [0.8, 1.5]$) to confirm point estimate stability.

### Pillar 5: Causal Inference — Confounders, Mediators, Shapley Waterfalls & TOST Equivalence
1. **Exogenous Confounders ($Z$) vs. Endogenous Mediators ($M$)**:
   * **Confounders ($Z$)**: Exogenous factors affecting both baseline structure and outcomes (e.g., age cohorts, sex, global commodity price super-cycles). Must be controlled for to isolate institutional or policy effects.
   * **Mediators ($M$)**: Mechanisms lying *on* the causal pathway between policy/governance ($X$) and outcome ($Y$):
     $$X \text{ (Policy / Governance / Status)} \longrightarrow M \text{ (Capex, Poverty, Brain Drain, Housing)} \longrightarrow Y \text{ (Output / Delinquency)}$$
   * Controlling for $M$ isolates the **Controlled Direct Effect (CDE)**. It identifies the mechanism explaining the difference, not that the total difference is non-existent.
2. **Path-Independent Shapley Value Decomposition for Waterfalls**:
   * Sequential waterfall charts are inherently path-dependent (ordering determines the apparent size of each bar's drop).
   * For $K$ sequential adjustment stages, evaluate all $K!$ order permutations and report **Shapley values** ($\phi_j = \frac{1}{K!} \sum_{\pi} \Delta_j(\pi)$) alongside the primary pedagogical sequence.
3. **Equivalence Testing via Two One-Sided Tests (TOST)**:
   * When testing whether an adjusted gap is negligible, replace the null-hypothesis fallacy with **TOST equivalence tests**:
     $$z_1 = \frac{\ln(\text{Ratio}) - (-\Delta)}{\text{SE}_{\ln}}, \quad z_2 = \frac{\Delta - \ln(\text{Ratio})}{\text{SE}_{\ln}}, \quad p_{\text{TOST}} = \max(1 - \Phi(z_1), 1 - \Phi(z_2))$$
     testing against explicit tolerance margins (e.g., $\pm 30\%$ or $\pm 50\%$).

### Pillar 6: Multi-Source Triangulation, Meta-Regression & Construct Validity
1. **Cross-Entity & Cross-National Meta-Regression (DerSimonian–Laird REMR)**:
   * When synthesizing empirical effect ratios from multiple external studies across jurisdictions, estimate between-study heterogeneity $\tau^2$, Cochran's $Q$, and Higgins' $I^2$.
   * Use **Random-Effects Meta-Regression (REMR)** with **Knapp–Hartung small-sample standard errors** to prevent single large registries from dominating weights.
   * Compute **Leave-One-Out (LOO) Jackknife sensitivity** across all entities, and report both **95% Confidence Intervals** (mean prediction) and **95% Prediction Intervals** ($\sqrt{\text{Var}(\hat{y}) + \tau^2}$) for new entity projections.
2. **Macro-Observational Gradients vs. Discordant Sibling Fixed-Effects**:
   * Distinguish between **macro-observational population risk gradients** (which reflect clustered structural disadvantage like neighborhood segregation and schooling quality) and **within-family discordant sibling models** (which isolate individual-level unconfounded levers). Do not misinterpret macro indicators as mechanical cash levers.
3. **Multi-Dimensional Construct Validity (Avoiding Goodhart's Law)**:
   * Never reduce complex constructs to a single noisy proxy. Triangulate across orthogonal empirical dimensions (e.g., citations, competitive grants, technology transfer).

### Pillar 7: Synoptic $3 \times 3$ Matrix Architecture (`src/modeling.py` & `plots/plot.md`)
1. **Unified 9-Panel Visual Synthesis**:
   * Synthesize multi-dimensional investigations into a cohesive **9-Panel ($3 \times 3$) Synoptic Matrix** (`figsize=(18, 15)`, `dpi=300`) alongside standalone panel exports (`panel_a_*.png` through `panel_i_*.png`) and macro waterfall charts.
2. **Exact Marginal Conservation on 2D Surfaces**:
   * Any 2D interaction surface $R(X_1, X_2)$ must conserve the empirical marginal distribution identically across slices:
     $$\mathbb{E}_{X_2}[R(x_1, X_2)] \equiv Y_{\text{empirical}}(x_1) \quad (\text{runtime assert drift } < 10^{-10})$$
3. **Strict Scope-Restricted Extrapolation**:
   * Never extrapolate counterfactual sensitivity bands or standardized curves across the entire life course or time horizon if empirical evidence only covers a sub-window (e.g., restrict youth precarity controls strictly to ages 14–30).
4. **Standardized 3-Row Pedagogical Flow**:
   * **Row 1 (Panels A–C): Empirical Baselines, Denominator Normalization & Structural Distributions**
   * **Row 2 (Panels D–F): Sub-Component Breakdown, Joint Conditioning & Bivariate Surface / Meta-Regression**
   * **Row 3 (Panels G–I): Dynamic Trajectories, Econometric Regressions, Shapley Waterfall & Demographic Standardizations**

---

## 5. Handling Scraped Web Data, PDF Extractions & Literature Benchmarks

When working with data scraped from the web (HTML tables, APIs, online CSV/Excel extracts) or extracted from PDF reports (statistical yearbooks, audited university budgets, academic papers):

### 1. Ingestion Protocol:
* **Preserve Untouched Originals**: Store original scraped files or downloaded PDFs in `rawdata/` (or `literature/`). Never modify them directly.
* **Cryptographic Provenance**: Record the download URL, timestamp, and SHA-256 hash in `rawdata.md` or `raw/MANIFEST.csv`.
* **Zero Hardcoded Magic Numbers**: Never paste numbers extracted from a website or PDF into `src/modeling.py`.
* **The Benchmark Catalog (`literature_empirical_benchmarks.csv`)**: Any isolated empirical value (odds ratios, peak historical output, institutional budget pass-through, survey regression slope) must be recorded in `datasets/literature_empirical_benchmarks.csv` with exact page numbers, table coordinates, and verbatim quotes.

### 2. Standard Schema & Sample Lines: `literature_empirical_benchmarks.csv`
```csv
parameter_id,themenbereich,indikator,gruppe,wert,einheit,intervall_95_ki,signifikanz_p,stichprobe_n,quelle_autor_institution,quelle_titel,jahr,fundstelle_seite_tabelle,exakte_zeile_fundstelle,exakter_quelltext_zitat,doi_url,lokale_datei,methodischer_status
OPEC_VEN_OIL_PROD_1998,Commodities,Venezuela Crude Oil Production Peak,venezuela,3134.0,Thousand_bbl_day,,,Vollerhebung,OPEC,OPEC Annual Statistical Bulletin (Historical Series),2023,Table 3.1 Page 28,"Table 3.1, Row 'Venezuela', Column '1998'","Average crude production 1998: 3,134.0 kb/d",https://asb.opec.org,literature/opec_asb_2023.pdf#page=28,Amtliche_Sekundaerstatistik
MIT_LINCOLN_LAB_BUDGET,Higher_Education,MIT Lincoln Laboratory Federal DoD Pass-Through,mit,1235.0,Million_USD,,,Vollerhebung,MIT Office of the Vice President for Finance,Report of the Treasurer for the Year Ended June 30 2023,2023,Financial Statements Page 14,"Operating Expenditures: Lincoln Laboratory: $1,235.0M","Sponsored research: Lincoln Laboratory accounts for $1,235.0 million in federal funding",https://vpf.mit.edu/treasurers-report,literature/mit_treasurers_report_2023.pdf#page=14,Audited_Financial_Statement
TUM_KLINIKUM_REVENUE,Higher_Education,TUM Klinikum rechts der Isar Clinical Turnover,tum,890.0,Million_EUR,,,Vollerhebung,TUM & Bayerisches Staatsministerium,Rechenschaftsbericht & Jahresabschluss Klinikum,2023,Wirtschaftsplan Tabelle 4 Seite 22,"Umsatzerloese aus Krankenhausleistungen: 890,0 Mio. EUR","Klinikum rechts der Isar: Krankenversorgungsumsatz 890 Mio. EUR",https://www.tum.de,literature/tum_jahresbericht_2023.pdf#page=22,Audited_Financial_Statement
CRIMOC_OR_CONTROLLED,Multivariate_Kohorte,Controlled Odds Ratio Delinquency,nichtdeutsch,1.054,Odds_Ratio,[0.94; 1.18],p = 0.38 (n.s.),N = 3.528,"Boers & Reinecke (CRIMOC)",Delinquenz im Altersverlauf,2019,Tabelle 7.3 Modell 3 S. 145,"Tabelle 7.3, Seite 145, Zeile 'Nichtdeutsch'","Modell 3: Nichtdeutsch OR = 1,054 (95%-KI: [0,94; 1,18], p = 0,38 n.s.)",https://www.waxmann.com/buch3966,literature/citations.md#L69-L70,Laengsschnitt_Panelstudie
```

### 3. Minimum Snippet: `src/data_preparation.py`
Ingests raw scraped series and audits literature benchmarks with strict assertions before exporting to `datasets/`:
```python
import csv, os

def audit_and_prepare_data(raw_benchmarks_path, raw_series_path, out_datasets_path):
    # 1. Audit benchmarks from PDF/literature
    benchmarks = {}
    with open(raw_benchmarks_path, "r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            pid = r["parameter_id"].strip()
            val = float(r["wert"])
            assert len(r["exakter_quelltext_zitat"].strip()) > 5, f"Missing quote for {pid}"
            benchmarks[pid] = val

    # 2. Ingest and normalize scraped series
    cleaned = []
    with open(raw_series_path, "r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            pop = float(r["population"])
            assert pop > 0, "Population denominator must be strictly positive!"
            per_capita = float(r["gross_output"]) / pop
            cleaned.append({"year": int(r["year"]), "per_capita_output": round(per_capita, 4)})

    # 3. Export auditable clean dataset
    with open(out_datasets_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["year", "per_capita_output"])
        writer.writeheader()
        writer.writerows(cleaned)
    print(f"✓ Audited {len(benchmarks)} benchmarks and exported {len(cleaned)} records.")
```

### 4. Minimum Snippet: `src/modeling.py`
Loads benchmark parameters dynamically and fits empirical curves without any synthetic random draws (`rvs`):
```python
import csv, os, matplotlib
matplotlib.use("Agg")  # Non-interactive headless backend
import matplotlib.pyplot as plt, numpy as np
from scipy.optimize import curve_fit

def run_modeling_and_plots(dataset_path, benchmarks_path, plot_path):
    # 1. Load benchmarks dynamically (NO hardcoded numbers!)
    benchmarks = {}
    with open(benchmarks_path, "r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            benchmarks[r["parameter_id"].strip()] = float(r["wert"])

    # 2. Ingest empirical data
    years, y_obs = [], []
    with open(dataset_path, "r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            years.append(int(r["year"])), y_obs.append(float(r["per_capita_output"]))
    years, y_obs = np.array(years), np.array(y_obs)

    # 3. Fit parametric model to empirical data (NEVER scipy.stats.norm.rvs!)
    def decay_func(t, y0, k): return y0 * np.exp(-k * (t - years[0]))
    popt, _ = curve_fit(decay_func, years, y_obs, p0=[y_obs[0], 0.05])

    # 4. Render deterministic plot
    fig, ax = plt.subplots(figsize=(7, 4.5), dpi=300)
    ax.scatter(years, y_obs, color="#1f4e78", label="Empirical Observations")
    t_dense = np.linspace(years[0], years[-1], 150)
    ax.plot(t_dense, decay_func(t_dense, *popt), color="#d9534f", lw=2, label="Fitted Trajectory")
    if "BENCHMARK_TARGET" in benchmarks:
        ax.axhline(benchmarks["BENCHMARK_TARGET"], color="gray", linestyle="--", label="Target Benchmark")
    ax.legend()
    plt.tight_layout()
    plt.savefig(plot_path, dpi=300)
    plt.close()
    print(f"✓ Generated plot: {plot_path}")
```

---

## 6. Domain Blueprints for $3 \times 3$ Synoptic Matrices

See [`references/synoptic_3x3_matrix_guide.md`](./references/synoptic_3x3_matrix_guide.md) for complete panel-by-panel design templates covering:
1. **Macro-Historical Commodity & Production Collapse**: *50-Year Declining Per-Capita Output of Commodities in Venezuela (1975–2025)* (Crude Oil, Steel/Iron, Aluminum, Electricity, Agricultural Staples).
2. **Cross-National University Benchmarking**: *TUM vs. MIT vs. ETH Zurich — Student-Facing Budget per FTE Student (PPP) & Multi-Dimensional Research Quality*.
3. **Demographic & Social Registry Decomposition**: *Cross-referencing [`responsible-demographics`](../responsible-demographics/SKILL.md)*.

---

## 7. Verification Checklist & Pre-Publication Audit

Before finalizing any empirical analysis or publication, verify every item:

- [ ] **Provenance Manifest**: Are all primary files stored in `rawdata/` (or `raw/`) and documented in `rawdata.md` with source URLs, retrieval dates, and SHA-256 hashes?
- [ ] **Deterministic ETL**: Does `python src/data_preparation.py` run cleanly from scratch and pass all `assert` checks (unit conversions, accounting sums, per-capita divisions)?
- [ ] **Benchmark Audit**: Are all isolated empirical figures from PDFs/websites logged in `literature_empirical_benchmarks.csv` with exact pages, tables, and verbatim quotes?
- [ ] **Boundary & Denominator Alignment**: Are numerators and denominators matched in scope (e.g., stripping non-student hospital/defense lab pass-throughs; using migration-adjusted population denominators)?
- [ ] **Explicit NaN Preservation**: Are unobservable sub-category denominators retained as `NaN` rather than interpolated or guessed?
- [ ] **Normalization Rigor**: Are monetary figures adjusted for inflation and PPP? Are physical commodities properly normalized per capita and indexed to a transparent base year?
- [ ] **Strict AST Code Invariants**: Does code pass static AST analysis (zero `.rvs`/`np.random`, zero silent `.get(k, <number>)` fallbacks, zero ternary/default domain floats, zero magic `assert ==` literals)?
- [ ] **Causal & Structural Clarity**: Are exogenous confounders, accounting boundary adjustments, structural breaks, and endogenous mediators clearly distinguished?
- [ ] **Path-Independent Shapley Values**: Are waterfall adjustments evaluated across all $K!$ order permutations and reported with Shapley values?
- [ ] **TOST Equivalence Tested**: If claiming that groups/outcomes are equivalent under controls, has formal TOST equivalence testing been conducted against explicit bounds ($\pm \Delta$)?
- [ ] **2D Marginal Conservation & Scope Clipping**: Does the 2D interaction surface conserve empirical marginals identically across slices ($< 10^{-10}$ drift), and are counterfactual curves strictly clipped to empirical study windows?
- [ ] **Unified Model & Plot Generation**: Does `src/modeling.py` fit all statistical models to `/datasets` and deterministically render Panels A–I, the waterfall chart, and the $3 \times 3$ synoptic matrix?
- [ ] **Plot Validity Documentation (`plot.md`)**: Does `plots/plot.md` document every single generated figure with its exact data sources, mathematical equations, parameter estimates, and methodological caveats?
- [ ] **Automated Pipeline Audit**: Has `python .agents/skills/responsible-research/scripts/audit_research_pipeline.py` been executed and passed all checks?

---

## 8. Associated Skill Resources

* **Scraped Data, PDFs & Literature Benchmarks Guide**: [`references/scraped_data_and_literature_benchmarks_guide.md`](./references/scraped_data_and_literature_benchmarks_guide.md)
* **Normalization, Accounting Boundaries & Comparability Guide**: [`references/normalization_and_comparability_guide.md`](./references/normalization_and_comparability_guide.md)
* **Synoptic $3 \times 3$ Matrix & Waterfall Architecture Guide**: [`references/synoptic_3x3_matrix_guide.md`](./references/synoptic_3x3_matrix_guide.md)
* **Minimal Data Preparation Template**: [`scripts/data_preparation_snippet.py`](./scripts/data_preparation_snippet.py)
* **Minimal Modeling Template**: [`scripts/modeling_snippet.py`](./scripts/modeling_snippet.py)
* **Example Literature Benchmarks CSV**: [`scripts/example_literature_empirical_benchmarks.csv`](./scripts/example_literature_empirical_benchmarks.csv)
* **Automated Research Pipeline Audit Script**: [`scripts/audit_research_pipeline.py`](./scripts/audit_research_pipeline.py)
* **Companion Skill for Demographic & Registry Data**: [`../responsible-demographics/SKILL.md`](../responsible-demographics/SKILL.md)


