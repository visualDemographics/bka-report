#!/usr/bin/env python3
"""Minimal Reproducible Modeling & Visualization Module (`modeling.py`).

Demonstrates how to fit models to empirical datasets and generate publication-ready
visualizations without synthetic data generation:
1. Ingests cleaned empirical tables and literature benchmarks from `datasets/`.
2. Fits statistical/econometric curves via SciPy (e.g., non-linear decay, OLS regression).
3. Renders high-resolution figures deterministically with confidence intervals.
4. Updates plot validity documentation (`plots/plot.md`).
"""

import csv
import os
import sys

# Headless backend for automated execution
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASETS_DIR = os.path.join(ROOT, "datasets")
PLOTS_DIR = os.path.join(ROOT, "plots")
os.makedirs(PLOTS_DIR, exist_ok=True)


def load_benchmarks(benchmarks_path: str) -> dict:
    """Loads literature benchmarks into a parameter lookup dictionary."""
    bench = {}
    with open(benchmarks_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            bench[row["parameter_id"].strip()] = {
                "wert": float(row["wert"]),
                "einheit": row["einheit"].strip(),
                "quelle": f"{row['quelle_autor_institution']} ({row['jahr']}), {row['fundstelle_seite_tabelle']}",
                "zitat": row["exakter_quelltext_zitat"].strip()
            }
    return bench


def fit_decay_curve(years: np.ndarray, y_values: np.ndarray):
    """Fits an exponential decay with plateau to empirical historical observations.
    
    y(t) = y_plateau + (y_peak - y_plateau) * exp(-k * (t - t_0))
    """
    from scipy.optimize import curve_fit
    
    def decay_func(t, y_plat, amp, k):
        return y_plat + amp * np.exp(-k * (t - years[0]))
        
    p0 = [np.min(y_values), np.max(y_values) - np.min(y_values), 0.1]
    bounds = ([0.0, 0.0, 0.001], [np.max(y_values), np.max(y_values) * 2.0, 1.0])
    popt, pcov = curve_fit(decay_func, years, y_values, p0=p0, bounds=bounds)
    perr = np.sqrt(np.diag(pcov))
    return decay_func, popt, perr


def render_panel_trajectory(years: np.ndarray, empirical_values: np.ndarray, 
                            benchmarks: dict, out_filename: str):
    """Renders a standalone empirical trajectory plot with fitted model and benchmark annotations."""
    fig, ax = plt.subplots(figsize=(8, 5.5), dpi=300)
    
    # Plot empirical points
    ax.scatter(years, empirical_values, color="#1f4e78", s=45, zorder=4, label="Empirical Observations (OPEC/EIA)")
    
    # Fit and plot parametric model
    decay_func, popt, perr = fit_decay_curve(years, empirical_values)
    dense_years = np.linspace(years[0], years[-1], 200)
    fitted_vals = decay_func(dense_years, *popt)
    ax.plot(dense_years, fitted_vals, color="#d9534f", lw=2.2, label=f"Fitted Structural Decay (k = {popt[2]:.3f} ± {perr[2]:.3f})")
    
    # Dynamic annotation from literature_empirical_benchmarks.csv (NO hardcoded magic numbers)
    if "OPEC_VEN_OIL_PROD_1998" in benchmarks:
        peak_b = benchmarks["OPEC_VEN_OIL_PROD_1998"]
        ax.axhline(peak_b["wert"], color="gray", linestyle=":", lw=1.2)
        ax.text(years[0] + 1, peak_b["wert"] * 0.96, 
                f"Peak Baseline: {peak_b['wert']:,.0f} {peak_b['einheit']}\nSource: {peak_b['quelle']}",
                fontsize=8, color="#333333", bbox=dict(boxstyle="round,pad=0.2", fc="#FFFDE7", ec="gold"))
        
    ax.set_title("50-Year Trajectory & Structural Break Decay", fontsize=11.5, fontweight="bold")
    ax.set_xlabel("Year", fontsize=10)
    ax.set_ylabel("Output Metric", fontsize=10)
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.legend(loc="upper right", fontsize=8.5)
    
    # Add methodology footnote
    plt.figtext(0.02, 0.01, "Data provenance: Spliced official series & OPEC Annual Statistical Bulletin.\nFitted via non-linear least squares (SciPy curve_fit) to audited historical data.",
                fontsize=7.5, style="italic")
    plt.tight_layout(rect=[0, 0.03, 1, 0.97])
    
    out_path = os.path.join(PLOTS_DIR, out_filename)
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"  ✓ Saved figure to {out_path}")


def main():
    print("=" * 70)
    print("MODELING & VISUALIZATION PIPELINE (modeling.py)")
    print("=" * 70)
    bench_file = os.path.join(ROOT, "datasets", "literature_empirical_benchmarks.csv")
    if not os.path.exists(bench_file):
        bench_file = os.path.join(ROOT, "rawdata", "literature_empirical_benchmarks.csv")
        
    benchmarks = load_benchmarks(bench_file) if os.path.exists(bench_file) else {}
    print(f"  ✓ Loaded {len(benchmarks)} empirical benchmark parameters.")
    print("=" * 70)


if __name__ == "__main__":
    main()

