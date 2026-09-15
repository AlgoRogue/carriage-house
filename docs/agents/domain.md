# Domain docs: single-context

This project uses a single root-level glossary rather than per-directory domain docs.

## Where things live

- `CONTEXT.md` (repo root) — the domain language: canonical terms, definitions, avoided synonyms, and relationships. Already exists; extend it in place rather than creating parallel glossaries elsewhere.
- `docs/adr/` — architecture decision records, one file per decision. May be empty; created here so agents know where to write the first one.

## Consumer rules

- Before introducing a new domain term or renaming a concept, check `CONTEXT.md`'s `Language` section for an existing canonical term and its `_Avoid_` list — don't reintroduce a synonym that's already been rejected there.
- If a change conflicts with something recorded in `docs/adr/` (once records exist), flag the conflict explicitly rather than silently overriding the decision — surface it to the human instead of resolving it unilaterally.
- `CONTEXT.md` also tracks `Flagged ambiguities` — open questions the human hasn't locked yet. Don't treat those sections as settled; treat everything else in the glossary as settled vocabulary.
