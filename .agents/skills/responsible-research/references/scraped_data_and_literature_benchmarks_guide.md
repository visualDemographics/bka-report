# Methodological Guide: Handling Scraped Web Data, PDF Extractions & Literature Empirical Benchmarks

This guide provides standard operating procedures on how to ingest, audit, and integrate data scraped from the internet or extracted from PDF reports into reproducible research pipelines.

---

## 1. Overview & Golden Rules of Data Extraction

In empirical investigations, primary data rarely arrives in clean CSV format. Researchers frequently encounter:
1. **Scraped Web Data**: Tabular data extracted from web portals, statistical APIs, or HTML tables (e.g., World Bank Open Data, OPEC bulletins, Eurostat/Destatis portals, Wikipedia historical lists, SEC EDGAR).
2. **PDF Extractions**: Statistical tables, audited university budgets, ministry reports, and econometric estimates buried inside static PDF documents (e.g., MIT Treasurer's Reports, TUM Annual Financial Statements, UN World Population Prospects, criminological surveys).

### The Four Golden Rules:
1. **Save Unmodified Originals in `rawdata/` (or `literature/`)**: Never clean or reformat raw downloaded files in-place. Store the original `.pdf`, `.html`, `.json`, or raw `.csv` with an immutable timestamp.
2. **Cryptographic Provenance in `rawdata.md`**: Record the source URL, exact retrieval date, file size, and SHA-256 hash in `rawdata/rawdata.md` or `raw/MANIFEST.csv`.
3. **Zero Magic Numbers in Source Code**: Never paste numbers extracted from a website or PDF directly into `src/modeling.py` or plotting functions.
4. **The Central Benchmark Catalog**: Every isolated empirical scalar (e.g., an odds ratio, a peak historical output, an institutional budget pass-through, or a survey parameter) must be registered in **`literature_empirical_benchmarks.csv`** with its exact page, table number, and verbatim quotation.

---

## 2. Ingesting Scraped Web Data

When scraping data from websites:
1. **Automate the Fetch**: Write a deterministic fetch function or script (e.g., `python src/data_preparation.py --download`) using standard libraries (`urllib.request` or `requests`).
2. **Handle Delimiters and Encodings**: Explicitly declare encodings (`utf-8`, `latin-1`) and CSV delimiters (semicolon `;` in European tables vs. comma `,` in US/international tables).
3. **Verify Header Layouts**: Government portals frequently place metadata in the first 3–6 rows. Document header offsets explicitly.
4. **Integrity Assertions**:
   ```python
   # Verify row count and non-null key columns immediately upon ingestion
   assert len(scraped_df) >= expected_min_rows, "Scraped table incomplete!"
   assert scraped_df["year"].is_monotonic_increasing, "Chronological order broken!"
   ```

---

## 3. Extracting Data from Static PDFs

PDF reports cannot be parsed natively without extraction tools. Use the following tiered workflow:

### Tooling Strategy:
* **Structured Vector Tables**: Use `pdfplumber` or `pypdf` to extract text tables into raw CSV tables.
* **Scanned Reports / Historical Yearbooks**: Use OCR (`tesseract` / `pytesseract`) or double-key manual entry with verified cross-checks.
* **Complex Multi-Page Financial Accounts**: For institutional annual statements (e.g., TUM, MIT, ETH), manually extract relevant line items directly into `literature_empirical_benchmarks.csv` or a dedicated raw table, citing the exact page, table name, and financial statement line.

### Extraction Quality Checklist:
- [ ] Record the exact PDF filename in `literature/` or `rawdata/`.
- [ ] Record the physical PDF page number (`#page=XX`).
- [ ] Record the official table number or section heading.
- [ ] Record verbatim quotation of the row label and explanatory footnotes.

---

## 4. The Standard Schema: `literature_empirical_benchmarks.csv`

The file `literature_empirical_benchmarks.csv` acts as the single auditable database for all empirical parameters, literature transfer values, and isolated register scalars extracted from PDFs and websites:

### Column Definitions:
| Column | Description | Example |
|---|---|---|
| `parameter_id` | Unique uppercase identifier | `MIT_LINCOLN_LAB_BUDGET` |
| `themenbereich` | High-level research domain | `Higher_Education` |
| `indikator` | Descriptive name of metric | `Lincoln Lab Federal Pass-Through` |
| `gruppe` | Population, sector, or entity | `mit` |
| `wert` | Numeric value (standardized float) | `1235.0` |
| `einheit` | Physical or economic unit | `Million_USD` |
| `intervall_95_ki` | 95% Confidence Interval (if reported) | `[1.15; 1.90]` |
| `signifikanz_p` | Statistical significance (p-value) | `p < 0.001` |
| `stichprobe_n` | Sample size or census type | `Vollerhebung` or `N = 3,528` |
| `quelle_autor_institution` | Author or issuing institution | `MIT Office of the Vice President for Finance` |
| `quelle_titel` | Full title of document / paper | `Report of the Treasurer Year Ended June 30 2023` |
| `jahr` | Year of publication | `2023` |
| `fundstelle_seite_tabelle` | Exact page and table coordinates | `Financial Statements Page 14` |
| `exakte_zeile_fundstelle` | Exact line description in source | `Operating Expenditures: Lincoln Laboratory` |
| `exakter_quelltext_zitat` | Verbatim quotation from source | `"Sponsored research: Lincoln Laboratory: $1,235.0M"` |
| `doi_url` | Official permanent URL or DOI | `https://vpf.mit.edu/treasurers-report` |
| `lokale_datei` | Local path with PDF anchor | `literature/mit_treasurers_report_2023.pdf#page=14` |
| `methodischer_status` | Classification of data quality | `Audited_Financial_Statement` |

### Concrete Multi-Domain Examples:
```csv
parameter_id,themenbereich,indikator,gruppe,wert,einheit,intervall_95_ki,signifikanz_p,stichprobe_n,quelle_autor_institution,quelle_titel,jahr,fundstelle_seite_tabelle,exakte_zeile_fundstelle,exakter_quelltext_zitat,doi_url,lokale_datei,methodischer_status
OPEC_VEN_OIL_PROD_1998,Commodities,Venezuela Crude Oil Production Peak,venezuela,3134.0,Thousand_bbl_day,,,Vollerhebung,OPEC,OPEC Annual Statistical Bulletin (Historical Series),2023,Table 3.1 Page 28,"Table 3.1, Row 'Venezuela', Column '1998'","Average crude production 1998: 3,134.0 kb/d",https://asb.opec.org,literature/opec_asb_2023.pdf#page=28,Amtliche_Sekundaerstatistik
MIT_LINCOLN_LAB_BUDGET,Higher_Education,MIT Lincoln Laboratory Federal DoD Pass-Through,mit,1235.0,Million_USD,,,Vollerhebung,MIT Office of the Vice President for Finance,Report of the Treasurer for the Year Ended June 30 2023,2023,Financial Statements Page 14,"Operating Expenditures: Lincoln Laboratory: $1,235.0M","Sponsored research: Lincoln Laboratory accounts for $1,235.0 million in federal funding",https://vpf.mit.edu/treasurers-report,literature/mit_treasurers_report_2023.pdf#page=14,Audited_Financial_Statement
TUM_KLINIKUM_REVENUE,Higher_Education,TUM Klinikum rechts der Isar Clinical Turnover,tum,890.0,Million_EUR,,,Vollerhebung,TUM & Bayerisches Staatsministerium,Rechenschaftsbericht & Jahresabschluss Klinikum,2023,Wirtschaftsplan Tabelle 4 Seite 22,"Umsatzerloese aus Krankenhausleistungen: 890,0 Mio. EUR","Klinikum rechts der Isar: Krankenversorgungsumsatz 890 Mio. EUR",https://www.tum.de,literature/tum_jahresbericht_2023.pdf#page=22,Audited_Financial_Statement
CRIMOC_OR_CONTROLLED,Multivariate_Kohorte,Controlled Odds Ratio Delinquency,nichtdeutsch,1.054,Odds_Ratio,[0.94; 1.18],p = 0.38 (n.s.),N = 3.528,"Boers & Reinecke (CRIMOC)",Delinquenz im Altersverlauf,2019,Tabelle 7.3 Modell 3 S. 145,"Tabelle 7.3, Seite 145, Zeile 'Nichtdeutsch'","Modell 3: Nichtdeutsch OR = 1,054 (95%-KI: [0,94; 1,18], p = 0,38 n.s.)",https://www.waxmann.com/buch3966,literature/citations.md#L69-L70,Laengsschnitt_Panelstudie
```

---

## 5. Minimum Snippet: `data_preparation.py`

This snippet illustrates how `data_preparation.py` ingests raw scraped data, audits benchmark citations, validates accounting identities with `assert`, and writes clean tables to `datasets/`:

```python
import csv
import os

def audit_and_prepare_data(raw_benchmarks_path, raw_time_series_path, out_datasets_path):
    # 1. Ingest & Audit Benchmarks
    benchmarks = {}
    with open(raw_benchmarks_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            pid = r["parameter_id"].strip()
            val = float(r["wert"])
            assert len(r["exakter_quelltext_zitat"].strip()) > 5, f"Missing citation quote for {pid}"
            benchmarks[pid] = val

    # 2. Ingest Scraped Data & Normalize
    cleaned = []
    with open(raw_time_series_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            year = int(r["year"])
            gross_output = float(r["gross_output"])
            population = float(r["population"])
            assert population > 0, "Population denominator must be strictly positive!"
            
            per_capita = gross_output / population
            cleaned.append({"year": year, "per_capita_output": round(per_capita, 4)})

    # 3. Export to datasets/
    with open(out_datasets_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["year", "per_capita_output"])
        writer.writeheader()
        writer.writerows(cleaned)
    print(f"✓ Audited {len(benchmarks)} benchmarks and exported {len(cleaned)} records.")
```

---

## 6. Minimum Snippet: `modeling.py`

This snippet demonstrates how `modeling.py` dynamically accesses benchmark values, fits empirical parametric models without synthetic random draws, and renders publication-ready plots:

```python
import csv
import matplotlib
matplotlib.use("Agg")  # Non-interactive headless backend
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

def run_modeling_and_plots(dataset_path, benchmarks_path, plot_path):
    # 1. Load benchmarks dynamically (NO hardcoded numbers in scripts!)
    benchmarks = {}
    with open(benchmarks_path, "r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            benchmarks[r["parameter_id"].strip()] = float(r["wert"])

    # 2. Load empirical observations
    years, y_obs = [], []
    with open(dataset_path, "r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            years.append(int(r["year"]))
            y_obs.append(float(r["per_capita_output"]))
    years, y_obs = np.array(years), np.array(y_obs)

    # 3. Fit parametric model to empirical data (NEVER scipy.stats.norm.rvs!)
    def decay_func(t, y0, k):
        return y0 * np.exp(-k * (t - years[0]))

    popt, pcov = curve_fit(decay_func, years, y_obs, p0=[y_obs[0], 0.05])

    # 4. Deterministic Plot Rendering
    fig, ax = plt.subplots(figsize=(7, 4.5), dpi=300)
    ax.scatter(years, y_obs, color="#1f4e78", label="Empirical Observations")
    t_dense = np.linspace(years[0], years[-1], 150)
    ax.plot(t_dense, decay_func(t_dense, *popt), color="#d9534f", lw=2, label="Fitted Trajectory")
    
    # Dynamic benchmark line from literature_empirical_benchmarks.csv
    if "BENCHMARK_TARGET" in benchmarks:
        ax.axhline(benchmarks["BENCHMARK_TARGET"], color="gray", linestyle="--", label="Target Benchmark")

    ax.set_title("Empirical Fit & Trajectory Decomposition", fontweight="bold")
    ax.legend(loc="upper right")
    plt.tight_layout()
    plt.savefig(plot_path, dpi=300)
    plt.close()
    print(f"✓ Generated plot: {plot_path}")
```

