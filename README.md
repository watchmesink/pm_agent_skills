# PM Agent Skills

Agent skills for the parts of product management that are actual work: framing a PRD before anyone writes requirements, keeping an evidence-backed read on what competitors shipped, and turning a demo call into something the team will read.

Each skill is a folder with a `SKILL.md` your agent loads on demand. None of them is a wrapper around a chat prompt. They carry workflows, templates, and scripts that do the mechanical parts properly, and they say plainly what they will not do.

## What's inside

### [write-prd](skills/write-prd)

Turns a rough feature idea into a framing-first PRD built on problem space, jobs to be done, success criteria, and scope boundaries. It asks a clarification round *before* it drafts, then keeps asking fresh questions until you explicitly tell it to write. Requirements stay optional, included only when they are needed to make the scope honest.

**Reach for it when** you have a vague request, a pile of user feedback, or a half-formed idea, and someone is about to start writing requirements against it.

### [monitor-ai-coding-competitors](skills/monitor-ai-coding-competitors)

Runs a stateful, evidence-first scan of AI coding tools and prompt-to-app builders: releases, product changes, pricing and availability moves, reliability problems, and community signals. Every factual claim carries a first-party source, a confidence tier (`confirmed`, `strongly_supported`, `community_signal`, `anecdotal_watch`) and a lifecycle label (`announced`, `preview`, `ga`, `deprecated`, and so on). Per-source checkpoints mean the next run starts where the last one stopped, and it will not collapse three releases from one product into a single "latest update". Outputs a Markdown report plus a deliberately minimal HTML dashboard.

**Reach for it when** you want a weekly or since-last-run competitor digest that keeps what shipped separate from what people are saying about it, without re-reading fourteen changelogs yourself.

### [demo-recap](https://github.com/watchmesink/demo-recap) · separate repo

Turns a recording of a demo call into a recap people will actually read: what each demo showed, how mature it is, what the team decided, what is still open, with screenshots and GIFs cut from the video itself. Detects the spoken language before transcribing, verifies a GIF actually moves before keeping it, and can emit zero-markdown plain text for pasting into Slack.

**Reach for it when** you ran a demo, showcase, or sprint review, and the people who missed it need more than "the recording is in the channel".

## Install

Using the [skills](https://github.com/vercel-labs/skills) CLI:

```bash
# see what's available
npx skills add watchmesink/pm_agent_skills --list

# install one
npx skills add watchmesink/pm_agent_skills --skill write-prd

# install everything, globally, into a specific agent
npx skills add watchmesink/pm_agent_skills --skill '*' -g -a claude-code
```

Try one without installing it:

```bash
npx skills use watchmesink/pm_agent_skills --skill write-prd --agent claude-code
```

Or install by hand — a skill is just a directory:

```bash
git clone https://github.com/watchmesink/pm_agent_skills
cp -R pm_agent_skills/skills/write-prd ~/.claude/skills/    # Claude Code
cp -R pm_agent_skills/skills/write-prd ~/.codex/skills/     # Codex
```

Then ask for it by name: `Use write-prd to frame this feature idea`.

`demo-recap` installs from [its own repo](https://github.com/watchmesink/demo-recap):

```bash
npx skills add watchmesink/demo-recap -g
```

## Prerequisites

Both skills in this repo run on the agent alone, with no extra binaries to install.

- **write-prd** needs nothing.
- **monitor-ai-coding-competitors** needs web access, and runs `python3` for its state-checkpoint and finding-validation scripts.

`demo-recap` needs `ffmpeg` and a local Whisper install; its own README covers that.

## Compatibility

The `SKILL.md` format is read by any agent that supports agent skills. Each skill also ships an `agents/openai.yaml` with display metadata for Codex.

Where a skill has been genuinely exercised is noted in its own documentation. Treat anything not listed there as untested rather than broken.

## Repository layout

```text
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
5. Add a section for the skill above, with an honest "reach for it when".

Keeping those sections and the per-skill READMEs current is the whole maintenance burden. If a skill's behaviour changes, its `description` and its section here are the two places that must change with it.

## License

[MIT](LICENSE).
