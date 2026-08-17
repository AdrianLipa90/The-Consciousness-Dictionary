from __future__ import annotations
from .registry import Lexicon

# This is a claim-strength lattice for software gating, not a philosophical ranking.
STATUS_TIER={
    'SPECULATIVE_EXTENSION':0,'INTERPRETATION':0,'OPEN_ONTOLOGY':0,
    'HYPOTHESIS':1,'OPEN_HYPOTHESIS':1,'MODEL_HYPOTHESIS':1,'CONSTITUTIVE_HYPOTHESIS':1,'THEORETICAL_POSITION':1,
    'WORKING_DEFINITION':2,'RIFC_WORKING_DEFINITION':2,'MODEL_DEFINITION':2,'MODEL_CLASS':2,'MODEL_PRINCIPLE':2,
    'DEFINITION':3,'METHODOLOGICAL_DEFINITION':3,'METHODOLOGICAL_PRINCIPLE':3,
    'IMPLEMENTED':3,'IMPLEMENTED_DEFINITION':3,'IMPLEMENTATION_PRINCIPLE':3,
    'EXACT_BINARY_RESULT':4,'ESTABLISHED_GEOMETRY':4,'ESTABLISHED_MATH_PHYSICS':4,'DERIVED_OR_EXACT_MODEL_RESULT':4,
}

def directly_non_equivalent(lexicon: Lexicon, a: str, b: str) -> bool:
    x=lexicon.get(a).term_id; y=lexicon.get(b).term_id
    return any(e.relation=='NOT_EQUIVALENT_TO' and ((e.source==x and e.target==y) or (e.source==y and e.target==x)) for e in lexicon.relations)

def can_semantically_merge(lexicon: Lexicon, a: str, b: str) -> tuple[bool,str]:
    if directly_non_equivalent(lexicon,a,b): return False,'explicit NOT_EQUIVALENT_TO gate'
    if lexicon.get(a).term_id==lexicon.get(b).term_id: return True,'same canonical term'
    return False,'no explicit equivalence/alias relation; similarity is insufficient'

def promotion_requires_evidence(old_status: str, new_status: str) -> bool:
    return STATUS_TIER.get(new_status,2) > STATUS_TIER.get(old_status,2)
