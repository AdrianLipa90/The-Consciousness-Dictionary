# AGENTS.md — repository contract

## Authority
The canonical machine-readable Source of Truth for this branch is `ontology/registry/v0_2/`: 12 lossless compact shards plus codebooks reconstructing all 548 complete term cards. Runtime vectors and generated artifacts are realizations, not authority over definitions. The editorial V0.2 working source remains provenance for future expansion.

## Hard boundaries
- Do not equate PhaseNav similarity with semantic equivalence.
- Do not promote affect, salience, resonance, frequency, or vector proximity into truth or authority.
- Do not treat a computational implementation as evidence of phenomenality.
- Preserve epistemic status and source provenance.
- `NOT_EQUIVALENT_TO` edges are semantic no-collapse constraints.
- Mathematical/projective identities, physical realizations, biological claims, phenomenological claims, and speculative extensions must remain separately typed.
- Changes to canonical definitions must be reviewable and traceable.

## Development
- Standard-library implementation is preferred for the core ontology runtime.
- New terms receive stable IDs and stable `phase_index` values; never renumber existing IDs to make the file prettier.
- Validation must pass before promotion.
- Do not write to `main` unless explicitly authorized by the owner.
