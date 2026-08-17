import unittest
from pathlib import Path
from consciousness_dictionary.registry import Lexicon
from consciousness_dictionary.gates import can_semantically_merge,directly_non_equivalent
from consciousness_dictionary.query import constrained_phase_path
ROOT=Path(__file__).resolve().parents[1]
class GateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.lex=Lexicon.load(ROOT/'ontology/registry',ROOT/'ontology/relations/relations.jsonl')
    def test_non_equivalence_blocks_merge(self):
        ok,reason=can_semantically_merge(self.lex,'Consciousness','Resonance'); self.assertFalse(ok); self.assertIn('NOT_EQUIVALENT',reason)
    def test_similarity_alone_never_merges(self):
        ok,_=can_semantically_merge(self.lex,'Qualia','Phenomenal Geometry'); self.assertFalse(ok)
    def test_negative_edges_not_used_as_paths(self):
        path=constrained_phase_path(self.lex,'Consciousness','Resonance'); self.assertNotEqual(path,[self.lex.get('Consciousness').term_id,self.lex.get('Resonance').term_id])
if __name__=='__main__': unittest.main()
