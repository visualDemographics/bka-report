---
name: parallel-literature-harvester
description: >-
  Orchestration protocol and subagent templates for parallelizing web searches, primary literature
  PDF acquisition, and raw dataset harvesting across multiple topics, countries, or statistical
  indicators simultaneously. Activate this skill whenever the user asks to search for new studies,
  expand literature benchmarks, acquire raw statistical tables across multiple topics/jurisdictions,
  or run parallel subagents for literature and raw data collection.
---

# Parallel Literature & Raw Data Harvester (`parallel-literature-harvester`)

This skill enables high-throughput, parallelized web search and primary source acquisition (`.pdf`, `.csv`, `.xlsx`, `.xml`) across multiple topics while strictly enforcing the cryptographic and methodological invariants of [`responsible-demographics`](../responsible-demographics/SKILL.md) and [`responsible-research`](../responsible-research/SKILL.md).

---

## 1. Architecture & Subagent Definitions

Two persistent subagent specifications are stored in [`.agents/agents/`](../../agents/):

| Subagent Name | Spec File | Role & Tool Permissions | When to Use |
| :--- | :--- | :--- | :--- |
| **`topic-literature-worker`** | [`.agents/agents/topic-literature-worker.md`](../../agents/topic-literature-worker.md) | Single-topic worker (`EnableWriteTools: true`, `EnableMCPTools: true`, `EnableSubagentTools: false`) | Spawn **$K$ instances in parallel** (one per topic/country/dataset) directly from the main agent or from the orchestrator. |
| **`parallel-literature-orchestrator`** | [`.agents/agents/parallel-literature-orchestrator.md`](../../agents/parallel-literature-orchestrator.md) | Multi-topic coordinator (`EnableWriteTools: true`, `EnableMCPTools: true`, `EnableSubagentTools: true`) | Delegate an entire multi-topic harvesting campaign to a single background coordinator that fans out workers and merges results. |

---

## 2. Step-by-Step Parallel Execution Workflow

### Step 1: Register the Subagent Type(s) in the Active Session
If `topic-literature-worker` (or `parallel-literature-orchestrator`) has not yet been registered in the current conversation via `define_subagent`, read its prompt from [`.agents/agents/topic-literature-worker.md`](../../agents/topic-literature-worker.md) and call `define_subagent`:

```json
{
  "Name": "topic-literature-worker",
  "Description": "Focused single-topic worker subagent for parallel literature review and raw data acquisition. Invoke multiple instances in parallel (one per topic, country, dataset, or benchmark).",
  "EnableWriteTools": true,
  "EnableSubagentTools": false,
  "EnableMCPTools": true,
  "SystemPrompt": "<contents of .agents/agents/topic-literature-worker.md>"
}
```

### Step 2: Decompose the Request into Orthogonal Topics & Fan Out in Parallel
Break the user's research request into $K$ independent topics (e.g., by country, cohort study, or statistical agency table). In a **single turn**, call `invoke_subagent` for all $K$ topics simultaneously so their web searches and downloads execute concurrently:

- **Crucial Concurrency Rule**: Assign each worker:
  1. A distinct target file path in `literature/` or `rawdata/` (e.g., `literature/Author_Year_Topic.pdf`).
  2. A distinct scratch JSON output path (`<appDataDir>/brain/<conversation-id>/scratch/topic_<slug>.json`).
  3. Instructions **not** to edit shared index files (`rawdata/MANIFEST.csv`, `datasets/literature_empirical_benchmarks.csv`) directly while sibling workers are running.

### Step 3: Wait Reactively (Zero Polling)
After invoking the $K$ subagents in parallel, **end your turn** (or proceed only with non-conflicting local work). Antigravity's reactive messaging system automatically wakes you up as each worker completes and returns its structured report.

### Step 4: Verify Files, Handle Paywalls & Atomically Merge
Once all parallel workers have reported back:

1. **Verify Downloaded Files (Anti-Corruption & Keyword Check)**:
   Run [verify_and_register_harvest.py](./scripts/verify_and_register_harvest.py) on every downloaded file to ensure no HTML paywall landing pages (`<!DOCTYPE html>`) were saved with `.pdf` extensions and no mismatched PMC XMLs occurred:
   ```bash
   .venv/bin/python3 .agents/skills/parallel-literature-harvester/scripts/verify_and_register_harvest.py \
     --verify-file literature/<filename>.pdf --keywords "<Author>,<SampleSize_or_KeyTerm>"
   ```

2. **Generate Verified Extract PDFs for Paywalled Studies (If Needed)**:
   If a primary journal PDF is behind a publisher paywall but exact abstract/table metrics are verified via PubMed/DOI metadata, generate an audit-compliant extract PDF:
   ```bash
   .venv/bin/python3 .agents/skills/parallel-literature-harvester/scripts/verify_and_register_harvest.py \
     --create-extract-pdf <scratch_dir>/spec_<slug>.json \
     --out literature/<Author>_<Year>_<Journal>_Extract.pdf
   ```

3. **Merge Worker Payloads & Synchronize Cryptographic Manifests**:
   Aggregate the worker scratch files and synchronize `rawdata/MANIFEST.csv` and `rawdata/rawdata.md`:
   ```bash
   .venv/bin/python3 .agents/skills/parallel-literature-harvester/scripts/verify_and_register_harvest.py \
     --merge-scratch <scratch_dir>

   .venv/bin/python3 .agents/skills/parallel-literature-harvester/scripts/verify_and_register_harvest.py \
     --sync-manifest --update
   ```

4. **Run the Mandatory Audit Gate**:
   Always conclude by running both repository audit suites to verify 100% compliance:
   ```bash
   .venv/bin/python3 .agents/skills/responsible-demographics/scripts/audit_demographics.py
   .venv/bin/python3 .agents/skills/responsible-research/scripts/audit_research_pipeline.py
   ```

---

## 3. Production Invariants & Anti-Corruption Protocol

Field testing across high-throughput literature harvesting revealed four common failure modes that must be proactively blocked:

### 1. Paywall Landing Pages Masquerading as PDFs
Publisher servers often return HTTP 200 containing HTML paywalls (`<!DOCTYPE html>`) when `curl` or `wget` attempts to fetch a `.pdf` URL:
* **The Check**: Every downloaded `.pdf` must begin with the `%PDF-` magic header, be $\ge 1{,}000$ bytes, and pass a test parse with `pypdf`.
* **Remedy**: Never rename an HTML landing page to `.pdf`. If paywalled, either query an open-access green repository (PubMed Central, institutional university handle, national statistical portal) or generate a verified extract PDF using `--create-extract-pdf`.

### 2. PubMed Central (PMC) ID Collisions & Title Verification
When querying PMC APIs or open-access mirrors, guessing or mistyping PMC numbers downloads a valid PDF of an entirely unrelated paper:
* **The Check**: Always run `verify_and_register_harvest.py --verify-file <path> --keywords "<Author>,<SampleSize_or_Term>"`. The verification script verifies that the author's surname and key sample size or topic term appear verbatim inside the parsed PDF or XML text.

### 3. Pure Conceptual/Taxonomy Papers vs. Empirical Meta-Regressions
Classic foundational literature (e.g., Moffitt 1993 dual taxonomy) is often cited for theoretical frameworks, but lacks empirical relative risks or odds ratios:
* **Rule**: Never insert invented effect sizes or sample sizes for theoretical papers into quantitative meta-regression tables (`oecd_precarity_crime_meta.csv`).
* **Correct Classification**: Theoretical parameters belong in `literature_empirical_benchmarks.csv` with `methodischer_status = Strukturelle_Modellkalibrierung`, and must be excluded from empirical cross-national meta-regressions.

### 4. Strict Directory Boundaries: `rawdata/` vs. Derived Syntheses
* **`rawdata/` is strictly for unmodified primary source files**: Never place hand-curated multi-study meta-analysis CSVs in `rawdata/` pretending they were downloaded from a single official server. Derived cross-study datasets belong in `datasets/` or `literature/`.
* **Bi-Directional Manifest Synchronization**: Whenever a new benchmark row is merged into `rawdata/literature_empirical_benchmarks.csv`, ensure it is synced to `datasets/literature_empirical_benchmarks.csv` **and** re-hash `rawdata/MANIFEST.csv` and `rawdata/rawdata.md` via `--sync-manifest --update`. Untracked files in `rawdata/` will fail the cryptographic audit gate.

