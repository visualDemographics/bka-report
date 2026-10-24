# Architectural Guide: Designing 9-Panel ($3 \times 3$) Synoptic Research Matrices & Waterfall Decompositions

A hallmark of the **Responsible Empirical Research Protocol** is synthesizing complex, multi-faceted empirical investigations into a single, self-contained **9-Panel ($3 \times 3$) Synoptic Matrix** (`figsize=(18, 15)`, `dpi=300`) generated deterministically by `src/modeling.py` alongside standalone figures (`panel_a_*.png` to `panel_i_*.png`) and documented in `plots/plot.md`.

---

## 1. Universal 3-Row Narrative Structure of a $3 \times 3$ Matrix

Every $3 \times 3$ synoptic matrix follows a rigorous three-row analytical progression from **observation** to **mechanism** to **controlled decomposition**:

```text
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                       ROW 1: BASELINES & STRUCTURAL DISTRIBUTIONS                       │
│  (A) Headline Metric:          (B) Structural / Temporal     (C) Input / Resource /     │
│      Raw vs. Normalized            Cohort Distribution           Sectoral Allocation    │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                     ROW 2: SUB-COMPONENTS, JOINT EXPOSURE & SURFACE                     │
│  (D) Categorical / Tier        (E) Multi-Factor Joint        (F) 2D Bivariate Response  │
│      Modality Breakdown            Conditioning & Bounds         Surface (X1 × X2 -> Y) │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                    ROW 3: DYNAMICS, REGRESSIONS & CAUSAL DECOMPOSITION                  │
│  (G) Non-Linear Trajectory /   (H) Econometric Gradient      (I) Sequential Waterfall   │
│      Structural Curve Fit          with Error Bars & CIs         or Controlled Model    │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### Technical Standards for `src/modeling.py`:
1. **No Hardcoded Numbers in Plotting Functions**: `fit_models(data)` computes all rates, curve fits, regressions, confidence intervals, and waterfall deltas from `/datasets` and returns a dictionary `m`. Plotting functions (`generate_individual_plots(m)` and `generate_composite_matrix(m)`) only read from `m`.
2. **Coordinated Visual Language**:
   * Consistent semantic color palette across all 9 panels (e.g., distinct institutional colors for TUM `#0065BD`, MIT `#A31F34`, ETH `#1F407A`; or commodity-specific colors for Oil, Steel, Aluminum, Agriculture, Electricity).
   * Shaded regime or risk zones (`ax.axvspan`, `ax.add_patch(Rectangle(...))`) highlighting structural breaks, crisis windows, or high-efficiency regimes.
   * Explicit uncertainty quantification: error bars (`yerr`), 95% confidence bands (`fill_between`), or Fréchet/sensitivity bounds on every inferential panel.
   * Comprehensive figure footnote (`plt.figtext`) citing exact data tables, time horizons, and methodological notes.
3. **Path-Independent Shapley Waterfall Decomposition**:
   * In sequential waterfalls (e.g., Panel H or I), the sequence of adjustments is inherently order-dependent. For $K$ factors, evaluate all $K!$ permutations and compute the Shapley attribution:
     $$\phi_j = \frac{1}{K!} \sum_{\pi} \Delta_j(\pi)$$
   * Report the primary pedagogical sequence on the bars and the Shapley values in an explanatory footnote or inset box.
4. **Exact Marginal Conservation on 2D Surfaces**:
   * Any 2D surface $R(X_1, X_2)$ must conserve empirical marginals along slices:
     $$\frac{1}{100} \int_{0}^{100} R(x_1, s) \, ds \equiv Y_{\text{empirical}}(x_1)$$
     Enforce this via runtime assertion: `assert np.max(np.abs(actual_marginal - expected_marginal)) < 1e-10`.
5. **Scope-Restricted Extrapolation**:
   * Counterfactual sensitivity bands or standardized curves derived from external empirical literature must be clipped strictly to the domain supported by evidence (e.g., restricting precarity adjustments strictly to ages 14–30).
6. **Dual-Mode Rendering (`is_standalone=True` vs. `False`)**:
   * Modularize panel renderers (`render_panel_x(ax, data, lang="de", is_standalone=False)`) to support both standalone exports (`figsize=(8, 6)`, larger typography and detailed callout boxes) and 3x3 composite matrices (`figsize=(18, 15)`, compact typography) with zero code duplication. Support internationalization (`lang="de"` and `lang="en"`).

---

## 2. Blueprint 1: 50-Year Declining Per-Capita Commodity Output in Venezuela (1975–2025)

When analyzing long-term macroeconomic and physical production collapse (e.g., Venezuela 1975–2025), structure the $3 \times 3$ matrix as follows:

| Panel | Title & Visual Type | Empirical Content & Methodological Safeguard |
|---|---|---|
| **Panel A** | **Peak vs. Current Per-Capita Output Across Key Commodities** *(Grouped Bar Chart / Dumbbell Plot)* | Compares physical output per capita in peak baseline vs. current period across Crude Oil ($\text{bbl/yr/cap}$), Steel ($\text{kg/cap}$), Aluminum ($\text{kg/cap}$), Electricity ($\text{MWh/cap}$), and Maize/Corn ($\text{kg/cap}$), showing percentage collapse ($-75\%$ to $-95\%$). |
| **Panel B** | **50-Year Multi-Commodity Per-Capita Index ($1975 = 100$)** *(Multi-Line Time Series with Shaded Regimes)* | Plots normalized per-capita physical indices ($1975\text{–}2025$) for all major commodities, highlighting key structural break windows (e.g., 1976 nationalization, 2002–2003 PDVSA strike & firing of $18{,}000$ engineers, 2007–2009SIDOR/agricultural expropriations, 2017–2020 hyperinflation & sanctions). |
| **Panel C** | **Demographic Denominator & Skilled Labor Exodus** *(Dual-Axis / Stacked Cohort Bar)* | Documents the population denominator $P_t$ (natural growth vs. post-2015 net emigration of $\sim 7.7\text{M}$) and the disproportionate flight of working-age technical/engineering cohorts (ENCOVI / UN WPP). |
| **Panel D** | **Sectoral Revenue vs. Reinvestment Breakdown (Capex Starvation)** *(Stacked Area / Bar Chart)* | Decomposes oil & mineral gross revenues into operational reinvestment (Capex/maintenance) vs. fiscal extraction/social transfers and debt service across decades. |
| **Panel E** | **Joint Operational Failure Concentration & Sensitivity Bounds** *(Bar Chart with Error/Sensitivity Bounds)* | Quantifies the joint probability of production facilities experiencing simultaneous Capex deficit $\cap$ Power grid outages (SEN) $\cap$ Skilled workforce loss, comparing pre-2000 vs. post-2014 regimes with sensitivity bounds for domestic vs. secondary international estimates. |
| **Panel F** | **2D Production Response Surface: Real Capex per Worker $\times$ Institutional Governance $\to$ Output per Capita** *(2D Contour Map `viridis`)* | Calibrates a Cobb-Douglas / CES production surface fitted to historical Venezuelan and Latin American peer panel data, showing how simultaneous collapse in capital maintenance and institutional rule-of-law drives output into the bottom-left collapse trap. |
| **Panel G** | **Hydrocarbon Extraction Decay Curve vs. Geological Reserve Potential** *(Fitted Structural Decay Model)* | Fits a piecewise exponential/logistic structural break model (`scipy.optimize.curve_fit`) to physical oil output per capita ($1975\text{–}2025$) compared against peer OPEC/Latin American producers (Colombia, Brazil, Norway), proving the collapse is institutional/operational rather than geological depletion. |
| **Panel H** | **Agro-Industrial & Metallurgical Yield vs. Price Controls & Import Compression** *(OLS Regression with Error Bars)* | Plots per-capita non-oil commodity output (steel, aluminum, cereals) against real domestic investment / intermediate input availability across 50 annual observations with $95\%$ confidence intervals. |
| **Panel I** | **Sequential Waterfall Decomposition of Per-Capita Output Collapse (1998 vs. 2024)** *(5-Bar Causal Waterfall)* | Decomposes the total drop in composite per-capita commodity output into: (1) Baseline 1998 per-capita level $\to$ (2) Human capital / technical purge & brain drain $\to$ (3) Expropriations & Capex/maintenance starvation $\to$ (4) Electric grid (Guri/SEN) & input collapse $\to$ (5) Sanctions & financing restrictions $\to$ (6) Demographic emigration denominator offset $\to$ Current level. |

---

## 3. Blueprint 2: Cross-National University Comparison (TUM vs. MIT vs. ETH Zurich)

When comparing **TUM, MIT, and ETH Zurich** on **student-facing budget per student** and **research quality**, structure the $3 \times 3$ matrix as follows:

| Panel | Title & Visual Type | Empirical Content & Methodological Safeguard |
|---|---|---|
| **Panel A** | **Gross Consolidated vs. Adjusted Student-Facing Budget per FTE Student (PPP)** *(Grouped Bar Chart)* | Contrasts Tier 0 (unadjusted gross budget / headcount) against Tier 2 (**PPP-adjusted Student-Facing Instructional & Academic Budget per FTE student**), removing TUM's *Klinikum rechts der Isar* and MIT's *Lincoln Lab*. |
| **Panel B** | **Student Body & Academic Staff Cohort Pyramid (Scale & Supervision Ratio)** *(Grouped Cohort Distribution)* | Compares enrollment composition across Bachelor, Master, Doctoral candidates, Postdocs, and Tenured Professors (illustrating TUM's $>50\text{k}$ mass student scale vs. ETH's $\sim 25\text{k}$ and MIT's $\sim 11.9\text{k}$ high-supervision model). |
| **Panel C** | **Revenue & Funding Architecture** *(Stacked Percentage / PPP Per-Faculty Bar Chart)* | Decomposes funding into State/Federal Core Grants (*Grundfinanzierung*), Endowment Return & Tuition, Competitive Public Research Grants (DFG, ERC, SNF, NSF), and Industry Contracts. |
| **Panel D** | **Expenditure Allocation by Functional Tier** *(Stacked Bar Breakdown)* | Separates total university expenditure into: (1) Direct Classroom & Lab Instruction, (2) Departmental Academic & Doctoral Supervision, (3) Sponsored Pure Research, and (4) Non-Academic Auxiliary / Clinical / Defense Labs. |
| **Panel E** | **Multi-Dimensional Research Quality Profile (Field-Normalized)** *(Grouped Bar Chart with 95% CIs)* | Compares TUM, MIT, and ETH across orthogonal quality indicators: Top-10% Citation Share ($PP_{\text{top 10\%}}$ Leiden), Top-1% Breakthrough Share, Competitive Grants (ERC/NSF) per 100 Faculty, and Spin-offs/Patents per $1{,}000$ Researchers. |
| **Panel F** | **2D Institutional Frontier: Student-Facing Budget per FTE $\times$ Faculty-to-Student Ratio $\to$ Academic Quality** *(2D Contour Surface)* | Maps the bivariate iso-quality surface across global technical universities, showing where TUM (high efficiency under mass enrollment), ETH (high public core funding), and MIT (endowment-intensive small cohort) sit on the production frontier. |
| **Panel G** | **15-Year Longitudinal Trajectory: Enrollment Expansion vs. Real Budget per Student** *(Fitted Trajectory Curves)* | Tracks how rapid student enrollment growth at TUM ($+100\%$ over 15 years) diluted per-student core resources compared to ETH and MIT trajectories, fitted with spline/trend models. |
| **Panel H** | **Departmental Research Impact (FWCI) vs. Resource Intensity per Faculty** *(Cross-Departmental OLS Regression)* | Plots Field-Weighted Citation Impact against PPP funding per faculty across comparable STEM departments (CS, Mechanical/Aerospace, Electrical, Physics, Chemistry, Life Sciences) with error bars. |
| **Panel I** | **Sequential Waterfall Decomposition of Per-Student Budget & Quality Gap** *(Causal Waterfall)* | Decomposes the raw funding/impact gap between MIT, ETH, and TUM into: (1) Raw nominal gap $\to$ (2) Stripping clinical hospitals & defense labs $\to$ (3) OECD PPP & local salary cost adjustment $\to$ (4) Student-to-faculty scale ratio (undergrad mass enrollment dilution) $\to$ (5) Endowment & core base funding differential. |

---

## 4. Mandatory Documentation in `plots/plot.md`

Every project using this architecture must maintain `plots/plot.md` containing:
1. **Summary Table of All Generated Figures** (Panel ID, filename, metric, methodological classification).
2. **Panel-by-Panel Validity Audit (Panels A–I)**:
   - Exact input dataset(s) from `/datasets/` and primary source tables from `/rawdata/`.
   - Exact mathematical formula and computed values.
   - Statistical validity classification (e.g., *Complete Audited Financial Statement*, *Harmonized International Registry*, *OLS Econometric Fit*, *Bivariate Marginal-Preserving Interaction Surface*).
   - Explicit caveats, accounting boundary definitions, and sensitivity intervals.

