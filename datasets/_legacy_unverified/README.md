# Quarantined Legacy Unverified Data & Scripts

> **STATUS: DEPRECATED & STRICTLY ISOLATED**

The contents of this directory (`datasets/_legacy_unverified/`) represent early exploratory prototypes and synthetic Gaussian scripts (e.g. `generate_datasets_UNVERIFIED.py`) that were quarantined during historical refactoring to ensure compliance with the **Responsible Empirical Research Protocol** (`SKILL.md`).

### Isolation Rules:
1. **Zero Pipeline Usage**: No production pipeline scripts (`src/data_preparation.py`, `src/modeling.py`) or automated audits (`audit_research_pipeline.py`, `audit_demographics.py`) ingest any data from this directory.
2. **Deterministic Empirical Data**: All active production datasets live in `/datasets/` and are derived deterministically from unmodified primary source files in `/rawdata/` and verified literature citations.
3. **Archival Purpose**: These files are preserved exclusively for internal audit trail completeness and historical version comparison.

