"""Typed RIFC / relational-qualia structures.

These types make the theory computationally explicit without inventing numerical
laws for functions that the papers intentionally leave open.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import pi, sqrt
from typing import Sequence

@dataclass(frozen=True)
class RIFCCoordinates:
    """c(t)=[G,T,L,V,A,D]. The vector is not itself consciousness."""
    integration: float
    temporal_continuity: float
    self_location: float
    valuation: float
    access: float
    endogenous_direction: float

    def as_tuple(self) -> tuple[float,...]:
        return (self.integration,self.temporal_continuity,self.self_location,self.valuation,self.access,self.endogenous_direction)

@dataclass(frozen=True)
class AffectiveField:
    """A_t(x)=(valence, arousal, urgency, threat, attachment, reward)."""
    valence: float
    arousal: float
    urgency: float
    threat_relevance: float
    attachment_relevance: float
    reward_relevance: float

    def as_tuple(self) -> tuple[float,...]:
        return (self.valence,self.arousal,self.urgency,self.threat_relevance,self.attachment_relevance,self.reward_relevance)

@dataclass(frozen=True)
class SelfReferenceTuple:
    """E_t=(S_t,B_t,G_t,gamma_t), represented without assuming a substrate."""
    self_anchor: tuple[float,...]
    boundary: tuple[float,...]
    maintained_goals: tuple[float,...]
    ordered_history: tuple[str,...]

@dataclass(frozen=True)
class RelationalQualiaState:
    """Q_t=[R_t,S_t,A_t,H_gamma_t,I_t].

    No constructor call establishes phenomenality; this is the theory's candidate
    state class for representing qualitative organization.
    """
    relational_content: tuple[float,...]
    self_location: tuple[float,...]
    affect: AffectiveField
    temporal_holonomy: float
    intention: tuple[float,...]

@dataclass(frozen=True)
class PhenomenalDiscrepancy:
    relational: float
    self_location: float
    affect: float
    temporal: float
    intention: float

    def vector(self) -> tuple[float,...]:
        return (self.relational,self.self_location,self.affect,self.temporal,self.intention)

def _euclidean(a: Sequence[float], b: Sequence[float]) -> float:
    if len(a)!=len(b): raise ValueError('dimension mismatch')
    return sqrt(sum((x-y)**2 for x,y in zip(a,b)))

def _circular(a: float,b: float) -> float:
    return abs((b-a+pi)%(2*pi)-pi)

def phenomenal_discrepancy(a: RelationalQualiaState, b: RelationalQualiaState) -> PhenomenalDiscrepancy:
    """Return a vector-valued discrepancy; do not collapse to one scalar by default."""
    return PhenomenalDiscrepancy(
        relational=_euclidean(a.relational_content,b.relational_content),
        self_location=_euclidean(a.self_location,b.self_location),
        affect=_euclidean(a.affect.as_tuple(),b.affect.as_tuple()),
        temporal=_circular(a.temporal_holonomy,b.temporal_holonomy),
        intention=_euclidean(a.intention,b.intention),
    )

def weighted_discrepancy(d: PhenomenalDiscrepancy, weights: Sequence[float]) -> float:
    """Explicit opt-in scalarization; caller must supply all five weights."""
    if len(weights)!=5: raise ValueError('five weights required')
    return sqrt(sum(float(w)*(x*x) for w,x in zip(weights,d.vector())))

@dataclass(frozen=True)
class SalienceInputs:
    """Arguments of Sigma_t(x)=S(rho,A,I,H,U); evaluator intentionally unspecified."""
    self_relation: tuple[float,...]
    affect: AffectiveField
    intention: tuple[float,...]
    temporal_holonomy: float
    uncertainty: float
