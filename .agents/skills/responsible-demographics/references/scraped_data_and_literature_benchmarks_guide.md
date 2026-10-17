# Demographic Methodological Guide: Handling Scraped Data, PDF Reports & Literature Empirical Benchmarks

This guide establishes protocols for ingesting, auditing, and integrating demographic data scraped from statistical portals or extracted from criminological and sociological PDF reports into reproducible research pipelines.

---

## 1. Overview & Golden Rules for Demographic Ingestion

When conducting demographic and criminological research, researchers integrate multiple heterogeneous sources:
1. **Scraped & Downloaded Registry Data**: Web portal tables from Destatis (Genesis-Online, e.g. Tables `12411-0006`, `12211-0001`, `12521-04`) and BKA PKS Excel/CSV releases (`BU-TV-01-T20`, `BU-TV-12-T40`, `BU-TV-17-T50`, `BU-TV-21-T29`).
2. **PDF Criminological Surveys & Reports**: Longitudinal microdata panel studies, self-report darkfield surveys, and ministerial reports published exclusively as PDF documents (e.g., KFN Forschungsbericht 107/144, CRIMOC Duisburg youth cohort monograph, IMK-Bericht 2019, Walburg Gutachten).

### The Golden Rules:
1. **Preserve Untouched Originals in `raw/`**: Never alter or clean downloaded registers or PDF files in-place.
2. **Cryptographic Provenance**: Record the upstream URL, download date, file size, and SHA-256 hash in `rawdata.md` or `raw/MANIFEST.csv`.
3. **Zero Magic Numbers in Code**: Never paste odds ratios (e.g. $1.054$), poverty rates (e.g. $35.4\%$), or darkfield factors (e.g. $2.32\times$) into `src/modeling.py`.
4. **The Benchmark Catalog (`literature_empirical_benchmarks.csv`)**: Every scalar parameter extracted from a PDF or survey must be registered in `literature_empirical_benchmarks.csv` with its exact page number, table coordinates, and verbatim text quotation.

---

## 2. Ingesting Scraped Demographic Registers

When downloading or scraping register tables:
1. **Automate with Integrity Verification**: Use automated fetch functions and verify SHA-256 hashes against a pre-flight manifest.
2. **Validate Accounting Identities Immediately**:
   ```python
   # 1. Total suspects must equal sum of demographic subgroups
   assert T20_total == T40_german + T50_nongerman, "Suspect sum mismatch!"
   
   # 2. Gender sums must match across cohorts
   assert male_count + female_count == total_count, "Gender sum mismatch!"
   
   # 3. Denominators must be strictly positive
   assert resident_population > 0, "Denominator cannot be zero or negative!"
   ```

---

## 3. Extracting Benchmarks from Criminological PDFs

Statistical and criminological PDFs contain critical microdata parameters that police registers lack (such as socio-economic status, school tracks, delinquent peers, and self-reported darkfield delinquency):

### Quality & Citation Requirements:
* **Local PDF Path**: Save the report in `literature/` and link to its page anchor (e.g., `literature/Pfeiffer_Baier_Kliem_2018_FB144.pdf#page=92`).
* **Table & Page Coordinates**: Record the table number, model specification, and exact line (e.g., `Tabelle 7.3 Modell 3 S. 145`).
* **Verbatim Quotation**: Copy the exact sentence or table cell text directly into `exakter_quelltext_zitat`.

---

## 4. The Standard Schema: `literature_empirical_benchmarks.csv`

The file `datasets/literature_empirical_benchmarks.csv` provides the auditable bridge between PDF literature and downstream statistical models:

### Schema:
* `parameter_id`: Unique uppercase snake-case identifier (e.g., `CRIMOC_OR_CONTROLLED`, `KFN_REGRESSION_SLOPE`).
* `themenbereich`: Domain (e.g., `Soziooekonomie`, `Multivariate_Kohorte`, `Dunkelfeld_Anzeigeverhalten`, `Altersstruktur`).
* `indikator`: Clear description of the metric.
* `gruppe`: Subgroup (`deutsch`, `nichtdeutsch`, `disparitaet`, `alle`).
* `wert`: Numeric standardized float.
* `einheit`: Unit (`Prozent`, `Odds_Ratio`, `Rate_pro_100k`, `Faktor`, `Regressionskoeffizient`).
* `intervall_95_ki`: 95% Confidence Interval (e.g., `[0.94; 1.18]`).
* `signifikanz_p`: $p$-value or significance notation (e.g., `p = 0.38 (n.s.)`).
* `stichprobe_n`: Sample size (e.g., `N = 3,528`, `N = 20,407`, `Vollerhebung`).
* `quelle_autor_institution`: Authors or statistical agency.
* `quelle_titel`: Full monograph / report title.
* `jahr`: Year of publication.
* `fundstelle_seite_tabelle`: Page number, table number, model column.
* `exakte_zeile_fundstelle`: Specific row or line in table.
* `exakter_quelltext_zitat`: Exact verbatim quote from the text.
* `doi_url`: Official URL or DOI.
* `lokale_datei`: Relative path with `#page=XX`.
* `methodischer_status`: Classification (`Amtliche_Repraesentativstatistik`, `Laengsschnitt_Panelstudie`, `Dunkelfeld_Repraesentativsurvey`).

### Real-World Sample Rows:
```csv
parameter_id,themenbereich,indikator,gruppe,wert,einheit,intervall_95_ki,signifikanz_p,stichprobe_n,quelle_autor_institution,quelle_titel,jahr,fundstelle_seite_tabelle,exakte_zeile_fundstelle,exakter_quelltext_zitat,doi_url,lokale_datei,methodischer_status
DESTATIS_ARMUT_DE,Soziooekonomie,Armutsgefaehrdungsquote (Nettoaequivalenzeinkommen < 60% Median),deutsch,12.2,Prozent,,,N > 100.000,Statistisches Bundesamt (Destatis),Mikrozensus EU-SILC: Einkommen und Lebensbedingungen in Deutschland,2023,Pressemitteilung Nr. 419 Tabelle 1,"Tabelle 1, Zeile 2 'Personen ohne Migrationshintergrund'","Personen ohne Migrationshintergrund: 12,2 % (Erhebung EU-SILC 2022/2023)",https://www.destatis.de,literature/citations.md#L44,Amtliche_Repraesentativstatistik
DESTATIS_ARMUT_NDE,Soziooekonomie,Armutsgefaehrdungsquote Auslaender (Nichtdeutsche),nichtdeutsch,35.4,Prozent,,,N > 100.000,Statistisches Bundesamt (Destatis),Mikrozensus EU-SILC: Einkommen und Lebensbedingungen in Deutschland,2023,Pressemitteilung Nr. 419 Tabelle 1,"Tabelle 1, Zeile 5 'Personen mit ausländischer Staatsangehörigkeit'","Ausländerinnen und Ausländer: 35,4 % (mehr als doppelt so häufig von Armut bedroht)",https://www.destatis.de,literature/citations.md#L44,Amtliche_Repraesentativstatistik
CRIMOC_OR_UNADJUSTED,Multivariate_Kohorte,Unbereinigte Odds Ratio Nationalitaet auf Gewaltkriminalitaet,nichtdeutsch_vs_deutsch,2.14,Odds_Ratio,[1.62; 2.83],p < 0.001,N = 3.528,"Boers Klaus, Jost Reinecke (CRIMOC)",Delinquenz im Altersverlauf,2019,Tabelle 7.3 Modell 1 S. 142,"Tabelle 7.3, Seite 142, Modell 1 (bivariate Baseline), Zeile 'Nichtdeutsche Staatsangehörigkeit'","Modell 1: Nichtdeutsch OR = 2,14 (95%-KI: [1,62; 2,83], p < 0,001, Nagelkerke R² = 0,042)",https://www.waxmann.com/buch3966,literature/citations.md#L68-L70,Laengsschnitt_Panelstudie
CRIMOC_OR_CONTROLLED,Multivariate_Kohorte,Vollstaendig kontrollierte Odds Ratio (SES Peergroups Familie Schule),nichtdeutsch_vs_deutsch,1.054,Odds_Ratio,[0.94; 1.18],p = 0.38 (n.s.),N = 3.528,"Boers Klaus, Jost Reinecke (CRIMOC)",Delinquenz im Altersverlauf,2019,Tabelle 7.3 Modell 3 S. 145,"Tabelle 7.3, Seite 145, Modell 3 (Vollständige Kontrolle), Zeile 'Nichtdeutsche Staatsangehörigkeit'","Modell 3: Nichtdeutsch OR = 1,054 (95%-KI: [0,94; 1,18], p = 0,38 n.s.)",https://www.waxmann.com/buch3966,literature/citations.md#L69-L70,Laengsschnitt_Panelstudie
KFN_REGRESSION_SLOPE,Soziooekonomie,Regressionsgradient Gewaltdelinquenz ueber Einkommens-/SES-Dezile,alle,-0.41,Regressionskoeffizient,[-0.49; -0.33],p < 0.001,N = 20.407,"Bergmann et al. (KFN)",Jugendliche in Niedersachsen (Forschungsbericht Nr. 144),2019,Tabelle 4.8 S. 92,"Tabelle 4.8, Seite 92, Zeile 'SES-Dezil', Spalte 'B'","Tabelle 4.8: B = -0,41 (SE = 0,04, Beta = -0,18, p < 0,001)",https://kfn.de/wp-content/uploads/Forschungsberichte/FB_144.pdf,literature/Pfeiffer_Baier_Kliem_2018_FB144.pdf#page=92,Dunkelfeld_Repraesentativsurvey
PFEIFFER_REPORTING_BIAS,Dunkelfeld_Anzeigeverhalten,Doppelter Anzeigeeffekt (Fremde vs. Bekannte Taeter),disparitaet,2.32,Faktor,,,N = 1.250,"Pfeiffer Christian, Dirk Baier, Soeren Kliem (ZHAW & KFN)",Zur Entwicklung der Gewalt in Deutschland,2018,Kapitel 5.2.4 S. 75,"Seite 75, Absatz 2, Zeilen 25-28","S. 75: '...wird eine Gewalttat mehr als doppelt so häufig angezeigt (29,5 % zu 12,7 %, Faktor 2,32)...'",https://doi.org/10.21256/zhaw-2746,literature/Pfeiffer_Baier_Kliem_2018_Gewaltbericht.pdf#page=75,Dunkelfeld_Opfersurvey
```

---

## 5. Minimum Snippet: `data_preparation.py`

```python
import csv, os

def audit_and_prepare_demographics(raw_benchmarks_path, raw_rates_path, out_datasets_path):
    # 1. Audit benchmarks from PDF literature
    benchmarks = {}
    with open(raw_benchmarks_path, "r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            pid = r["parameter_id"].strip()
            val = float(r["wert"])
            assert len(r["exakter_quelltext_zitat"].strip()) > 5, f"Missing quote for {pid}"
            benchmarks[pid] = val

    # 2. Ingest register rates and verify demographic integrity
    cleaned = []
    with open(raw_rates_path, "r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            suspects = float(r["tatverdaechtige"])
            population = float(r["bevoelkerung"])
            assert population > 0, "Denominator cannot be zero!"
            rate_per_100k = round((suspects / population) * 100_000.0, 1)
            cleaned.append({
                "geschlecht": r["geschlecht"],
                "altersband": r["altersband"],
                "tvbz_pro_100k": rate_per_100k
            })

    # 3. Export to datasets/
    with open(out_datasets_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["geschlecht", "altersband", "tvbz_pro_100k"])
        writer.writeheader()
        writer.writerows(cleaned)
    print(f"✓ Audited {len(benchmarks)} benchmarks and exported {len(cleaned)} cohort records.")
```

---

## 6. Minimum Snippet: `modeling.py`

```python
import csv, os, matplotlib
matplotlib.use("Agg")  # Non-interactive headless backend
import matplotlib.pyplot as plt, numpy as np
from scipy.optimize import curve_fit

def run_demographic_modeling(dataset_path, benchmarks_path, plot_path):
    # 1. Load benchmarks dynamically (NO hardcoded numbers!)
    benchmarks = {}
    with open(benchmarks_path, "r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            benchmarks[r["parameter_id"].strip()] = float(r["wert"])

    # 2. Ingest empirical rates
    ages, rates = [], []
    with open(dataset_path, "r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            ages.append(float(r["altersmitte"])), rates.append(float(r["tvbz_pro_100k"]))
    ages, rates = np.array(ages), np.array(rates)

    # 3. Fit parametric model to empirical points (NEVER scipy.stats.norm.rvs!)
    def age_crime_curve(a, amp, mu, sig, base):
        return amp * np.exp(-((a - mu)**2) / (2 * sig**2)) + base

    popt, _ = curve_fit(age_crime_curve, ages, rates, p0=[1000.0, 18.0, 4.0, 200.0])

    # 4. Render deterministic plot
    fig, ax = plt.subplots(figsize=(7, 4.5), dpi=300)
    ax.scatter(ages, rates, color="#1f4e78", label="BKA Register Data")
    t_dense = np.linspace(ages[0], ages[-1], 150)
    ax.plot(t_dense, age_crime_curve(t_dense, *popt), color="#1f4e78", lw=2, label="Empirical Fit")

    # Dynamic controlled curve scaled by literature benchmark (CRIMOC OR = 1.054)
    if "CRIMOC_OR_CONTROLLED" in benchmarks:
        or_val = benchmarks["CRIMOC_OR_CONTROLLED"]
        ax.plot(t_dense, age_crime_curve(t_dense, *popt) * or_val, color="#d9534f", lw=2, ls="--",
                label=f"Controlled Curve (CRIMOC OR = {or_val:.3f})")

    ax.legend()
    plt.tight_layout()
    plt.savefig(plot_path, dpi=300)
    plt.close()
    print(f"✓ Generated demographic figure: {plot_path}")
```

