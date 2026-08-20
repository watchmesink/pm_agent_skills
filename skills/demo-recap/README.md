# Demo Recap

`demo-recap` turns a recording of a team demo call into a recap that someone who missed the call can actually follow: what each demo showed, how mature it is, what the team decided, and what is still open, with screenshots and short GIFs cut from the recording itself.

It exists because the useful part of a demo call is perishable. The decisions live in one hour of video that nobody rewatches, and a transcript alone does not tell you what was on screen.

## What you get

A single deliverable folder:

```
demo-recap-YYYY-MM-DD/
  SUMMARY.txt                  plain text, ready to paste into Slack
  01_bulk-import.jpg           one or two stills per demo, presenter webcam cropped out
  01_bulk-import.gif           a short GIF where the demo actually moved
  ...
  _ALL-visuals-preview.jpg     every visual on one sheet, for a last look
  transcript-EN.txt / .srt     the transcript the recap was written from
```

Each section carries a timestamp into the recording, an honest maturity note (design only, in the nightly, ships in the next release, not merged yet), and its unresolved items phrased as questions so they can be answered in the thread.

## How it behaves

- **Checks the spoken language before transcribing.** Pointing an English-only Whisper model at non-English audio does not fail, it returns fluent nonsense. The skill samples a few points first and switches to translation when the call is not English, or is mixed.
- **Maps the video visually** with timecoded contact sheets, so demo boundaries and presenters come from what is on screen rather than from guesswork.
- **Separates agreed from open strictly.** Only explicit decisions count as agreed. Anything hedged stays an open question. This split is the highest-value part of the recap and the easiest to get wrong, so it gets verified against the transcript before writing.
- **Proves a GIF moves before keeping it,** by comparing the first and last frame of the window. A static screen with a drifting mouse becomes a still instead.
- **Crops the presenter webcam** and any floating meeting window out of every visual.
- **Writes short.** Roughly one tight paragraph per demo. Prose gets compressed, open questions never do.
- **Optionally emits zero markdown,** because `#`, `*` and backticks arrive as visible clutter when a recap is pasted into a Slack message.

## Prerequisites

- `ffmpeg` and `ffprobe`
- The [openai-whisper](https://github.com/openai/whisper) CLI (`whisper`), which runs on CPU here
- Optional, only for the notes-PDF path: `pypdf`

```bash
brew install ffmpeg
pip install -U openai-whisper pypdf
```

Transcription is the slow step. Translating a 55 minute call takes roughly 14 minutes on an idle CPU, so the skill starts it in the background and maps the video while it runs.

## Usage

Point your agent at a recording:

```
Use $demo-recap on ~/Downloads/team-demo.mp4
```

Useful things to say alongside it:

- "plain text, I'm pasting it into Slack" or "markdown, it's going in a doc"
- "shorter" — the default is already tight, and it will compress further
- "these are the topics" — if you know the agenda, it will structure the recap that way instead of inferring it

If there is no usable recording but you have a meeting-notes PDF with a transcript and embedded screenshots, hand over the PDF instead. The skill has a path for that.

## Files

- [SKILL.md](SKILL.md) — the workflow the agent follows
- [references/recap-templates.md](references/recap-templates.md) — the plain-text and markdown recap shapes
- [scripts/media.sh](scripts/media.sh) — all ffmpeg and whisper work, one subcommand per job

## Security and permissions

This skill:

- Reads only the recording you point it at, and writes only into the scratch and deliverable folders.
- Sends nothing to any external service. Transcription runs locally on CPU via the `whisper` CLI, so the audio never leaves the machine.
- Runs `ffmpeg`, `ffprobe`, `whisper`, and `python3` (the latter only for time arithmetic and the optional PDF path).
- Does not modify the source recording and needs no credentials.

Review [scripts/media.sh](scripts/media.sh) before installing. It is a single readable shell script with no network calls.

## Known limitations

- Whisper is unreliable with names. The skill deliberately keeps presenter names out of the recap unless a name is legible on a webcam label.
- Language is detected once per sample, so a heavily code-switching call is best handled by the translation path.
- Crop coordinates assume a 1920x1080 screen share with the presenter webcam on the right. Other layouts need a manual crop, which the skill checks by reading the cropped frames back.
- GIF size is bounded by hand. Text-dense screens such as diffs and specs need a shorter or smaller clip.
