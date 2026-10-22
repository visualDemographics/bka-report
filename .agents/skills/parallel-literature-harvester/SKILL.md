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

