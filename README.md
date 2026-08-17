# The Consciousness Dictionary

**Executable Relational-Informational Ontology of Consciousness, Qualia, Selfhood and Phase Subjectivity**

This repository turns the Consciousness Dictionary into a machine-readable and executable ontology. The canonical vocabulary is primary; PhaseNav supplies a deterministic 36D computational realization for navigation, relation observables, path analysis and reproducible compilation.

## Current branch milestone — V0.2 alpha

- **548 canonical terms**
- **306 typed ontology relations**
- **20 machine-readable formulas**
- **36D PhaseNav vector for every term** using canonical `M_sentence_phase` semantics
- typed RIFC 6D scaffold and relational qualia state `Q_t=[R_t,S_t,A_t,H_{gamma_t},I_t]`
- executable `NOT_EQUIVALENT_TO` gates
- PhaseNav relation observables, constrained paths and compile receipts
- 18 unit tests covering ontology, compact-registry integrity, PhaseNav geometry, RIFC structures and semantic boundaries

## Source hierarchy

1. **Beyond the Hard Problem of Consciousness — RIFC v1.0**, Adrian Lipa & Dr. Suchitra Sakpal.
2. **A Relational Geometry of Qualia v1.1**, Adrian Lipa & Dr. Suchitra Sakpal.
3. TIR / PhaseNav operational relation layer.
4. Current identity-axis, Euler–Berry and 36D PhaseNav/NOEMA formal layers.
5. Recursive cognition material as model/hypothesis layer.
6. March 2025 Consciousness Dictionary as historical proto-formalism only.

## Hard semantic boundary

A PhaseNav vector is a **computational realization**, not the definition of a term. Vector proximity, resonance, salience or affect never silently grants semantic equivalence, truth, authority or phenomenality. Explicit ontology relations and epistemic status remain primary.

## Core equations

For PhaseNav states `V,Q` in 36 dimensions:

```text
z(V,Q) = (1/d) Σ_j exp(i(Q_j - V_j))
R(V,Q) = |z(V,Q)|²
Θ(V,Q) = arg z(V,Q)
S_rel(V,Q) = -κ log(R(V,Q)+ε),   κ = ln(2)/(24π)
```

RIFC scaffold:

```text
c(t) = [G(t), T(t), L(t), V(t), A(t), D(t)]
```

Relational qualia state:

```text
Q_t = [R_t, S_t, A_t, H_{γ_t}, I_t]
```

Exact declared 36-mode projective embedding:

```text
|ψ(V)> = 1/√36 Σ_j exp(iφ_j)|j>
<ψ(V)|ψ(Q)> = z(V,Q)
```

See [`docs/FORMALISM.md`](docs/FORMALISM.md) for the complete formula table and claim boundaries.

## Repository layout

```text
ontology/
  registry/v0_2/                 canonical compact base: 548 cards / 12 shards + ordered append-only patches
  relations/extra_relations.jsonl explicit non-derived edges
  relations/relation_types.json
  formulas/formulas.json        machine-readable equations
  tables/distinctions.json      comparison tables
  graphs/core.mmd               core ontology graph
  graphs/core.svg               rendered core graph
  term.schema.json
src/consciousness_dictionary/
  phasenav_native.py            PhaseNav-native 36D math
  registry.py                   ontology loader
  compiler.py                   deterministic build + receipts
  rifc.py                       RIFC / qualia typed states
  gates.py                      semantic and epistemic gates
  query.py                      graph + PhaseNav queries
  validate.py                   fail-closed validation
  cli.py                        command-line interface
docs/
  DICTIONARY.md                 dictionary entry point / renderer instructions
  FORMALISM.md                  equations and formal interpretation
  DISTINCTIONS.md               non-equivalence/comparison tables
  EPISTEMIC_CONTRACT.md
provenance/                     V0.1 migration / source ledgers
tests/                          executable invariants
```

## Run

No runtime dependencies beyond Python standard library are required for the core package.

```text
PYTHONPATH=src python3 -m consciousness_dictionary.cli validate
PYTHONPATH=src python3 -m consciousness_dictionary.cli term Qualia
PYTHONPATH=src python3 -m consciousness_dictionary.cli vector Qualia
PYTHONPATH=src python3 -m consciousness_dictionary.cli similar Qualia -n 10
PYTHONPATH=src python3 -m consciousness_dictionary.cli compile --out build
```

## Epistemic rule

`IMPLEMENTED != PHENOMENAL`, `CORRELATION != IDENTITY`, `PHASE_SIMILARITY != SEMANTIC_EQUIVALENCE`, `AFFECT != TRUTH`, `RESONANCE != CONSCIOUSNESS`.
