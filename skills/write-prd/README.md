# Write PRD

`write-prd` is a product-management skill for turning rough product ideas, user feedback, issue notes, or existing drafts into a framing-first PRD.

## How It Behaves

- Starts by gathering the available context: feature idea, current behavior, user pain, product constraints, related issues, screenshots, and target audience.
- Builds a short current frame, asks at least one fresh clarification round before drafting, then keeps asking fresh, non-repeated clarifying questions until the user explicitly asks to craft the PRD.
- Focuses questions on problem space, jobs to be done, success criteria, high-level solution, and scope boundaries.
- Does not let an initial draft request bypass the first question round. Does not treat a clear frame as permission to draft. `Stop asking questions` alone is not enough unless the user also asks to start the PRD.
- Keeps requirements optional. Requirements are included only when requested or essential to make the scope honest.
- Uses a compact default PRD structure: Title, Situation, Problem space, Jobs to be done, Success criteria, High-level solution, and Scope boundaries.

## Default Output Shape

1. Title
2. Situation
3. Problem space
4. Jobs to be done
5. Success criteria
6. High-level solution
7. Scope boundaries
8. Requirements, only when requested or essential

## Usage

Ask Codex to use `$write-prd` when you want to frame, draft, or revise a PRD. Answer the first discovery round and any follow-up rounds that are useful, then explicitly say `draft the PRD`, `craft the PRD`, or `write the PRD` when you want the draft to start.
