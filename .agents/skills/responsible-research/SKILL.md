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
* **Building joint distributions from independent marginals**: Assuming $P(A \cap B \cap C) = P(A) \cdot P(B) \cdot P(C)$ when structural variables (e.g., capital investment, labor productivity, institutional scale, socio-economic factors) are correlated.
* **Conflating descriptive and inferential statistics**:
  - *Descriptive statistics* must be computed directly from `/datasets` and reflect audited empirical observations.
  - *Inferential statistics* must be estimated in `/src/modeling.py`, reporting fitted parameters, standard errors, $R^2$, confidence intervals, or analytical bounds.
* **Asserting equivalence or difference without uncertainty quantification**: Claiming two trajectories, slopes, or institutional efficiencies are "identical" or "significantly different" without standard errors, confidence intervals, or hypothesis tests.
* **Conflating mediators with confounders**: Treating endogenous mechanisms on the causal pathway (e.g., capex collapse, institutional brain drain, funding allocation) as exogenous baseline confounders.

### Bad Code & Visualization Practices:
* **Uncommented, opaque code**: Writing scripts without docstrings, clear variable names, or mathematical explanations.
* **Hardcoded guessed parameters**: Pasting invented distribution parameters ($\mu, \sigma, \lambda$, regression slopes) into scripts instead of fitting them to `/datasets`.
* **Generating synthetic random data for empirical claims**: Never use `scipy.stats.norm.rvs(size=...)` or `np.random.normal(...)` to fabricate artificial observations and plot them as empirical distributions. Always plot empirical cohorts/series or fit parametric/non-parametric models (`scipy.optimize.curve_fit`, `scipy.stats.linregress`, KDE) to real data.
* **Missing pipeline assertions**: Omitting automated checks in `src/data_preparation.py` (e.g., verifying that sub-budgets sum to total budget, physical output / population = per-capita output, or index base year $= 100.0$).
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
2. **Institutional AccountingHarmonization (e.g., University Comparisons: TUM vs. MIT vs. ETH)**:
   * **Consolidated vs. Core Academic Budgets**: University financial statements differ vastly in scope. TUM’s consolidated figures often interface with the *Klinikum rechts der Isar* (medical center with massive clinical patient revenue/costs); MIT’s gross operating revenues include the federally funded *MIT Lincoln Laboratory* ($>\$1.2\text{B}$) and auxiliary dining/housing enterprises; ETH Domain figures distinguish between ETH Zurich proper and sister research institutes (PSI, Empa, Eawag, WSL).
   * **Student-Facing Budget Isolation**: To measure *student-facing budget per student*, researchers must strip non-academic clinical hospitals, external defense/national labs, and pure industrial contract pass-throughs, isolating **Instructional & Student-Facing Academic Expenditure** (core teaching budget + instructional share of central infrastructure and academic support) divided by **Full-Time Equivalent (FTE) enrolled students** (separating bachelor/master teaching loads from external doctoral employees).
3. **Longitudinal Denominator Integrity (e.g., Multi-Decade Per-Capita Output in Venezuela)**:
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
2. **Currency, Inflation, and PPP Normalization**:
   * Cross-national monetary metrics (e.g., EUR in Munich, USD in Cambridge MA, CHF in Zurich) must be converted using **OECD / World Bank Purchasing Power Parity (PPP)** and adjusted for local academic cost structures (salary scales, living costs), always reporting both nominal exchange-rate equivalents and PPP-adjusted real values.
   * Multi-decade monetary series must be deflated to constant real base-year prices (or evaluated in physical units: barrels/day, metric tons, GWh per capita).
3. **Multi-Series Base-Year Indexing**:
   * When comparing heterogeneous physical commodities (e.g., crude oil in bbl/day, steel/aluminum in tons/capita, electricity in kWh/capita, cereals in kg/capita), normalize trajectories to a shared baseline index ($\text{Index}_{t_0} = 100$ at peak or initial year $t_0$) in comparative panels while preserving exact physical units in dedicated panels and tables.

### Pillar 4: Joint Distributions, Conditional Chain Rule & Bounds
1. **Avoid the Independence Fallacy**:
   * When evaluating multi-factor intersections (e.g., probability that a student is in a small-cohort seminar $\cap$ taught by tenured faculty $\cap$ high-equipment lab, or a commodity sector experiencing simultaneous capex starvation $\cap$ skilled-labor exodus $\cap$ price controls), never multiply unconditional marginals without checking correlation.
2. **Conditional Chain Rule & Fréchet Bounds**:
   * Express joint concentrations via empirical conditional probabilities $P(A \cap B \cap C) = P(A) \cdot P(B \mid A) \cdot P(C \mid A, B)$ and compute **Fréchet–Hoeffding bounds** $[P_{\min}, P_{\max}]$ when exact joint cross-tabulations are partially unobserved.

### Pillar 5: Causal Inference — Confounders, Mediators & Structural Breaks
1. **Exogenous Confounders ($Z$) vs. Endogenous Mediators ($M$)**:
   * **Confounders ($Z$)**: Exogenous factors affecting both baseline structure and outcomes (e.g., global commodity price super-cycles, geological basin maturity, national statutory tuition frameworks, disciplinary mandate). Must be controlled for to isolate institutional or policy effects.
   * **Mediators ($M$)**: Mechanisms lying *on* the causal pathway between policy/institutional governance ($X$) and outcome ($Y$):
     $$X \text{ (Policy / Governance / Endowment)} \longrightarrow M \text{ (Capex, Brain Drain, Faculty-Student Ratio)} \longrightarrow Y \text{ (Per-Capita Output / Research & Teaching Quality)}$$
   * Controlling for $M$ in a sequential waterfall decomposition quantifies **how much of the total effect is explained by each mechanism** (e.g., how much of Venezuela's per-capita output collapse is attributable to PDVSA/SIDOR expropriation & capex cessation vs. skilled personnel flight vs. macroeconomic hyperinflation/import compression; or how much of a research impact gap is driven by endowment per faculty vs. teaching load vs. postdoc/PhD ratio).

### Pillar 6: Multi-Source Triangulation & Proxy Validity
1. **Triangulating Censored or Degraded Official Data**:
   * When primary domestic reporting suffers from blackouts or political distortion (e.g., Venezuelan central bank/ministry reporting gaps post-2015), cross-validate and splice series using independent international registries (OPEC Secondary Sources, U.S. EIA, USGS Mineral Yearbooks, World Steel Association, FAOSTAT, UN Comtrade, ENCOVI). Document exact splicing years and concordance checks.
2. **Multi-Dimensional Construct Validity (Avoiding Goodhart's Law)**:
   * Never reduce complex constructs like "Research Quality" or "Teaching Quality" to a single noisy proxy. Measure **Research Quality** across orthogonal empirical dimensions:
     1. *Field-Weighted Citation Impact (FWCI)* / Top-1% & Top-10% highly cited publication share (CWTS Leiden / Scopus / OpenAlex).
     2. *Competitive Peer-Reviewed Grant Capture per Faculty* (ERC grants, NSF/NIH/DFG awards).
     3. *High-Impact Breakthroughs & Technology Transfer* (Nature/Science index, triadic patents, spin-offs per 1,000 researchers).

### Pillar 7: Synoptic $3 \times 3$ Matrix Architecture (`src/modeling.py` & `plots/plot.md`)
1. **Unified 9-Panel Visual Synthesis**:
   * Complex multi-dimensional research questions should be synthesized into a cohesive **9-Panel ($3 \times 3$) Synoptic Matrix** (`figsize=(18, 15)`, `dpi=300`), accompanied by standalone high-resolution exports of each panel (`panel_a_*.png` through `panel_i_*.png`) and a macro waterfall chart.
2. **Standardized 3-Row Pedagogical Flow**:
   * **Row 1 (Panels A–C): Empirical Baselines, Denominator Normalization & Structural Distributions**
     - *Panel A*: Headline Crude vs. Normalized Comparison (e.g., Total vs. Per-Capita / Per-Student PPP Baseline).
     - *Panel B*: Primary Structural / Temporal / Cohort Distribution (e.g., 50-year multi-commodity index trajectories or student/faculty cohort structure).
     - *Panel C*: Resource / Input / Sectoral Distribution (e.g., budget composition across teaching, base funding, and third-party grants; or real capital investment / export revenue deciles).
   * **Row 2 (Panels D–F): Sub-Component Breakdown, Joint Conditioning & Bivariate Surface**
     - *Panel D*: Modality / Sub-Sector / Accounting Tier Breakdown (stacked or grouped decomposition of numerators and denominators).
     - *Panel E*: Multi-Factor Joint Concentration or Efficiency Ratio with uncertainty/Fréchet bounds.
     - *Panel F*: 2D Bivariate Interaction Surface ($X_1 \times X_2 \to Y$ contour map calibrated to preserve empirical marginals, e.g., Student-Faculty Ratio $\times$ Instructional Budget per Student $\to$ Learning/Research Output, or Capital Investment $\times$ Institutional Governance $\to$ Per-Capita Commodity Yield).
   * **Row 3 (Panels G–I): Dynamic Curves, Econometric Regressions & Sequential Waterfall Decomposition**
     - *Panel G*: Fitted Structural Curve / Longitudinal Decay or Scale Trajectory (`scipy.optimize.curve_fit` over empirical observations with highlighted regime windows).
     - *Panel H*: Econometric Regression Gradient with Empirical Error Bars (`scipy.stats.linregress` / OLS across deciles, time periods, or departments).
     - *Panel I*: Sequential Waterfall Decomposition or Controlled Multivariate Benchmark (quantifying the stepwise contribution of accounting boundaries, confounders, and mediators from raw gap to residual).

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
- [ ] **Normalization Rigor**: Are monetary figures adjusted for inflation and PPP? Are physical commodities properly normalized per capita and indexed to a transparent base year?
- [ ] **Zero Synthetic Data**: Are all plotted distributions and trajectories derived from empirical data in `/datasets` without any guessed Gaussian/synthetic random generation (`rvs`)?
- [ ] **Causal & Structural Clarity**: Are exogenous confounders, accounting boundary adjustments, structural breaks, and endogenous mediators clearly distinguished?
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


