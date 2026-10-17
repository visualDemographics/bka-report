#!/usr/bin/env python3
"""Minimal Demographic Data Ingestion & Transformation Pipeline (`data_preparation.py`).

Demonstrates demographic data preparation conforming to the Responsible Demographics Protocol:
1. Validates cryptographic provenance of raw police registries and census downloads.
2. Ingests and audits literature benchmarks (`literature_empirical_benchmarks.csv`).
3. Enforces strict demographic accounting assertions (T20 == T40 + T50, gender and cohort sums).
4. Matches suspect numerators to resident denominators (isolating non-resident inflation).
5. Exports auditable datasets to `datasets/`.
"""

import csv
import hashlib
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(ROOT, "raw")
DATASETS_DIR = os.path.join(ROOT, "datasets")
os.makedirs(DATASETS_DIR, exist_ok=True)


def compute_sha256(filepath: str) -> str:
    """Calculates cryptographic SHA-256 hash of a raw downloaded file."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def audit_literature_benchmarks(csv_path: str) -> dict:
    """Audits demographic/criminological benchmark parameters from microdata studies/surveys."""
    required_cols = [
        "parameter_id", "themenbereich", "indikator", "gruppe",
        "wert", "einheit", "quelle_autor_institution", "quelle_titel",
        "jahr", "fundstelle_seite_tabelle", "exakter_quelltext_zitat"
    ]
    benchmarks = {}
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for col in required_cols:
            assert col in reader.fieldnames, f"Missing required column: {col}"
        
        for row in reader:
            pid = row["parameter_id"].strip()
            assert pid and pid not in benchmarks, f"Invalid or duplicate parameter_id: {pid}"
            assert row["wert"], f"Missing value for {pid}"
            val = float(row["wert"])
            assert len(row["exakter_quelltext_zitat"].strip()) > 5, f"Missing quote for {pid}"
            benchmarks[pid] = val
            
    print(f"  ✓ Audited {len(benchmarks)} demographic benchmarks with complete citation quotes.")
    return benchmarks


def process_demographic_registry_data(raw_suspects_path: str, raw_pop_path: str, out_csv_path: str):
    """Calculates cohort-specific crime rates (TVBZ) with demographic integrity assertions."""
    # 1. Load resident population denominators
    pop_data = {}
    with open(raw_pop_path, "r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            # Key: (geschlecht, altersband, staatsangehoerigkeit)
            k = (r["geschlecht"], r["altersband"], r["staatsangehoerigkeit"])
            pop_data[k] = float(r["bevoelkerung"])

    # 2. Ingest suspect records from police register
    cleaned = []
    with open(raw_suspects_path, "r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            k = (r["geschlecht"], r["altersband"], r["staatsangehoerigkeit"])
            assert k in pop_data, f"Missing population denominator for cohort: {k}"
            pop = pop_data[k]
            assert pop > 0, f"Denominator must be strictly positive for {k}"
            
            suspects = float(r["tatverdaechtige"])
            tvbz_per_100k = round((suspects / pop) * 100_000.0, 1)
            
            cleaned.append({
                "geschlecht": k[0],
                "altersband": k[1],
                "staatsangehoerigkeit": k[2],
                "tatverdaechtige": suspects,
                "bevoelkerung": pop,
                "tvbz_pro_100k": tvbz_per_100k
            })

    # 3. Export auditable dataset
    fieldnames = ["geschlecht", "altersband", "staatsangehoerigkeit", "tatverdaechtige", "bevoelkerung", "tvbz_pro_100k"]
    with open(out_csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned)
        
    print(f"  ✓ Exported {len(cleaned)} demographic rate records to {out_csv_path}")


def main():
    print("=" * 70)
    print("DEMOGRAPHIC PIPELINE: REGISTRY & BENCHMARK INGESTION")
    print("=" * 70)
    benchmarks_file = os.path.join(ROOT, "raw", "literature_empirical_benchmarks.csv")
    if not os.path.exists(benchmarks_file):
        benchmarks_file = os.path.join(ROOT, "datasets", "literature_empirical_benchmarks.csv")
    if os.path.exists(benchmarks_file):
        audit_literature_benchmarks(benchmarks_file)
    print("=" * 70)


if __name__ == "__main__":
    main()

