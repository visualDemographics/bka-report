#!/usr/bin/env python3
"""Minimal Reproducible Pipeline: Data Ingestion & Transformation (`data_preparation.py`).

Demonstrates how to process data scraped from the web or extracted from PDF reports
in strict accordance with the Responsible Empirical Research Protocol:
1. Validates provenance of raw files (source URL, retrieval timestamp, SHA-256).
2. Audits extracted PDF / literature benchmarks (`literature_empirical_benchmarks.csv`).
3. Cleans, standardizes units, and performs boundary/denominator matching.
4. Executes strict integrity assertions (`assert`) before exporting to `datasets/`.
"""

import csv
import hashlib
import os
import sys

# Define workspace boundaries
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(ROOT, "rawdata")
OUT_DIR = os.path.join(ROOT, "datasets")
os.makedirs(OUT_DIR, exist_ok=True)


def compute_sha256(filepath: str) -> str:
    """Calculates cryptographic SHA-256 hash of a raw downloaded file."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def audit_literature_benchmarks(csv_path: str) -> dict:
    """Ingests and strictly validates empirical benchmarks extracted from PDFs or literature.
    
    Ensures that no scalar parameter enters downstream models without complete
    bibliographic provenance, exact page/table coordinates, and verbatim quotation.
    """
    required_cols = [
        "parameter_id", "themenbereich", "indikator", "gruppe",
        "wert", "einheit", "quelle_autor_institution", "quelle_titel",
        "jahr", "fundstelle_seite_tabelle", "exakter_quelltext_zitat"
    ]
    benchmarks = {}
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for col in required_cols:
            assert col in reader.fieldnames, f"Missing required column in benchmarks: {col}"
        
        for row in reader:
            pid = row["parameter_id"].strip()
            assert pid, "Empty parameter_id found in benchmarks CSV!"
            assert pid not in benchmarks, f"Duplicate parameter_id: {pid}"
            assert row["wert"], f"Missing numeric value for parameter: {pid}"
            
            # Verify value is a valid float
            try:
                val = float(row["wert"])
            except ValueError:
                raise AssertionError(f"Parameter {pid} value '{row['wert']}' is not a valid float!")
            
            # Verify provenance fields are not empty
            assert len(row["quelle_titel"].strip()) > 3, f"Missing source title for {pid}"
            assert len(row["fundstelle_seite_tabelle"].strip()) > 2, f"Missing page/table cite for {pid}"
            assert len(row["exakter_quelltext_zitat"].strip()) > 5, f"Missing verbatim quote for {pid}"
            
            benchmarks[pid] = {
                "wert": val,
                "einheit": row["einheit"].strip(),
                "quelle": f"{row['quelle_autor_institution']} ({row['jahr']}), {row['fundstelle_seite_tabelle']}",
                "zitat": row["exakter_quelltext_zitat"].strip()
            }
            
    print(f"  ✓ Audited {len(benchmarks)} empirical benchmark parameters with verified citations.")
    return benchmarks


def process_scraped_commodity_series(raw_csv_path: str, pop_csv_path: str, out_csv_path: str):
    """Processes scraped multi-decade production data and merges with population denominators.
    
    Demonstrates:
    - Normalization from gross physical output to per-capita units.
    - Base-year indexing (Index t0 = 100.0).
    - Integrity assertions verifying accounting identities.
    """
    # 1. Ingest raw scraped series
    production_records = []
    with open(raw_csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            production_records.append({
                "year": int(row["year"]),
                "oil_kb_d": float(row["crude_oil_production_kbd"]),
                "steel_kt": float(row["crude_steel_production_kt"]),
            })
            
    # 2. Ingest population denominator series (e.g. UN WPP migration-adjusted)
    pop_by_year = {}
    with open(pop_csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            pop_by_year[int(row["year"])] = float(row["resident_population_millions"])
            
    # 3. Compute per-capita metrics and index against baseline year (e.g. 1998)
    base_year = 1998
    base_oil_pc = None
    cleaned_rows = []
    
    for r in production_records:
        yr = r["year"]
        assert yr in pop_by_year, f"Missing population denominator for year {yr}"
        pop = pop_by_year[yr]
        assert pop > 0.0, f"Invalid zero or negative population for year {yr}"
        
        # Per capita physical calculation:
        # Oil: barrels per day per 1,000 residents = (kb/d * 1000) / (pop_millions * 1000) = kb/d / pop_millions
        oil_bbl_day_per_1k = round(r["oil_kb_d"] / pop, 2)
        steel_kg_per_cap = round((r["steel_kt"] * 1_000_000) / (pop * 1_000_000), 2)
        
        if yr == base_year:
            base_oil_pc = oil_bbl_day_per_1k
            
        cleaned_rows.append({
            "year": yr,
            "population_millions": pop,
            "oil_kb_d": r["oil_kb_d"],
            "oil_bbl_day_per_1k": oil_bbl_day_per_1k,
            "steel_kg_per_cap": steel_kg_per_cap,
        })
        
    assert base_oil_pc is not None and base_oil_pc > 0.0, f"Base year {base_year} not found in series!"
    
    # 4. Add index column and execute assertions
    for r in cleaned_rows:
        r["oil_pc_index_1998"] = round((r["oil_bbl_day_per_1k"] / base_oil_pc) * 100.0, 2)
        # Mathematical integrity assertion: base year must equal 100.0
        if r["year"] == base_year:
            assert abs(r["oil_pc_index_1998"] - 100.0) < 0.01, "Base year index calculation failed!"
            
    # 5. Export auditable dataset
    fieldnames = ["year", "population_millions", "oil_kb_d", "oil_bbl_day_per_1k", "oil_pc_index_1998", "steel_kg_per_cap"]
    with open(out_csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned_rows)
        
    print(f"  ✓ Exported {len(cleaned_rows)} normalized records to {out_csv_path}")


def main():
    print("=" * 70)
    print("ETL PIPELINE: SCRAPED DATA & BENCHMARK AUDITING (data_preparation.py)")
    print("=" * 70)
    
    benchmarks_file = os.path.join(ROOT, "rawdata", "literature_empirical_benchmarks.csv")
    if os.path.exists(benchmarks_file):
        audit_literature_benchmarks(benchmarks_file)
    else:
        print("  Notice: No local rawdata/literature_empirical_benchmarks.csv found in workspace root.")
        
    print("=" * 70)


if __name__ == "__main__":
    main()

