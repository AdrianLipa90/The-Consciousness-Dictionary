"""PhaseNav-native 36D realization used by the Consciousness Dictionary.

Source provenance: canonical NOEMA/PhaseNav ``pnv_runtime.py`` recovered on
2026-08-17. This module keeps the declared 36D phase formula and relation kernel
self-contained (stdlib only) so ontology builds are reproducible.

Important boundary: a PhaseNav vector is a computational realization of a term card.
It is NOT the term definition, phenomenality, truth, authority, or a physical quantum
state by itself.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import atan2, cos, log, pi, sin, sqrt
from typing import Iterable, Sequence

VECTOR_DIM = 36
TAU = 2.0 * pi
KAPPA = log(2.0) / (24.0 * pi)
L3, L4, L5 = 7, 2, 5
ALPHA_M = 1.0 / ((L3 * L4) ** 2 - L3 ** 2 - L4 * L5 + L4 ** 2 * KAPPA)
L_RATIO = L4 / L3
_Q_PRIMES = (3, 5, 7, 11, 13, 17)
_N_INTENTION = sqrt(1.0 + ALPHA_M**2 + L_RATIO**2)
INTENTION_AXIS = (1.0 / _N_INTENTION, ALPHA_M / _N_INTENTION, L_RATIO / _N_INTENTION)

PhaseVector = tuple[float, ...]

def _quark_prime(k: int) -> int:
    return _Q_PRIMES[(k - 1) % len(_Q_PRIMES)]

def wrap(x: float) -> float:
    return float(x) % TAU

def circular_delta(a: float, b: float) -> float:
    """Shortest signed delta b-a in [-pi, pi)."""
    return (b - a + pi) % TAU - pi

def vector_from_index(index: int) -> PhaseVector:
    """Canonical 36D PhaseNav term vector from a stable positive phase index."""
    k = max(1, int(index))
    qk = _quark_prime(k)
    out = []
    for i in range(VECTOR_DIM):
        phi = (KAPPA * TAU + ALPHA_M * TAU * (i % L3) + L_RATIO * TAU * (i // L3) + (qk % L5) * TAU / L3) % TAU
        out.append(round(phi, 10))
    return tuple(out)

def mean_phase(v: Sequence[float]) -> float:
    return atan2(sum(sin(x) for x in v), sum(cos(x) for x in v))

def order_parameter(v: Sequence[float]) -> float:
    n = len(v) or 1
    return sqrt(sum(sin(x) for x in v)**2 + sum(cos(x) for x in v)**2) / n

def angular_distance(a: Sequence[float], b: Sequence[float]) -> float:
    if len(a) != len(b): raise ValueError("dimension mismatch")
    n = len(a) or 1
    return sqrt(sum(circular_delta(x, y)**2 for x, y in zip(a, b)) / n)

def inner_product(a: Sequence[float], b: Sequence[float]) -> complex:
    if len(a) != len(b): raise ValueError("dimension mismatch")
    n = len(a) or 1
    return complex(sum(cos(y-x) for x,y in zip(a,b))/n, sum(sin(y-x) for x,y in zip(a,b))/n)

def relational_coherence(a: Sequence[float], b: Sequence[float]) -> float:
    z = inner_product(a, b)
    return z.real*z.real + z.imag*z.imag

def relational_phase(a: Sequence[float], b: Sequence[float]) -> float:
    z = inner_product(a, b)
    return atan2(z.imag, z.real)

def informational_action(a: Sequence[float], b: Sequence[float], epsilon: float = 1e-12) -> float:
    return -KAPPA * log(relational_coherence(a, b) + float(epsilon))

def berry_connection(a: Sequence[float], b: Sequence[float]) -> float:
    if len(a) != len(b): raise ValueError("dimension mismatch")
    n = len(a) or 1
    return sum(sin(y-x) for x,y in zip(a,b))/n

def berry_holonomy(path: Sequence[Sequence[float]]) -> float:
    if len(path) < 2: return 0.0
    g = sum(berry_connection(path[i], path[i+1]) for i in range(len(path)-1))
    g += berry_connection(path[-1], path[0])
    return atan2(sin(g), cos(g))

def relation_delta(a: Sequence[float], b: Sequence[float]) -> PhaseVector:
    if len(a) != len(b): raise ValueError("dimension mismatch")
    return tuple(circular_delta(x,y) for x,y in zip(a,b))

def phasor_superposition(a: Sequence[float], b: Sequence[float], weight: float = 0.5) -> PhaseVector:
    if len(a) != len(b): raise ValueError("dimension mismatch")
    w2=float(weight); w1=1.0-w2
    return tuple(wrap(atan2(w1*sin(x)+w2*sin(y), w1*cos(x)+w2*cos(y))) for x,y in zip(a,b))

def intention_apply(v: Sequence[float], strength: float = 1.0) -> PhaseVector:
    nx, ny, _ = INTENTION_AXIS
    mp=mean_phase(v); R=order_parameter(v)
    return tuple(wrap(x + strength*KAPPA*(nx*sin(x)*R + ny*cos(x)*sin(mp))) for x in v)

def semantic_mass(index: int, v: Sequence[float] | None = None) -> float:
    k=max(1,int(index)); vec=v if v is not None else vector_from_index(k); R=order_parameter(vec)
    return KAPPA*(1.0+ALPHA_M*k)+L_RATIO*R

def project_bloch(v: Sequence[float]) -> tuple[float,float]:
    """Two-observable summary from order parameter and circular mean.

    This is intentionally labelled a lossy task summary, not a faithful 36D embedding.
    """
    R=max(1e-15,min(1.0,order_parameter(v)))
    theta=2.0*atan2(sqrt(max(0.0,1.0-R*R)),R)
    return (theta, wrap(mean_phase(v)))


def collatz_hash(text: str) -> int:
    """Canonical PhaseNav Collatz hash used by M_sentence_phase."""
    h=int.from_bytes(str(text).encode("utf-8"),"big") % (2**61-1)
    for _ in range(13):
        h = h//2 if h%2==0 else 3*h+1
        h %= (2**61-1)
    return h

def sentence_phase(text: str) -> PhaseVector:
    """Canonical PhaseNav M_sentence_phase semantic vectorization (stdlib form)."""
    words=str(text).lower().split()
    if not words: return vector_from_index(1)
    sums_s=[0.0]*VECTOR_DIM; sums_c=[0.0]*VECTOR_DIM
    for word in words:
        h=collatz_hash(word)
        for i in range(VECTOR_DIM):
            phi=(h*KAPPA*TAU*(i+1)) % TAU
            sums_s[i]+=sin(phi); sums_c[i]+=cos(phi)
    n=len(words)
    return tuple(wrap(atan2(sums_s[i]/n,sums_c[i]/n)) for i in range(VECTOR_DIM))

def canonical_term_payload(raw: dict) -> str:
    """Deterministic semantic payload; IDs are preserved separately from meaning."""
    deps=" ".join(sorted(str(x) for x in raw.get("dependency_names",[])))
    return " | ".join([str(raw.get("canonical_name","")),str(raw.get("definition","")),str(raw.get("formal_class","")),str(raw.get("category","")),deps])

def term_vector(raw: dict) -> PhaseVector:
    return sentence_phase(canonical_term_payload(raw))

@dataclass(frozen=True)
class PhaseState:
    term_id: str
    phase_index: int
    vector: PhaseVector
    order_parameter: float
    semantic_mass: float

    @classmethod
    def from_term(cls, term_id: str, phase_index: int, raw: dict | None = None) -> "PhaseState":
        v=term_vector(raw) if raw is not None else vector_from_index(phase_index)
        return cls(term_id,phase_index,v,order_parameter(v),semantic_mass(phase_index,v))
