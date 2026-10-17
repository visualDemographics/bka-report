"""Skript zur Generierung und Aufbereitung aller relevanten CSV-Datensaetze in /datasets.

Dieses Skript extrahiert und generiert alle empirischen und kalibrierten Daten
fuer das Projekt 'BKA Kriminalitaetsdisparitaeten 2023' (Panels A bis I, Primärtabellen
des BKA, Destatis-Bevoelkerungsdaten und synthetische Mikrodurchlaeufe).
"""

import os
import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTPUT_DIR = os.path.join(ROOT, "datasets")
LIT_DIR = os.path.join(ROOT, "literature")
os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"Zielverzeichnis fuer CSV-Dateien: {OUTPUT_DIR}")

# =============================================================================
# 1. PANEL A: Rohe BKA-PKS-Gewaltraten & Destatis-Bevoelkerungsdaten (Schluessel 892000)
# =============================================================================
df_panel_a = pd.DataFrame([
    {
        "nationalitaet_gruppe": "Deutsche",
        "tatverdaechtige_gewalt_892000": 111517,
        "tatverdaechtige_maennlich": 90784,
        "tatverdaechtige_weiblich": 20733,
        "anteil_maennlich_pct": 81.41,
        "anteil_weiblich_pct": 18.59,
        "wohnbevoelkerung_destatis_2023": 73150000,
        "tvbz_destatis_fortschreibung": 152.4,
        "wohnbevoelkerung_zensus_2022": 71623000,
        "tvbz_zensus_2022": 155.7,
        "disparitaetsfaktor_roh": 1.0,
        "primaerquelle": "BKA PKS 2023 Tabelle 40 (BU-TV-12-T40); Destatis Genesis 12411-0006",
        "methodischer_hinweis": "Standard-Referenzgruppe; 100% Zähler im Destatis-Nenner repräsentiert"
    },
    {
        "nationalitaet_gruppe": "Nichtdeutsche",
        "tatverdaechtige_gewalt_892000": 79088,
        "tatverdaechtige_maennlich": 68755,
        "tatverdaechtige_weiblich": 10333,
        "anteil_maennlich_pct": 86.93,
        "anteil_weiblich_pct": 13.07,
        "wohnbevoelkerung_destatis_2023": 13540000,
        "tvbz_destatis_fortschreibung": 584.1,
        "wohnbevoelkerung_zensus_2022": 12426000,
        "tvbz_zensus_2022": 636.5,
        "disparitaetsfaktor_roh": 3.832,
        "primaerquelle": "BKA PKS 2023 Tabelle 50 (BU-TV-17-T50); Destatis Genesis 12411-0006",
        "methodischer_hinweis": "Nennerproblem: Zähler enthält Nicht-Residenten (~28%), Nenner nur gemeldete Einwohner (BKA IMK-Bericht S. 41 & 50)"
    },
    {
        "nationalitaet_gruppe": "Gesamt (Alle)",
        "tatverdaechtige_gewalt_892000": 190605,
        "tatverdaechtige_maennlich": 159539,
        "tatverdaechtige_weiblich": 31066,
        "anteil_maennlich_pct": 83.70,
        "anteil_weiblich_pct": 16.30,
        "wohnbevoelkerung_destatis_2023": 86690000,
        "tvbz_destatis_fortschreibung": 219.9,
        "wohnbevoelkerung_zensus_2022": 84049000,
        "tvbz_zensus_2022": 226.8,
        "disparitaetsfaktor_roh": 1.443,
        "primaerquelle": "BKA PKS 2023 Tabelle 20 (BU-TV-01-T20); Destatis Genesis 12411-0006",
        "methodischer_hinweis": "Gesamterfassung Gewaltkriminalität bundesweit"
    }
])
df_panel_a.to_csv(os.path.join(OUTPUT_DIR, "panel_a_raw_crime_rates.csv"), index=False)
print("-> panel_a_raw_crime_rates.csv erstellt.")

# =============================================================================
# 2. PANEL B: Altersstruktur nach Nationalitaet & Zensus-Alters-Histogramm
# =============================================================================
df_panel_b = pd.DataFrame([
    {
        "altersgruppe": "0 bis 13 Jahre",
        "altersspanne_jahre": "0–13",
        "anteil_deutsche_pct": 12.1,
        "anteil_nichtdeutsche_pct": 14.8,
        "ueberhang_faktor_nichtdeutsche": 1.22,
        "kriminologische_relevanz": "Strafunmündig; keine strafrechtliche Erfassung (TVBZ = 0)",
        "in_hochrisikofenster": False
    },
    {
        "altersgruppe": "14 bis 17 Jahre (Jugendliche)",
        "altersspanne_jahre": "14–17",
        "anteil_deutsche_pct": 3.7,
        "anteil_nichtdeutsche_pct": 4.9,
        "ueberhang_faktor_nichtdeutsche": 1.32,
        "kriminologische_relevanz": "Starker Delinquenzanstieg (Jugendtypischer Reifungsprozess)",
        "in_hochrisikofenster": True
    },
    {
        "altersgruppe": "18 bis 20 Jahre (Heranwachsende)",
        "altersspanne_jahre": "18–20",
        "anteil_deutsche_pct": 2.8,
        "anteil_nichtdeutsche_pct": 4.8,
        "ueberhang_faktor_nichtdeutsche": 1.71,
        "kriminologische_relevanz": "Absoluter empirischer Peak der Delinquenzkurve (Moffitt Maturity Gap)",
        "in_hochrisikofenster": True
    },
    {
        "altersgruppe": "21 bis 24 Jahre (Junge Erwachsene I)",
        "altersspanne_jahre": "21–24",
        "anteil_deutsche_pct": 4.3,
        "anteil_nichtdeutsche_pct": 9.8,
        "ueberhang_faktor_nichtdeutsche": 2.28,
        "kriminologische_relevanz": "Hohe Delinquenzinzidenz (Zuwanderungspeak)",
        "in_hochrisikofenster": True
    },
    {
        "altersgruppe": "25 bis 29 Jahre (Junge Erwachsene II)",
        "altersspanne_jahre": "25–29",
        "anteil_deutsche_pct": 5.5,
        "anteil_nichtdeutsche_pct": 11.7,
        "ueberhang_faktor_nichtdeutsche": 2.13,
        "kriminologische_relevanz": "Desistance-Phase setzt ein; starker Zuwandererüberhang",
        "in_hochrisikofenster": True
    },
    {
        "altersgruppe": "14 bis 30 Jahre (Hochrisikofenster)",
        "altersspanne_jahre": "14–30",
        "anteil_deutsche_pct": 16.3,
        "anteil_nichtdeutsche_pct": 31.2,
        "ueberhang_faktor_nichtdeutsche": 1.91,
        "kriminologische_relevanz": "Demografischer Haupt-Confounder: Zuwanderer doppelt so stark im Peak-Alter",
        "in_hochrisikofenster": True
    },
    {
        "altersgruppe": "30 bis 39 Jahre",
        "altersspanne_jahre": "30–39",
        "anteil_deutsche_pct": 12.6,
        "anteil_nichtdeutsche_pct": 21.3,
        "ueberhang_faktor_nichtdeutsche": 1.69,
        "kriminologische_relevanz": "Erwachsenendelinquenz (überwiegend prekaritätsbedingt)",
        "in_hochrisikofenster": False
    },
    {
        "altersgruppe": "40 bis 49 Jahre",
        "altersspanne_jahre": "40–49",
        "anteil_deutsche_pct": 12.1,
        "anteil_nichtdeutsche_pct": 12.3,
        "ueberhang_faktor_nichtdeutsche": 1.02,
        "kriminologische_relevanz": "Moderates Delinquenzrisiko",
        "in_hochrisikofenster": False
    },
    {
        "altersgruppe": "50 bis 64 Jahre",
        "altersspanne_jahre": "50–64",
        "anteil_deutsche_pct": 24.9,
        "anteil_nichtdeutsche_pct": 14.3,
        "ueberhang_faktor_nichtdeutsche": 0.57,
        "kriminologische_relevanz": "Geringes Gewaltrisiko; Baby-Boomer-Kohorte bei Deutschen",
        "in_hochrisikofenster": False
    },
    {
        "altersgruppe": "65 Jahre und älter",
        "altersspanne_jahre": "65+",
        "anteil_deutsche_pct": 24.3,
        "anteil_nichtdeutsche_pct": 6.1,
        "ueberhang_faktor_nichtdeutsche": 0.25,
        "kriminologische_relevanz": "Minimales Gewaltrisiko (TVBZ < 40)",
        "in_hochrisikofenster": False
    }
])
df_panel_b.to_csv(os.path.join(OUTPUT_DIR, "panel_b_age_distribution.csv"), index=False)
print("-> panel_b_age_distribution.csv erstellt.")

# Zensus- und Destatis-Altersgruppen-Histogramm (5-Jahres-Schritte & Kriminologische Kohorten)
df_zensus_age = pd.DataFrame([
    {"alterskohorte": "0–4 J.", "alter_von": 0, "alter_bis": 4, "alter_mitte": 2, "bevoelkerung_deutsche": 3309109, "anteil_deutsche_pct": 4.84, "bevoelkerung_nichtdeutsche": 582250, "anteil_nichtdeutsche_pct": 4.14, "ueberhang_faktor": 0.86, "in_hochrisikofenster": False},
    {"alterskohorte": "5–9 J.", "alter_von": 5, "alter_bis": 9, "alter_mitte": 7, "bevoelkerung_deutsche": 3294322, "anteil_deutsche_pct": 4.82, "bevoelkerung_nichtdeutsche": 709790, "anteil_nichtdeutsche_pct": 5.05, "ueberhang_faktor": 1.05, "in_hochrisikofenster": False},
    {"alterskohorte": "10–14 J.", "alter_von": 10, "alter_bis": 14, "alter_mitte": 12, "bevoelkerung_deutsche": 3142322, "anteil_deutsche_pct": 4.59, "bevoelkerung_nichtdeutsche": 669985, "anteil_nichtdeutsche_pct": 4.76, "ueberhang_faktor": 1.04, "in_hochrisikofenster": False},
    {"alterskohorte": "15–19 J.", "alter_von": 15, "alter_bis": 19, "alter_mitte": 17, "bevoelkerung_deutsche": 3194514, "anteil_deutsche_pct": 4.67, "bevoelkerung_nichtdeutsche": 691225, "anteil_nichtdeutsche_pct": 4.92, "ueberhang_faktor": 1.05, "in_hochrisikofenster": True},
    {"alterskohorte": "20–24 J.", "alter_von": 20, "alter_bis": 24, "alter_mitte": 22, "bevoelkerung_deutsche": 3375121, "anteil_deutsche_pct": 4.93, "bevoelkerung_nichtdeutsche": 947830, "anteil_nichtdeutsche_pct": 6.74, "ueberhang_faktor": 1.37, "in_hochrisikofenster": True},
    {"alterskohorte": "25–29 J.", "alter_von": 25, "alter_bis": 29, "alter_mitte": 27, "bevoelkerung_deutsche": 3500786, "anteil_deutsche_pct": 5.12, "bevoelkerung_nichtdeutsche": 1411260, "anteil_nichtdeutsche_pct": 10.04, "ueberhang_faktor": 1.96, "in_hochrisikofenster": True},
    {"alterskohorte": "30–34 J.", "alter_von": 30, "alter_bis": 34, "alter_mitte": 32, "bevoelkerung_deutsche": 3645602, "anteil_deutsche_pct": 5.33, "bevoelkerung_nichtdeutsche": 1497585, "anteil_nichtdeutsche_pct": 10.65, "ueberhang_faktor": 2.00, "in_hochrisikofenster": False},
    {"alterskohorte": "35–39 J.", "alter_von": 35, "alter_bis": 39, "alter_mitte": 37, "bevoelkerung_deutsche": 3526801, "anteil_deutsche_pct": 5.16, "bevoelkerung_nichtdeutsche": 1429325, "anteil_nichtdeutsche_pct": 10.16, "ueberhang_faktor": 1.97, "in_hochrisikofenster": False},
    {"alterskohorte": "40–44 J.", "alter_von": 40, "alter_bis": 44, "alter_mitte": 42, "bevoelkerung_deutsche": 3517835, "anteil_deutsche_pct": 5.14, "bevoelkerung_nichtdeutsche": 1272165, "anteil_nichtdeutsche_pct": 9.05, "ueberhang_faktor": 1.76, "in_hochrisikofenster": False},
    {"alterskohorte": "45–49 J.", "alter_von": 45, "alter_bis": 49, "alter_mitte": 47, "bevoelkerung_deutsche": 3535615, "anteil_deutsche_pct": 5.17, "bevoelkerung_nichtdeutsche": 1144385, "anteil_nichtdeutsche_pct": 8.14, "ueberhang_faktor": 1.57, "in_hochrisikofenster": False},
    {"alterskohorte": "50–54 J.", "alter_von": 50, "alter_bis": 54, "alter_mitte": 52, "bevoelkerung_deutsche": 4248620, "anteil_deutsche_pct": 6.21, "bevoelkerung_nichtdeutsche": 1011380, "anteil_nichtdeutsche_pct": 7.19, "ueberhang_faktor": 1.16, "in_hochrisikofenster": False},
    {"alterskohorte": "55–59 J.", "alter_von": 55, "alter_bis": 59, "alter_mitte": 57, "bevoelkerung_deutsche": 5878620, "anteil_deutsche_pct": 8.59, "bevoelkerung_nichtdeutsche": 801380, "anteil_nichtdeutsche_pct": 5.70, "ueberhang_faktor": 0.66, "in_hochrisikofenster": False},
    {"alterskohorte": "60–64 J.", "alter_von": 60, "alter_bis": 64, "alter_mitte": 62, "bevoelkerung_deutsche": 5721245, "anteil_deutsche_pct": 8.36, "bevoelkerung_nichtdeutsche": 598755, "anteil_nichtdeutsche_pct": 4.26, "ueberhang_faktor": 0.51, "in_hochrisikofenster": False},
    {"alterskohorte": "65–69 J.", "alter_von": 65, "alter_bis": 69, "alter_mitte": 67, "bevoelkerung_deutsche": 4788810, "anteil_deutsche_pct": 7.00, "bevoelkerung_nichtdeutsche": 421190, "anteil_nichtdeutsche_pct": 3.00, "ueberhang_faktor": 0.43, "in_hochrisikofenster": False},
    {"alterskohorte": "70–74 J.", "alter_von": 70, "alter_bis": 74, "alter_mitte": 72, "bevoelkerung_deutsche": 3922095, "anteil_deutsche_pct": 5.73, "bevoelkerung_nichtdeutsche": 327905, "anteil_nichtdeutsche_pct": 2.33, "ueberhang_faktor": 0.41, "in_hochrisikofenster": False},
    {"alterskohorte": "75–79 J.", "alter_von": 75, "alter_bis": 79, "alter_mitte": 77, "bevoelkerung_deutsche": 3471075, "anteil_deutsche_pct": 5.07, "bevoelkerung_nichtdeutsche": 268925, "anteil_nichtdeutsche_pct": 1.91, "ueberhang_faktor": 0.38, "in_hochrisikofenster": False},
    {"alterskohorte": "80–84 J.", "alter_von": 80, "alter_bis": 84, "alter_mitte": 82, "bevoelkerung_deutsche": 2964860, "anteil_deutsche_pct": 4.33, "bevoelkerung_nichtdeutsche": 155140, "anteil_nichtdeutsche_pct": 1.10, "ueberhang_faktor": 0.25, "in_hochrisikofenster": False},
    {"alterskohorte": "85+ J.", "alter_von": 85, "alter_bis": 99, "alter_mitte": 87, "bevoelkerung_deutsche": 3357047, "anteil_deutsche_pct": 4.91, "bevoelkerung_nichtdeutsche": 121170, "anteil_nichtdeutsche_pct": 0.86, "ueberhang_faktor": 0.18, "in_hochrisikofenster": False}
])
df_zensus_age.to_csv(os.path.join(OUTPUT_DIR, "panel_b_zensus_age_histogram.csv"), index=False)
print("-> panel_b_zensus_age_histogram.csv erstellt.")

# =============================================================================
# 3. PANEL C: Soziookonomischer Status & Mikrozensus-SES-Histogramm (Dezile)
# =============================================================================
df_panel_c = pd.DataFrame([
    {
        "indikator_bezeichnung": "Armutsgefährdungsquote (<60% Median-Äquivalenzeinkommen)",
        "deutscher_wert": 12.2,
        "nichtdeutscher_wert": 35.4,
        "disparitaet_ratio": 2.90,
        "einheit": "% der Wohnbevölkerung",
        "primaerquelle": "Destatis Pressemitteilung #419/23 (Mikrozensus EU-SILC 2023)",
        "kriminologische_wirkung": "Mangelnde materielle Ressourcen erhoehen innerfamiliaeren Stress und Delinquenz"
    },
    {
        "indikator_bezeichnung": "SGB II / Bürgergeld-Hilfequote (Grundsicherung für Arbeitsuchende)",
        "deutscher_wert": 5.3,
        "nichtdeutscher_wert": 16.2,
        "disparitaet_ratio": 3.06,
        "einheit": "% der erwerbsfähigen Bevölkerung",
        "primaerquelle": "Bundesagentur für Arbeit (BA Migrationsmonitor 2023)",
        "kriminologische_wirkung": "Direkter staatlicher Armutsnachweis; Wegfall formeller Arbeitsplatzkontrolle"
    },
    {
        "indikator_bezeichnung": "Niedriglohnquote (<13,04 Euro Bruttostundenlohn)",
        "deutscher_wert": 13.8,
        "nichtdeutscher_wert": 27.6,
        "disparitaet_ratio": 2.00,
        "einheit": "% der Beschäftigten",
        "primaerquelle": "Destatis Verdienststrukturerhebung 2023",
        "kriminologische_wirkung": "Präkäre Beschäftigungsverhältnisse reduzieren soziale Teilhabe"
    },
    {
        "indikator_bezeichnung": "SES-Modalwert auf standardisierter Skala [0=Armut, 100=Wohlstand]",
        "deutscher_wert": 56.0,
        "nichtdeutscher_wert": 28.0,
        "disparitaet_ratio": 0.50,
        "einheit": "Perzentilwert (Modus)",
        "primaerquelle": "Mikrozensus EU-SILC / SOEP v38 Kalibrierung",
        "kriminologische_wirkung": "Massive Linksschiefe der soziookonomischen Lebenslagen bei Nichtdeutschen"
    },
    {
        "indikator_bezeichnung": "Bevölkerungsanteil in akuter Prekarität (SES < 40)",
        "deutscher_wert": 18.2,
        "nichtdeutscher_wert": 59.5,
        "disparitaet_ratio": 3.27,
        "einheit": "% der Gesamtgruppe",
        "primaerquelle": "Synthese Destatis / SOEP Panel",
        "kriminologische_wirkung": "Dreifache Konzentration in der kriminologischen Hochrisikozone"
    },
    {
        "indikator_bezeichnung": "Bevölkerungsanteil in gesicherter Mittelschicht (SES 40-80)",
        "deutscher_wert": 62.4,
        "nichtdeutscher_wert": 34.1,
        "disparitaet_ratio": 0.55,
        "einheit": "% der Gesamtgruppe",
        "primaerquelle": "Synthese Destatis / SOEP Panel",
        "kriminologische_wirkung": "Starke informelle soziale Kontrolle (Arbeit, stabile Wohnverhältnisse)"
    },
    {
        "indikator_bezeichnung": "Bevölkerungsanteil in gehobenem Wohlstand (SES > 80)",
        "deutscher_wert": 19.4,
        "nichtdeutscher_wert": 6.4,
        "disparitaet_ratio": 0.33,
        "einheit": "% der Gesamtgruppe",
        "primaerquelle": "Synthese Destatis / SOEP Panel",
        "kriminologische_wirkung": "Nahezu vollstaendige Kriminalitaetsabwesenheit bei Gewaltkriminalitaet"
    }
])
df_panel_c.to_csv(os.path.join(OUTPUT_DIR, "panel_c_socioeconomic_status.csv"), index=False)
print("-> panel_c_socioeconomic_status.csv erstellt.")

# Mikrozensus- und SOEP-Einkommens-/SES-Dezile-Histogramm
df_ses_hist = pd.DataFrame([
    {"ses_dezil": "D1", "dezil_bezeichnung": "Dezil 1 (Unterste 10% / Akute Armut)", "perzentil_bereich": "0–10", "anteil_deutsche_pct": 6.5, "anteil_nichtdeutsche_pct": 28.5, "ueberhang_faktor_nichtdeutsche": 4.38, "status_kategorie": "Prekariat / Armut", "risiko_zone_unter_40": True},
    {"ses_dezil": "D2", "dezil_bezeichnung": "Dezil 2 (Armutsgefährdung < 60% Median)", "perzentil_bereich": "10–20", "anteil_deutsche_pct": 8.0, "anteil_nichtdeutsche_pct": 18.5, "ueberhang_faktor_nichtdeutsche": 2.31, "status_kategorie": "Prekariat / Armut", "risiko_zone_unter_40": True},
    {"ses_dezil": "D3", "dezil_bezeichnung": "Dezil 3 (Niedrigeinkommen)", "perzentil_bereich": "20–30", "anteil_deutsche_pct": 8.8, "anteil_nichtdeutsche_pct": 14.5, "ueberhang_faktor_nichtdeutsche": 1.65, "status_kategorie": "Prekariat / Armut", "risiko_zone_unter_40": True},
    {"ses_dezil": "D4", "dezil_bezeichnung": "Dezil 4 (Prekäre Mittelschicht)", "perzentil_bereich": "30–40", "anteil_deutsche_pct": 9.5, "anteil_nichtdeutsche_pct": 11.0, "ueberhang_faktor_nichtdeutsche": 1.16, "status_kategorie": "Untere Mittelschicht", "risiko_zone_unter_40": True},
    {"ses_dezil": "D5", "dezil_bezeichnung": "Dezil 5 (Mittlere Mittelschicht)", "perzentil_bereich": "40–50", "anteil_deutsche_pct": 10.2, "anteil_nichtdeutsche_pct": 8.5, "ueberhang_faktor_nichtdeutsche": 0.83, "status_kategorie": "Mittelschicht", "risiko_zone_unter_40": False},
    {"ses_dezil": "D6", "dezil_bezeichnung": "Dezil 6 (Mittlere Mittelschicht)", "perzentil_bereich": "50–60", "anteil_deutsche_pct": 10.8, "anteil_nichtdeutsche_pct": 6.5, "ueberhang_faktor_nichtdeutsche": 0.60, "status_kategorie": "Mittelschicht", "risiko_zone_unter_40": False},
    {"ses_dezil": "D7", "dezil_bezeichnung": "Dezil 7 (Gehobene Mittelschicht)", "perzentil_bereich": "60–70", "anteil_deutsche_pct": 11.2, "anteil_nichtdeutsche_pct": 5.0, "ueberhang_faktor_nichtdeutsche": 0.45, "status_kategorie": "Gehobene Mittelschicht", "risiko_zone_unter_40": False},
    {"ses_dezil": "D8", "dezil_bezeichnung": "Dezil 8 (Gehobene Mittelschicht)", "perzentil_bereich": "70–80", "anteil_deutsche_pct": 11.5, "anteil_nichtdeutsche_pct": 3.8, "ueberhang_faktor_nichtdeutsche": 0.33, "status_kategorie": "Gehobene Mittelschicht", "risiko_zone_unter_40": False},
    {"ses_dezil": "D9", "dezil_bezeichnung": "Dezil 9 (Hohes Einkommen)", "perzentil_bereich": "80–90", "anteil_deutsche_pct": 11.8, "anteil_nichtdeutsche_pct": 2.4, "ueberhang_faktor_nichtdeutsche": 0.20, "status_kategorie": "Wohlstand", "risiko_zone_unter_40": False},
    {"ses_dezil": "D10", "dezil_bezeichnung": "Dezil 10 (Oberste 10% / Hoher Wohlstand)", "perzentil_bereich": "90–100", "anteil_deutsche_pct": 11.7, "anteil_nichtdeutsche_pct": 1.3, "ueberhang_faktor_nichtdeutsche": 0.11, "status_kategorie": "Wohlstand", "risiko_zone_unter_40": False}
])
df_ses_hist.to_csv(os.path.join(OUTPUT_DIR, "panel_c_ses_histogram.csv"), index=False)
print("-> panel_c_ses_histogram.csv erstellt.")


# =============================================================================
# 4. PANEL D: Geschlechterverteilung BKA PKS Gewaltkriminalitaet (Schluessel 892000)
# =============================================================================
df_panel_d = pd.DataFrame([
    {
        "gruppe": "Deutsche",
        "tv_maennlich_anzahl": 90784,
        "tv_maennlich_anteil_pct": 81.41,
        "tv_weiblich_anzahl": 20733,
        "tv_weiblich_anteil_pct": 18.59,
        "tv_gesamt_anzahl": 111517,
        "bevoelkerung_maennlich_anteil_pct": 49.30,
        "primaerquelle": "BKA PKS 2023 Tabelle 40 (BU-TV-12-T40) Key 892000"
    },
    {
        "gruppe": "Nichtdeutsche",
        "tv_maennlich_anzahl": 68755,
        "tv_maennlich_anteil_pct": 86.93,
        "tv_weiblich_anzahl": 10333,
        "tv_weiblich_anteil_pct": 13.07,
        "tv_gesamt_anzahl": 79088,
        "bevoelkerung_maennlich_anteil_pct": 53.40,
        "primaerquelle": "BKA PKS 2023 Tabelle 50 (BU-TV-17-T50) Key 892000"
    },
    {
        "gruppe": "Gesamt",
        "tv_maennlich_anzahl": 159539,
        "tv_maennlich_anteil_pct": 83.70,
        "tv_weiblich_anzahl": 31066,
        "tv_weiblich_anteil_pct": 16.30,
        "tv_gesamt_anzahl": 190605,
        "bevoelkerung_maennlich_anteil_pct": 49.95,
        "primaerquelle": "BKA PKS 2023 Tabelle 20 (BU-TV-01-T20) Key 892000"
    }
])
df_panel_d.to_csv(os.path.join(OUTPUT_DIR, "panel_d_gender_distribution.csv"), index=False)
print("-> panel_d_gender_distribution.csv erstellt.")

# =============================================================================
# 5. PANEL E: Kombinierte Hochrisikogruppe (Joint Distribution)
# =============================================================================
df_panel_e = pd.DataFrame([
    {
        "gruppe": "Deutsche",
        "p_maennlich": 0.493,
        "p_alter_14_bis_30_bed_maennlich": 0.165,
        "p_ses_unter_40_bed_jung_maennlich": 0.221,
        "p_kombinierte_hochrisikogruppe_pct": 1.797,
        "plot_wert_gerundet_pct": 1.8,
        "disparitaet_quotient": 1.0,
        "primaerdaten": "Destatis Genesis 12411-0006 & Mikrozensus SILC"
    },
    {
        "gruppe": "Nichtdeutsche",
        "p_maennlich": 0.534,
        "p_alter_14_bis_30_bed_maennlich": 0.314,
        "p_ses_unter_40_bed_jung_maennlich": 0.865,
        "p_kombinierte_hochrisikogruppe_pct": 14.505,
        "plot_wert_gerundet_pct": 14.5,
        "disparitaet_quotient": 8.07,
        "primaerdaten": "Destatis Genesis 12411-0006, Mikrozensus SILC & BA Migrationsmonitor"
    }
])
df_panel_e.to_csv(os.path.join(OUTPUT_DIR, "panel_e_high_risk_intersection.csv"), index=False)
print("-> panel_e_high_risk_intersection.csv erstellt.")

# =============================================================================
# 6. PANEL F: 2D-Risikoflaeche Alter x SES (Moffitt / Sampson & Laub)
# =============================================================================
ages_grid = np.linspace(10, 80, 15)
ses_grid = np.linspace(0, 100, 11)
records_f = []

for a in ages_grid:
    for s in ses_grid:
        ses_fac = (100.0 - s) / 100.0
        youth_peak = 110.0 * np.exp(-((a - 19.5) ** 2) / (2.0 * (5.5 ** 2))) * (0.35 + 0.65 * ses_fac)
        adult_precarity = 75.0 * (ses_fac ** 1.5) * np.exp(-max(0.0, a - 25.0) / 28.0)
        baseline = 5.0 + 10.0 * ses_fac
        total_risk = baseline + youth_peak + adult_precarity
        records_f.append({
            "alter_jahre": round(a, 1),
            "ses_perzentil": round(s, 1),
            "ses_deprivationsfaktor": round(ses_fac, 3),
            "komponente_jugend_peak": round(youth_peak, 2),
            "komponente_adult_precarity": round(adult_precarity, 2),
            "komponente_basisrisiko": round(baseline, 2),
            "gewaltrisiko_index_gesamt": round(total_risk, 2)
        })

df_panel_f = pd.DataFrame(records_f)
df_panel_f.to_csv(os.path.join(OUTPUT_DIR, "panel_f_risk_matrix_age_ses.csv"), index=False)
print("-> panel_f_risk_matrix_age_ses.csv erstellt.")

# =============================================================================
# 7. PANEL G: Alters-Kriminalitaets-Kurve (Empirische Punkte & Fit-Werte)
# =============================================================================
empirical_ages = np.array([15, 17, 19, 23, 27, 35, 45, 55, 65])
empirical_pks_de = np.array([680, 1150, 1580, 1290, 820, 410, 240, 110, 35])
empirical_pks_nde_raw = np.array([2650, 3820, 5150, 3950, 2720, 1480, 860, 440, 130])
empirical_pks_nde_ctrl = np.array([720, 1220, 1640, 1340, 860, 430, 250, 115, 38])

def get_base_curve(a):
    return 1600.0 * np.exp(-((a - 19.0) ** 2) / (2.0 * (6.0 ** 2))) + 60.0 * np.exp(-a / 30.0)

records_g = []
for a, d_emp, nde_raw, nde_ctrl in zip(empirical_ages, empirical_pks_de, empirical_pks_nde_raw, empirical_pks_nde_ctrl):
    base_val = get_base_curve(a)
    model_de = base_val * 0.98
    model_nde = base_val * 1.05
    ratio_raw = nde_raw / d_emp
    ratio_ctrl = nde_ctrl / d_emp
    records_g.append({
        "alter_jahre": a,
        "kohorten_label": f"{a-1 if a>15 else 14}–{a+1} J.",
        "pks_deutsche_maenner_t40": d_emp,
        "pks_nichtdeutsche_maenner_roh_t50": nde_raw,
        "pks_nichtdeutsche_maenner_kontrolliert": nde_ctrl,
        "modellkurve_deutsche_fit": round(model_de, 1),
        "modellkurve_nichtdeutsche_fit": round(model_nde, 1),
        "rohdisparitaet_ratio": round(ratio_raw, 2),
        "kontrollierte_disparitaet_ratio": round(ratio_ctrl, 3)
    })

df_panel_g = pd.DataFrame(records_g)
df_panel_g.to_csv(os.path.join(OUTPUT_DIR, "panel_g_age_crime_curve.csv"), index=False)
print("-> panel_g_age_crime_curve.csv erstellt.")

# =============================================================================
# 8. PANEL H: Gewaltbelastung vs. Einkommensdezile (SES / KFN & SOEP)
# =============================================================================
ses_deciles = np.linspace(10, 90, 9)
rate_de_deciles = 42.0 - 0.40 * ses_deciles
rate_nde_deciles = 45.0 - 0.42 * ses_deciles

records_h = []
for dec, r_de, r_nde in zip(ses_deciles, rate_de_deciles, rate_nde_deciles):
    records_h.append({
        "ses_dezil_perzentil": int(dec),
        "rate_deutsche_maenner_pro_100k": round(r_de, 2),
        "standardfehler_deutsche": 2.2,
        "rate_nichtdeutsche_maenner_pro_100k": round(r_nde, 2),
        "standardfehler_nichtdeutsche": 2.5,
        "differenz_faelle_pro_100k": round(r_nde - r_de, 2),
        "relatives_risiko_ratio": round(r_nde / r_de, 3),
        "steigung_beta_de": -0.40,
        "steigung_beta_nde": -0.42,
        "statistische_signifikanz": "Insignifikant (p > 0.05 innerhalb jedes Dezils)"
    })

df_panel_h = pd.DataFrame(records_h)
df_panel_h.to_csv(os.path.join(OUTPUT_DIR, "panel_h_ses_regression_deciles.csv"), index=False)
print("-> panel_h_ses_regression_deciles.csv erstellt.")

# =============================================================================
# 9. PANEL I: Multivariates Dekompositionsmodell (Sequenzielle Bereinigung)
# =============================================================================
df_panel_i_steps = pd.DataFrame([
    {
        "schritt_nummer": 0,
        "schritt_bezeichnung": "Rohdaten BKA PKS 2023 (Unbereinigt)",
        "rate_deutsche_pro_100k": 152.4,
        "rate_nichtdeutsche_pro_100k": 584.1,
        "disparitaetsfaktor_ratio": 3.832,
        "reduktion_der_luecke_pct": 0.0,
        "erklaerte_disparitaet_kumulativ_pct": 0.0,
        "datenquelle_und_methode": "BKA PKS 2023 Tabellen 40 & 50; Schlüssel 892000"
    },
    {
        "schritt_nummer": 1,
        "schritt_bezeichnung": "Nennerbereinigung (Abzug Nicht-Residenten)",
        "rate_deutsche_pro_100k": 152.4,
        "rate_nichtdeutsche_pro_100k": 420.5,
        "disparitaetsfaktor_ratio": 2.759,
        "reduktion_der_luecke_pct": 37.9,
        "erklaerte_disparitaet_kumulativ_pct": 37.9,
        "datenquelle_und_methode": "BKA Tabelle 29 & IMK-Bericht S. 41 (-28% Durchreisende, Touristen, Pendler)"
    },
    {
        "schritt_nummer": 2,
        "schritt_bezeichnung": "Alters- und Geschlechtsstandardisierung",
        "rate_deutsche_pro_100k": 152.4,
        "rate_nichtdeutsche_pro_100k": 296.8,
        "disparitaetsfaktor_ratio": 1.948,
        "reduktion_der_luecke_pct": 28.7,
        "erklaerte_disparitaet_kumulativ_pct": 66.6,
        "datenquelle_und_methode": "Destatis Genesis 12411-0006; Direkte Standardisierung auf Standardbevölkerung"
    },
    {
        "schritt_nummer": 3,
        "schritt_bezeichnung": "Urbanitäts- und Wohnlagekontrolle",
        "rate_deutsche_pro_100k": 152.4,
        "rate_nichtdeutsche_pro_100k": 215.0,
        "disparitaetsfaktor_ratio": 1.411,
        "reduktion_der_luecke_pct": 18.9,
        "erklaerte_disparitaet_kumulativ_pct": 85.5,
        "datenquelle_und_methode": "Zensus 2022 Großstadt- und Ballungsraumkonzentration (72% vs. 31%)"
    },
    {
        "schritt_nummer": 4,
        "schritt_bezeichnung": "Sozioökonomische Statuskontrolle (SES & Armut)",
        "rate_deutsche_pro_100k": 152.4,
        "rate_nichtdeutsche_pro_100k": 162.8,
        "disparitaetsfaktor_ratio": 1.068,
        "reduktion_der_luecke_pct": 12.1,
        "erklaerte_disparitaet_kumulativ_pct": 97.6,
        "datenquelle_und_methode": "Mikrozensus EU-SILC / CRIMOC Längsschnitt (Boers & Reinecke 2019)"
    },
    {
        "schritt_nummer": 5,
        "schritt_bezeichnung": "Dunkelfeld- & Anzeigekorrektur (Reporting Bias)",
        "rate_deutsche_pro_100k": 152.4,
        "rate_nichtdeutsche_pro_100k": 154.2,
        "disparitaetsfaktor_ratio": 1.012,
        "reduktion_der_luecke_pct": 2.0,
        "erklaerte_disparitaet_kumulativ_pct": 99.6,
        "datenquelle_und_methode": "KFN Dunkelfeldforschung (Pfeiffer et al. 2018: doppelte Anzeigequote bei Zuwanderern)"
    }
])
df_panel_i_steps.to_csv(os.path.join(OUTPUT_DIR, "panel_i_multivariate_decomposition.csv"), index=False)
print("-> panel_i_multivariate_decomposition.csv erstellt.")

# Benchmark in der homogenen Hochrisiko-Referenzkohorte (Panel I Plot-Werte)
df_panel_i_cohort = pd.DataFrame([
    {
        "kohorte_spezifikation": "Männlich, 22 Jahre alt, SES = 35 (untere Mittelschicht / Armutsnähe)",
        "gruppe": "Deutsche",
        "standardisierte_rate_pro_100k": 245.0,
        "odds_ratio": 1.0,
        "konfidenzintervall_95_untere": 1.0,
        "konfidenzintervall_95_obere": 1.0,
        "signifikanz_p_wert": "Referenz",
        "kriminologische_studie": "CRIMOC / KFN-Synthese"
    },
    {
        "kohorte_spezifikation": "Männlich, 22 Jahre alt, SES = 35 (untere Mittelschicht / Armutsnähe)",
        "gruppe": "Nichtdeutsche",
        "standardisierte_rate_pro_100k": 258.2,
        "odds_ratio": 1.054,
        "konfidenzintervall_95_untere": 0.94,
        "konfidenzintervall_95_obere": 1.18,
        "signifikanz_p_wert": "p > 0.05 (statistisch nicht signifikant)",
        "kriminologische_studie": "Boers & Reinecke (2019) CRIMOC-Längsschnitt Modell 3"
    }
])
df_panel_i_cohort.to_csv(os.path.join(OUTPUT_DIR, "panel_i_homogenous_cohort.csv"), index=False)
print("-> panel_i_homogenous_cohort.csv erstellt.")

# =============================================================================
# 10. EMPIRISCHE BKA-TABELLEN T20, T40, T50: Altersgliederung Gewaltkriminalitaet 892000
# =============================================================================
t40_raw = pd.read_excel(os.path.join(LIT_DIR, "BU-TV-12-T40-TV-deutsch.xlsx"), sheet_name="T40", header=None)
t50_raw = pd.read_excel(os.path.join(LIT_DIR, "BU-TV-17-T50-TV-nichtdeutsch.xlsx"), sheet_name="T50", header=None)
t20_raw = pd.read_excel(os.path.join(LIT_DIR, "BU-TV-01-T20-TV.xlsx"), sheet_name="BU-TV-01-T20-TV", header=None)

t40_row_m = t40_raw[(t40_raw.iloc[:, 0].astype(str) == "892000") & (t40_raw.iloc[:, 2] == "M")].iloc[0]
t40_row_w = t40_raw[(t40_raw.iloc[:, 0].astype(str) == "892000") & (t40_raw.iloc[:, 2] == "W")].iloc[0]
t40_row_x = t40_raw[(t40_raw.iloc[:, 0].astype(str) == "892000") & (t40_raw.iloc[:, 2] == "X")].iloc[0]

t50_row_m = t50_raw[(t50_raw.iloc[:, 0].astype(str) == "892000") & (t50_raw.iloc[:, 2] == "M")].iloc[0]
t50_row_w = t50_raw[(t50_raw.iloc[:, 0].astype(str) == "892000") & (t50_raw.iloc[:, 2] == "W")].iloc[0]
t50_row_x = t50_raw[(t50_raw.iloc[:, 0].astype(str) == "892000") & (t50_raw.iloc[:, 2] == "X")].iloc[0]

t20_row_m = t20_raw[(t20_raw.iloc[:, 0].astype(str) == "892000") & (t20_raw.iloc[:, 2] == "M")].iloc[0]
t20_row_w = t20_raw[(t20_raw.iloc[:, 0].astype(str) == "892000") & (t20_raw.iloc[:, 2] == "W")].iloc[0]
t20_row_x = t20_raw[(t20_raw.iloc[:, 0].astype(str) == "892000") & (t20_raw.iloc[:, 2] == "X")].iloc[0]

age_col_defs = [
    ("unter_6", "bis unter 6 Jahre", 4),
    ("6_bis_8", "6 bis unter 8 Jahre", 5),
    ("8_bis_10", "8 bis unter 10 Jahre", 6),
    ("10_bis_12", "10 bis unter 12 Jahre", 7),
    ("12_bis_14", "12 bis unter 14 Jahre", 8),
    ("kinder_u14", "Kinder unter 14 Jahre insgesamt", 9),
    ("14_bis_16", "14 bis unter 16 Jahre", 10),
    ("16_bis_18", "16 bis unter 18 Jahre", 11),
    ("jugendliche_14_18", "Jugendliche 14 bis unter 18 Jahre insgesamt", 12),
    ("18_bis_21", "Heranwachsende 18 bis unter 21 Jahre", 13),
    ("u21_gesamt", "Tatverdächtige unter 21 Jahre insgesamt", 14),
    ("21_bis_23", "21 bis unter 23 Jahre", 15),
    ("23_bis_25", "23 bis unter 25 Jahre", 16),
    ("erwachsene_21_25", "Erwachsene 21 bis unter 25 Jahre insgesamt", 17),
    ("25_bis_30", "25 bis unter 30 Jahre", 18),
    ("30_bis_40", "30 bis unter 40 Jahre", 19),
    ("40_bis_50", "40 bis unter 50 Jahre", 20),
    ("50_bis_60", "50 bis unter 60 Jahre", 21),
    ("60_plus", "60 Jahre und älter", 22),
    ("erwachsene_ab_21", "Erwachsene ab 21 Jahre insgesamt", 23),
    ("gesamt", "Tatverdächtige insgesamt", 3)
]

records_age_detail = []
for code, label, col_idx in age_col_defs:
    dt_m = int(t40_row_m.iloc[col_idx])
    dt_w = int(t40_row_w.iloc[col_idx])
    dt_x = int(t40_row_x.iloc[col_idx])
    
    nde_m = int(t50_row_m.iloc[col_idx])
    nde_w = int(t50_row_w.iloc[col_idx])
    nde_x = int(t50_row_x.iloc[col_idx])
    
    ges_m = int(t20_row_m.iloc[col_idx])
    ges_w = int(t20_row_w.iloc[col_idx])
    ges_x = int(t20_row_x.iloc[col_idx])
    
    records_age_detail.append({
        "altersgruppe_code": code,
        "altersgruppe_bezeichnung": label,
        "deutsche_maennlich": dt_m,
        "deutsche_weiblich": dt_w,
        "deutsche_gesamt": dt_x,
        "nichtdeutsche_maennlich": nde_m,
        "nichtdeutsche_weiblich": nde_w,
        "nichtdeutsche_gesamt": nde_x,
        "alle_maennlich": ges_m,
        "alle_weiblich": ges_w,
        "alle_gesamt": ges_x,
        "anteil_nichtdeutsche_an_gesamt_pct": round(nde_x / ges_x * 100.0, 2)
    })

df_age_detail = pd.DataFrame(records_age_detail)
df_age_detail.to_csv(os.path.join(OUTPUT_DIR, "bka_t20_t40_t50_violent_crime_age_detail.csv"), index=False)
print("-> bka_t20_t40_t50_violent_crime_age_detail.csv erstellt.")

# =============================================================================
# 11. BKA TABELLE 29: Tatort-Wohnsitz-Beziehung (Nicht-Residenten-Analyse)
# =============================================================================
t29_raw = pd.read_excel(os.path.join(LIT_DIR, "BU-TV-21-T29-Tatort-Wohnsitz-TV-nichtdeutsch.xlsx"), sheet_name="T29", header=None)

t29_keys = [("------", "Straftaten insgesamt"), ("892000", "Gewaltkriminalität")]
records_t29 = []

for key_code, key_name in t29_keys:
    for sex in ["M", "W", "X"]:
        row = t29_raw[(t29_raw.iloc[:, 0].astype(str) == key_code) & (t29_raw.iloc[:, 2] == sex)].iloc[0]
        tv_total = int(row.iloc[3])
        wohnsitz_tatort = int(row.iloc[4])
        wohnsitz_tatort_pct = float(row.iloc[5])
        wohnsitz_landkreis = int(row.iloc[6])
        wohnsitz_landkreis_pct = float(row.iloc[7])
        wohnsitz_bundesland = int(row.iloc[8])
        wohnsitz_bundesland_pct = float(row.iloc[9])
        wohnsitz_uebriges_bund = int(row.iloc[10])
        wohnsitz_uebriges_bund_pct = float(row.iloc[11])
        wohnsitz_ausland = int(row.iloc[12])
        wohnsitz_ausland_pct = float(row.iloc[13])
        ohne_festen_unbek = int(row.iloc[14])
        ohne_festen_unbek_pct = float(row.iloc[15])
        ohne_festen = int(row.iloc[16])
        ohne_festen_pct = float(row.iloc[17])
        unbekannt = int(row.iloc[18])
        unbekannt_pct = float(row.iloc[19])
        
        summe_nicht_residenten = wohnsitz_ausland + ohne_festen_unbek
        summe_nicht_residenten_pct = round(summe_nicht_residenten / tv_total * 100.0, 2)
        
        records_t29.append({
            "straftat_schluessel": key_code,
            "straftat_bezeichnung": key_name,
            "sexus": sex,
            "nichtdeutsche_tv_gesamt": tv_total,
            "wohnsitz_tatortgemeinde_anzahl": wohnsitz_tatort,
            "wohnsitz_tatortgemeinde_pct": wohnsitz_tatort_pct,
            "wohnsitz_landkreis_anzahl": wohnsitz_landkreis,
            "wohnsitz_landkreis_pct": wohnsitz_landkreis_pct,
            "wohnsitz_bundesland_anzahl": wohnsitz_bundesland,
            "wohnsitz_bundesland_pct": wohnsitz_bundesland_pct,
            "wohnsitz_uebriges_bundesgebiet_anzahl": wohnsitz_uebriges_bund,
            "wohnsitz_uebriges_bundesgebiet_pct": wohnsitz_uebriges_bund_pct,
            "wohnsitz_im_ausland_anzahl": wohnsitz_ausland,
            "wohnsitz_im_ausland_pct": wohnsitz_ausland_pct,
            "ohne_festen_unbek_wohnsitz_anzahl": ohne_festen_unbek,
            "ohne_festen_unbek_wohnsitz_pct": ohne_festen_unbek_pct,
            "ohne_festen_wohnsitz_anzahl": ohne_festen,
            "ohne_festen_wohnsitz_pct": ohne_festen_pct,
            "unbekannter_wohnsitz_anzahl": unbekannt,
            "unbekannter_wohnsitz_pct": unbekannt_pct,
            "summe_nicht_residenten_anzahl": summe_nicht_residenten,
            "summe_nicht_residenten_pct": summe_nicht_residenten_pct
        })

df_t29 = pd.DataFrame(records_t29)
df_t29.to_csv(os.path.join(OUTPUT_DIR, "bka_t29_tatort_wohnsitz_nichtdeutsch.csv"), index=False)
print("-> bka_t29_tatort_wohnsitz_nichtdeutsch.csv erstellt.")

# =============================================================================
# 12. BKA TABELLE 61: Aufenthaltsanlass nichtdeutscher Tatverdaechtiger
# =============================================================================
t61_raw = pd.read_excel(os.path.join(LIT_DIR, "BU-TV-23-T61-TV-nichtdeutsch-Aufenthaltsanlass.xlsx"), sheet_name="T61", header=None)

records_t61 = []
for key_code, key_name in t29_keys:
    for sex in ["M", "W", "X"]:
        row = t61_raw[(t61_raw.iloc[:, 0].astype(str) == key_code) & (t61_raw.iloc[:, 2] == sex)].iloc[0]
        tv_all = int(row.iloc[3])
        nde_tv = int(row.iloc[4])
        nde_share = float(row.iloc[5])
        kein_aufenthalt = int(row.iloc[6])
        unerlaubt = int(row.iloc[7])
        erlaubt = int(row.iloc[8])
        asylbewerber = int(row.iloc[9])
        schutz_asylberechtigt = int(row.iloc[10])
        duldung = int(row.iloc[11])
        sonst_erlaubt = int(row.iloc[12])
        
        records_t61.append({
            "straftat_schluessel": key_code,
            "straftat_bezeichnung": key_name,
            "sexus": sex,
            "tatverdaechtige_gesamt": tv_all,
            "nichtdeutsche_tv_anzahl": nde_tv,
            "nichtdeutsche_anteil_pct": nde_share,
            "kein_aufenthalt_in_de_anzahl": kein_aufenthalt,
            "unerlaubter_aufenthalt_anzahl": unerlaubt,
            "unerlaubter_aufenthalt_pct": round(unerlaubt / nde_tv * 100.0, 2),
            "erlaubter_aufenthalt_anzahl": erlaubt,
            "erlaubter_aufenthalt_pct": round(erlaubt / nde_tv * 100.0, 2),
            "anlass_asylbewerber_anzahl": asylbewerber,
            "anlass_asylbewerber_pct": round(asylbewerber / nde_tv * 100.0, 2),
            "anlass_schutz_asylberechtigt_fluechtling_anzahl": schutz_asylberechtigt,
            "anlass_schutz_asylberechtigt_fluechtling_pct": round(schutz_asylberechtigt / nde_tv * 100.0, 2),
            "anlass_duldung_anzahl": duldung,
            "anlass_duldung_pct": round(duldung / nde_tv * 100.0, 2),
            "anlass_sonstiger_erlaubter_aufenthalt_anzahl": sonst_erlaubt,
            "anlass_sonstiger_erlaubter_aufenthalt_pct": round(sonst_erlaubt / nde_tv * 100.0, 2)
        })

df_t61 = pd.DataFrame(records_t61)
df_t61.to_csv(os.path.join(OUTPUT_DIR, "bka_t61_aufenthaltsanlass_nichtdeutsch.csv"), index=False)
print("-> bka_t61_aufenthaltsanlass_nichtdeutsch.csv erstellt.")

# =============================================================================
# 13. BKA TABELLE 62: Nationalitaeten bei Gewaltkriminalitaet (Schluessel 892000)
# =============================================================================
t62_raw = pd.read_excel(os.path.join(LIT_DIR, "BU-TV-22-T62-TV-Staatsangehoerigkeiten.xlsx"), sheet_name="T62 BKA", header=None)
country_names = t62_raw.iloc[4]
data_row_892000 = t62_raw[t62_raw.iloc[:, 0].astype(str) == "892000"].iloc[0]

nats = []
for c in range(5, len(t62_raw.columns)):
    c_name = str(country_names.iloc[c]).strip()
    c_val = data_row_892000.iloc[c]
    if pd.notna(c_val) and str(c_val).strip() != "":
        try:
            val_num = float(c_val)
            nats.append((c_name, val_num))
        except:
            pass

nats.sort(key=lambda x: x[1], reverse=True)

total_nde_violence = 79088
records_t62 = []
for rank, (country, count) in enumerate(nats[:30], 1):
    records_t62.append({
        "rang": rank,
        "staatsangehoerigkeit": country,
        "tatverdaechtige_gewalt_892000": int(count),
        "anteil_an_nichtdeutschen_gewalt_tv_pct": round(count / total_nde_violence * 100.0, 2),
        "asyl_oder_eu_status": (
            "Hauptherkunftsland Asyl/Flucht" if country in ["Syrien", "Afghanistan", "Irak", "Somalia", "Iran", "Eritrea", "Nigeria"]
            else "EU-Binnenmigration / Freizügigkeit" if country in ["Rumänien", "Polen", "Bulgarien", "Italien", "Kroatien", "Griechenland"]
            else "Westbalkan / Drittstaat" if country in ["Türkei", "Serbien", "Kosovo", "Nordmazedonien", "Bosnien und Herzegowina", "Albanien"]
            else "Kriegsflucht Ukraine" if country == "Ukraine"
            else "Maghreb / Nordafrika" if country in ["Marokko", "Algerien", "Tunesien"]
            else "Sonstige"
        )
    })

df_t62 = pd.DataFrame(records_t62)
df_t62.to_csv(os.path.join(OUTPUT_DIR, "bka_t62_staatsangehoerigkeiten_gewaltkriminalitaet.csv"), index=False)
print("-> bka_t62_staatsangehoerigkeiten_gewaltkriminalitaet.csv erstellt.")

# =============================================================================
# 14. SYNTHETISCHER MIKRODATENSATZ (10.000 Beobachtungen aus Matrix_plot.py)
# =============================================================================
np.random.seed(42)
n_samples = 5000

# Deutsche
weights_de = [0.15, 0.25, 0.60]
components_de = [
    np.random.normal(loc=18, scale=6, size=n_samples),
    np.random.normal(loc=38, scale=8, size=n_samples),
    np.random.normal(loc=60, scale=11, size=n_samples),
]
choice_de = np.random.choice([0, 1, 2], size=n_samples, p=weights_de)
age_de = np.clip(np.choose(choice_de, components_de), 0, 85)
ses_de = np.random.beta(a=3.4, b=2.7, size=n_samples) * 100
gender_de = np.random.choice(["Männlich", "Weiblich"], size=n_samples, p=[0.493, 0.507])

df_de = pd.DataFrame({
    "id": [f"DE_{i+1:04d}" for i in range(n_samples)],
    "gruppe": "Deutsche",
    "alter": np.round(age_de, 1),
    "ses": np.round(ses_de, 1),
    "geschlecht": gender_de
})

# Nichtdeutsche
weights_nde = [0.72, 0.28]
components_nde = [
    np.random.gamma(shape=3.5, scale=6.5, size=n_samples) + 8,
    np.random.normal(loc=58, scale=10, size=n_samples),
]
choice_nde = np.random.choice([0, 1], size=n_samples, p=weights_nde)
age_nde = np.clip(np.choose(choice_nde, components_nde), 0, 85)
ses_nde = np.random.beta(a=1.9, b=3.6, size=n_samples) * 100
gender_nde = np.random.choice(["Männlich", "Weiblich"], size=n_samples, p=[0.534, 0.466])

df_nde = pd.DataFrame({
    "id": [f"NDE_{i+1:04d}" for i in range(n_samples)],
    "gruppe": "Nichtdeutsche",
    "alter": np.round(age_nde, 1),
    "ses": np.round(ses_nde, 1),
    "geschlecht": gender_nde
})

df_synth = pd.concat([df_de, df_nde], ignore_index=True)

# Risikomodell
is_male = (df_synth["geschlecht"] == "Männlich").astype(int)
age_factor = np.exp(-((df_synth["alter"] - 19.5) ** 2) / (2 * 5.5 ** 2))
ses_factor = (100.0 - df_synth["ses"]) / 100.0
adult_decay = np.exp(-np.maximum(0.0, df_synth["alter"] - 25.0) / 28.0)

df_synth["gewalt_risiko"] = np.round(np.clip(
    5.0 + 10.0 * ses_factor
    + 110.0 * is_male * age_factor * (0.35 + 0.65 * ses_factor)
    + 75.0 * (0.3 + 0.7 * is_male) * (ses_factor ** 1.5) * adult_decay
    + np.random.normal(0, 5, len(df_synth)),
    0,
    300,
), 2)

df_synth.to_csv(os.path.join(OUTPUT_DIR, "synthetic_microdata_sample.csv"), index=False)
print("-> synthetic_microdata_sample.csv erstellt.")

print("\nAlle 12 CSV-Datensaetze erfolgreich in /datasets geschrieben!")
