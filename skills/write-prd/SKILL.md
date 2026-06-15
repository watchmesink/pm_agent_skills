---
name: write-prd
description: Draft, revise, or structure Product Requirements Documents in a narrative product style. Use when Codex needs to create a PRD, product brief, feature requirements document, jobs-to-be-done section, numbered product requirements, or convert rough feature notes into a clear PRD with Situation, Problem, Solution, Jobs to Be Done, and Requirements.
---

# Write PRD

## Overview

Create PRDs that start from context and customer/product pressure, then narrow into numbered problems, solutions, jobs to be done, and lean product requirements. Prefer a sharp product narrative over a generic template.

## Workflow

1. Gather the source material: feature brief, user feedback, market movement, product constraints, existing screenshots/docs, related issues, and any desired audience.
2. Treat PRD creation as an iterative discovery conversation. Keep asking focused follow-up questions while meaningful product uncertainty remains, and stop only when the user asks to draft, proceed, stop asking, or explicitly requests a best-effort draft.
3. Focus clarifying questions on the Problem, Solution, and Jobs to be done sections. Ask about requirements only when a missing requirement-level decision is fundamental to the product direction or would make the PRD misleading.
4. Draft directly only when the user asks to draft, proceed, stop asking questions, or requests a best-effort draft. State minor non-blocking assumptions in the relevant section instead of inventing specifics.
5. Load `references/prd-template.md` when drafting a full PRD or when the user asks for the preferred structure.
6. Write the Situation first as a narrative, then write the remaining core sections as numbered lists.
7. Keep requirements concrete enough to guide product direction, but not so detailed that they replace design or engineering judgment. Use `must` for firm requirements and `should` for strong product direction that may allow implementation discretion.
8. Use only the preferred structure below unless the user explicitly asks for another section.

## Clarifying Questions

Ask questions when missing information would make the Problem, Solution, or Jobs to be done vague, unconvincing, or likely wrong. Prefer asking before drafting over filling gaps silently, and continue with follow-up questions until the user signals that the discovery loop should stop.

Trigger clarifying questions for missing details such as:

- Target users, release surface, or product edition.
- Current behavior and the specific limitation being changed.
- Primary user flow, entry points, and expected end state.
- Scope boundaries or exclusions when they change the product story.
- Data model, permissions, privacy, retention, or cross-device behavior only when they shape the core user experience or product direction.
- Success criteria when they clarify the problem or intended outcome.
- Known technical, business, legal, or platform constraints that affect the user experience.

When asking, include only the questions needed to make the next PRD draft more concrete. Prefer small batches of high-impact questions over long questionnaires. Do not ask detailed requirements or acceptance-criteria questions unless they are fundamental to the product direction.

## Preferred Structure

Use this order by default:

1. Title
2. Situation
3. Problem
4. Solution
5. Jobs to be done
6. Requirements

## Section Rules

**Situation**
Write prose, not a numbered list. Describe the current landscape, existing product behavior, current challenges, and what is changing in the market or user workflow. Mention existing product surfaces and constraints when they matter. Use short bullets only when listing concrete existing capabilities.

**Problem**
Use a numbered list. Each item should state a current product/user problem and its consequence. Avoid solution language unless needed to explain why the current state fails.

**Solution**
Write prose that explains the overall product idea, product direction, and customer value. Blend in any launch-style narrative or value proposition here when useful. Keep detailed behavior in Jobs to be done and Requirements. Describe the product behavior the user should experience, not the implementation plan.

**Jobs to be done**
Use a numbered list in this form: `When [situation], I want [capability], so I can [outcome].` Keep each job user-centered and independent from implementation.

**Requirements**
Use a numbered list of lean product requirements. Write in sentences, not vague bullets. Requirements should be observable and scoped, but should not over-specify interaction design, technical implementation, edge-case handling, or acceptance criteria unless the user explicitly asks or the detail is fundamental. Include labels like `Functional requirements` or `For [persona/surface] only for now` only when the scope needs to be explicit.

## Writing Standards

- Start with why this matters now.
- Prefer concrete product nouns over abstract PM language.
- Avoid generic sections that add ceremony without decisions.
- Keep the line between product requirements and implementation details clear.
- Make every numbered item carry one idea.
- Preserve the user's domain language when revising an existing PRD, but fix unclear phrasing and obvious typos.
- If minor non-blocking information is missing, state the assumption in the relevant section instead of inventing specifics. If the missing information affects the problem framing, solution direction, jobs to be done, or a fundamental product requirement, ask clarifying questions before drafting.

## Quality Check

Before finalizing, verify:

1. Situation explains the landscape and timing.
2. Problems are numbered and describe real current pain.
3. Solutions answer the problems without over-specifying engineering.
4. Jobs to be done are user-centered.
5. Requirements are numbered, observable, and not overly prescriptive.
6. Clarifying questions focused on Problem, Solution, and Jobs to be done before Requirements.
7. No Status/scope note or Press release section is included unless the user explicitly asks for a different structure.
