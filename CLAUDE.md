# CLAUDE.md — Knowledge Graph AI Assistant

## Project Overview

AI-powered knowledge graph pipeline that extracts nodes and relationships from math textbooks using a **Plan → Generate → Evaluate** LLM pipeline. Outputs interactive pyvis HTML visualizations and JSON data consumed by a Streamlit web app.

## Key Commands

```bash
# Start the Streamlit web app (main UI)
streamlit run streamlit_app.py

# Run the batch pipeline (configure scripts/config.py first)
python scripts/run_pipeline.py

# Run tests
python -m pytest tests/
```

## Architecture

```
src/
  agents/       — LLM agents (TwoStepPlanningAgent, GenerationAgent, EvaluationAgent, IslandIntegrationAgent)
  pipeline/     — Orchestration (PipelineOrchestrator, TaskExecutor, IterationManager, DependencyResolver)
  core/         — Data types: Node, Relation, TaskStatus, TaskType, exceptions
  infrastructure/ — APIClient (OpenAI-compatible), ConversationManager, Logger
  config/       — provider_config.py (DeepSeek/SJTU), prompts.py (all system prompts)
  utils/        — JSON parsing, section extraction, length calculation
```

## Entry Points

| File | Purpose |
|------|---------|
| `streamlit_app.py` | Primary interactive UI — pipeline runner + graph editor |
| `show.py` | Standalone pyvis HTML renderer (no Streamlit required) |
| `scripts/run_pipeline.py` | CLI batch processing |

## Configuration

Copy `.env.example` → `.env` and set:
- `LLM_PROVIDER` — `deepseek` (default) or `sjtu_zhiyuan`
- `DEEPSEEK_API_KEY` / `SJTU_API_KEY`
- `DEEPSEEK_API_ENDPOINT` / `SJTU_API_ENDPOINT`

Provider switching is zero-code — handled by `src/config/provider_config.py`.

## Data Layout

```
material/<topic>/
  <topic>.md              ← raw textbook input
  <topic>_nodes.json      ← extracted nodes (list of [name, {desc,level,color}])
  <topic>_relations.json  ← extracted relations (list of [src, dst, {rel,定理,color}])

output/                   ← generated HTML visualizations
```

## Data Formats

**Nodes** — `[[name, {desc, level, color}], ...]`  
**Relations** — `[[source, target, {rel, 定理, color}], ...]`

Use `Node.from_tuple()` / `Relation.from_tuple()` (in `src/core/result_types.py`) to deserialize.

## Testing Notes

- Tests in `tests/` cover agents, JSON parsing, section extraction, and iteration logic.
- Files named `test_*_real_api.py` require valid API credentials to run — skip them in CI without keys.
- Run offline tests only: `python -m pytest tests/ --ignore=tests/test_evaluation_agent_real_api.py --ignore=tests/test_generation_agent_real_api.py`

## Common Gotchas

- `prompts.py` is large (51 KB) — all system prompts live there alongside `two_step_planning_prompts.py`.
- `scripts/run_island_integration_once.py` is a one-off utility; hardcodes `material/数学分析I/` paths — edit before use.
- `scripts/config.py` requires manual edits (`MATERIAL_NAME`, `MATERIAL_FILE`) before running the pipeline script.
