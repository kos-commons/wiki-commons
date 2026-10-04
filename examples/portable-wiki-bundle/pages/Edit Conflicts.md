---
id: 018f6c3e-9d2b-7c4a-8e1f-2b3c4d5e6f70
title: Edit Conflicts
aliases: [Edit conflict, Editing collisions]
tags: [history, collaboration]
lang: en
translations:
  ja: 編集の競合
created: "2024-03-02T10:15:00+09:00"
updated: "2026-07-14T15:50:00Z"
contributors:
  - {name: Aiko Tanaka, id: aiko}
  - {name: anonymous, kind: anonymous}
  - {name: LinkFix bot, id: bot-linkfix, kind: bot}
status: stable
review:
  state: verified
  by: Docs team
  at: "2026-06-01T09:00:00Z"
  revision: r0004
license: CC-BY-SA-4.0
summary: What happens when two people save the same page at once, and how engines reconcile it.
source: https://wiki.example.org/wiki/Edit_Conflicts
ext:
  examplewiki:
    page_id: 20481
---

An **edit conflict** happens when two people save changes to the same page
based on the same earlier revision.[^1] See [[Revision History]] for the
general model and [[#Merging|how merging works]] below.

> [!NOTE]
> Most engines merge non-overlapping changes automatically. Only overlapping
> changes need a person to decide.

## Merging

When both edits touch different parts of the page, the engine applies a
three-way merge against the common base revision. The resolution screen shows
both versions side by side. ^conflict-ui

![Sequence diagram of two editors saving changes to the same page](../attachments/conflict-diagram.svg)

## Terminology

The glossary defines the key term:

![[Glossary#^optimistic-concurrency]]

## Related

- [[Glossary]]
- [[wikipedia:Edit conflict]]
- `[[Edit Conflicts|this page]]` is how a labelled link is written in source.

[^1]: The base revision is the one the editor loaded before starting to type.
