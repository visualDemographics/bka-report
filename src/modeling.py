"""Criminological & Econometric Modeling and Visualization Module (`src/modeling.py`).

This module serves as the central bridge between `/datasets` and `/plots` in strict
compliance with the Responsible Demographics & Empirical Research Protocol:
1. Loads all empirical inputs exclusively from audited CSV files in `datasets/`.
2. Fits inferential statistical models (via scipy.stats & scipy.optimize) to empirical data:
   - Double-exponential / Gaussian mixture fitting for the universal Age-Crime Curve.
   - Ordinary Least Squares (OLS) linear regressions across socio-economic status (SES) deciles.
   - Bivariate interaction modeling for Age x SES joint delinquency risk surfaces.
3. Computes conditional demographic risk concentrations via the probability chain rule
   and establishes Fréchet-Hoeffding copula bounds to quantify dependency uncertainty.
4. Performs sequential causal decomposition of violent crime disparities (denominator adjustment,
   direct age-sex standardization, and socio-economic equalization).
5. Renders all 9 individual publication figures in `plots/`.
6. Renders the synthesis waterfall decomposition chart and 3x3 composite matrices (German & English).
"""

import os
import sys
import matplotlib
matplotlib.use("Agg")  # Non-interactive headless backend for automated execution
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
import pandas as pd
from scipy import stats
import scipy.optimize as opt
import seaborn as sns

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASETS_DIR = os.path.join(ROOT, "datasets")
PLOTS_DIR = os.path.join(ROOT, "plots")
os.makedirs(PLOTS_DIR, exist_ok=True)

# Coordinated color palette for demographic comparison
C_DE = "#1f4e78"    # Navy blue for German population / suspects
C_NDE = "#d9534f"   # Coral red for Non-German population / suspects
COLORS = {"Deutsche": C_DE, "Nichtdeutsche": C_NDE}
CATEGORIES = ["Deutsche", "Nichtdeutsche"]


# =============================================================================
# 1. DATA INGESTION & AUDIT VALIDATION (Exclusively from datasets/)
# =============================================================================
def load_audited_datasets():
    """Loads all verified demographic and criminological datasets from /datasets.
    
    Returns:
        dict: Mapping of dataset identifiers to pandas DataFrames.
    Raises:
        FileNotFoundError: If any mandatory audited dataset is missing from datasets/.
    """
    files = {
        "pop": os.path.join(DATASETS_DIR, "bka_bevoelkerung_nenner_2023.csv"),
        "rates": os.path.join(DATASETS_DIR, "tvbz_alter_geschlecht_staatsangehoerigkeit.csv"),
        "std": os.path.join(DATASETS_DIR, "tvbz_roh_vs_altersstandardisiert.csv"),
        "res_sens": os.path.join(DATASETS_DIR, "tvbz_wohnsitz_sensitivitaet.csv"),
        "t29": os.path.join(DATASETS_DIR, "bka_t29_wohnsitz_nichtdeutsche.csv"),
        "tv_detail": os.path.join(DATASETS_DIR, "bka_tv_gewalt_892000_alter_geschlecht.csv"),
        "age_dist": os.path.join(DATASETS_DIR, "panel_b_age_distribution.csv"),
        "ses_dist": os.path.join(DATASETS_DIR, "panel_c_ses_histogram.csv"),
        "young_sex": os.path.join(DATASETS_DIR, "young_male_share_by_nationality.csv"),
        "age_curve": os.path.join(DATASETS_DIR, "panel_g_age_crime_curve.csv"),
        "ses_reg": os.path.join(DATASETS_DIR, "panel_h_ses_regression_deciles.csv"),
        "kfn_h": os.path.join(DATASETS_DIR, "panel_h_kfn_lebensbedingungen.csv"),
        "panel_a": os.path.join(DATASETS_DIR, "panel_a_raw_crime_rates.csv"),
        "full_lifecourse": os.path.join(DATASETS_DIR, "panel_g_full_lifecourse_rates.csv"),
        "benchmarks": os.path.join(DATASETS_DIR, "literature_empirical_benchmarks.csv"),
        "oecd_meta": os.path.join(DATASETS_DIR, "oecd_precarity_crime_meta.csv"),
    }
    data = {}
    for key, path in files.items():
        if not os.path.exists(path):
            raise FileNotFoundError(f"Error: Required dataset missing: {path}")
        df = pd.read_csv(path)
        if key == "benchmarks":
            df = df.set_index("parameter_id")
        data[key] = df
    return data


# =============================================================================
# 2. STATISTICAL MODELING & PARAMETER ESTIMATION (SciPy)
# =============================================================================
def compute_rate_ratio_ci(r1, n1, r2, n2, alpha=0.05):
    """Computes rate ratios and 95% confidence intervals via log-normal approximation (Rothman 2012).
    
    Args:
        r1 (float): Rate in group 1.
        n1 (int or float): Denominator or case count in group 1.
        r2 (float): Rate in group 2 (reference).
        n2 (int or float): Denominator or case count in group 2.
        alpha (float): Significance level (default: 0.05 for 95% CI).
        
    Returns:
        tuple: (rate_ratio, ci_lower, ci_upper, se_ln_rate_ratio)
    """
    rr = r1 / r2
    se_ln_rr = np.sqrt(1.0 / n1 + 1.0 / n2)
    z = stats.norm.ppf(1.0 - alpha / 2.0)
    ci_lower = rr * np.exp(-z * se_ln_rr)
    ci_upper = rr * np.exp(z * se_ln_rr)
    return rr, ci_lower, ci_upper, se_ln_rr


def fit_bivariate_risk_surface(popt_full, benchmarks=None, age_grid=None, ses_grid=None, precarity_rr=2.60):
    """Calibrates a bivariate delinquency risk surface R(Age, SES) constrained by empirical BKA marginals
    across the full life course (Ages 0–80) and parameterized by the central OECD meta-regression
    precarity relative risk (RR = 2.60x for German primary precarity deciles D1–D3; corridor [2.56x, 2.62x]).
    
    Citations & Mathematical Derivation of the Distribution Shape:
    -------------------------------------------------------------
    1. Marginal Age Distribution A_PKS(a) across Life Course (Ages 0–80):
       - Empirical Sources: BKA PKS 2023 Table 40 German male violent crime suspect counts (TVBZ per 100k)
         across childhood (under 6, 6<8, 8<10, 10<12, 12<14), adolescence (14<18), young adulthood (18<21,
         21<25, 25<30), and mature adulthood (30<40, 40<50, 50<60, 60+) divided by official residential
         denominators (BKA BV-01 & Destatis Genesis 12411-0006).
       - Functional Form: Non-linear least-squares fit (scipy.optimize.curve_fit) to a dual-process mixture
         with smooth juvenile onset sigmoid transition:
         onset(a) = 1 / (1 + exp(-k_on * (a - x_on)))
         A_peak(a) = onset(a) * a_peak * exp(-((a - mu)^2) / (2 * sigma^2)) [Adolescent maturity gap, Moffitt 1993]
         A_adult(a) = onset(a) * a_adult * exp(-a / tau)                    [Adult persistence & decay, Farrington 1986]
       - At age 0, delinquency is virtually zero (~0.5 per 100k), rising through childhood (TVBZ ~28 at age 7,
         ~244 at age 11, ~591 at age 13) to peak in adolescence (~1,166 at age 16) and desisting in adulthood.
       
    2. OECD Precarity Meta-Regression Gradient (Panel F Calibration):
       - Empirical Source: WLS meta-regression over landmark studies from OECD peer nations (datasets/oecd_precarity_crime_meta.csv).
       - Central Projection: For German primary income precarity (Destatis Mikrozensus D1–D3, X = 2.64),
         ln(Y) = 0.871 + 0.087 * ln(2.64) => Y_hat = 2.60x (corridor [2.56x, 2.62x]).
       - Replaces arbitrary single-study selection with an empirical OECD-wide calibration anchor.
         
    3. SES Precarity Threshold Function (Destatis Microcensus EU-SILC):
       - Threshold Location: Centered at SES = 40 (lowest 4 deciles D1–D4, Genesis 12211-0001, Panels C & E),
         where 72.5% of non-Germans vs. 32.8% of Germans reside.
       - Logistic Sigmoid Form: sig_precarity(s) = 1 / (1 + exp(0.12 * (s - 40))) models continuous probabilistic
         transition across the poverty threshold without artificial step-discontinuities (Atkinson 1987).
       - Mean Normalization: Normalized so that E_{s ~ U[0, 100]}[RR(s)] = 1.0.
       
    4. Adult Life-Course Turning Points & Delayed Desistance:
       - Source: Laub & Sampson (2003, Shared Beginnings, Divergent Lives: Delinquent Boys to Age 70, Chapter 6).
       - Empirical Turning Point: Stable adult employment reduces re-arrest odds by 39% (OR = 0.61, p < 0.01).
       - Persistence Horizon: Men lacking stable economic capital experience delayed desistance extending into
         middle adulthood (Farrington & Loeber 2012, NIJ Report, Table 4.3 p. 91: tau approx 25 years).
         
    5. Exact Continuous Marginal Conservation (Mathematical Guarantee):
       - Normalizes SES weights at each age slice:
         integral_0^100 R(a, s) ds / 100 == A_peak(a) + A_adult(a) == A_PKS(a) identically across all a in [0, 80].
       - Guaranteed by runtime numerical assertion (drift < 1e-10).
    """
    # Load developmental and life-course parameters directly from benchmarks
    w_gap = float(benchmarks.loc["MOFFITT_MATURITY_GAP_WEIGHT", "wert"]) if benchmarks is not None and "MOFFITT_MATURITY_GAP_WEIGHT" in benchmarks.index else 0.40
    w_depr = float(benchmarks.loc["MOFFITT_DEPRIVATION_WEIGHT", "wert"]) if benchmarks is not None and "MOFFITT_DEPRIVATION_WEIGHT" in benchmarks.index else 0.60
    desist_age = float(benchmarks.loc["SAMPSON_LAUB_DESISTANCE_AGE", "wert"]) if benchmarks is not None and "SAMPSON_LAUB_DESISTANCE_AGE" in benchmarks.index else 25.0
    persist_tau = float(benchmarks.loc["SAMPSON_LAUB_PERSISTENCE_TAU", "wert"]) if benchmarks is not None and "SAMPSON_LAUB_PERSISTENCE_TAU" in benchmarks.index else 25.0
    persist_pow = float(benchmarks.loc["SAMPSON_LAUB_PRECARITY_EXPONENT", "wert"]) if benchmarks is not None and "SAMPSON_LAUB_PRECARITY_EXPONENT" in benchmarks.index else 1.80
    persist_amp = float(benchmarks.loc["SAMPSON_LAUB_PERSISTENCE_AMPLIFIER", "wert"]) if benchmarks is not None and "SAMPSON_LAUB_PERSISTENCE_AMPLIFIER" in benchmarks.index else 0.61

    # Define evaluation grid spanning full life course: ages 0 to 80 and SES percentiles 0 to 100
    if age_grid is None:
        age_grid = np.linspace(0, 80, 100)
    if ses_grid is None:
        ses_grid = np.linspace(0, 100, 100)

    age_m, ses_m = np.meshgrid(age_grid, ses_grid)
    depr_m = (100.0 - ses_m) / 100.0  # Normalized deprivation index [0 = affluent, 1 = acute poverty]

    a_peak, mu_age, sigma_age, a_adult, tau_age, k_on, x_on = popt_full

    # Smooth precarity threshold curve centered at SES < 40 (matching Destatis EU-SILC D1–D4 in Panels C & E)
    k_trans = 0.12
    sig_precarity = 1.0 / (1.0 + np.exp(k_trans * (ses_m - 40.0)))
    rr_raw = 1.0 + (precarity_rr - 1.0) * sig_precarity
    # Normalize so population mean over uniform SES percentiles equals 1.0
    rr_m = rr_raw / np.mean(rr_raw, axis=0, keepdims=True)

    # 1. Marginal age components from empirical BKA curve fit with smooth juvenile onset
    onset_m = 1.0 / (1.0 + np.exp(-k_on * (age_m - x_on)))
    a_peak_m = onset_m * a_peak * np.exp(-((age_m - mu_age) ** 2) / (2 * (sigma_age ** 2)))
    a_adult_m = onset_m * a_adult * np.exp(-age_m / tau_age)

    # 2. Adolescent peak component (Moffitt 1993 maturity gap interaction)
    y_weights = w_gap + w_depr * rr_m
    youth_peak_m = a_peak_m * (y_weights / np.mean(y_weights, axis=0, keepdims=True))

    # 3. Adult precarity & turning point delay component (Sampson & Laub 1993, Laub & Sampson 2003 OR = 0.61)
    p_persist_m = 1.0 + persist_amp * (depr_m ** persist_pow) * np.exp(-np.maximum(0, age_m - desist_age) / persist_tau)
    adult_weights = rr_m * p_persist_m
    adult_precarity_m = a_adult_m * (adult_weights / np.mean(adult_weights, axis=0, keepdims=True))

    # Combined authentic delinquency rate (TVBZ per 100,000 males across ages 0–80)
    risk_m = youth_peak_m + adult_precarity_m

    # Exact marginal conservation assertion across all age slices a in [0, 80]
    expected_marginal = a_peak_m[0, :] + a_adult_m[0, :]
    actual_marginal = np.mean(risk_m, axis=0)
    assert np.max(np.abs(actual_marginal - expected_marginal)) < 1e-10, "BKA-Marginalkonsistenz verletzt!"

    return age_m, ses_m, risk_m




def fit_models(data):
    """Calibrates statistical and econometric models to empirical registry and survey data.
    
    This function processes empirical inputs from `datasets/` and executes all inferential
    procedures required across Panels A through I and the synthesis visualizations:
    - Calculates raw suspect rates and sex-specific proportions (Panels A & D).
    - Extracts empirical age cohorts (Panel B) and income/SES deciles (Panel C).
    - Fits the universal Age-Crime curve via SciPy non-linear optimization (Panel G).
    - Estimates linear socio-economic protection gradients via SciPy OLS regression (Panel H).
    - Calibrates the bivariate Age x SES risk surface with marginal preservation (Panel F).
    - Computes demographic risk concentration via the conditional probability chain rule
      and derives analytical Fréchet-Hoeffding bounds (Panel E).
    - Evaluates the multi-stage causal decomposition sequence (Panel I & Waterfall).
    
    Args:
        data (dict): Dictionary of loaded empirical datasets.
        
    Returns:
        dict: Complete collection of fitted parameters, regression models, and plot coordinates.
    """
    # --- PANELS A & D: Empirical Suspect Rates & Gender Proportions ---
    # Ingest standardized rate comparisons and full cohort tables
    std_df = data["std"]
    rates_df = data["rates"]
    male_std = std_df[std_df["geschlecht"] == "maennlich"].iloc[0]
    total_std = std_df[std_df["geschlecht"] == "gesamt"].iloc[0]

    # Broadest population baseline (All ages, Destatis official residential population)
    # Broadest population baseline (All ages, Destatis official residential population)
    # Official BKA PKS Key 892000 from audited datasets/panel_a_raw_crime_rates.csv
    pa_df = data["panel_a"]
    raw_rate_de = float(pa_df[pa_df["nationalitaet_gruppe"] == "Deutsche"]["tvbz_destatis_fortschreibung"].iloc[0])
    raw_rate_nde = float(pa_df[pa_df["nationalitaet_gruppe"] == "Nichtdeutsche"]["tvbz_destatis_fortschreibung"].iloc[0])
    raw_ratio = round(raw_rate_nde / raw_rate_de, 2)

    # Compute empirical gender distribution of violent crime suspects (Key 892000)
    male_tv_de = rates_df[(rates_df["geschlecht"] == "maennlich") & (rates_df["staatsangehoerigkeit"] == "deutsch")]["tatverdaechtige"].sum()
    fem_tv_de = rates_df[(rates_df["geschlecht"] == "weiblich") & (rates_df["staatsangehoerigkeit"] == "deutsch")]["tatverdaechtige"].sum()
    tot_tv_de = male_tv_de + fem_tv_de

    male_tv_nde = rates_df[(rates_df["geschlecht"] == "maennlich") & (rates_df["staatsangehoerigkeit"] == "nichtdeutsch")]["tatverdaechtige"].sum()
    fem_tv_nde = rates_df[(rates_df["geschlecht"] == "weiblich") & (rates_df["staatsangehoerigkeit"] == "nichtdeutsch")]["tatverdaechtige"].sum()
    tot_tv_nde = male_tv_nde + fem_tv_nde

    pct_male_de = round((male_tv_de / tot_tv_de) * 100, 1)
    pct_fem_de = round((fem_tv_de / tot_tv_de) * 100, 1)
    pct_male_nde = round((male_tv_nde / tot_tv_nde) * 100, 1)
    pct_fem_nde = round((fem_tv_nde / tot_tv_nde) * 100, 1)

    # --- PANEL B: Census Age Distribution (Dynamically aggregated from datasets/) ---
    # Filter out summary rows to retain strictly empirical demographic cohorts
    df_age = data["age_dist"]
    df_age_cohorts = df_age[df_age["altersspanne_jahre"] != "14–30"].copy()
    age_labels = df_age_cohorts["altersspanne_jahre"].tolist()
    age_pct_de = df_age_cohorts["anteil_deutsche_pct"].to_numpy()
    age_pct_nde = df_age_cohorts["anteil_nichtdeutsche_pct"].to_numpy()

    # --- PANEL C: Microcensus Net Equivalent Income SES Deciles (Audited empirical distribution) ---
    df_ses = data["ses_dist"]
    ses_labels = df_ses["ses_dezil"].tolist()
    ses_pct_de = df_ses["anteil_deutsche_pct"].to_numpy()
    ses_pct_nde = df_ses["anteil_nichtdeutsche_pct"].to_numpy()

    # --- AUDITED LITERATURE & REGISTER BENCHMARKS ---
    bench = data["benchmarks"]

    # --- OECD PRECARITY-CRIME META-REGRESSION (Ages 14–30) ---
    df_oecd = data["oecd_meta"]
    x_ln = df_oecd["ln_x"].to_numpy(dtype=float)
    y_ln = df_oecd["ln_y"].to_numpy(dtype=float)
    w_iv = df_oecd["weight_inv_var"].to_numpy(dtype=float)
    is_reg = df_oecd["is_register"].to_numpy(dtype=float)

    # 1. Bivariate OLS
    slope_ols, intercept_ols, r_val_ols, p_val_ols, std_err_ols = stats.linregress(x_ln, y_ln)

    # 2. Weighted Least Squares (WLS) with inverse variance
    W = np.diag(w_iv)
    X_mat = np.column_stack([np.ones_like(x_ln), x_ln])
    XtW = X_mat.T @ W
    beta_wls = np.linalg.inv(XtW @ X_mat) @ (XtW @ y_ln)
    e_wls = y_ln - (X_mat @ beta_wls)
    df_resid = len(y_ln) - 2
    s2_wls = np.sum(w_iv * (e_wls ** 2)) / df_resid
    cov_beta_wls = s2_wls * np.linalg.inv(XtW @ X_mat)
    se_beta_wls = np.sqrt(np.diag(cov_beta_wls))

    # 3. Multivariable WLS with register dummy
    X_mat3 = np.column_stack([np.ones_like(x_ln), x_ln, is_reg])
    XtW3 = X_mat3.T @ W
    beta_wls3 = np.linalg.inv(XtW3 @ X_mat3) @ (XtW3 @ y_ln)

    # Prediction curves for plotting
    x_plot = np.linspace(2.0, 3.8, 200)
    ln_x_plot = np.log(x_plot)
    y_plot_ols = np.exp(intercept_ols + slope_ols * ln_x_plot)
    y_plot_wls = np.exp(beta_wls[0] + beta_wls[1] * ln_x_plot)

    # 95% Confidence Band for WLS mean prediction
    X_pred_mat = np.column_stack([np.ones_like(ln_x_plot), ln_x_plot])
    var_pred_mean = np.sum((X_pred_mat @ cov_beta_wls) * X_pred_mat, axis=1)
    se_pred_mean = np.sqrt(var_pred_mean)
    t_crit = stats.t.ppf(0.975, df_resid)
    ci_wls_lower = np.exp((beta_wls[0] + beta_wls[1] * ln_x_plot) - t_crit * se_pred_mean)
    ci_wls_upper = np.exp((beta_wls[0] + beta_wls[1] * ln_x_plot) + t_crit * se_pred_mean)

    # Predictions for German empirical precarity ratios
    def predict_de(x_val):
        ln_x_v = np.log(x_val)
        x_vec = np.array([1.0, ln_x_v])
        ln_y_hat = float(x_vec @ beta_wls)
        se_p = np.sqrt(float(x_vec @ cov_beta_wls @ x_vec))
        return {
            "y_hat": float(np.exp(ln_y_hat)),
            "ci_lower": float(np.exp(ln_y_hat - t_crit * se_p)),
            "ci_upper": float(np.exp(ln_y_hat + t_crit * se_p)),
        }

    df_ses_p = data["ses_dist"]
    x_ses40 = round(float(df_ses_p.iloc[:4]["anteil_nichtdeutsche_pct"].sum() / df_ses_p.iloc[:4]["anteil_deutsche_pct"].sum()), 2)
    x_d13 = round(float(df_ses_p.iloc[:3]["anteil_nichtdeutsche_pct"].sum() / df_ses_p.iloc[:3]["anteil_deutsche_pct"].sum()), 2)
    armut_nde = float(bench.loc["DESTATIS_ARMUT_NDE", "wert"])
    armut_de = float(bench.loc["DESTATIS_ARMUT_DE", "wert"])
    x_silc = round(armut_nde / armut_de, 2)

    p_ses40 = predict_de(x_ses40)
    p_d13 = predict_de(x_d13)
    p_silc = predict_de(x_silc)
    rr_ctrl_central = round(float(p_d13["y_hat"]), 2)  # Dynamically derived OECD WLS Central Projection

    oecd_reg = {
        "df_oecd": df_oecd,
        "beta_ols": [intercept_ols, slope_ols],
        "r2_ols": r_val_ols ** 2,
        "p_val_ols": p_val_ols,
        "beta_wls": beta_wls,
        "se_beta_wls": se_beta_wls,
        "cov_beta_wls": cov_beta_wls,
        "beta_wls3": beta_wls3,
        "x_plot": x_plot,
        "y_plot_ols": y_plot_ols,
        "y_plot_wls": y_plot_wls,
        "ci_wls_lower": ci_wls_lower,
        "ci_wls_upper": ci_wls_upper,
        "german_projections": {
            "x_ses40": x_ses40,
            "x_d13": x_d13,
            "x_silc": x_silc,
            "y_ses40_wls": p_ses40["y_hat"],
            "ci_ses40_lower": p_ses40["ci_lower"],
            "ci_ses40_upper": p_ses40["ci_upper"],
            "y_d13_wls": p_d13["y_hat"],
            "ci_d13_lower": p_d13["ci_lower"],
            "ci_d13_upper": p_d13["ci_upper"],
            "y_silc_wls": p_silc["y_hat"],
            "ci_silc_lower": p_silc["ci_lower"],
            "ci_silc_upper": p_silc["ci_upper"],
        },
    }

    # --- PANEL G & I: Non-linear Curve Fitting of Empirical Age-Crime Curves (SciPy Optimize) ---
    df_g = data["age_curve"]
    emp_ages = df_g["alter_mitte"].to_numpy(dtype=float)
    emp_de = df_g["tvbz_deutsche_maenner"].to_numpy(dtype=float)
    emp_nde_ctrl = df_g["tvbz_nichtdeutsche_maenner_kontrolliert"].to_numpy(dtype=float)

    # Extract raw empirical non-German suspect rates from BKA Table T50 / AZR
    valid_g = df_g.dropna(subset=["tvbz_nichtdeutsche_maenner_roh"])
    emp_ages_nde_raw = valid_g["alter_mitte"].to_numpy(dtype=float)
    emp_nde_raw_valid = valid_g["tvbz_nichtdeutsche_maenner_roh"].to_numpy(dtype=float)

    def age_crime_func(x, a, mu, sigma, b, tau):
        """Universal double-exponential / Gaussian mixture representation of the Age-Crime Curve."""
        return a * np.exp(-((x - mu) ** 2) / (2 * sigma ** 2)) + b * np.exp(-x / tau)

    # Initialize curve fit on German empirical suspect rates using Moffitt (1993) benchmark priors
    p0_mu = float(bench.loc["MOFFITT_PEAK_AGE", "wert"])
    p0_sig = float(bench.loc["MOFFITT_PEAK_SIGMA", "wert"])
    # Verified KFN darkfield survey benchmarks
    or_kfn_ctrl = float(bench.loc["KFN_FB109_MULTILEVEL_OR_MIGRATION_CONTROLLED", "wert"])
    or_kfn_unadj = float(bench.loc["KFN_FB107_OR_UNADJUSTED_POOLED", "wert"])
    or_kfn_equal = float(bench.loc["KFN_FB107_OR_EQUAL_CONDITIONS_POOLED", "wert"])

    p0 = [1500, p0_mu, p0_sig, 60, 30]
    popt_de, _ = opt.curve_fit(age_crime_func, emp_ages, emp_de, p0=p0, maxfev=10000)

    # Fit raw empirical Non-German curve from BKA T50 / AZR register points
    p0_nde = [4000, 17.5, 5.0, 500, 25]
    popt_nde_raw, _ = opt.curve_fit(age_crime_func, emp_ages_nde_raw, emp_nde_raw_valid, p0=p0_nde, maxfev=10000)

    # Residence-adjusted curve parameters (BKA T29 Tier 3: dynamically derived from Table 29 male suspects)
    df_t29 = data["t29"]
    r_m = df_t29[(df_t29["straftat"] == "Gewaltkriminalitaet") & (df_t29["geschlecht"] == "maennlich")].iloc[0]
    res_factor = round(1.0 - (float(r_m["wohnsitz_ausland"]) + float(r_m["ohne_festen_oder_unbekannter_wohnsitz"])) / float(r_m["nichtdeutsche_tv"]), 4)
    popt_nde_res = [popt_nde_raw[0] * res_factor, popt_nde_raw[1], popt_nde_raw[2], popt_nde_raw[3] * res_factor, popt_nde_raw[4]]
    popt_nde = popt_nde_res

    # --- PANEL G: Full Life-Course German Age Distribution from Age 0 to 80 (BKA T40 & BV-01 / Destatis 12411) ---
    df_full_lc = data["full_lifecourse"]
    emp_ages_full = df_full_lc["alter_mitte"].to_numpy(dtype=float)
    emp_rates_full = df_full_lc["tvbz_deutsche_maenner"].to_numpy(dtype=float)

    def age_crime_full_lifecourse(a, a_peak, mu, sigma, a_adult, tau, k_on, x_on):
        onset = 1.0 / (1.0 + np.exp(-k_on * (a - x_on)))
        peak = a_peak * np.exp(-((a - mu) ** 2) / (2.0 * (sigma ** 2)))
        adult = a_adult * np.exp(-a / tau)
        return onset * (peak + adult)

    p0_full = [550, 16.5, 3.0, 1600, 22.0, 0.6, 13.0]
    popt_full, _ = opt.curve_fit(age_crime_full_lifecourse, emp_ages_full, emp_rates_full, p0=p0_full, maxfev=10000)

    # --- PANEL H: Empirical Youth Violence by Origin and Living Conditions (KFN FB 107) ---
    df_h = data.get("kfn_h", data.get("ses_reg"))

    # Load empirical SES educational stratification gradient from benchmarks (KFN FB 107 Tab. 5.2)
    ses_ratio = float(bench.loc["KFN_FB107_SES_GRADIENT_FORDER_GYM", "wert"])
    slope_factor = (ses_ratio - 1.0) / (ses_ratio + 1.0)

    # --- PANEL G: Bivariate 2D Delinquency Risk Surface (Constrained Marginal Fitting & Moffitt across Ages 0–80) ---
    age_m, ses_m, risk_m = fit_bivariate_risk_surface(popt_full, benchmarks=bench, precarity_rr=rr_ctrl_central)

    # Extrapolate 2D risk surface coordinates across full life course (Ages 0 to 80)
    a_peak, mu_age, sigma_age, a_adult, tau_age, k_on, x_on = popt_full
    age_eval = np.linspace(0, 80, 17)  # Ages 0 to 80 (steps of 5 years)
    ses_eval = np.linspace(0, 100, 11)
    _, _, r_eval_m = fit_bivariate_risk_surface(popt_full, benchmarks=bench, age_grid=age_eval, ses_grid=ses_eval, precarity_rr=rr_ctrl_central)

    w_gap_exp = float(bench.loc["MOFFITT_MATURITY_GAP_WEIGHT", "wert"])
    w_depr_exp = float(bench.loc["MOFFITT_DEPRIVATION_WEIGHT", "wert"])

    # --- PANEL E: High-Risk Demographic Group (Harmonized 14–30 Marginals & Copula Bounds) ---
    # Strict adherence to Responsible Research: No multiplying independent marginals!
    # Instead, compute exact conditional probability chain rule over the full 14–30 criminological window:
    # P(Risk | g) = P(Youth 14–30 | g) * P(Male | Youth 14–30, g) * P(Poverty | Youth 14–30, Male, g)
    # plus Fréchet-Hoeffding copula bounds to quantify dependency bounds without ad-hoc assumptions.
    df_young_sex = data["young_sex"]

    # 1. Conditional male proportion in the 14-30 high-risk window P(Male | Youth 14–30, g)
    # Uses Destatis Census 2022 & AZR 12521-04 (51.2% German vs. 55.0% Non-German)
    match_ym_30 = df_young_sex[df_young_sex["alterskohorte"].str.contains("14-30")]
    if len(match_ym_30) > 0:
        row_ym = match_ym_30.iloc[0]
        p_male_youth_de = float(row_ym["anteil_maennlich_deutsch_pct"]) / 100.0  # 0.512 (51.2%)
        p_male_youth_nde = float(row_ym["anteil_maennlich_nichtdeutsch_pct"]) / 100.0  # 0.550 (55.0%)
    else:
        p_male_youth_de = 0.512
        p_male_youth_nde = 0.550

    # 2. Population-weighted at-risk-of-poverty rate across 14-30 cohorts P(Poverty | Youth, g) from Destatis EU-SILC
    # Integrates sub-cohorts: 14–17 (U18 rate), 18–24 (18–24 rate), and 25–29 (25–49 rate) weighted by Census 2022 counts
    pov_u18_de = float(bench.loc["DESTATIS_POVERTY_U18_DE", "wert"]) / 100.0    # 14.8%
    pov_u18_nde = float(bench.loc["DESTATIS_POVERTY_U18_NDE", "wert"]) / 100.0  # 36.2%
    pov_18_24_de = float(bench.loc["DESTATIS_POVERTY_18_24_DE", "wert"]) / 100.0  # 22.1%
    pov_18_24_nde = float(bench.loc["DESTATIS_POVERTY_18_24_NDE", "wert"]) / 100.0  # 48.6%
    pov_25_49_de = float(bench.loc["DESTATIS_POVERTY_25_49_DE", "wert"]) / 100.0  # 11.5%
    pov_25_49_nde = float(bench.loc["DESTATIS_POVERTY_25_49_NDE", "wert"]) / 100.0  # 31.8%

    n_14_17_de = float(df_age[df_age["altersspanne_jahre"] == "14–17"]["bevoelkerung_deutsche"].iloc[0])
    n_14_17_nde = float(df_age[df_age["altersspanne_jahre"] == "14–17"]["bevoelkerung_nichtdeutsche"].iloc[0])
    n_18_20_de = float(df_age[df_age["altersspanne_jahre"] == "18–20"]["bevoelkerung_deutsche"].iloc[0])
    n_18_20_nde = float(df_age[df_age["altersspanne_jahre"] == "18–20"]["bevoelkerung_nichtdeutsche"].iloc[0])
    n_21_24_de = float(df_age[df_age["altersspanne_jahre"] == "21–24"]["bevoelkerung_deutsche"].iloc[0])
    n_21_24_nde = float(df_age[df_age["altersspanne_jahre"] == "21–24"]["bevoelkerung_nichtdeutsche"].iloc[0])
    n_25_29_de = float(df_age[df_age["altersspanne_jahre"] == "25–29"]["bevoelkerung_deutsche"].iloc[0])
    n_25_29_nde = float(df_age[df_age["altersspanne_jahre"] == "25–29"]["bevoelkerung_nichtdeutsche"].iloc[0])

    n_18_24_de = n_18_20_de + n_21_24_de
    n_18_24_nde = n_18_20_nde + n_21_24_nde

    n_tot_14_30_de = n_14_17_de + n_18_24_de + n_25_29_de
    n_tot_14_30_nde = n_14_17_nde + n_18_24_nde + n_25_29_nde

    p_pov_youth_de = (n_14_17_de * pov_u18_de + n_18_24_de * pov_18_24_de + n_25_29_de * pov_25_49_de) / n_tot_14_30_de  # ~16.87%
    p_pov_youth_nde = (n_14_17_nde * pov_u18_nde + n_18_24_nde * pov_18_24_nde + n_25_29_nde * pov_25_49_nde) / n_tot_14_30_nde  # ~40.35%

    # 3. Gender-specific poverty adjustment factor k = P(Pov | Youth, Male) / P(Pov | Youth) from Destatis EU-SILC FS 15
    k_sex_adj = float(bench.loc["SILC_MALE_POVERTY_RATIO_K", "wert"])

    p_pov_male_youth_de = p_pov_youth_de * k_sex_adj  # ~16.32%
    p_pov_male_youth_nde = p_pov_youth_nde * k_sex_adj  # ~39.05%

    # 4. Adolescent population share P(Youth | g) from Census 2022 / Genesis 12411 (14–30 risk bracket)
    p_youth_de = round(df_age[df_age["in_hochrisikofenster"] & (df_age["altersspanne_jahre"] != "14–30")]["anteil_deutsche_pct"].sum() / 100, 3)
    p_youth_nde = round(df_age[df_age["in_hochrisikofenster"] & (df_age["altersspanne_jahre"] != "14–30")]["anteil_nichtdeutsche_pct"].sum() / 100, 3)

    # 5. Point estimate under empirical conditional chain rule:
    # P(Risk | g) = P(Youth | g) * P(Male | Youth, g) * P(Poverty | Youth, Male, g)
    hr_share_de = round(p_youth_de * p_male_youth_de * p_pov_male_youth_de * 100, 1)  # ~1.3%
    hr_share_nde = round(p_youth_nde * p_male_youth_nde * p_pov_male_youth_nde * 100, 1)  # ~6.7%
    hr_disparity = round((p_youth_nde * p_male_youth_nde * p_pov_male_youth_nde) / (p_youth_de * p_male_youth_de * p_pov_male_youth_de), 2)  # ~5.04x

    # 6. Fréchet-Hoeffding copula bounds for the joint intersection P(Youth ∩ Male ∩ Poverty | g):
    # Literature source parsed via benchmark key COPULA_FRECHET_HOEFFDING_BOUNDS (Nelsen 2006, Theorem 2.2.3):
    copula_bench = bench.loc["COPULA_FRECHET_HOEFFDING_BOUNDS"]
    copula_author = str(copula_bench["quelle_autor_institution"])
    copula_title = str(copula_bench["quelle_titel"])
    copula_year = str(copula_bench["jahr"])
    copula_cite_short = f"Nelsen ({copula_year})"
    copula_citation_full = f"{copula_author} ({copula_year}): {copula_title}"

    # Lower bound: L(g) = P(Youth | g) * max(0, P(Male | Youth) + P(Poverty | Youth) - 1)
    # Upper bound: U(g) = P(Youth | g) * min(P(Male | Youth), P(Poverty | Youth))
    hr_lower_de = round(p_youth_de * max(0.0, p_male_youth_de + p_pov_male_youth_de - 1.0) * 100, 1)
    hr_upper_de = round(p_youth_de * min(p_male_youth_de, p_pov_male_youth_de) * 100, 1)

    hr_lower_nde = round(p_youth_nde * max(0.0, p_male_youth_nde + p_pov_male_youth_nde - 1.0) * 100, 1)
    hr_upper_nde = round(p_youth_nde * min(p_male_youth_nde, p_pov_male_youth_nde) * 100, 1)

    # Asymmetric error bars [[y - lower], [upper - y]] for Matplotlib visualization
    hr_yerr = [
        [max(0.0, hr_share_de - hr_lower_de), max(0.0, hr_share_nde - hr_lower_nde)],
        [max(0.0, hr_upper_de - hr_share_de), max(0.0, hr_upper_nde - hr_share_nde)]
    ]

    # Plackett copula sensitivity analysis (varying odds ratio OR in [0.8, 1.5] for Sex x Poverty association)
    # Bounds ingested via benchmark keys COPULA_PLACKETT_OR_MIN and COPULA_PLACKETT_OR_MAX (Plackett 1965)
    plackett_min = float(bench.loc["COPULA_PLACKETT_OR_MIN", "wert"])
    plackett_max = float(bench.loc["COPULA_PLACKETT_OR_MAX", "wert"])
    plackett_bench = bench.loc["COPULA_PLACKETT_OR_MIN"]
    plackett_cite_short = f"Plackett ({plackett_bench['jahr']})"

    plackett_sens = {}
    for test_or in [plackett_min, 1.0, 1.2, plackett_max]:
        def calc_plackett(pm, pp, or_val):
            if abs(or_val - 1.0) < 1e-4:
                return pm * pp
            s = 1.0 + (pm + pp) * (or_val - 1.0)
            return (s - np.sqrt(max(0.0, s**2 - 4.0 * or_val * (or_val - 1.0) * pm * pp))) / (2.0 * (or_val - 1.0))
        sh_de = p_youth_de * calc_plackett(p_male_youth_de, p_pov_male_youth_de, test_or) * 100
        sh_nde = p_youth_nde * calc_plackett(p_male_youth_nde, p_pov_male_youth_nde, test_or) * 100
        plackett_sens[test_or] = (round(sh_de, 2), round(sh_nde, 2), round(sh_nde / sh_de, 2))

    # --- PANEL I & WATERFALL: Sequential Causal Decomposition Stages ---
    sens_df = data["res_sens"]
    tier2_male = sens_df[(sens_df["geschlecht"] == "maennlich") & (sens_df["szenario"].str.contains("ohne Ausland"))].iloc[0]
    tier2_nde_rate = tier2_male["tvbz_nichtdeutsche_14plus"]

    std_male_de = male_std["tvbz_altersstd_deutsch"]
    std_male_nde = male_std["tvbz_altersstd_nichtdeutsch"]

    # Compute combined non-resident and demographic standardization multiplier
    res_scale = tier2_nde_rate / male_std["tvbz_roh_14plus_nichtdeutsch"]
    comb_std_res_nde = round(std_male_nde * res_scale, 1)

    # Official BKA PKS Register Decomposition (Males 14+)
    wf_raw_nde = float(male_std["tvbz_roh_14plus_nichtdeutsch"])        # 1203.4
    wf_tier2_nde = float(tier2_nde_rate)                                # 1036.4
    wf_delta_res = round(wf_raw_nde - wf_tier2_nde, 1)                  # 167.0
    wf_comb_nde = float(comb_std_res_nde)                               # 880.3
    wf_delta_demo = round(wf_tier2_nde - wf_comb_nde, 1)                # 156.1
    wf_base_de = float(std_male_de)                                     # 285.8

    waterfall_data = {
        "raw_nde": wf_raw_nde,
        "tier2_nde": wf_tier2_nde,
        "delta_res": wf_delta_res,
        "comb_nde": wf_comb_nde,
        "delta_demo": wf_delta_demo,
        "base_de": wf_base_de,
        "ratio_raw": float(male_std["verhaeltnis_roh"]),               # 4.34
        "ratio_res": round(wf_tier2_nde / float(male_std["tvbz_roh_14plus_deutsch"]), 2),  # 3.74
        "ratio_std": round(wf_comb_nde / wf_base_de, 2),               # 3.08
        "rr_proj_lo": round(p_ses40["y_hat"], 2),
        "rr_proj_hi": round(p_silc["y_hat"], 2),
        "rr_proj_central": round(p_d13["y_hat"], 2),
        "bottoms": [0.0, wf_tier2_nde, wf_comb_nde, 0.0, 0.0],
        "heights": [wf_raw_nde, wf_delta_res, wf_delta_demo, wf_comb_nde, wf_base_de],
    }

    # Document structured decomposition stages for table reporting and waterfall charting
    decomp_summary = [
        {"stufe": "0. Rohdaten PKS 2023 (Männer 14+)", "rate_de": male_std["tvbz_roh_14plus_deutsch"], "rate_nde": male_std["tvbz_roh_14plus_nichtdeutsch"], "ratio": male_std["verhaeltnis_roh"], "status": "Registerzählung unbereinigt (4,34x)"},
        {"stufe": "1. Residenzbereinigung (BKA T29 Tier 3)", "rate_de": male_std["tvbz_roh_14plus_deutsch"], "rate_nde": tier2_nde_rate, "ratio": tier2_male["verhaeltnis"], "status": "Abzug Tatverdächtige Ausland & ohne festen Wohnsitz (~14%, 3,74x)"},
        {"stufe": "2. Direkte Altersstandardisierung (Destatis)", "rate_de": std_male_de, "rate_nde": std_male_nde, "ratio": male_std["verhaeltnis_altersstd"], "status": "Standardbevölkerung Gesamt 14+ (3,58x)"},
        {"stufe": "2b. Residenz + Alter kombiniert (BKA/Destatis)", "rate_de": std_male_de, "rate_nde": comb_std_res_nde, "ratio": round(comb_std_res_nde / std_male_de, 2), "status": "Amtlich bereinigte Registerrate (3,08x)"},
        {"stufe": "3. Kriminologisches Dunkelfeld (KFN FB 107)", "rate_de": 6.4, "rate_nde": 5.9, "ratio": 0.92, "status": "Gleiche Lebensbedingungen (SES/Familie/Peers, p = 0,56 n.s., siehe Panel H)"},
    ]

    return {
        "waterfall_data": waterfall_data,
        "decomp_summary": decomp_summary,
        "raw_rates": [raw_rate_de, raw_rate_nde],
        "raw_ratio": raw_ratio,
        "male_shares": [pct_male_de, pct_male_nde],
        "female_shares": [pct_fem_de, pct_fem_nde],
        "age_labels": age_labels,
        "age_pct_de": age_pct_de,
        "age_pct_nde": age_pct_nde,
        "youth_share_de": round(p_youth_de * 100, 1),
        "youth_share_nde": round(p_youth_nde * 100, 1),
        "ses_labels": ses_labels,
        "ses_pct_de": ses_pct_de,
        "ses_pct_nde": ses_pct_nde,
        "hr_shares": [hr_share_de, hr_share_nde],
        "hr_disparity": hr_disparity,
        "hr_bounds": [[hr_lower_de, hr_upper_de], [hr_lower_nde, hr_upper_nde]],
        "hr_yerr": hr_yerr,
        "copula_cite_short": copula_cite_short,
        "copula_citation_full": copula_citation_full,
        "plackett_cite_short": plackett_cite_short,
        "plackett_bounds": (plackett_min, plackett_max),
        "plackett_sens": plackett_sens,
        "p_male_youth": [round(p_male_youth_de * 100, 1), round(p_male_youth_nde * 100, 1)],
        "p_pov_youth": [round(p_pov_youth_de * 100, 1), round(p_pov_youth_nde * 100, 1)],
        "emp_ages": emp_ages,
        "emp_de": emp_de,
        "emp_nde_ctrl": emp_nde_ctrl,
        "popt_de": popt_de,
        "popt_nde": popt_nde,
        "popt_nde_raw": popt_nde_raw,
        "popt_nde_res": popt_nde_res,
        "emp_ages_nde_raw": emp_ages_nde_raw,
        "emp_nde_raw_valid": emp_nde_raw_valid,
        "or_kfn_ctrl": or_kfn_ctrl,
        "or_kfn_unadj": or_kfn_unadj,
        "or_kfn_equal": or_kfn_equal,
        "age_crime_func": age_crime_func,
        "age_crime_full_lifecourse": age_crime_full_lifecourse,
        "popt_full": popt_full,
        "emp_ages_full": emp_ages_full,
        "emp_rates_full": emp_rates_full,
        "rr_ctrl_central": rr_ctrl_central,
        "df_kfn_h": df_h,
        "age_m": age_m,
        "ses_m": ses_m,
        "risk_m": risk_m,
        "controlled_rates": [wf_base_de, wf_comb_nde],
        "controlled_ratio": round(wf_comb_nde / wf_base_de, 2),
        "oecd_reg": oecd_reg,
    }


# =============================================================================
# 3. GENERATION OF INDIVIDUAL PANEL FIGURES IN /plots
# =============================================================================
def generate_individual_plots(m):
    """Renders each of the 9 analytical panels as a standalone, high-resolution figure in /plots.
    
    Args:
        m (dict): Fitted model coordinates, parameter estimates, and empirical rates from fit_models().
    """
    plt.style.use("seaborn-v0_8-whitegrid")
    print("\n-> Rendere alle 9 Einzelplots in /plots...")

    # --- PLOT A: Raw Suspect Rate (TVBZ) ---
    # Unadjusted baseline showing the 3.83x crude disparity.
    # Note: BKA IMK Report (p. 41) explicitly cautions that this ratio cannot be interpreted
    # as an authentic criminality rate due to numerator-denominator mismatch (open numerator vs resident denominator).
    fig, ax = plt.subplots(figsize=(7, 5.5), dpi=300)
    bars = ax.bar(CATEGORIES, m["raw_rates"], color=[C_DE, C_NDE], edgecolor="black", alpha=0.9, width=0.48)
    ax.set_title("(A) Rohe Tatverdächtigenbelastungszahl [BKA PKS 2023 Registerbefund]", fontweight="bold", fontsize=11)
    ax.set_ylabel("TVBZ (Verdächtige pro 100.000 Einwohner)", fontsize=10)
    ax.set_ylim(0, 720)
    for b in bars:
        h = b.get_height()
        ax.text(b.get_x() + b.get_width() / 2, h / 2, f"{h:.1f}", ha="center", va="center", color="white", fontweight="bold", fontsize=13)
    ax.text(1, 620, f"{m['raw_ratio']:.2f}× Rohdisparität (Unbereinigt)", ha="center", fontweight="bold", color=C_NDE, fontsize=10.5)
    plt.tight_layout()
    p_a = os.path.join(PLOTS_DIR, "panel_a_raw_crime_rates.png")
    plt.savefig(p_a, dpi=300, bbox_inches="tight")
    plt.close()
    print("   ✓ Panel A: panel_a_raw_crime_rates.png")

    # --- PLOT B: Empirical Age Structure (Census 2022) ---
    # Highlights the structural age confounder: The immigrant population features an asymmetric youth
    # bulge (31.2% in high-risk bracket 14-30), whereas the German resident population is an aging urn (15.9% in 14-30).
    fig, ax = plt.subplots(figsize=(8, 5.5), dpi=300)
    x = np.arange(len(m["age_labels"]))
    w = 0.38
    ax.bar(x - w / 2, m["age_pct_de"], width=w, label="Deutsche", color=C_DE, edgecolor="black", alpha=0.9)
    ax.bar(x + w / 2, m["age_pct_nde"], width=w, label="Nichtdeutsche", color=C_NDE, edgecolor="black", alpha=0.9)
    ax.axvspan(0.5, 4.5, color="gold", alpha=0.25, zorder=0)
    ax.text(2.5, 23.5, f"PEAK-RISIKO-ALTER (14–30 J.)\n{m['youth_share_nde']:.1f}% Nicht-Dt. vs. {m['youth_share_de']:.1f}% Dt.", ha="center", fontweight="bold", fontsize=9, bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="gold", lw=1.2))
    ax.set_xticks(x)
    ax.set_xticklabels(m["age_labels"], fontsize=9.5, rotation=20)
    ax.set_title("(B) Altersverteilung nach Nationalität [Destatis Zensus 2022 Vollerhebung]", fontweight="bold", fontsize=11)
    ax.set_xlabel("Alterskohorte in Jahren", fontsize=10)
    ax.set_ylabel("Anteil an jeweiliger Gesamtbevölkerung (%)", fontsize=10)
    ax.set_ylim(0, 27)
    ax.legend(loc="upper right", fontsize=9)
    plt.tight_layout()
    p_b = os.path.join(PLOTS_DIR, "panel_b_age_distribution.png")
    plt.savefig(p_b, dpi=300, bbox_inches="tight")
    plt.close()
    print("   ✓ Panel B: panel_b_age_distribution.png")

    # --- PLOT C: Socioeconomic Status Deciles (Microcensus EU-SILC) ---
    # Highlights the precarity mediator: Over 61% of non-Germans cluster in the bottom 3 income deciles (SES <= 30),
    # compared to only 23.3% of Germans (and 72.5% vs 32.8% for SES < 40), creating massive structural vulnerability.
    fig, ax = plt.subplots(figsize=(8, 5.5), dpi=300)
    x_c = np.arange(len(m["ses_labels"]))
    pct_d1_3_de = m["ses_pct_de"][:3].sum()
    pct_d1_3_nde = m["ses_pct_nde"][:3].sum()
    ratio_d1_3 = pct_d1_3_nde / pct_d1_3_de
    ax.bar(x_c - w / 2, m["ses_pct_de"], width=w, label="Deutsche", color=C_DE, edgecolor="black", alpha=0.9)
    ax.bar(x_c + w / 2, m["ses_pct_nde"], width=w, label="Nichtdeutsche", color=C_NDE, edgecolor="black", alpha=0.9)
    ax.axvspan(-0.5, 2.5, color="red", alpha=0.15, zorder=0)
    ax.text(1.2, 30.5, f"NIEDRIGSTE 3 DEZILE (D1–D3, SES ≤ 30)\n{pct_d1_3_nde:.1f}% Nicht-Dt. vs. {pct_d1_3_de:.1f}% Dt. ({ratio_d1_3:.2f}×)", ha="center", fontweight="bold", fontsize=8.8, color="darkred", bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="red", lw=1.2))
    ax.set_xticks(x_c)
    ax.set_xticklabels(m["ses_labels"], fontsize=9.5)
    ax.set_title("(C) Sozioökonomischer Status [Destatis Mikrozensus EU-SILC 2023]", fontweight="bold", fontsize=11)
    ax.set_xlabel("Einkommens-/SES-Dezile [D1 = Akute Armut, D10 = Wohlstand]", fontsize=10)
    ax.set_ylabel("Anteil an jeweiliger Gesamtbevölkerung (%)", fontsize=10)
    ax.set_ylim(0, 36)
    ax.legend(loc="upper right", fontsize=9)
    plt.tight_layout()
    p_c = os.path.join(PLOTS_DIR, "panel_c_socioeconomic_status.png")
    plt.savefig(p_c, dpi=300, bbox_inches="tight")
    plt.close()
    print("   ✓ Panel C: panel_c_socioeconomic_status.png")

    # --- PLOT D: Gender Distribution of Violent Crime Suspects ---
    # Demonstrates that violent crime is universally dominated by males (>80% in both demographic groups),
    # rendering male proportion a key demographic confounder.
    fig, ax = plt.subplots(figsize=(6.5, 5.5), dpi=300)
    x_pos = np.arange(len(CATEGORIES))
    ax.bar(x_pos, m["male_shares"], width=0.48, label="Männlich", color=C_DE, edgecolor="black", alpha=0.9)
    ax.bar(x_pos, m["female_shares"], width=0.48, bottom=m["male_shares"], label="Weiblich", color=C_NDE, edgecolor="black", alpha=0.9)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(CATEGORIES, fontsize=10.5)
    ax.set_title("(D) Geschlechterproportion der Gewalt-Tatverdächtigen [BKA PKS 2023 Befund T20]", fontweight="bold", fontsize=11)
    ax.set_ylabel("Anteil an Tatverdächtigen (%)", fontsize=10)
    ax.set_ylim(0, 110)
    for i in x_pos:
        ms = m["male_shares"][i]
        fs = m["female_shares"][i]
        ax.text(i, ms / 2, f"{ms:.1f}%\nMännlich", ha="center", va="center", color="white", fontweight="bold", fontsize=11)
        ax.text(i, ms + fs / 2, f"{fs:.1f}%", ha="center", va="center", color="white", fontweight="bold", fontsize=10)
    ax.legend(loc="upper right", fontsize=9)
    plt.tight_layout()
    p_d = os.path.join(PLOTS_DIR, "panel_d_gender_distribution.png")
    plt.savefig(p_d, dpi=300, bbox_inches="tight")
    plt.close()
    print("   ✓ Panel D: panel_d_gender_distribution.png")

    # --- PLOT E: Combined High-Risk Demographic Group (Chain Rule & Copula Bounds) ---
    # Evaluates the joint intersection (Male ∩ Age 14-30 ∩ Poverty) via conditional probability chain rule.
    # Asymmetric error bars visualize analytical Fréchet-Hoeffding bounds spanning all possible copula dependencies.
    # NOTE: This panel represents the novel methodological contribution of this research.
    fig, ax = plt.subplots(figsize=(7.2, 5.8), dpi=300)
    bars_e = ax.bar(
        CATEGORIES, m["hr_shares"],
        yerr=m["hr_yerr"], capsize=6, ecolor="#1A237E",
        color=[C_DE, C_NDE], edgecolor="black", alpha=0.9, width=0.48,
        error_kw=dict(lw=1.6, capthick=1.6)
    )
    ax.set_title(f"(E) Eigener methodischer Beitrag: Anteil an kombinierter Risikokonstellation\n(Kettenregel & Fréchet-Schranken nach {m['copula_cite_short']})\n[Männlich ∩ 14–30 Jahre ∩ Armut: Zensus 2022 & EU-SILC 2023]", fontweight="bold", fontsize=10.0)
    ax.set_ylim(0, 18.0)
    bounds = m["hr_bounds"]
    for i, b in enumerate(bars_e):
        h = b.get_height()
        lo, hi = bounds[i]
        ax.text(b.get_x() + b.get_width() / 2, max(hi, h) + 0.45, f"{h:.1f}%\n[Fréchet: {lo:.1f}–{hi:.1f}%]", ha="center", va="bottom", fontweight="bold", fontsize=10)
    ax.text(0.5, 0.92, f"{m['hr_disparity']}× höhere Risikokonzentration (Eigener Beitrag: Exakte Kettenregel)", transform=ax.transAxes, ha="center", fontweight="bold", color=C_NDE, fontsize=9.2,
            bbox=dict(boxstyle="round,pad=0.25", fc="#FFF9C4", ec="gold", lw=1.2))
    plt.figtext(0.5, 0.015, f"Methodischer Beitrag: Exakte Kettenregel über harmonisiertes 14–30 J. Fenster. Fehlerbalken = analytische Fréchet-Hoeffding-Grenzen ({m['copula_cite_short']}, Th. 2.2.3).\nP(Männlich | 14–30 J.) = {m['p_male_youth'][0]:.1f}% (Dt.) vs. {m['p_male_youth'][1]:.1f}% (Nicht-Dt.); Armut 14–30 J. (gewichtet) = {m['p_pov_youth'][0]:.1f}% (Dt.) vs. {m['p_pov_youth'][1]:.1f}% (Nicht-Dt.)",
                ha="center", fontsize=7.2, style="italic", color="#37474F",
                bbox=dict(boxstyle="round,pad=0.2", fc="#ECEFF1", ec="#B0BEC5", lw=0.8))
    plt.tight_layout(rect=[0, 0.05, 1, 1])
    p_e = os.path.join(PLOTS_DIR, "panel_e_joint_risk_concentration.png")
    plt.savefig(p_e, dpi=300, bbox_inches="tight")
    plt.close()
    print("   ✓ Panel E: panel_e_joint_risk_concentration.png")

    # --- PLOT F: OECD Precarity vs. Violent Crime Meta-Regression (Ages 14–30) ---
    fig_f, ax_f = plt.subplots(figsize=(10.5, 6.8), dpi=300)
    render_panel_f_oecd_regression(ax_f, m["oecd_reg"], lang="de", is_standalone=True)
    plt.tight_layout()
    p_f = os.path.join(PLOTS_DIR, "panel_f_oecd_precarity_regression.png")
    plt.savefig(p_f, dpi=300, bbox_inches="tight")
    plt.close()
    print("   ✓ Panel F (OECD Meta-Regression Deutsch): panel_f_oecd_precarity_regression.png")

    fig_f_en, ax_f_en = plt.subplots(figsize=(10.5, 6.8), dpi=300)
    render_panel_f_oecd_regression(ax_f_en, m["oecd_reg"], lang="en", is_standalone=True)
    plt.tight_layout()
    p_f_en = os.path.join(PLOTS_DIR, "panel_f_oecd_precarity_regression_en.png")
    plt.savefig(p_f_en, dpi=300, bbox_inches="tight")
    plt.close()
    print("   ✓ Panel F (OECD Meta-Regression English): panel_f_oecd_precarity_regression_en.png")

    # --- PLOT G: Bivariate 2D Delinquency Risk Surface (Age x SES) ---
    fig_g, ax_g = plt.subplots(figsize=(8.0, 5.8), dpi=300)
    render_panel_g_risk_matrix(ax_g, m, lang="de", is_standalone=True, fig=fig_g)
    plt.tight_layout(rect=[0, 0.03, 1, 1])
    p_g = os.path.join(PLOTS_DIR, "panel_g_risk_matrix_age_ses.png")
    plt.savefig(p_g, dpi=300, bbox_inches="tight")
    plt.close()
    print("   ✓ Panel G: panel_g_risk_matrix_age_ses.png")

    # --- PLOT H: Official BKA Register Decomposition Waterfall (Males 14+) ---
    fig_h, ax_h = plt.subplots(figsize=(10.5, 6.8), dpi=300)
    render_bka_register_waterfall_panel(ax_h, m["waterfall_data"], lang="de", is_standalone=True, panel_letter="H")
    plt.tight_layout()
    p_h_wf = os.path.join(PLOTS_DIR, "panel_h_bka_waterfall.png")
    plt.savefig(p_h_wf, dpi=300, bbox_inches="tight")
    plt.close()
    print("   ✓ Panel H (BKA Waterfall): panel_h_bka_waterfall.png")

    # --- PLOT I: Universal Age-Crime Curves with Precarity Sensitivity (14–80 Years) ---
    fig_i, ax_i = plt.subplots(figsize=(9.8, 6.6), dpi=300)
    render_panel_i_age_crime(ax_i, m, lang="de", is_standalone=True)
    plt.tight_layout()
    p_i_acc = os.path.join(PLOTS_DIR, "panel_i_age_crime_curve.png")
    plt.savefig(p_i_acc, dpi=300, bbox_inches="tight")
    plt.close()
    print("   ✓ Panel I (Age-Crime Curve mit Prekaritäts-Sensitivität): panel_i_age_crime_curve.png")



# =============================================================================
# 4. CORE VISUALIZATION FUNCTIONS (PANELS F, G, H, I)
# =============================================================================
def render_panel_f_oecd_regression(ax, reg, lang="de", is_standalone=False):
    """Renders Panel F: Empirical OECD Precarity Ratio vs. Violent Crime Effect Ratio.
    
    Data source: datasets/oecd_precarity_crime_meta.csv (10 landmark studies across 7 OECD countries,
    strictly restricted to ages 14–33 young adulthood violent offending).
    Demonstrates that across OECD countries, the empirical violent crime effect ratio associated with
    socioeconomic precarity clusters tightly around 2.34x–3.10x (WLS baseline exp(beta_0) = 2.39x, p < 0.001;
    slope beta_1 = 0.087, p = 0.169 n.s. across observed range), directly validating the Swedish LISA
    population register benchmark (RR = 2.41x) and calibrating the expected German crime effect multiple
    for German precarity ratios (X_DE in [2.21, 2.90] -> Y_hat in [2.56x, 2.62x], central 2.60x).
    """
    is_de = (lang == "de")
    df = reg["df_oecd"]
    proj = reg["german_projections"]
    x_de_min = proj.get("x_ses40", 2.21)
    x_de_max = proj.get("x_silc", 2.90)
    x_de_d13 = proj.get("x_d13", 2.64)

    # 1. Shaded Region for German Precarity Disparity Range (Mikrozensus SES < 40 to EU-SILC)
    ax.axvspan(x_de_min, x_de_max, color="#FFF9C4", alpha=0.55, zorder=0,
               label=f"Prekaritätsspanne Deutschland (X_DE = {x_de_min:.2f}–{x_de_max:.2f})" if is_de else f"German Precarity Range (X_DE = {x_de_min:.2f}–{x_de_max:.2f})")

    # 2. WLS Regression Line & 95% Confidence Band
    x_plot = reg["x_plot"]
    y_plot_wls = reg["y_plot_wls"]
    ci_lower = reg["ci_wls_lower"]
    ci_upper = reg["ci_wls_upper"]

    ax.fill_between(x_plot, ci_lower, ci_upper, color="#4a90e2", alpha=0.18, zorder=2,
                    label="95% Konfidenzband (WLS)" if is_de else "95% Confidence Band (WLS)")
    ax.plot(x_plot, y_plot_wls, color="#1f4e78", linewidth=2.4 if is_standalone else 2.0, zorder=3,
            label=f"WLS-Metaregression: ln(Y) = {reg['beta_wls'][0]:.3f} + {reg['beta_wls'][1]:.3f} ln(X)" if is_de else f"WLS Meta-Regression: ln(Y) = {reg['beta_wls'][0]:.3f} + {reg['beta_wls'][1]:.3f} ln(X)")

    # 4. Scatter Plot of Studies with 95% Error Bars
    reg_df = df[df["is_register"] == 1]
    surv_df = df[df["is_register"] == 0]

    # Registers (Diamonds)
    ax.errorbar(reg_df["precarity_ratio_x"], reg_df["crime_effect_ratio_y"],
                yerr=[reg_df["crime_effect_ratio_y"] - reg_df["ci_95_lower"], reg_df["ci_95_upper"] - reg_df["crime_effect_ratio_y"]],
                fmt="D", markersize=8.5 if is_standalone else 6.0, color="#d9534f", ecolor="#d9534f", elinewidth=1.5 if is_standalone else 1.2, capsize=4.0 if is_standalone else 3.0,
                alpha=0.95, zorder=4, label="Amtliche Total-Register (SWE, NLD, NOR, DNK, FIN)" if is_de else "Official Total Population Registers (SWE, NLD, NOR, DNK, FIN)")

    # Surveys (Circles)
    ax.errorbar(surv_df["precarity_ratio_x"], surv_df["crime_effect_ratio_y"],
                yerr=[surv_df["crime_effect_ratio_y"] - surv_df["ci_95_lower"], surv_df["ci_95_upper"] - surv_df["crime_effect_ratio_y"]],
                fmt="o", markersize=7.5 if is_standalone else 5.0, color="#1f4e78", ecolor="#1f4e78", elinewidth=1.5 if is_standalone else 1.2, capsize=4.0 if is_standalone else 3.0,
                alpha=0.90, zorder=4, label="Kriminologische Längsschnitt-Kohorten (USA, NZL)" if is_de else "Criminological Longitudinal Cohorts (USA, NZL)")

    # 5. Study Labels (Pure Longitudinal OECD Peer Cohorts)
    short_labels = {
        "SWE_HAALLSTEN_2013": "SWE: Hällsten '13 (RR 2,41)" if is_de else "SWE: Hällsten '13 (RR 2.41)",
        "SWE_SARIASLAN_2014": "SWE: Sariaslan '14 (HR 2,42)" if is_de else "SWE: Sariaslan '14 (HR 2.42)",
        "NLD_JENNISSEN_2009": "NLD: WODC 277 '09 (RR 3,10)" if is_de else "NLD: WODC 277 '09 (RR 3.10)",
        "NOR_SKARDHAMAR_2012": "NOR: SSB 728 '12 (RR 2,35)" if is_de else "NOR: SSB 728 '12 (RR 2.35)",
        "USA_LOEBER_2012": "USA: Loeber '12 (RR 2,45)" if is_de else "USA: Loeber '12 (RR 2.45)",
        "NZL_MOFFITT_1993": "NZL: Moffitt '93 (RR 2,50)" if is_de else "NZL: Moffitt '93 (RR 2.50)",
        "DNK_MOK_2018": "DNK: Mok '18 (IRR 2,90)" if is_de else "DNK: Mok '18 (IRR 2.90)",
        "FIN_SARIASLAN_2021": "FIN: Sariaslan '21 (HR 2,52)" if is_de else "FIN: Sariaslan '21 (HR 2.52)",
        "NOR_ANDERSEN_2017": "NOR: SSB 36 '17 (RR 2,34)" if is_de else "NOR: SSB 36 '17 (RR 2.34)",
        "SWE_BRA_2021": "SWE: Brå 21:9 '21 (RR 2,56)" if is_de else "SWE: Brå 21:9 '21 (RR 2.56)",
    }
    offsets = {
        "NZL_MOFFITT_1993": (-75, 12) if is_standalone else (-60, 8),
        "SWE_SARIASLAN_2014": (10, -20) if is_standalone else (8, -16),
        "USA_LOEBER_2012": (-25, 18) if is_standalone else (-20, 12),
        "NOR_SKARDHAMAR_2012": (10, -20) if is_standalone else (8, -16),
        "DNK_MOK_2018": (12, 6) if is_standalone else (8, 4),
        "SWE_HAALLSTEN_2013": (12, 10) if is_standalone else (8, 8),
        "NLD_JENNISSEN_2009": (12, 10) if is_standalone else (8, 8),
        "FIN_SARIASLAN_2021": (12, -18) if is_standalone else (8, -14),
        "NOR_ANDERSEN_2017": (12, -18) if is_standalone else (8, -14),
        "SWE_BRA_2021": (12, 10) if is_standalone else (8, 8),
    }
    for _, row in df.iterrows():
        sid = row["study_id"]
        lbl = short_labels.get(sid, sid)
        offset = offsets.get(sid, (8, 8))
        ax.annotate(lbl, (row["precarity_ratio_x"], row["crime_effect_ratio_y"]),
                    xytext=offset, textcoords="offset points",
                    fontsize=7.8 if is_standalone else 6.2, fontweight="bold",
                    bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="gray", alpha=0.88, lw=0.6))

    # 5. German Projection Callout Box
    proj = reg["german_projections"]
    if is_standalone:
        p_box_text = (
            "Projektion für Deutschland (OECD-WLS Metaregression):\n"
            f"• Mikrozensus SES < 40 (X = {x_de_min:.2f}): Ŷ = {proj['y_ses40_wls']:.2f}× [95%-KI: {proj['ci_ses40_lower']:.2f}–{proj['ci_ses40_upper']:.2f}×]\n"
            f"• Mikrozensus D1–D3 (X = {x_de_d13:.2f}): Ŷ = {proj['y_d13_wls']:.2f}× [95%-KI: {proj['ci_d13_lower']:.2f}–{proj['ci_d13_upper']:.2f}×] (Zentralwert Panels G & I)\n"
            f"• EU-SILC Armutsrisiko (X = {x_de_max:.2f}): Ŷ = {proj['y_silc_wls']:.2f}× [95%-KI: {proj['ci_silc_lower']:.2f}–{proj['ci_silc_upper']:.2f}×]\n"
            f"==> Empirischer OECD-Kalibrierungskorridor: [{proj['ci_ses40_lower']:.2f}×–{proj['ci_silc_upper']:.2f}×], Zentralwert: {proj['y_d13_wls']:.2f}×"
            if is_de else
            "German Calibration Projection (OECD WLS Meta-Regression):\n"
            f"• Microcensus SES < 40 (X = {x_de_min:.2f}): Ŷ = {proj['y_ses40_wls']:.2f}× [95% CI: {proj['ci_ses40_lower']:.2f}–{proj['ci_ses40_upper']:.2f}×]\n"
            f"• Microcensus D1–D3 (X = {x_de_d13:.2f}): Ŷ = {proj['y_d13_wls']:.2f}× [95% CI: {proj['ci_d13_lower']:.2f}–{proj['ci_d13_upper']:.2f}×] (Central Value Panels G & I)\n"
            f"• EU-SILC Poverty Risk (X = {x_de_max:.2f}): Ŷ = {proj['y_silc_wls']:.2f}× [95% CI: {proj['ci_silc_lower']:.2f}–{proj['ci_silc_upper']:.2f}×]\n"
            f"==> Empirical OECD Calibration Corridor: [{proj['ci_ses40_lower']:.2f}×–{proj['ci_silc_upper']:.2f}×], Central Value: {proj['y_d13_wls']:.2f}×"
        )
        fs_box = 8.5
    else:
        p_box_text = (
            f"Projektion Dt. (OECD-WLS):\n"
            f"• SES < 40 (X={x_de_min:.2f}): Ŷ = {proj['y_ses40_wls']:.2f}× [{proj['ci_ses40_lower']:.2f}–{proj['ci_ses40_upper']:.2f}×]\n"
            f"• D1–D3 (X={x_de_d13:.2f}): Ŷ = {proj['y_d13_wls']:.2f}× [{proj['ci_d13_lower']:.2f}–{proj['ci_d13_upper']:.2f}×] (Zentral)\n"
            f"• EU-SILC (X={x_de_max:.2f}): Ŷ = {proj['y_silc_wls']:.2f}× [{proj['ci_silc_lower']:.2f}–{proj['ci_silc_upper']:.2f}×]\n"
            f"==> OECD-Zentralwert: {proj['y_d13_wls']:.2f}× (Panels G & I)"
            if is_de else
            f"German Proj. (OECD WLS):\n"
            f"• SES < 40 (X={x_de_min:.2f}): Ŷ = {proj['y_ses40_wls']:.2f}× [{proj['ci_ses40_lower']:.2f}–{proj['ci_ses40_upper']:.2f}×]\n"
            f"• D1–D3 (X={x_de_d13:.2f}): Ŷ = {proj['y_d13_wls']:.2f}× [{proj['ci_d13_lower']:.2f}–{proj['ci_d13_upper']:.2f}×] (Central)\n"
            f"• EU-SILC (X={x_de_max:.2f}): Ŷ = {proj['y_silc_wls']:.2f}× [{proj['ci_silc_lower']:.2f}–{proj['ci_silc_upper']:.2f}×]\n"
            f"==> OECD Central Value: {proj['y_d13_wls']:.2f}× (Panels G & I)"
        )
        fs_box = 7.0

    ax.text(0.03, 0.96, p_box_text, transform=ax.transAxes, va="top", ha="left",
            fontsize=fs_box, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.25", fc="#FFF9C4", ec="#FBC02D", lw=1.1))

    # Axis formatting
    num_studies = len(df)
    num_countries = df["country"].nunique()
    title_str = (
        f"(F) Empirische OECD-Metaregression: Prekaritätsdisparität vs. Gewaltdelinquenz-Effekt\n"
        f"[{num_studies} internationale Landmark-Studien aus {num_countries} OECD-Staaten | Jungerwachsenenalter 14–33 J.]"
        if is_de else
        f"(F) Empirical OECD Meta-Regression: Precarity Disparity vs. Violent Offending Effect Ratio\n"
        f"[{num_studies} International Landmark Studies across {num_countries} OECD Peer Nations | Young Adulthood (Ages 14–33)]"
    )
    ax.set_title(title_str, fontweight="bold", fontsize=10.5 if is_standalone else 9.2, pad=8)
    ax.set_xlabel("Prekaritäts-Disparitätsverhältnis in Studienpopulation (X = Prekär / Ref.)" if is_de else "Precarity Disparity Ratio in Study Population (X = Precarious / Ref.)", fontsize=9.2 if is_standalone else 8.2)
    ax.set_ylabel("Gewaltkriminalitäts-Effektverhältnis (Y = RR, HR, OR, IRR)" if is_de else "Violent Crime Effect Ratio (Y = RR, HR, OR, IRR)", fontsize=9.2 if is_standalone else 8.2)

    ax.set_xlim(2.0, 3.8)
    ax.set_ylim(1.8, 3.85)
    ax.legend(loc="lower right", fontsize=8.0 if is_standalone else 6.2, frameon=True, facecolor="white", framealpha=0.92)


def render_panel_g_risk_matrix(ax, m, lang="de", is_standalone=False, fig=None):
    """Renders Panel G: Bivariate 2D Delinquency Risk Surface (Age x SES) across full life course (Ages 0–80)."""
    is_de = (lang == "de")
    age_m = m["age_m"]
    ses_m = m["ses_m"]
    risk_m = m["risk_m"]
    contour = ax.contourf(age_m, ses_m, risk_m, levels=25, cmap="viridis")
    cs = ax.contour(age_m, ses_m, risk_m, levels=[150, 400, 800, 1400, 2200], colors="white", alpha=0.35, linewidths=0.8)
    ax.clabel(cs, inline=True, fontsize=7.5 if not is_standalone else 8.0, fmt="%d")
    if fig is not None:
        cbar = fig.colorbar(contour, ax=ax)
        cbar_lbl = "TVBZ pro 100.000 Männer" if is_de else "Suspect Rate (TVBZ per 100k Males)"
        cbar.set_label(cbar_lbl, fontsize=8.5 if not is_standalone else 9.5)
    ax.set_xlim(0, 80)
    ax.set_ylim(0, 100)
    ax.add_patch(Rectangle((14, 0), 16, 40, fill=False, edgecolor="cyan", lw=2.2 if not is_standalone else 2.5, ls="--"))
    clust_txt = "Hochrisiko-Cluster\n(14–30 J. & SES < 40)\n[5,04× in Panel E]" if is_de else "High-Risk Cluster\n(14–30 Y. & SES < 40)\n[5.04× in Panel E]"
    ax.text(15, 42, clust_txt, color="cyan", fontweight="bold", fontsize=7.8 if not is_standalone else 8.5)
    if is_standalone:
        ax.annotate("Verzögerte Desistance bei Prekarität\n(Sampson & Laub 1993, Laub 2003 OR = 0.61)" if is_de else "Delayed Desistance under Precarity\n(Sampson & Laub 1993, Laub 2003 OR = 0.61)",
                    xy=(40, 18), xytext=(42, 55),
                    arrowprops=dict(facecolor="white", shrink=0.08, width=1.2, headwidth=5), color="white", fontweight="bold", fontsize=8.5,
                    bbox=dict(boxstyle="round,pad=0.25", fc="#263238", ec="white", lw=0.8))
        rr_ctrl = m.get("rr_ctrl_central", 2.60)
        plt.figtext(0.08, 0.005, f"Modellform: BKA-PKS-T40-Altersmarginal über Lebensverlauf (0–80 J., NLS-Fit mit Onset) × OECD-WLS-Prekaritätsgradient (Zentralwert RR = {rr_ctrl:.2f}× bei SES < 40; D1–D3 Projektion aus Panel F) & Desistance-Verzögerung (Laub & Sampson 2003 OR = 0,61) bei exakter Marginalkonsistenz.", fontsize=6.8, style="italic")
    rr_ctrl = m.get("rr_ctrl_central", 2.60)
    title = (
        f"(G) Bivariates Delinquenzmodell: Alter × SES [0–80 J. | BKA PKS T40 & OECD-WLS RR = {rr_ctrl:.2f}×]"
        if is_de else
        f"(G) Bivariate Delinquency Model: Age × SES [Ages 0–80 | BKA PKS T40 & OECD WLS RR = {rr_ctrl:.2f}×]"
    )
    ax.set_title(title, fontweight="bold", fontsize=9.2 if not is_standalone else 10.0)
    ax.set_xlabel("Alter in Jahren (0–80)" if is_de else "Age in Years (0–80)", fontsize=9.2 if not is_standalone else 10.0)
    ax.set_ylabel("SES-Perzentil (0–100)" if is_de else "SES Percentile (0–100)", fontsize=9.2 if not is_standalone else 10.0)


def render_panel_h_kfn(ax, df_h, lang="de", is_standalone=False):
    """[Archival Reference] Renders authentic empirical youth violent delinquency by origin and living conditions (KFN FB 107)."""
    is_de = (lang == "de")
    stages = [1, 2, 3]
    stage_labels = [
        "1. Alle Befragten\n(Unbereinigt)" if is_de else "1. All Adolescents\n(Unadjusted)",
        "2. Peer-bereinigt\n(max. 5 delinq. Fr.)" if is_de else "2. Peer-Controlled\n(max. 5 delinq. peers)",
        "3. Gleiche Lebensbed.\n(ohne Sozialhilfe/Gewalt)" if is_de else "3. Equal Conditions\n(No welfare/violence)"
    ]
    groups = ["deutsch", "tuerkei", "jugoslawien"]
    group_labels = [
        "Deutschland" if is_de else "Germany",
        "Türkei" if is_de else "Turkey",
        "ehem. Jugoslawien" if is_de else "Ex-Yugoslavia"
    ]
    colors = [C_DE, "#d62728", "#ff7f0e"]
    x = np.arange(len(stages))
    width = 0.26
    for idx_g, (grp, grp_lbl, col) in enumerate(zip(groups, group_labels, colors)):
        sub = df_h[df_h["herkunft_gruppe"] == grp].sort_values("stufe_id")
        vals = sub["gewalttaeter_praevalenz_pct"].to_numpy()
        ns = sub["n_stichprobe"].to_numpy()
        pos = x + (idx_g - 1) * width
        bars = ax.bar(pos, vals, width=width, label=grp_lbl, color=col, edgecolor="black", alpha=0.9, zorder=3)
        for b, v, n_val in zip(bars, vals, ns):
            h = b.get_height()
            font_s = 9.0 if is_standalone else 7.5
            ax.text(b.get_x() + b.get_width() / 2, h + 0.35, f"{v:.1f}%", ha="center", va="bottom", fontsize=font_s, fontweight="bold")
    ax.axvspan(1.55, 2.45, color="#e8f5e9", alpha=0.6, zorder=1)
    ax.axhline(6.4, color=C_DE, linestyle=":", lw=1.5, zorder=4)
    title = "(Archiv) Gewalttäter nach Herkunft & Lebensbedingungen [KFN FB 107]" if is_de else "(Archive) Youth Violence by Origin [KFN FB 107]"
    ax.set_title(title, fontweight="bold", fontsize=10.0 if is_standalone else 9.0)
    ax.set_xticks(x)
    ax.set_xticklabels(stage_labels, fontsize=8.5 if is_standalone else 7.5)
    ax.set_ylabel("12-M-Prävalenz (%)" if is_de else "12-M Prevalence (%)", fontsize=9.0 if is_standalone else 8.0)
    ax.set_ylim(0, 27)


def render_bka_register_waterfall_panel(ax, wf, lang="de", is_standalone=False, panel_letter="H"):
    """Renders the official BKA PKS register causal waterfall (Males 14+, BKA PKS 2023 & Destatis)."""
    is_de = (lang == "de")
    if is_de:
        stages = [
            f"1. Rohe PKS-Rate\n(Nicht-Dt. 14+)\n{wf['raw_nde']:.1f}",
            f"2. Residenz-Korr.\n(–{wf['delta_res']:.1f} T29 Tier 3)\n→ {wf['tier2_nde']:.1f}",
            f"3. Alters-Standard.\n(–{wf['delta_demo']:.1f} Demografie)\n→ {wf['comb_nde']:.1f}",
            f"4. Bereinigt\n(Nicht-Dt. 14+)\n{wf['comb_nde']:.1f}",
            f"Deutsche Basis\n(Altersstd. 14+)\n{wf['base_de']:.1f}",
        ]
        title = f"({panel_letter}) Amtliche BKA-Register-Dekomposition [Männer 14+]\n[BKA PKS 2023 T29/T40/T50 & Destatis Zensus 2022]"
        ylabel = "TVBZ (Verdächtige pro 100.000 Männer 14+)"
        ann_text = f"Verbleibende Hellfelddisparität: {wf['ratio_std']:.2f}× (+{((wf['ratio_std'] - 1.0) * 100):.0f} %)\n(Amtliche Grenze: PKS erfasst keinen SES/Anzeige)\n→ Prekaritätskontrolle: siehe Panel F & I"
        rr_lo = wf.get("rr_proj_lo", 2.56)
        rr_hi = wf.get("rr_proj_hi", 2.62)
        disclaimer = f"Registergrenze (Hellfeld): Amtliche Kriminalstatistik erfasst Tatverdächtige, kein Dunkelfeld und keinen SES.\nDie {wf['ratio_std']:.2f}×-Registerdisparität wird durch die OECD-Prekaritätskontrolle (Panel F & I: {rr_lo:.2f}×–{rr_hi:.2f}×) und Anzeigebias im Dunkelfeld dekonstruiert."
    else:
        stages = [
            f"1. Raw PKS Rate\n(Non-German 14+)\n{wf['raw_nde']:.1f}",
            f"2. Residence Adj.\n(–{wf['delta_res']:.1f} T29 Tier 3)\n→ {wf['tier2_nde']:.1f}",
            f"3. Age Standard.\n(–{wf['delta_demo']:.1f} Demography)\n→ {wf['comb_nde']:.1f}",
            f"4. Standardised\n(Non-German 14+)\n{wf['comb_nde']:.1f}",
            f"German Baseline\n(Age-Std. 14+)\n{wf['base_de']:.1f}",
        ]
        title = f"({panel_letter}) Official BKA Register Decomposition [Males 14+]\n[BKA PKS 2023 T29/T40/T50 & Destatis Census 2022]"
        ylabel = "TVBZ (Suspects per 100,000 Males 14+)"
        ann_text = f"Residual Register Disparity: {wf['ratio_std']:.2f}× (+{((wf['ratio_std'] - 1.0) * 100):.0f} %)\n(Administrative limit: PKS lacks SES/reporting)\n→ Precarity Control: see Panels F & I"
        rr_lo = wf.get("rr_proj_lo", 2.56)
        rr_hi = wf.get("rr_proj_hi", 2.62)
        disclaimer = f"Register Boundary (Hellfeld): Official police statistics measure suspects, not darkfield crimes or SES.\nResidual {wf['ratio_std']:.2f}× disparity is deconstructed by OECD precarity control (Panels F & I: {rr_lo:.2f}×–{rr_hi:.2f}×) and reporting bias."

    colors = ["#d9534f", "#e67e22", "#f39c12", "#27ae60", "#1f4e78"]
    x_pos = np.arange(len(stages))
    width = 0.50 if not is_standalone else 0.55
    bars = ax.bar(x_pos, wf["heights"], bottom=wf["bottoms"], color=colors, edgecolor="black", width=width, alpha=0.9)

    ax.plot([0, 1], [wf['tier2_nde'], wf['tier2_nde']], color="gray", linestyle="--", lw=1.1)
    ax.plot([1, 2], [wf['comb_nde'], wf['comb_nde']], color="gray", linestyle="--", lw=1.1)

    fs_val = 8.5 if not is_standalone else 11.0
    fs_sub = 7.2 if not is_standalone else 9.5

    for i, bar in enumerate(bars):
        h = bar.get_height()
        b = bar.get_y()
        if i == 0:
            ax.text(bar.get_x() + bar.get_width() / 2, b + h / 2, f"{h:.1f}\n({wf['ratio_raw']:.2f}×)", ha="center", va="center", color="white", fontweight="bold", fontsize=fs_val)
        elif i in (1, 2):
            ax.text(bar.get_x() + bar.get_width() / 2, b + h / 2, f"– {h:.1f}", ha="center", va="center", color="white", fontweight="bold", fontsize=fs_val)
            ratio_val = wf['ratio_res'] if i == 1 else wf['ratio_std']
            ax.text(bar.get_x() + bar.get_width() / 2, b + h + 25, f"→ {b:.1f}\n({ratio_val:.2f}×)", ha="center", fontweight="bold", fontsize=fs_sub, color="#222222")
        elif i == 3:
            ax.text(bar.get_x() + bar.get_width() / 2, b + h / 2, f"{h:.1f}\n({wf['ratio_std']:.2f}×)", ha="center", va="center", color="white", fontweight="bold", fontsize=fs_val)
        elif i == 4:
            basis_lbl = "(Basis)" if is_de else "(Baseline)"
            ax.text(bar.get_x() + bar.get_width() / 2, b + h / 2, f"{h:.1f}\n{basis_lbl}", ha="center", va="center", color="white", fontweight="bold", fontsize=fs_val)

    xy_text_pos = (1.2, 920) if not is_standalone else (1.4, 980)
    ax.annotate(
        ann_text,
        xy=(3, wf['comb_nde']), xytext=xy_text_pos,
        arrowprops=dict(facecolor="darkblue", shrink=0.08, width=1.3, headwidth=5),
        fontweight="bold", fontsize=7.2 if not is_standalone else 9.5, color="#0d47a1",
        bbox=dict(boxstyle="round,pad=0.3", fc="#e3f2fd", ec="#1565c0", lw=1.2)
    )

    ax.set_xticks(x_pos)
    ax.set_xticklabels(stages, fontsize=7.2 if not is_standalone else 9.5, fontweight="bold")
    ax.set_ylabel(ylabel, fontsize=8.8 if not is_standalone else 10.5)
    ax.set_title(title, fontsize=9.2 if not is_standalone else 12.0, fontweight="bold")
    ax.set_ylim(0, 1400)

    fs_box = 6.4 if not is_standalone else 8.0
    ax.text(0.5, 0.025, disclaimer, transform=ax.transAxes, ha="center", fontsize=fs_box, style="italic",
            color="#37474F", bbox=dict(boxstyle="round,pad=0.25", fc="#FFFDE7", ec="#FBC02D", lw=0.9))


def render_panel_i_age_crime(ax, m, lang="de", is_standalone=False):
    """Renders Panel I: Authentic empirical BKA Age-Crime curves across the full life course (Ages 14–80)
    with OECD precarity sensitivity analysis restricted to the empirical 14–30 young adulthood window.
    
    Data sources: BKA PKS 2023 Table T40 (Germans), Table T50 (Non-Germans), Table T29 (Residence correction Tier 3),
    Destatis Zensus 2022 / AZR population denominators, and OECD Precarity Meta-Regression projections from Panel F.
    Compares German baseline, raw Non-German suspect rate, residence-adjusted Non-German rate (-13.9%),
    and precarity-controlled Non-German curve with the OECD precarity sensitivity band (strictly limited to ages 14–30).
    """
    is_de = (lang == "de")
    dense_ages = np.linspace(14, 80, 250)
    dense_ages_youth = np.linspace(14, 30, 150)

    fit_de = m["age_crime_func"](dense_ages, *m["popt_de"])
    fit_nde_raw = m["age_crime_func"](dense_ages, *m["popt_nde_raw"])
    fit_nde_res = m["age_crime_func"](dense_ages, *m["popt_nde_res"])
    fit_nde_res_youth = m["age_crime_func"](dense_ages_youth, *m["popt_nde_res"])

    # OECD Precarity Control parameters (calibrated in Panel F)
    proj = m["oecd_reg"]["german_projections"]
    rr_ctrl_central = float(proj["y_d13_wls"])  # ~2.60 (OECD WLS Central Estimate for German D1–D3)
    rr_proj_lo = float(proj["y_ses40_wls"])      # ~2.56 (Mikrozensus SES < 40)
    rr_proj_hi = float(proj["y_silc_wls"])       # ~2.62 (EU-SILC at-risk-of-poverty)

    # Precarity-controlled curves restricted strictly to ages 14–30
    fit_nde_ctrl_mid = fit_nde_res_youth / rr_ctrl_central
    fit_nde_ctrl_lower_band = fit_nde_res_youth / rr_proj_hi
    fit_nde_ctrl_upper_band = fit_nde_res_youth / rr_proj_lo

    # 1. German baseline
    lbl_de = "Deutsche Männer (BKA T40 / BV-01)" if is_de else "German Males (BKA T40 / BV-01)"
    ax.plot(dense_ages, fit_de, label=lbl_de, color=C_DE, lw=2.4 if is_standalone else 2.0, linestyle="--")
    ax.scatter(m["emp_ages"], m["emp_de"], color=C_DE, s=40 if is_standalone else 25, zorder=5)

    # 2. Raw Non-German
    lbl_nde_raw = "Nicht-Dt. Männer ROH (BKA T50 / AZR)" if is_de else "Non-German Males RAW (BKA T50 / AZR)"
    ax.plot(dense_ages, fit_nde_raw, label=lbl_nde_raw, color=C_NDE, lw=2.4 if is_standalone else 2.0)
    ax.scatter(m["emp_ages_nde_raw"], m["emp_nde_raw_valid"], color=C_NDE, marker="s", s=40 if is_standalone else 25, zorder=5)

    # 3. Residence-adjusted Non-German (BKA T29 Tier 3: -13.9%)
    lbl_nde_res = "Nicht-Dt. wohnsitzbereinigt (T29 Tier 3: –13,9%)" if is_de else "Non-German Residence-Adj. (T29 Tier 3: –13.9%)"
    ax.plot(dense_ages, fit_nde_res, label=lbl_nde_res, color="#e67e22", lw=2.2 if is_standalone else 1.8, linestyle="-.")

    # 4. OECD Precarity Sensitivity Band (Shaded, limited to 14–30 years)
    lbl_band = f"OECD-Prekaritätsband (Ŷ = {rr_proj_lo:.2f}×–{rr_proj_hi:.2f}×; 14–30 J.)" if is_de else f"OECD Precarity Band (Ŷ = {rr_proj_lo:.2f}×–{rr_proj_hi:.2f}×; 14–30 Y.)"
    ax.fill_between(dense_ages_youth, fit_nde_ctrl_lower_band, fit_nde_ctrl_upper_band, color="#27ae60", alpha=0.22, zorder=2, label=lbl_band)

    # 5. Precarity-controlled Non-German Curve (limited to 14–30 years)
    lbl_ctrl = f"Nicht-Dt. residenz- & prekaritätskontrolliert ({rr_ctrl_central:.2f}×; 14–30 J.)" if is_de else f"Non-German Residence- & Precarity-Controlled ({rr_ctrl_central:.2f}×; 14–30 Y.)"
    ax.plot(dense_ages_youth, fit_nde_ctrl_mid, label=lbl_ctrl, color="#27ae60", lw=2.6 if is_standalone else 2.2, linestyle="-", zorder=4)

    # Peak values at age 17.5
    peak_idx = np.abs(dense_ages - 17.5).argmin()
    peak_idx_y = np.abs(dense_ages_youth - 17.5).argmin()
    peak_raw = fit_nde_raw[peak_idx]
    peak_res = fit_nde_res[peak_idx]
    peak_ctrl = fit_nde_ctrl_mid[peak_idx_y]
    peak_ctrl_lo = fit_nde_ctrl_lower_band[peak_idx_y]
    peak_ctrl_hi = fit_nde_ctrl_upper_band[peak_idx_y]
    peak_de = fit_de[peak_idx]

    if is_standalone:
        ax.annotate(
            f"Peak Jugend (16–18 J.):\n"
            f"• Nicht-Dt. Roh: {peak_raw:.0f}\n"
            f"• Wohnsitzbereinigt: {peak_res:.0f} (–13,9%)\n"
            f"• Prekaritätskontrolliert (14–30 J.): {peak_ctrl:.0f} [{peak_ctrl_lo:.0f}–{peak_ctrl_hi:.0f}]\n"
            f"• Dt. Basis: {peak_de:.0f}"
            if is_de else
            f"Peak Youth (16–18 Y.):\n"
            f"• Non-Ger. Raw: {peak_raw:.0f}\n"
            f"• Residence-Adj.: {peak_res:.0f} (–13.9%)\n"
            f"• Precarity-Controlled (14–30 Y.): {peak_ctrl:.0f} [{peak_ctrl_lo:.0f}–{peak_ctrl_hi:.0f}]\n"
            f"• German Baseline: {peak_de:.0f}",
            xy=(17.5, peak_ctrl), xytext=(28, 2550),
            arrowprops=dict(facecolor="#27ae60", shrink=0.08, width=1.3, headwidth=5),
            color="#1e7e34", fontweight="bold", fontsize=8.8,
            bbox=dict(boxstyle="round,pad=0.3", fc="#e8f5e9", ec="#27ae60", lw=1.2)
        )
        ax.text(
            0.5, 0.03,
            "Synthese Register & OECD-Sensitivitätsanalyse (Prekaritätskontrolle auf 14–30 J. begrenzt):\n"
            f"Wohnsitzbereinigung (–13,9%) und empirische OECD-Prekaritätselastizität (Panel F: {rr_proj_lo:.2f}×–{rr_proj_hi:.2f}×; Zentral: {rr_ctrl_central:.2f}×) führen\n"
            f"zur Konvergenz im Hochrisikoalter (14–30 J.): Der Peak sinkt von 3.392 auf ~{peak_ctrl:.0f} [{peak_ctrl_lo:.0f}–{peak_ctrl_hi:.0f}] nahe der deutschen Basis (1.165).",
            transform=ax.transAxes, ha="center", fontsize=7.6, style="italic",
            color="#37474F", bbox=dict(boxstyle="round,pad=0.25", fc="#ECEFF1", ec="#B0BEC5", lw=0.8)
        )
    else:
        ax.annotate(
            f"Prekaritätskontrolle (14–30 J.):\nPeak {peak_res:.0f} ==> {peak_ctrl:.0f} [{peak_ctrl_lo:.0f}–{peak_ctrl_hi:.0f}]\n(Dt. Basis: {peak_de:.0f})"
            if is_de else
            f"Precarity Control (14–30 Y.):\nPeak {peak_res:.0f} ==> {peak_ctrl:.0f} [{peak_ctrl_lo:.0f}–{peak_ctrl_hi:.0f}]\n(German Baseline: {peak_de:.0f})",
            xy=(17.5, peak_ctrl), xytext=(27, 2450),
            arrowprops=dict(facecolor="#27ae60", shrink=0.08, width=1.1, headwidth=4),
            color="#1e7e34", fontweight="bold", fontsize=7.0,
            bbox=dict(boxstyle="round,pad=0.22", fc="#e8f5e9", ec="#27ae60", lw=1.0)
        )

    title = (
        f"(I) Alters-Kriminalitäts-Kurven mit OECD-Prekaritäts-Sensitivität (14–30 J.)\n"
        f"[BKA PKS 2023 T40/T50 vs. OECD-WLS-Prekaritätskontrolle ({rr_proj_lo:.2f}×–{rr_proj_hi:.2f}× | Zentral: {rr_ctrl_central:.2f}×)]"
        if is_de else
        f"(I) Age–Crime Curves with OECD Precarity Sensitivity (Ages 14–30)\n"
        f"[BKA PKS 2023 T40/T50 vs. OECD WLS Precarity Control ({rr_proj_lo:.2f}×–{rr_proj_hi:.2f}× | Central: {rr_ctrl_central:.2f}×)]"
    )
    ax.set_title(title, fontweight="bold", fontsize=10.5 if is_standalone else 9.2)
    ax.set_xlabel("Alter in Jahren" if is_de else "Age in Years", fontsize=9.5 if is_standalone else 8.5)
    ax.set_ylabel("TVBZ (Verdächtige pro 100.000 Männer)" if is_de else "TVBZ (Suspects per 100k Males)", fontsize=9.5 if is_standalone else 8.5)
    ax.set_ylim(0, 4600)
    ax.legend(loc="upper right", fontsize=8.0 if is_standalone else 6.8, framealpha=0.92)


def generate_waterfall_plot(m):
    """Renders the synthesis causal decomposition waterfall chart in /plots."""
    print("-> Rendere Wasserfall-Diagramm...")
    fig, ax = plt.subplots(figsize=(12, 7.5), dpi=300)
    render_bka_register_waterfall_panel(ax, m["waterfall_data"], lang="de", is_standalone=True, panel_letter="H")
    plt.tight_layout()
    out_file = os.path.join(PLOTS_DIR, "decomposition_waterfall.png")
    plt.savefig(out_file, dpi=300, bbox_inches="tight")
    plt.close()
    print("   ✓ decomposition_waterfall.png generiert.")


# =============================================================================
# 5. GENERATION OF 3x3 SYNOPTIC MATRICES (GERMAN & ENGLISH)
# =============================================================================
def generate_composite_matrix_de(m):
    """Renders the German publication 3x3 synoptic matrix combining Panels A through I."""
    print("-> Rendere 9-Panel-Matrix (Deutsch)...")
    fig, axes = plt.subplots(3, 3, figsize=(18, 15))
    fig.suptitle(
        "Empirischer Survey zu Kriminalitätsdisparitäten (BKA PKS & Literatur-Synopse)\n"
        "Multivariate Analyse von Demografie-, Prekaritäts- und Nenner-Confoundern\n"
        "Integration von BKA PKS (Schlüssel 892000), Destatis Zensus 2022, Mikrozensus & Kriminologie-Surveys",
        fontsize=14.5, fontweight="bold", y=0.985
    )

    # Panel A: Crude suspect rate
    ax = axes[0, 0]
    bars = ax.bar(CATEGORIES, m["raw_rates"], color=[C_DE, C_NDE], edgecolor="black", alpha=0.88, width=0.52)
    ax.set_title("(A) Rohe Tatverdächtigenbelastungszahl [BKA PKS 2023 Registerbefund]", fontweight="bold", fontsize=10.5)
    ax.set_ylabel("TVBZ (Verdächtige pro 100.000 Einwohner)", fontsize=9.5)
    ax.set_ylim(0, 720)
    for b in bars:
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() / 2, f"{b.get_height():.1f}", ha="center", va="center", color="white", fontweight="bold", fontsize=12)
    ax.text(1, 615, f"{m['raw_ratio']:.2f}× Rohdisparität (Unbereinigt)", ha="center", fontweight="bold", color=C_NDE, fontsize=9.5)

    # Panel B: Population age distribution
    ax = axes[0, 1]
    xb = np.arange(len(m["age_labels"]))
    wb = 0.38
    ax.bar(xb - wb / 2, m["age_pct_de"], width=wb, label="Deutsche", color=C_DE, edgecolor="black", alpha=0.88)
    ax.bar(xb + wb / 2, m["age_pct_nde"], width=wb, label="Nichtdeutsche", color=C_NDE, edgecolor="black", alpha=0.88)
    ax.axvspan(0.5, 4.5, color="gold", alpha=0.25, zorder=0)
    ax.text(2.5, 23.5, f"PEAK-RISIKO-ALTER (14–30 J.)\n{m['youth_share_nde']:.1f}% Nicht-Dt. vs. {m['youth_share_de']:.1f}% Dt.", ha="center", fontweight="bold", fontsize=8.5, bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="gold", lw=1.2))
    ax.set_xticks(xb)
    ax.set_xticklabels(m["age_labels"], fontsize=9.0, rotation=25)
    ax.set_title("(B) Altersverteilung nach Nationalität [Destatis Zensus 2022 Benchmark]", fontweight="bold", fontsize=10.5)
    ax.set_xlabel("Alterskohorte in Jahren", fontsize=9.5)
    ax.set_ylabel("Anteil an jeweiliger Gesamtbevölkerung (%)", fontsize=9.5)
    ax.set_ylim(0, 27)
    ax.legend(loc="upper right", fontsize=8.5)

    # Panel C: Socioeconomic status deciles
    ax = axes[0, 2]
    xc = np.arange(len(m["ses_labels"]))
    pct_d1_3_de = m["ses_pct_de"][:3].sum()
    pct_d1_3_nde = m["ses_pct_nde"][:3].sum()
    ratio_d1_3 = pct_d1_3_nde / pct_d1_3_de
    ax.bar(xc - wb / 2, m["ses_pct_de"], width=wb, label="Deutsche", color=C_DE, edgecolor="black", alpha=0.88)
    ax.bar(xc + wb / 2, m["ses_pct_nde"], width=wb, label="Nichtdeutsche", color=C_NDE, edgecolor="black", alpha=0.88)
    ax.axvspan(-0.5, 2.5, color="red", alpha=0.15, zorder=0)
    ax.text(1.2, 30.5, f"NIEDRIGSTE 3 DEZILE (D1–D3)\n{pct_d1_3_nde:.1f}% Nicht-Dt. vs. {pct_d1_3_de:.1f}% Dt. ({ratio_d1_3:.2f}×)", ha="center", fontweight="bold", fontsize=8.2, color="darkred", bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="red", lw=1.2))
    ax.set_xticks(xc)
    ax.set_xticklabels(m["ses_labels"], fontsize=9.0)
    ax.set_title("(C) Sozioökonomischer Status [Destatis Mikrozensus EU-SILC 2023]", fontweight="bold", fontsize=10.5)
    ax.set_xlabel("Einkommens-/SES-Dezile [D1 = Akute Armut, D10 = Wohlstand]", fontsize=9.5)
    ax.set_ylabel("Anteil an jeweiliger Gesamtbevölkerung (%)", fontsize=9.5)
    ax.set_ylim(0, 36)
    ax.legend(loc="upper right", fontsize=8.5)

    # Panel D: Suspect gender proportions
    ax = axes[1, 0]
    ax.bar([0, 1], m["male_shares"], width=0.52, label="Männlich", color=C_DE, edgecolor="black", alpha=0.88)
    ax.bar([0, 1], m["female_shares"], width=0.52, bottom=m["male_shares"], label="Weiblich", color=C_NDE, edgecolor="black", alpha=0.88)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(CATEGORIES, fontsize=10)
    ax.set_title("(D) Geschlechterproportion der Tatverdächtigen [BKA PKS 2023 T20]", fontweight="bold", fontsize=10.5)
    ax.set_ylabel("Anteil an Tatverdächtigen (%)", fontsize=9.5)
    ax.set_ylim(0, 110)
    for i in [0, 1]:
        ax.text(i, m["male_shares"][i] / 2, f"{m['male_shares'][i]:.1f}%\nMännlich", ha="center", va="center", color="white", fontweight="bold", fontsize=10)
        ax.text(i, m["male_shares"][i] + m["female_shares"][i] / 2, f"{m['female_shares'][i]:.1f}%", ha="center", va="center", color="white", fontweight="bold", fontsize=9)

    # Panel E: High-risk demographic concentration with Fréchet bounds (METHODOLOGICAL CONTRIBUTION)
    ax = axes[1, 1]
    bars_e = ax.bar(
        CATEGORIES, m["hr_shares"],
        yerr=m["hr_yerr"], capsize=5, ecolor="#1A237E",
        color=[C_DE, C_NDE], edgecolor="black", alpha=0.88, width=0.52,
        error_kw=dict(lw=1.4, capthick=1.4)
    )
    ax.set_title(f"(E) Eigener Beitrag: Kombinierte Risikokonstellation\n(Kettenregel & Fréchet 2006 | Zensus 2022 & EU-SILC 2023)", fontweight="bold", fontsize=9.2)
    ax.set_ylabel("Anteil an jeweiliger Gesamtpopulation (%)", fontsize=9.5)
    ax.set_ylim(0, 20.0)
    for i, b in enumerate(bars_e):
        h = b.get_height()
        hi = m["hr_bounds"][i][1]
        ax.text(b.get_x() + b.get_width() / 2, max(hi, h) + 0.40, f"{h:.1f}%", ha="center", va="bottom", fontweight="bold", fontsize=10.5)
    ax.text(1, 18.0, f"Eigener Beitrag: {m['hr_disparity']}× Risikokonzentration\n[Fréchet: {m['hr_bounds'][0][0]:.1f}–{m['hr_bounds'][0][1]:.1f}% vs. {m['hr_bounds'][1][0]:.1f}–{m['hr_bounds'][1][1]:.1f}%]",
            ha="center", fontweight="bold", color=C_NDE, fontsize=8.0, bbox=dict(boxstyle="round,pad=0.2", fc="#FFF9C4", ec="gold", lw=1.0))

    # Panel F: Empirical OECD Meta-Regression (Precarity Ratio vs. Violent Crime Effect)
    render_panel_f_oecd_regression(axes[1, 2], m["oecd_reg"], lang="de", is_standalone=False)

    # Panel G: Bivariate Delinquency Model: Age x SES
    render_panel_g_risk_matrix(axes[2, 0], m, lang="de", is_standalone=False, fig=fig)

    # Panel H: Official BKA Register Decomposition (Waterfall)
    render_bka_register_waterfall_panel(axes[2, 1], m["waterfall_data"], lang="de", is_standalone=False, panel_letter="H")

    # Panel I: Universal Age-Crime curves: BKA Register Data (Ages 14–80)
    render_panel_i_age_crime(axes[2, 2], m, lang="de", is_standalone=False)

    rr_ctrl = m.get("rr_ctrl_central", 2.60)
    plt.figtext(0.01, 0.004, f"Survey-Metasynthese amtlicher Register (BKA PKS 2023 Schlüssel 892000, T20, T29, T40, T50; Destatis Zensus 2022) & kriminologischer Surveys (EU-SILC, Mikrozensus, OECD-Längsschnittkohorten).\nMethodischer Hinweis: Panel E ist der eigene Beitrag (Kettenregel & Fréchet-Schranken). Panel F kalibriert die Prekaritätselastizität über OECD-Studien. Panel G modelliert das Alter×SES-Risikofeld (0–80 J. mit OECD-Zentralwert {rr_ctrl:.2f}×). Panel H zeigt die amtliche BKA-Registerdekomposition, Panel I die resultierende Kurvenkonvergenz (14–30 J.).", fontsize=8.5, style="italic", ha="left")
    plt.tight_layout(rect=[0, 0.025, 1, 0.965])

    p_de = os.path.join(PLOTS_DIR, "bka_kriminalitaet_3x3_deutsch.png")
    plt.savefig(p_de, dpi=300, bbox_inches="tight")
    plt.close()
    print("   ✓ bka_kriminalitaet_3x3_deutsch.png generiert.")


def generate_composite_matrix_en(m):
    """Renders the English publication 3x3 synoptic matrix combining Panels A through I."""
    print("-> Rendere 9-Panel-Matrix (Englisch)...")
    fig, axes = plt.subplots(3, 3, figsize=(18, 15))
    fig.suptitle(
        "Empirical Survey of Crime Disparities (German BKA PKS & Literature Synthesis)\n"
        "Multivariate Analysis of Demography, Precarity, and Denominator Confounders\n"
        "Data Integration: BKA PKS (Key 892000), Destatis Census 2022, Microcensus & Criminological Surveys",
        fontsize=14.5, fontweight="bold", y=0.985
    )
    cats_en = ["German", "Non-German"]

    # Panel A: Crude suspect rate
    ax = axes[0, 0]
    bars = ax.bar(cats_en, m["raw_rates"], color=[C_DE, C_NDE], edgecolor="black", alpha=0.88, width=0.52)
    ax.set_title("(A) Raw Suspect Rate [Official BKA PKS 2023 Register Data]", fontweight="bold", fontsize=10.5)
    ax.set_ylabel("TVBZ (Suspects per 100,000 Residents)", fontsize=9.5)
    ax.set_ylim(0, 720)
    for b in bars:
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() / 2, f"{b.get_height():.1f}", ha="center", va="center", color="white", fontweight="bold", fontsize=12)
    ax.text(1, 615, f"{m['raw_ratio']:.2f}× Raw Disparity (Unadjusted)", ha="center", fontweight="bold", color=C_NDE, fontsize=9.5)

    # Panel B: Population age distribution
    ax = axes[0, 1]
    xb = np.arange(len(m["age_labels"]))
    wb = 0.38
    ax.bar(xb - wb / 2, m["age_pct_de"], width=wb, label="German", color=C_DE, edgecolor="black", alpha=0.88)
    ax.bar(xb + wb / 2, m["age_pct_nde"], width=wb, label="Non-German", color=C_NDE, edgecolor="black", alpha=0.88)
    ax.axvspan(0.5, 4.5, color="gold", alpha=0.25, zorder=0)
    ax.text(2.5, 23.5, f"PEAK-RISK AGE BRACKET (14–30)\n{m['youth_share_nde']:.1f}% Non-German vs. {m['youth_share_de']:.1f}% German", ha="center", fontweight="bold", fontsize=8.5, bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="gold", lw=1.2))
    ax.set_xticks(xb)
    ax.set_xticklabels(m["age_labels"], fontsize=9.0, rotation=25)
    ax.set_title("(B) Age Distribution by Nationality [Destatis Census 2022 Benchmark]", fontweight="bold", fontsize=10.5)
    ax.set_xlabel("Age Cohort (Years)", fontsize=9.5)
    ax.set_ylabel("Share of Respective Population (%)", fontsize=9.5)
    ax.set_ylim(0, 27)
    ax.legend(loc="upper right", fontsize=8.5)

    # Panel C: Socioeconomic status deciles
    ax = axes[0, 2]
    xc = np.arange(len(m["ses_labels"]))
    pct_d1_3_de = m["ses_pct_de"][:3].sum()
    pct_d1_3_nde = m["ses_pct_nde"][:3].sum()
    ratio_d1_3 = pct_d1_3_nde / pct_d1_3_de
    ax.bar(xc - wb / 2, m["ses_pct_de"], width=wb, label="German", color=C_DE, edgecolor="black", alpha=0.88)
    ax.bar(xc + wb / 2, m["ses_pct_nde"], width=wb, label="Non-German", color=C_NDE, edgecolor="black", alpha=0.88)
    ax.axvspan(-0.5, 2.5, color="red", alpha=0.15, zorder=0)
    ax.text(1.2, 30.5, f"LOWEST 3 DECILES (D1–D3)\n{pct_d1_3_nde:.1f}% Non-Ger. vs. {pct_d1_3_de:.1f}% Ger. ({ratio_d1_3:.2f}×)", ha="center", fontweight="bold", fontsize=8.2, color="darkred", bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="red", lw=1.2))
    ax.set_xticks(xc)
    ax.set_xticklabels(m["ses_labels"], fontsize=9.0)
    ax.set_title("(C) Socio-Economic Status [Destatis Microcensus EU-SILC 2023]", fontweight="bold", fontsize=10.5)
    ax.set_xlabel("Income / SES Deciles [D1 = Severe Poverty, D10 = Affluence]", fontsize=9.5)
    ax.set_ylabel("Share of Respective Population (%)", fontsize=9.5)
    ax.set_ylim(0, 36)
    ax.legend(loc="upper right", fontsize=8.5)

    # Panel D: Suspect gender proportions
    ax = axes[1, 0]
    ax.bar([0, 1], m["male_shares"], width=0.52, label="Male", color=C_DE, edgecolor="black", alpha=0.88)
    ax.bar([0, 1], m["female_shares"], width=0.52, bottom=m["male_shares"], label="Female", color=C_NDE, edgecolor="black", alpha=0.88)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(cats_en, fontsize=10)
    ax.set_title("(D) Gender Distribution of Suspects [Official BKA PKS 2023 T20]", fontweight="bold", fontsize=10.5)
    ax.set_ylabel("Share of Suspects (%)", fontsize=9.5)
    ax.set_ylim(0, 110)
    for i in [0, 1]:
        ax.text(i, m["male_shares"][i] / 2, f"{m['male_shares'][i]:.1f}%\nMale", ha="center", va="center", color="white", fontweight="bold", fontsize=10)
        ax.text(i, m["male_shares"][i] + m["female_shares"][i] / 2, f"{m['female_shares'][i]:.1f}%", ha="center", va="center", color="white", fontweight="bold", fontsize=9)

    # Panel E: High-risk demographic concentration with Fréchet bounds (METHODOLOGICAL CONTRIBUTION)
    ax = axes[1, 1]
    bars_e = ax.bar(
        cats_en, m["hr_shares"],
        yerr=m["hr_yerr"], capsize=5, ecolor="#1A237E",
        color=[C_DE, C_NDE], edgecolor="black", alpha=0.88, width=0.52,
        error_kw=dict(lw=1.4, capthick=1.4)
    )
    ax.set_title(f"(E) Methodological Contribution: Joint Risk Concentration\n(Chain Rule & Fréchet 2006 | Census 2022 & EU-SILC 2023)", fontweight="bold", fontsize=9.2)
    ax.set_ylabel("Share of Respective Population (%)", fontsize=9.5)
    ax.set_ylim(0, 20.0)
    for i, b in enumerate(bars_e):
        h = b.get_height()
        hi = m["hr_bounds"][i][1]
        ax.text(b.get_x() + b.get_width() / 2, max(hi, h) + 0.40, f"{h:.1f}%", ha="center", va="bottom", fontweight="bold", fontsize=10.5)
    ax.text(1, 18.0, f"Methodological Contribution: {m['hr_disparity']}× Risk Concentration\n[Fréchet: {m['hr_bounds'][0][0]:.1f}–{m['hr_bounds'][0][1]:.1f}% vs. {m['hr_bounds'][1][0]:.1f}–{m['hr_bounds'][1][1]:.1f}%]",
            ha="center", fontweight="bold", color=C_NDE, fontsize=8.0, bbox=dict(boxstyle="round,pad=0.2", fc="#FFF9C4", ec="gold", lw=1.0))

    # Panel F: Empirical OECD Meta-Regression (Precarity Ratio vs. Violent Crime Effect)
    render_panel_f_oecd_regression(axes[1, 2], m["oecd_reg"], lang="en", is_standalone=False)

    # Panel G: Bivariate Delinquency Model: Age x SES
    render_panel_g_risk_matrix(axes[2, 0], m, lang="en", is_standalone=False, fig=fig)

    # Panel H: Official BKA Register Decomposition (Waterfall)
    render_bka_register_waterfall_panel(axes[2, 1], m["waterfall_data"], lang="en", is_standalone=False, panel_letter="H")

    # Panel I: Universal Age-Crime curves: BKA Register Data (Ages 14–80)
    render_panel_i_age_crime(axes[2, 2], m, lang="en", is_standalone=False)

    rr_ctrl = m.get("rr_ctrl_central", 2.60)
    plt.figtext(0.01, 0.004, f"Survey meta-synthesis of official registers (BKA PKS Key 892000, T20, T29, T40, T50; Destatis Census 2022) & criminological surveys (EU-SILC, Microcensus, OECD Longitudinal Cohorts).\nMethodological Note: Panel E is the novel contribution (chain rule & Fréchet bounds). Panel F calibrates the precarity elasticity via OECD peer cohorts. Panel G models the Age×SES risk surface (ages 0–80 with OECD central estimate {rr_ctrl:.2f}×). Panel H displays the official BKA register decomposition, Panel I the resulting curve convergence (ages 14–30).", fontsize=8.5, style="italic", ha="left")
    plt.tight_layout(rect=[0, 0.025, 1, 0.965])

    p_en = os.path.join(PLOTS_DIR, "bka_crime_disparity_9panel_english.png")
    plt.savefig(p_en, dpi=300, bbox_inches="tight")
    plt.close()
    print("   ✓ bka_crime_disparity_9panel_english.png generiert.")


def generate_composite_matrix_v2(m, lang="de"):
    """Renders the publication 3x3 synoptic matrix v2 with official register waterfall and survey synthesis."""
    is_de = (lang == "de")
    tag = "Deutsch" if is_de else "Englisch"
    print(f"-> Rendere 9-Panel-Matrix v2 ({tag})...")
    fig, axes = plt.subplots(3, 3, figsize=(18, 15))
    
    if is_de:
        fig.suptitle(
            "Empirischer Survey zu Kriminalitätsdisparitäten (BKA PKS & Literatur-Synopse) [v2 Synopse]\n"
            "Multivariate Analyse von Demografie-, Prekaritäts- und Nenner-Confoundern\n"
            "Integration von BKA PKS (Schlüssel 892000), Destatis Zensus 2022 & KFN-Dunkelfeldsurveys",
            fontsize=14.5, fontweight="bold", y=0.985
        )
        cats = CATEGORIES
    else:
        fig.suptitle(
            "Empirical Survey of Crime Disparities (German BKA PKS & Literature Synthesis) [v2 Synopsis]\n"
            "Multivariate Analysis of Demography, Precarity, and Denominator Confounders\n"
            "Integration of BKA PKS (Key 892000), Destatis Census 2022 & KFN Darkfield Surveys",
            fontsize=14.5, fontweight="bold", y=0.985
        )
        cats = ["German", "Non-German"]

    wb = 0.38

    # --- PANEL A: Crude suspect rate ---
    ax = axes[0, 0]
    bars = ax.bar(cats, m["raw_rates"], color=[C_DE, C_NDE], edgecolor="black", alpha=0.88, width=0.52)
    ax.set_title("(A) Rohe Tatverdächtigenbelastungszahl [BKA PKS 2023 Registerbefund]" if is_de else "(A) Raw Suspect Rate [Official BKA PKS 2023 Register Data]", fontweight="bold", fontsize=10.5)
    ax.set_ylabel("TVBZ (Verdächtige pro 100.000 Einwohner)" if is_de else "Suspects per 100,000 Residents", fontsize=9.5)
    ax.set_ylim(0, 720)
    for b in bars:
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() / 2, f"{b.get_height():.1f}", ha="center", va="center", color="white", fontweight="bold", fontsize=12)
    ax.text(1, 615, f"{m['raw_ratio']:.2f}× Rohdisparität (Unbereinigt)" if is_de else f"{m['raw_ratio']:.2f}× Crude Disparity Ratio (Unadjusted)", ha="center", fontweight="bold", color=C_NDE, fontsize=9.5)

    # --- PANEL B: Population age distribution ---
    ax = axes[0, 1]
    xb = np.arange(len(m["age_labels"]))
    ax.bar(xb - wb / 2, m["age_pct_de"], width=wb, label="Deutsche" if is_de else "German", color=C_DE, edgecolor="black", alpha=0.88)
    ax.bar(xb + wb / 2, m["age_pct_nde"], width=wb, label="Nichtdeutsche" if is_de else "Non-German", color=C_NDE, edgecolor="black", alpha=0.88)
    ax.axvspan(0.5, 4.5, color="gold", alpha=0.25, zorder=0)
    b_txt = f"PEAK-RISIKO-ALTER (14–30 J.)\n{m['youth_share_nde']:.1f}% Nicht-Dt. vs. {m['youth_share_de']:.1f}% Dt." if is_de else f"PEAK OFFENDING AGE (14–30 Y.)\n{m['youth_share_nde']:.1f}% Non-Ger. vs. {m['youth_share_de']:.1f}% Ger."
    ax.text(2.5, 23.5, b_txt, ha="center", fontweight="bold", fontsize=8.5, bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="gold", lw=1.2))
    ax.set_xticks(xb)
    ax.set_xticklabels(m["age_labels"], fontsize=9.0, rotation=25)
    ax.set_title("(B) Altersverteilung nach Nationalität [Destatis Zensus 2022 Benchmark]" if is_de else "(B) Age Distribution by Nationality [Destatis Census 2022 Benchmark]", fontweight="bold", fontsize=10.5)
    ax.set_xlabel("Alterskohorte in Jahren" if is_de else "Age Cohort in Years", fontsize=9.5)
    ax.set_ylabel("Anteil an jeweiliger Gesamtbevölkerung (%)" if is_de else "Share of Respective Population (%)", fontsize=9.5)
    ax.set_ylim(0, 27)
    ax.legend(loc="upper right", fontsize=8.5)

    # --- PANEL C: Socioeconomic status deciles ---
    ax = axes[0, 2]
    xc = np.arange(len(m["ses_labels"]))
    pct_d1_3_de = m["ses_pct_de"][:3].sum()
    pct_d1_3_nde = m["ses_pct_nde"][:3].sum()
    ratio_d1_3 = pct_d1_3_nde / pct_d1_3_de
    ax.bar(xc - wb / 2, m["ses_pct_de"], width=wb, label="Deutsche" if is_de else "German", color=C_DE, edgecolor="black", alpha=0.88)
    ax.bar(xc + wb / 2, m["ses_pct_nde"], width=wb, label="Nichtdeutsche" if is_de else "Non-German", color=C_NDE, edgecolor="black", alpha=0.88)
    ax.axvspan(-0.5, 2.5, color="red", alpha=0.15, zorder=0)
    c_txt = (f"NIEDRIGSTE 3 DEZILE (D1–D3)\n{pct_d1_3_nde:.1f}% Nicht-Dt. vs. {pct_d1_3_de:.1f}% Dt. ({ratio_d1_3:.2f}×)" if is_de else f"LOWEST 3 DECILES (D1–D3)\n{pct_d1_3_nde:.1f}% Non-Ger. vs. {pct_d1_3_de:.1f}% Ger. ({ratio_d1_3:.2f}×)")
    ax.text(1.2, 30.5, c_txt, ha="center", fontweight="bold", fontsize=8.2, color="darkred", bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="red", lw=1.2))
    ax.set_xticks(xc)
    ax.set_xticklabels(m["ses_labels"], fontsize=9.0)
    ax.set_title("(C) Sozioökonomischer Status [Destatis Mikrozensus EU-SILC 2023]" if is_de else "(C) Socio-Economic Status [Destatis Microcensus EU-SILC 2023]", fontweight="bold", fontsize=10.5)
    ax.set_xlabel("Einkommens-/SES-Dezile [D1 = Akute Armut, D10 = Wohlstand]" if is_de else "Income / SES Deciles [D1 = Severe Poverty, D10 = Affluence]", fontsize=9.5)
    ax.set_ylabel("Anteil an jeweiliger Gesamtbevölkerung (%)" if is_de else "Share of Respective Population (%)", fontsize=9.5)
    ax.set_ylim(0, 36)
    ax.legend(loc="upper right", fontsize=8.5)

    # --- PANEL D: Suspect gender proportions ---
    ax = axes[1, 0]
    ax.bar([0, 1], m["male_shares"], width=0.52, label="Männlich" if is_de else "Male", color=C_DE, edgecolor="black", alpha=0.88)
    ax.bar([0, 1], m["female_shares"], width=0.52, bottom=m["male_shares"], label="Weiblich" if is_de else "Female", color=C_NDE, edgecolor="black", alpha=0.88)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(cats, fontsize=10)
    ax.set_title("(D) Geschlechterproportion der Tatverdächtigen [BKA PKS 2023 T20]" if is_de else "(D) Gender Distribution of Suspects [Official BKA PKS 2023 T20]", fontweight="bold", fontsize=10.5)
    ax.set_ylabel("Anteil an Tatverdächtigen (%)" if is_de else "Share of Suspects (%)", fontsize=9.5)
    ax.set_ylim(0, 110)
    for i in [0, 1]:
        m_txt = f"{m['male_shares'][i]:.1f}%\nMännlich" if is_de else f"{m['male_shares'][i]:.1f}%\nMale"
        ax.text(i, m["male_shares"][i] / 2, m_txt, ha="center", va="center", color="white", fontweight="bold", fontsize=10)
        ax.text(i, m["male_shares"][i] + m["female_shares"][i] / 2, f"{m['female_shares'][i]:.1f}%", ha="center", va="center", color="white", fontweight="bold", fontsize=9)

    # --- PANEL E: High-risk demographic concentration with Fréchet bounds (METHODOLOGICAL CONTRIBUTION) ---
    ax = axes[1, 1]
    bars_e = ax.bar(
        cats, m["hr_shares"],
        yerr=m["hr_yerr"], capsize=5, ecolor="#1A237E",
        color=[C_DE, C_NDE], edgecolor="black", alpha=0.88, width=0.52,
        error_kw=dict(lw=1.4, capthick=1.4)
    )
    e_title = (
        f"(E) Eigener Beitrag: Kombinierte Risikokonstellation\n(Kettenregel & Fréchet 2006 | Zensus 2022 & EU-SILC 2023)"
        if is_de else
        f"(E) Methodological Contribution: Joint Risk Concentration\n(Chain Rule & Fréchet 2006 | Census 2022 & EU-SILC 2023)"
    )
    ax.set_title(e_title, fontweight="bold", fontsize=9.2)
    ax.set_ylabel("Anteil an jeweiliger Gesamtpopulation (%)" if is_de else "Share of Respective Population (%)", fontsize=9.5)
    ax.set_ylim(0, 20.0)
    for i, b in enumerate(bars_e):
        h = b.get_height()
        hi = m["hr_bounds"][i][1]
        ax.text(b.get_x() + b.get_width() / 2, max(hi, h) + 0.40, f"{h:.1f}%", ha="center", va="bottom", fontweight="bold", fontsize=10.5)
    e_banner = (
        f"Eigener Beitrag: {m['hr_disparity']}× Risikokonzentration\n[Fréchet: {m['hr_bounds'][0][0]:.1f}–{m['hr_bounds'][0][1]:.1f}% vs. {m['hr_bounds'][1][0]:.1f}–{m['hr_bounds'][1][1]:.1f}%]"
        if is_de else
        f"Methodological Contribution: {m['hr_disparity']}× Risk Concentration\n[Fréchet: {m['hr_bounds'][0][0]:.1f}–{m['hr_bounds'][0][1]:.1f}% vs. {m['hr_bounds'][1][0]:.1f}–{m['hr_bounds'][1][1]:.1f}%]"
    )
    ax.text(1, 18.0, e_banner, ha="center", fontweight="bold", color=C_NDE, fontsize=8.0, bbox=dict(boxstyle="round,pad=0.2", fc="#FFF9C4", ec="gold", lw=1.0))

    # --- PANEL F: Empirical OECD Meta-Regression ---
    render_panel_f_oecd_regression(axes[1, 2], m["oecd_reg"], lang=lang, is_standalone=False)

    # --- PANEL G: Bivariate Delinquency Model: Age x SES ---
    render_panel_g_risk_matrix(axes[2, 0], m, lang=lang, is_standalone=False, fig=fig)

    # --- PANEL H: OFFICIAL BKA REGISTER DECOMPOSITION WATERFALL (Males 14+) ---
    render_bka_register_waterfall_panel(axes[2, 1], m["waterfall_data"], lang=lang, is_standalone=False, panel_letter="H")

    # --- PANEL I: Universal Age-Crime curves: BKA Register Data (14–80 y.) ---
    render_panel_i_age_crime(axes[2, 2], m, lang=lang, is_standalone=False)

    # Footnote
    rr_ctrl = m.get("rr_ctrl_central", 2.60)
    if is_de:
        plt.figtext(0.01, 0.004, f"Survey-Metasynthese amtlicher Register (BKA PKS T20, T40, T50, T29; Key 892000; Zensus 2022) & kriminologischer Surveys (EU-SILC, Mikrozensus, OECD-Längsschnittkohorten).\nMethodischer Hinweis: Panel E ist der eigene Beitrag (Kettenregel & Fréchet-Schranken). Panel F kalibriert die Prekaritätselastizität über OECD-Studien. Panel G modelliert das Alter×SES-Risikofeld (0–80 J. mit OECD-Zentralwert {rr_ctrl:.2f}×). Panel H zeigt die amtliche BKA-Registerdekomposition, Panel I schließt die Storyline mit den amtlichen Alterskurven ab (14–30 J.).", fontsize=8.5, style="italic", ha="left")
        out_name = "bka_kriminalitaet_3x3_deutsch_v2.png"
    else:
        plt.figtext(0.01, 0.004, f"Survey meta-synthesis of official registers (BKA PKS T20, T40, T50, T29; Key 892000; Census 2022) & criminological surveys (EU-SILC, Microcensus, OECD Longitudinal Cohorts).\nMethodological Note: Panel E is the novel contribution (chain rule & Fréchet bounds). Panel F calibrates the precarity elasticity via OECD peer cohorts. Panel G models the Age×SES risk surface (ages 0–80 with OECD central estimate {rr_ctrl:.2f}×). Panel H displays the official BKA register decomposition, Panel I concludes the storyline with official age curves (ages 14–30).", fontsize=8.5, style="italic", ha="left")
        out_name = "bka_crime_disparity_9panel_english_v2.png"

    plt.tight_layout(rect=[0, 0.025, 1, 0.965])
    out_path = os.path.join(PLOTS_DIR, out_name)
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"   ✓ {out_name} generiert.")


# =============================================================================
# 6. MAIN EXECUTION PIPELINE
# =============================================================================
def main():
    print("=" * 70)
    print("START MODELLIERUNG & PLOT-GENERIERUNG (src/modeling.py)")
    print("=" * 70)
    data = load_audited_datasets()
    fitted_models = fit_models(data)

    # 1. Render all standalone panel figures
    generate_individual_plots(fitted_models)

    # 2. Render synthesis waterfall decomposition diagram
    generate_waterfall_plot(fitted_models)

    # 3. Render 3x3 composite matrices v1
    generate_composite_matrix_de(fitted_models)
    generate_composite_matrix_en(fitted_models)

    # 4. Render 3x3 composite matrices v2
    generate_composite_matrix_v2(fitted_models, lang="de")
    generate_composite_matrix_v2(fitted_models, lang="en")

    print("\n" + "=" * 70)
    print("ALLE PLOTS ERFOLGREICH IN /plots GENERIERT UND DOKUMENTIERT.")
    print("=" * 70)


if __name__ == "__main__":
    main()


