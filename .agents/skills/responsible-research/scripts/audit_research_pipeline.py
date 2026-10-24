#!/usr/bin/env python3
"""General Automated Audit Script for Responsible Empirical Research Pipelines.

This script verifies compliance with the Responsible Empirical Research Protocol:
1. Repository structure completeness (goal, literature, rawdata/raw, datasets, src, plots, methodology, requirements.txt).
2. Data provenance & cryptographic manifest synchronization (rawdata/MANIFEST.csv and rawdata/rawdata.md).
3. Strict AST static code audit of `src/*.py` against uncorroborated values, synthetic generators, silent fallbacks, domain defaults, and dead code.
4. Active datasets integrity and quarantine verification (`datasets/_legacy_unverified/README.md`).
5. Synchronization between generated figures in plots/ and documentation in plots/plot.md.
"""

import ast
import csv
import hashlib
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

# Structural mathematical and indexing constants permitted in source code
STRUCTURAL_NUMBERS = {
    -1, -1.0, 0, 0.0, 0.05, 0.5, 0.975, 1, 1.0, 2, 2.0, 3, 3.0, 4, 4.0,
    5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24,
    30, 80, 100, 100.0, 150, 200, 250, 300, 1000, 10000, 100000, 100000.0,
    1e-4, 1e-10, 1.95996,
}


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
    print("\n[Check 2] Validating Rawdata Manifest & Cryptographic SHA-256 Provenance...")
    raw_dir = os.path.join(ROOT, "rawdata") if os.path.isdir(os.path.join(ROOT, "rawdata")) else os.path.join(ROOT, "raw")
    manifest_path = os.path.join(raw_dir, "MANIFEST.csv")
    raw_md_path = os.path.join(raw_dir, "rawdata.md")
    if not os.path.exists(manifest_path):
        print(f"  FAIL [Check 2]: Missing {manifest_path}")
        return False

    raw_md_text = ""
    if os.path.exists(raw_md_path):
        with open(raw_md_path, "r", encoding="utf-8") as f:
            raw_md_text = f.read()

    with open(manifest_path, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    for r in rows:
        fname = r["file"]
        fpath = os.path.join(raw_dir, fname)
        if not os.path.exists(fpath):
            print(f"  FAIL [Check 2]: Missing raw file {fname}")
            return False
        h = hashlib.sha256()
        with open(fpath, "rb") as bf:
            for chunk in iter(lambda: bf.read(1 << 20), b""):
                h.update(chunk)
        digest = h.hexdigest()
        if digest != r["sha256"].strip():
            print(f"  FAIL [Check 2]: SHA-256 mismatch for {fname}")
            return False
        if raw_md_text and (fname not in raw_md_text or digest not in raw_md_text):
            print(f"  FAIL [Check 2]: {fname} or its hash missing from rawdata/rawdata.md")
            return False

    print(f"  ✓ Verified SHA-256 integrity for all {len(rows)} files in {os.path.basename(raw_dir)}/MANIFEST.csv.")
    return True


def check_datasets_integrity():
    print("\n[Check 3] Validating Active Datasets & Quarantine Hygiene in datasets/...")
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

    legacy_dir = os.path.join(datasets_dir, "_legacy_unverified")
    if os.path.exists(legacy_dir):
        readme_path = os.path.join(legacy_dir, "README.md")
        if not os.path.exists(readme_path):
            print("  FAIL [Check 3]: datasets/_legacy_unverified/ missing mandatory README.md quarantine notice.")
            return False

    print(f"  ✓ Verified {len(csv_files)} non-empty empirical CSV datasets and quarantine boundaries in datasets/.")
    return True


def check_strict_ast_code_contract():
    print("\n[Check 4] Running Strict AST Static Code Analysis on src/*.py...")
    src_dir = os.path.join(ROOT, "src")
    prohibited_patterns = [
        (r"\.rvs\s*\(", "scipy.stats.<dist>.rvs() synthetic data generation"),
        (r"np\.random\.(normal|uniform|poisson|binomial|exponential|randn|rand)\s*\(", "numpy.random synthetic sampling"),
        (r"random\.(gauss|normalvariate|uniform)\s*\(", "python random synthetic sampling"),
    ]
    py_files = sorted([f for f in os.listdir(src_dir) if f.endswith(".py")])
    violations = []

    for fname in py_files:
        fpath = os.path.join(src_dir, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        # 4a. Regex scan on active lines
        for line_no, line in enumerate(content.splitlines(), start=1):
            stripped = line.strip()
            if stripped.startswith("#"):
                continue
            for pat, desc in prohibited_patterns:
                if re.search(pat, stripped):
                    violations.append(f"{fname}:{line_no} - Prohibited {desc}")

        tree = ast.parse(content, filename=fname)
        for node in ast.walk(tree):
            # 4b. Silent numeric fallback `.get(key, <numeric>)`
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "get":
                if len(node.args) >= 2:
                    arg1 = node.args[1]
                    if isinstance(arg1, ast.Constant) and isinstance(arg1.value, (int, float)) and not isinstance(arg1.value, bool):
                        violations.append(f"{fname}:{node.lineno} - Silent numeric fallback `.get(..., {arg1.value})`")

            # 4c. Function definitions
            if isinstance(node, ast.FunctionDef):
                fn_name = node.name
                is_data_fn = fn_name.startswith(("build_", "fit_", "compute_", "load_", "check_"))

                # Check unreachable dead code after `return`
                for stmt_idx, stmt in enumerate(node.body):
                    if isinstance(stmt, ast.Return) and stmt_idx < len(node.body) - 1:
                        next_stmt = node.body[stmt_idx + 1]
                        violations.append(f"{fname}:{next_stmt.lineno} - Unreachable dead code after `return` in `{fn_name}`")
                        break

                # Check uncorroborated domain floats in default arguments
                for d in node.args.defaults + [k for k in node.args.kw_defaults if k is not None]:
                    if isinstance(d, ast.Constant) and isinstance(d.value, (int, float)) and not isinstance(d.value, bool):
                        if d.value not in STRUCTURAL_NUMBERS:
                            violations.append(f"{fname}:{node.lineno} - Domain float default `{d.value}` in `{fn_name}()`")

                if is_data_fn:
                    for sub in ast.walk(node):
                        # Ternary fallback `x if cond else <float>`
                        if isinstance(sub, ast.IfExp):
                            for branch in (sub.body, sub.orelse):
                                if isinstance(branch, ast.Constant) and isinstance(branch.value, (int, float)) and not isinstance(branch.value, bool):
                                    if branch.value not in STRUCTURAL_NUMBERS:
                                        violations.append(f"{fname}:{sub.lineno} - Conditional fallback literal `{branch.value}` in `{fn_name}`")

                        # Direct assignment of domain constants
                        if isinstance(sub, ast.Assign) and isinstance(sub.value, ast.Constant):
                            val = sub.value.value
                            if isinstance(val, (int, float)) and not isinstance(val, bool):
                                if val not in STRUCTURAL_NUMBERS:
                                    targets = ", ".join(ast.unparse(t) for t in sub.targets)
                                    violations.append(f"{fname}:{sub.lineno} - Hardcoded assignment `{targets} = {val}` in `{fn_name}`")

                        # Hardcoded empirical literals in equality assertions
                        if isinstance(sub, ast.Assert) and fn_name != "build_literature_benchmarks":
                            if isinstance(sub.test, ast.Compare) and any(isinstance(op, ast.Eq) for op in sub.test.ops):
                                for comp_node in [sub.test.left] + list(sub.test.comparators):
                                    if isinstance(comp_node, ast.Constant) and isinstance(comp_node.value, (int, float)) and not isinstance(comp_node.value, bool):
                                        if comp_node.value not in STRUCTURAL_NUMBERS:
                                            violations.append(f"{fname}:{sub.lineno} - Hardcoded empirical literal `{comp_node.value}` in assertion")

    if violations:
        print("  FAIL [Check 4]: AST Code Audit detected violations:")
        for v in violations:
            print(f"    ✗ {v}")
        return False

    print(f"  ✓ Audited AST of {len(py_files)} Python modules in src/: zero synthetic data, silent fallbacks, or domain defaults.")
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
        check_strict_ast_code_contract,
        check_plot_documentation,
    ]
    passed = sum(1 for check in checks if check())
    print("\n" + "=" * 70)
    print(f"PIPELINE AUDIT COMPLETE: {passed}/{len(checks)} CHECKS PASSED.")
    print("=" * 70)
    sys.exit(0 if passed == len(checks) else 1)


if __name__ == "__main__":
    main()
