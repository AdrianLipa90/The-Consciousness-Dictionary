# W_sem — nonlocal semantic coupling as U(1) phase holonomy

Status: `EXECUTABLE_MODEL_BINDING / CHYBA / CANON_TERMSET_UNCHANGED`

Date: 2026-09-19

## Definition

The Consciousness Dictionary binds the symbol

\[
W^{\rm sem}_{ij}[\gamma]
\]

to a nonlocal semantic phase transporter derived from a local semantic connection/potential `A_sem`:

\[
\boxed{
W^{\rm sem}_{ij}[\gamma]
=
\exp\!\left(i\int_{\gamma_{ij}} A_{\rm sem}\right)
\in U(1).
}
\]

For the discrete executable realization,

\[
\boxed{
W^{\rm sem}_{ij}[\gamma]
=
\exp\!\left(i\sum_{e\in\gamma}A_e^{\rm sem}\right).
}
\]

The local edge values are the potential/connection data. `W_sem` is the path-level, nonlocal transport.

## Semantic coupling observable

For the exact 36-mode PhaseNav projective realization,

\[
z(V_i,V_j)
=
\langle\psi(V_i)|\psi(V_j)\rangle.
\]

The transported semantic coupling is

\[
\boxed{
\mathcal C_{ij}[\gamma]
=
W^{\rm sem}_{ij}[\gamma]z(V_i,V_j).
}
\]

Therefore

\[
S_{ij}=|\mathcal C_{ij}|,
\qquad
\Phi_{ij}=\arg\mathcal C_{ij}.
\]

Pure U(1) transport preserves the overlap magnitude and changes its relational phase.

## Gauge rule

For

\[
A_{\rm sem}\mapsto A_{\rm sem}+d\chi,
\]

an open transporter is endpoint-covariant,

\[
W_{ij}^{\rm sem}
\mapsto
e^{i\chi(i)}W_{ij}^{\rm sem}e^{-i\chi(j)}.
\]

For a closed loop,

\[
\boxed{
W_\gamma^{\rm sem}
=
\exp\!\left(i\oint_\gamma A_{\rm sem}\right)
}
\]

is gauge invariant. A nonzero loop phase is a model-level relational/semantic curvature or frustration witness.

## Collision firewall

The symbol `A_t` is already used by RIFC for the affect field

\[
A_t(x)=(v,a,u,\tau,\alpha,r).
\]

Therefore the connection in this contract is always written `A_sem`, `A_conn`, or `\\mathcal A^{sem}`. It is **not** the affect field.

Likewise `W_sem` is not a weak-interaction `W^\pm` boson.

## Executable API

`src/consciousness_dictionary/phasenav_native.py` exposes:

- `u1_semantic_transport(edge_potentials)`;
- `u1_semantic_holonomy_phase(edge_potentials)`;
- `semantic_holonomy_coupling(a, b, edge_potentials)`.

The implementation uses only the existing stdlib PhaseNav realization.

## Epistemic boundary

The exact U(1) algebra and gauge identities are mathematical/software statements.

This binding does not establish a physical gauge field, physical nonlocal signalling, hypercharge, or a theory of consciousness. It gives the dictionary an executable representation of the declared nonlocal semantic coupling.

The canonical 548-term registry is unchanged in this candidate. Promotion to a new canonical dictionary term requires a separate ontology/card decision.
