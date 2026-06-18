---
name: write-prd
description: Draft, revise, or structure product framing PRDs centered on problem space, jobs to be done, success criteria, scope boundaries, and a concise high-level solution. Use when Codex needs to create a PRD, product brief, feature framing document, jobs-to-be-done section, success criteria, scope narrative, or convert rough feature notes into an iterative PRD process that asks at least one fresh clarification round before drafting, then keeps asking fresh, non-repeated questions until the user explicitly asks to craft the PRD.
---

# Write PRD

## Overview

Create framing-first PRDs. The goal is to define the product scope through the problem space, jobs to be done, success criteria, and a concise high-level solution, not to replace design exploration or engineering planning.

Prefer a sharp product narrative over a generic requirements template. Treat each PRD as an iterative discovery artifact: first ask at least one clarification round, then keep clarifying the frame through as many fresh question rounds as needed, and draft only after the user explicitly asks to craft the PRD after discovery has started.

## Workflow

1. Gather the source material: feature brief, user feedback, current product behavior, target users, related issues, business pressure, screenshots/docs, constraints, and the intended audience.
2. Start with a short working frame: summarize the apparent user, problem, core job, success outcome, and likely solution direction in 3-5 bullets. Mark uncertain points plainly.
3. Ask a small batch of high-impact clarifying questions before drafting on every new PRD or substantial framing request. Do not let an initial request to craft, draft, write, or produce the PRD skip this first question round.
4. Keep the discovery loop active indefinitely while the user keeps answering questions. Ask follow-up questions in focused batches; do not turn this into a long questionnaire.
5. Never treat a clear frame as permission to draft. Draft only after at least one clarification round has been asked and the user explicitly asks to craft, draft, write, produce, proceed with, or create the PRD. `Stop asking questions` alone is not enough unless it also asks to start the PRD.
6. Load `references/prd-template.md` when drafting a full PRD or when the user asks for the preferred structure.
7. Keep detailed functional requirements optional. Include them only when the user asks for requirements or when a requirement-level decision is necessary to make the scope honest.
8. State minor non-blocking assumptions in the relevant section. Ask before drafting when missing information could change the problem framing, jobs, success criteria, scope boundaries, or solution direction.

## Discovery Loop

Use questions to improve framing, not to collect implementation detail. Prefer 3-6 questions per round. Each question should make the eventual draft materially clearer. The first round is mandatory for new PRDs and substantial PRD framing changes; an initial draft request does not bypass it.

Maintain a running mental list of questions already asked and topics already answered in the current conversation. Do not ask the same question twice, and do not ask a semantic duplicate with different wording. If an answer is unclear, ask a narrower follow-up that points to the specific unresolved gap instead of repeating the original question.

When asking the first round, use this shape:

1. `Current frame:` 3-5 bullets summarizing the apparent user, problem, job, success outcome, and solution direction.
2. `Questions:` 3-6 focused questions ordered by impact.

After each user answer, refresh the `Current frame` only when it helps orient the next round, then ask the next non-repeated questions. Continue this discovery loop until the user explicitly tells you to start crafting the PRD after at least one question round has been asked.

After drafting, treat the PRD as a candidate frame. Ask the user to correct the problem space, jobs, success criteria, or solution direction before polishing wording or adding optional requirements.

### First Round Priorities

Ask about the highest-impact unknowns in this order:

1. **Problem space:** Who has the problem, what happens today, where the current workflow breaks, and why this matters now.
2. **Jobs to be done:** What users are trying to accomplish, what outcome they need, and which situations should define the scope.
3. **Success criteria:** What product/user/business signals would prove the problem is solved or meaningfully reduced.
4. **High-level solution:** What product direction is already intended, what must stay flexible for design, and what alternatives are explicitly not the goal.
5. **Scope boundaries:** Which users, editions, surfaces, workflows, or cases are in scope now, later, or out of scope.

### Follow-Up Rules

- Ask a follow-up when the user's answer is broad, contradictory, solution-heavy without a clear problem, or missing the user outcome.
- Prefer "which of these is the primary driver?" questions when multiple possible problems or jobs appear.
- Ask for concrete examples of current pain when the problem sounds abstract.
- Ask for success criteria before requirements; success criteria should describe outcomes, not UI behavior.
- Ask about constraints only when they shape the user experience, scope boundary, or solution direction.
- When the core frame is already strong, move to fresh questions about prioritization, non-goals, tradeoffs, excluded personas, rollout risk, success evidence, and decision criteria.
- Do not ask detailed acceptance-criteria, interaction-design, data-model, edge-case, or implementation questions unless they are fundamental to the product framing.

### Drafting Gate

Use these as a readiness check, not as permission to draft:

1. Target user or customer segment.
2. Current problem and consequence.
3. One or more user jobs that define the scope.
4. Expected success criteria or measurable outcomes.
5. One-paragraph solution direction.
6. Main scope boundaries or explicit assumption that boundaries are still open.

When these are clear enough but the user has not asked to craft the PRD after at least one question round, say that the frame is ready when useful, then keep asking fresh non-repeated questions. Do not draft, outline, or produce the PRD until discovery has started and the user explicitly asks for it.

## Preferred Structure

Use this order by default:

1. Title
2. Situation
3. Problem space
4. Jobs to be done
5. Success criteria
6. High-level solution
7. Scope boundaries
8. Requirements, only when requested or essential

## Section Rules

**Situation**
Write prose, not a numbered list. Explain the current landscape, existing product behavior, workflow pressure, and why this is the right time to solve the problem. Mention existing product surfaces and constraints only when they matter to the framing.

**Problem space**
Use a numbered list. Each item should state a current user/product problem and its consequence. Avoid solution language unless needed to explain why the current state fails.

**Jobs to be done**
Use a numbered list in this form: `When [situation], I want [capability], so I can [outcome].` Treat these jobs as the main scope drivers. Keep each job user-centered, outcome-oriented, and independent from implementation.

**Success criteria**
Use a numbered list. Describe observable outcomes that indicate the problem has been solved or reduced. Prefer user behavior, workflow completion, quality, adoption, retention, support load, or business signals over implementation milestones. Include metrics only when the user provided them or they can be stated as directional targets.

**High-level solution**
Write one paragraph by default. Explain the overall product idea, user-facing behavior, customer value, and product direction. Keep detailed behavior in Jobs to be done or optional Requirements. Do not describe the implementation plan.

**Scope boundaries**
Use short bullets or a numbered list when boundaries matter. Clarify what is in scope now, what is intentionally deferred, and what is out of scope. Omit this section when boundaries would add noise and are already clear from the jobs.

**Requirements**
Use only when requested or essential. Keep requirements lean, numbered, observable, and product-level. Do not over-specify interaction design, technical implementation, edge-case handling, or acceptance criteria. Use `must` for firm product decisions and `should` for strong direction that still leaves implementation discretion.

## Writing Standards

- Start with why this matters now.
- Keep the PRD focused on framing and scope, not execution detail.
- Let jobs to be done define the main shape of scope.
- Keep the high-level solution to one paragraph unless the user asks for more detail.
- Prefer concrete product nouns over abstract PM language.
- Avoid generic sections that add ceremony without decisions.
- Preserve the user's domain language when revising an existing PRD, but fix unclear phrasing and obvious typos.
- Make every numbered item carry one idea.
- Clearly separate problem, job, success outcome, solution direction, and requirement-level detail.

## Quality Check

Before finalizing, verify:

1. The Situation explains the landscape and timing.
2. The Problem space describes real current pain and consequences.
3. Jobs to be done are user-centered and define the scope.
4. Success criteria describe outcomes, not implementation tasks.
5. The High-level solution is one concise paragraph and does not over-specify design or engineering.
6. Scope boundaries are explicit when they affect interpretation.
7. Requirements are omitted unless requested or essential, and remain lean if included.
8. At least one clarification round was asked before drafting, and clarifying questions continued until the user explicitly asked to craft the PRD.
9. No repeated or semantically duplicate questions were asked across discovery rounds.
