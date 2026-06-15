# Preferred PRD Template

Use this as a starting point, then adjust for feature size and audience. Keep Requirements out unless the user asks for them or they are needed to make the scope unambiguous.

```markdown
# PRD: [Feature name]

## Situation

[Describe the current landscape, current product behavior, workflow pressure, and why this is the right time to solve the problem. Use prose.]

## Problem space

1. [Current user/product problem and consequence.]
2. [Current user/product problem and consequence.]
3. [Current user/product problem and consequence.]

## Jobs to be done

1. When [situation], I want [capability], so I can [outcome].
2. When [situation], I want [capability], so I can [outcome].
3. When [situation], I want [capability], so I can [outcome].

## Success criteria

1. [Observable user, workflow, quality, adoption, support, or business outcome.]
2. [Observable user, workflow, quality, adoption, support, or business outcome.]
3. [Observable user, workflow, quality, adoption, support, or business outcome.]

## High-level solution

[Describe the overall product idea, user-facing behavior, customer value, and product direction in one paragraph. Do not describe implementation details.]

## Scope boundaries

- In scope: [users, surfaces, workflows, or cases included now.]
- Deferred: [important follow-up areas intentionally left for later.]
- Out of scope: [areas the PRD should not imply.]
```

Append this only when requirements are requested or essential:

```markdown
## Requirements

1. The product must [observable product requirement that defines core behavior without prescribing design or implementation details].
2. The product should [product direction where designers and developers may choose the exact solution].
```
