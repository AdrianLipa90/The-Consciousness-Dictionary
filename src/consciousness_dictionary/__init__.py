"""Executable ontology for The Consciousness Dictionary.

The ontology definition is primary. PhaseNav vectors are deterministic computational
realizations and never silently promote epistemic status or semantic identity.
"""
from .registry import Lexicon, Term, Relation
from .phasenav_native import PhaseVector, vector_from_index, relational_coherence, relational_phase, informational_action
from .affect_detection import AffectDetector, AffectTracker, AffectEstimate, AffectEvidence, TrackedAffectState, affect_phase36

__all__ = [
    "Lexicon", "Term", "Relation",
    "PhaseVector", "vector_from_index", "relational_coherence", "relational_phase", "informational_action",
    "AffectDetector", "AffectTracker", "AffectEstimate", "AffectEvidence", "TrackedAffectState", "affect_phase36",
]
__version__ = "0.2.0-alpha"
