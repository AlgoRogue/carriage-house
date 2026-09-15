# Issue tracker: local markdown

Issues and specs live as markdown under `.scratch/` — no external tracker.

## Layout

- One feature per directory: `.scratch/<feature-slug>/`
- Spec: `.scratch/<feature-slug>/spec.md`
- Issues: `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01`

## Issue file shape

- A **Status** line near the top (e.g. `Status: open`, `Status: in-progress`, `Status: closed`)
- Body: description, acceptance criteria, links to the feature spec
- **Comments** section at the bottom — append-only log of updates, newest last

## Wayfinding

- To find a feature's issues, list `.scratch/<feature-slug>/issues/`
- To find the current state of a feature, read `.scratch/<feature-slug>/spec.md` first, then scan issue Status lines
- Slugs are kebab-case and stable once created — don't rename a feature directory after issues exist under it

## Skill mapping

- **Publish** (create a ticket): create the file under `.scratch/<feature-slug>/issues/`, following the numbering and Status conventions above. If the feature directory doesn't exist yet, create it with a `spec.md`.
- **Fetch ticket**: read the issue file directly at its `.scratch/` path — there is no API or ID lookup, the path is the identifier.
