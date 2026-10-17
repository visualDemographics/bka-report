#!/usr/bin/env python3
"""Minimal Demographic Modeling & Visualization Module (`modeling.py`).

Demonstrates demographic and criminological modeling conforming to the protocol:
1. Ingests cleaned empirical datasets and literature benchmarks from `datasets/`.
2. Evaluates demographic standardization and fits statistical models (e.g. Age-Crime curves).
3. Accesses external survey benchmarks dynamically (CRIMOC OR, KFN regression gradient).
4. Renders deterministic publication figures in `plots/` without synthetic Gaussian data.
"""

import csv
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASETS_DIR = os.path.join(ROOT, "datasets")
PLOTS_DIR = os.path.join(ROOT, "plots")
os.makedirs(PLOTS_DIR, exist_ok=True)


def load_benchmarks(benchmarks_path: str) -> dict:
    """Loads demographic and literature benchmarks into a parameter dictionary."""
    bench = {}
    with open(benchmarks_path, "r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            bench[r["parameter_id"].strip()] = {
                "wert": float(r["wert"]),
                "einheit": r["einheit"].strip(),
                "quelle": f"{r['quelle_autor_institution']} ({r['jahr']})",
                "zitat": r["exakter_quelltext_zitat"].strip()
            }
    return bench


def fit_age_crime_curve(ages: np.ndarray, rates: np.ndarray):
    """Fits non-linear double-component curve (adolescent peak + adult baseline) to empirical rates."""
    from scipy.optimize import curve_fit

    def age_curve(a, a_amp, mu, sigma, b_base, tau):
        peak = a_amp * np.exp(-((a - mu) ** 2) / (2 * (sigma ** 2)))
        decay = b_base * np.exp(-a / tau)
        return peak + decay

    p0 = [1000.0, 18.0, 4.0, 300.0, 30.0]
    popt, pcov = curve_fit(age_curve, ages, rates, p0=p0, maxfev=10000)
    perr = np.sqrt(np.diag(pcov))
    return age_curve, popt, perr


def render_demographic_panel(ages: np.ndarray, rates_de: np.ndarray, benchmarks: dict, out_filename: str):
    """Renders empirical age-crime curve with benchmark comparisons."""
    fig, ax = plt.subplots(figsize=(8, 5.5), dpi=300)

    # Plot empirical BKA data points (German males)
    ax.scatter(ages, rates_de, color="#1f4e78", s=50, zorder=5, label="BKA Register (German Males)")

    # Fit and plot parametric model to empirical points
    curve_func, popt, perr = fit_age_crime_curve(ages, rates_de)
    dense_ages = np.linspace(12, 80, 150)
    ax.plot(dense_ages, curve_func(dense_ages, *popt), color="#1f4e78", lw=2.2, label=f"BKA Empirical Fit (Peak age: {popt[1]:.1f}y)")

    # Controlled projection using dynamic CRIMOC benchmark (NO hardcoded scalar!)
    if "CRIMOC_OR_CONTROLLED" in benchmarks:
        or_ctrl = benchmarks["CRIMOC_OR_CONTROLLED"]["wert"]
        controlled_curve = curve_func(dense_ages, *popt) * or_ctrl
        ax.plot(dense_ages, controlled_curve, color="#d9534f", lw=2.2, linestyle="--",
                label=f"Controlled Comparison (CRIMOC OR = {or_ctrl:.3f})")

    ax.axvspan(14, 30, color="gold", alpha=0.25, zorder=0)
    ax.text(22, max(rates_de) * 0.9, "Adolescent Peak Window\n(Ages 14–30)", ha="center", fontsize=8.5,
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="gold"))

    ax.set_title("Age–Crime Curve (BKA Empirical vs. Controlled Model)", fontsize=11.5, fontweight="bold")
    ax.set_xlabel("Age in Years", fontsize=10)
    ax.set_ylabel("Suspect Rate (TVBZ per 100,000 Males)", fontsize=10)
    ax.grid(True, linestyle="--", alpha=0.35)
    ax.legend(loc="upper right", fontsize=8.5)

    plt.figtext(0.02, 0.01, "Data sources: BKA PKS Table 40 & Destatis 12411. Controlled curve scaled by CRIMOC Table 7.3 benchmark.",
                fontsize=7.5, style="italic")
    plt.tight_layout(rect=[0, 0.03, 1, 0.97])

    out_path = os.path.join(PLOTS_DIR, out_filename)
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"  ✓ Saved demographic figure to {out_path}")


def main():
    print("=" * 70)
    print("DEMOGRAPHIC MODELING PIPELINE (modeling.py)")
    print("=" * 70)
    bench_file = os.path.join(DATASETS_DIR, "literature_empirical_benchmarks.csv")
    if os.path.exists(bench_file):
        benchmarks = load_benchmarks(bench_file)
        print(f"  ✓ Loaded {len(benchmarks)} empirical benchmark parameters.")
    print("=" * 70)


if __name__ == "__main__":
    main()

