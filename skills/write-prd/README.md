# Write PRD

`write-prd` is a product-management skill for turning rough product ideas, user feedback, issue notes, or existing drafts into a concise PRD.

## How It Behaves

- Starts by gathering the available context: feature idea, current behavior, user pain, product constraints, related issues, screenshots, and target audience.
- Runs PRD creation as an iterative discovery conversation. It keeps asking focused follow-up questions while important product uncertainty remains, and stops only when the user says to draft, proceed, stop asking, or create a best-effort draft.
- Focuses questions on the Problem, Solution, and Jobs to be done sections. It avoids detailed requirements questions unless the missing decision would change the product direction.
- Keeps requirements lean. Requirements should guide the product direction without prescribing detailed interaction design, implementation choices, edge-case handling, or acceptance criteria.
- Uses a compact default PRD structure: Title, Situation, Problem, Solution, Jobs to be done, and Requirements.
- Omits Status/scope note and Press release sections by default. Launch-style value narrative can be blended into the Solution section when useful.

## Default Output Shape

1. Title
2. Situation
3. Problem
4. Solution
5. Jobs to be done
6. Requirements

## Usage

Ask Codex to use `$write-prd` when you want to draft or revise a PRD. Answer the discovery questions until the product story is clear enough, then say `draft`, `proceed`, or `stop asking questions` to move into the PRD draft.
