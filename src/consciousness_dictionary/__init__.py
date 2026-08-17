"""Executable ontology for The Consciousness Dictionary.

The ontology definition is primary. PhaseNav vectors are deterministic computational
realizations and never silently promote epistemic status or semantic identity.
"""
from .registry import Lexicon, Term, Relation
from .phasenav_native import PhaseVector, vector_from_index, relational_coherence, relational_phase, informational_action

__all__ = ["Lexicon", "Term", "Relation", "PhaseVector", "vector_from_index", "relational_coherence", "relational_phase", "informational_action"]
__version__ = "0.2.0-alpha"
