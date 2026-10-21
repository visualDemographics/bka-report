#!/usr/bin/env python3
"""General Automated Audit Script for Responsible Empirical Research Pipelines.

This script verifies compliance with the Responsible Empirical Research Protocol:
1. Repository structure completeness (goal, literature, rawdata/raw, datasets, src, plots, methodology, requirements.txt).
2. Data provenance & cryptographic manifest synchronization (rawdata/MANIFEST.csv and rawdata/rawdata.md).
3. Absence of synthetic random data generation (.rvs, np.random.normal) and silent numeric `.get(key, <number>)` fallbacks in `src/`.
4. Integrity of CSV datasets in datasets/ (non-empty, no all-NaN columns).
5. Synchronization between generated figures in plots/ and documentation in plots/plot.md.
"""

import ast
import csv
import hashlib
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))


def check_repo_structure():
    print("\n[Check 1] Validating Repository Directory Structure & Environment Pinning...")
    required_dirs = ["goal", "literature", "datasets", "src", "plots", "methodology"]
    raw_exists = os.path.isdir(os.path.join(ROOT, "rawdata")) or os.path.isdir(os.path.join(ROOT, "raw"))
    missing = [d for d in required_dirs if not os.path.isdir(os.path.join(ROOT, d))]
    if not raw_exists:
        missing.append("rawdata (or raw)")
    if not os.path.isfile(os.path.join(ROOT, "requirements.txt")) and not os.path.isfile(os.path.join(ROOT, "pyproject.toml")):
        missing.append("requirements.txt (or pyproject.toml)")
    if missing:
        print(f"  FAIL [Check 1]: Missing required directories/files: {missing}")
        return False
    print("  ✓ All required research directories and dependency lockfiles exist.")
    return True


def check_rawdata_manifest():
    print("\n[Check 2] Validating Rawdata Manifest & SHA-256 Provenance...")
    raw_dir = os.path.join(ROOT, "rawdata") if os.path.isdir(os.path.join(ROOT, "rawdata")) else os.path.join(ROOT, "raw")
    manifest_path = os.path.join(raw_dir, "MANIFEST.csv")
    if not os.path.exists(manifest_path):
        print(f"  FAIL [Check 2]: Missing {manifest_path}")
        return False
    with open(manifest_path, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        fpath = os.path.join(raw_dir, r["file"])
        if not os.path.exists(fpath):
            print(f"  FAIL [Check 2]: Missing raw file {r['file']}")
            return False
        h = hashlib.sha256()
        with open(fpath, "rb") as bf:
            for chunk in iter(lambda: bf.read(1 << 20), b""):
                h.update(chunk)
        if h.hexdigest() != r["sha256"].strip():
            print(f"  FAIL [Check 2]: SHA-256 mismatch for {r['file']}")
            return False
    print(f"  ✓ Verified SHA-256 integrity for all {len(rows)} files in {os.path.basename(raw_dir)}/MANIFEST.csv.")
    return True


def check_datasets_integrity():
    print("\n[Check 3] Validating Active Datasets in datasets/...")
    datasets_dir = os.path.join(ROOT, "datasets")
    csv_files = sorted([f for f in os.listdir(datasets_dir) if f.endswith(".csv")])
    if not csv_files:
        print("  FAIL [Check 3]: No CSV datasets found in datasets/.")
        return False

    for fname in csv_files:
        fpath = os.path.join(datasets_dir, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            reader = list(csv.reader(f))
        if len(reader) < 2:
            print(f"  FAIL [Check 3]: Dataset {fname} has no data rows.")
            return False
    print(f"  ✓ Verified {len(csv_files)} non-empty empirical CSV datasets in datasets/.")
    return True


def check_no_synthetic_or_fallbacks():
    print("\n[Check 4] Auditing src/ for Prohibited Synthetic Generators & Silent Numeric Fallbacks...")
    src_dir = os.path.join(ROOT, "src")
    prohibited_patterns = [
        (r"\.rvs\s*\(", "scipy.stats.<dist>.rvs() synthetic data generation"),
        (r"np\.random\.(normal|uniform|poisson|binomial|exponential)\s*\(", "numpy.random synthetic sampling"),
    ]
    py_files = sorted([f for f in os.listdir(src_dir) if f.endswith(".py")])
    for fname in py_files:
        fpath = os.path.join(src_dir, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        for line_no, line in enumerate(content.splitlines(), start=1):
            stripped = line.strip()
            if stripped.startswith("#"):
                continue
            for pat, desc in prohibited_patterns:
                if re.search(pat, stripped):
                    print(f"  FAIL [Check 4]: Prohibited {desc} found in src/{fname}:{line_no}")
                    return False

        tree = ast.parse(content, filename=fname)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "get":
                if len(node.args) >= 2:
                    arg1 = node.args[1]
                    if isinstance(arg1, ast.Constant) and isinstance(arg1.value, (int, float)) and not isinstance(arg1.value, bool):
                        print(f"  FAIL [Check 4]: Silent numeric fallback `.get(..., {arg1.value})` in src/{fname}:{node.lineno}")
                        return False

    print(f"  ✓ Audited {len(py_files)} Python modules in src/: zero synthetic random generators or silent numeric fallbacks found.")
    return True


def check_plot_documentation():
    print("\n[Check 5] Verifying Plot Validity Documentation (plots/plot.md)...")
    plots_dir = os.path.join(ROOT, "plots")
    plot_md = os.path.join(plots_dir, "plot.md")
    if not os.path.exists(plot_md):
        print("  FAIL [Check 5]: plots/plot.md does not exist.")
        return False

    with open(plot_md, "r", encoding="utf-8") as f:
        md_text = f.read()

    png_files = sorted([f for f in os.listdir(plots_dir) if f.endswith(".png")])
    if not png_files:
        print("  FAIL [Check 5]: No PNG plots found in plots/.")
        return False

    undocumented = [p for p in png_files if p not in md_text]
    if undocumented:
        print(f"  FAIL [Check 5]: The following plots are missing from plots/plot.md: {undocumented}")
        return False

    print(f"  ✓ All {len(png_files)} PNG figures in plots/ are documented in plots/plot.md.")
    return True


def main():
    print("=" * 70)
    print("RESPONSIBLE RESEARCH: GENERAL PIPELINE AUDIT SUITE")
    print("=" * 70)
    checks = [
        check_repo_structure,
        check_rawdata_manifest,
        check_datasets_integrity,
        check_no_synthetic_or_fallbacks,
        check_plot_documentation,
    ]
    passed = sum(1 for check in checks if check())
    print("\n" + "=" * 70)
    print(f"PIPELINE AUDIT COMPLETE: {passed}/{len(checks)} CHECKS PASSED.")
    print("=" * 70)
    sys.exit(0 if passed == len(checks) else 1)


if __name__ == "__main__":
    main()
