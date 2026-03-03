---
name: web-to-markdown
description: Source intake tool for converting web content to structured markdown; feeds the SOURCE_INTAKE skill chain for research and documentation
wraps: web-to-markdown (vibeship)
provenance: vibeship (MIT)
vetted: 2026-02-12
pipeline_stages: [RESEARCH]
---

# Web to Markdown

## Syncrescendence Integration

**Agents:** Commander (COO), Cartographer (CIO)

This skill converts web content into clean, structured markdown for ingestion into the Syncrescendence knowledge pipeline. It is the entry point of the SOURCE_INTAKE skill chain.

### How it fits the pipeline

- **RESEARCH stage:** When an agent needs to incorporate external knowledge (documentation, API references, blog posts, research papers), this skill fetches and converts the source into a normalized markdown format suitable for downstream processing.
- **SOURCE_INTAKE chain:** The converted markdown feeds into:
  1. **readize** -- Deep reading and comprehension
  2. **listenize** -- Extraction of actionable insights
  3. **integrate** -- Integration into the project knowledge base
- **Commander usage:** Commander uses this skill during plan research phases to gather technical documentation, dependency docs, and reference implementations.
- **Cartographer usage:** Cartographer uses this skill to ingest external architecture documentation, API specs, and system diagrams for dependency mapping.

### Config notes

- Output should be clean markdown: no tracking scripts, no navigation chrome, no ads. Content only.
- Large pages should be chunked into sections that fit within agent context windows.
- Source URLs must be preserved in the output metadata for provenance tracking.
- Rate limiting and caching should be applied to avoid redundant fetches during a session.

## Original Reference

@~/.agents/skills/web-to-markdown/SKILL.md
