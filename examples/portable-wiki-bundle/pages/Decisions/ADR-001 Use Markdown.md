---
id: 018f6c3e-0004-7c4a-8e1f-2b3c4d5e6f04
title: ADR-001 Use Markdown
tags: [decisions]
lang: en
created: "2024-04-10T11:00:00+09:00"
updated: "2024-04-12T09:20:00+09:00"
contributors:
  - {name: Aiko Tanaka, id: aiko}
  - {name: Ben, id: ben}
status: stable
schema: structured/schemas/decision-record.schema.json
properties:
  adr_number: 1
  decision_status: accepted
  deciders: ["[[User:Aiko]]", "[[User:Ben]]"]
  decided_on: "2024-04-12"
---

<!-- wiki:snapshot kind="template" name="Decision Record" engine="examplewiki" params='{"status":"accepted"}' at="2026-10-04T02:00:00Z" -->
> [!IMPORTANT]
> Status: **accepted** (2024-04-12)
<!-- /wiki:snapshot -->

## Context

The wiki needed a markup that contributors already knew and that other tools
could read. Several contributors paste from and into other systems daily.

## Decision

Pages are written in Markdown following the portable profile, with
`[[free links]]` for internal links.

## Consequences

- Exports are readable without the engine.
- A few constructs (tables with merged cells) need a small HTML subset.
