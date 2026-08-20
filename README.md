# PM Agent Skills

Agent skills for the parts of product management that are real work: turning a demo call into something the team can read, framing a PRD before writing it, and keeping track of what competitors actually shipped.

Each skill is a folder with a `SKILL.md` your agent reads on demand. Nothing here is a wrapper around a chat prompt — the skills carry workflows, templates, and scripts that do the mechanical parts properly.

## What's inside

| Skill | What it does | Reach for it when |
| --- | --- | --- |
| [demo-recap](skills/demo-recap) | Turns a recording of a demo call into a shareable recap: what each demo showed, how mature it is, what was decided, what is still open, with screenshots and GIFs cut from the video. | You ran a demo or showcase call and the people who missed it need more than "the recording is in the channel". |
| [write-prd](skills/write-prd) | Drafts a framing-first PRD around problem space, jobs to be done, success criteria, and scope. Asks a clarification round before drafting, and keeps asking until you say draft it. | You have a rough feature idea, a pile of user feedback, or a vague request, and you need the frame straight before anyone writes requirements. |
| [monitor-ai-coding-competitors](skills/monitor-ai-coding-competitors) | Runs a stateful, evidence-first scan of AI coding tools and prompt-to-app builders: releases, product changes, pricing moves, reliability problems, community signals. Keeps per-source checkpoints and cites every finding. | You want a weekly or since-last-run competitor digest where every claim has a source, and observation stays separate from interpretation. |

## Install

Using the [skills](https://github.com/vercel-labs/skills) CLI:

```bash
# see what's available
npx skills add watchmesink/pm_agent_skills --list

# install one
npx skills add watchmesink/pm_agent_skills --skill demo-recap

# install everything, into a specific agent
npx skills add watchmesink/pm_agent_skills --skill '*' -a claude-code
```

Try one without installing it:

```bash
npx skills use watchmesink/pm_agent_skills --skill write-prd --agent claude-code
```

Or install by hand — a skill is just a directory:

```bash
git clone https://github.com/watchmesink/pm_agent_skills
cp -R pm_agent_skills/skills/demo-recap ~/.claude/skills/    # Claude Code
cp -R pm_agent_skills/skills/demo-recap ~/.codex/skills/     # Codex
```

Then ask for it by name: `Use demo-recap on ~/Downloads/team-demo.mp4`.

## Prerequisites

Most skills need nothing beyond the agent. The exception:

- **demo-recap** needs `ffmpeg`, `ffprobe`, and the `whisper` CLI, because it transcribes and cuts video locally.
  ```bash
  brew install ffmpeg && pip install -U openai-whisper
  ```

Each skill's README lists its own requirements and what it is allowed to touch.

## Compatibility

The `SKILL.md` format is read by any agent that supports agent skills. Each skill also ships an `agents/openai.yaml` with display metadata for Codex.

Where a skill has been genuinely exercised is noted in its own README. Treat anything not listed there as untested rather than broken.

## Repository layout

```
skills/
  <skill-name>/
    SKILL.md              required: frontmatter (name, description) + the workflow
    README.md             human-facing: what you get, prerequisites, limitations
    agents/openai.yaml    display metadata for Codex
    references/           templates and reference docs the skill links to
    scripts/              executable helpers the workflow calls
```

## Adding or updating a skill

1. Create `skills/<skill-name>/SKILL.md`. The frontmatter carries the whole activation contract:

   ```markdown
   ---
   name: skill-name
   description: What it does, in one sentence. Then: use when the user asks for X, Y, or Z.
   ---
   ```

   The `description` is what an agent reads to decide whether to load the skill, so it has to say **what it does and when to trigger**. "Helps with product docs" is not enough; name the artifacts and the phrasings a user would actually type.

2. Write the workflow as numbered steps a competent stranger could follow. Put failure modes inline, next to the step where they bite — that is what stops the same mistake happening twice.
3. Move anything long or reusable into `references/`, and anything mechanical into `scripts/`. Link to them from `SKILL.md` with relative links so the agent can open them on demand.
4. Add a `README.md` covering what you get, prerequisites, a security and permissions note, and known limitations.
5. Add the skill to the table at the top of this file, with an honest "reach for it when".

Keeping the table and the per-skill READMEs current is the whole maintenance burden. If a skill's behaviour changes, the description and the table are the two places that must change with it.

## License

[MIT](LICENSE).
