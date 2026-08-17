import unittest
from pathlib import Path
from consciousness_dictionary.registry import Lexicon
from consciousness_dictionary.query import phase_similarity

ROOT=Path(__file__).resolve().parents[1]
class BoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.lex=Lexicon.load(ROOT/'ontology/registry',ROOT/'ontology/relations/relations.jsonl')
    def test_similarity_never_claims_equivalence(self):
        rows=phase_similarity(self.lex,'Consciousness',5); self.assertTrue(all(r['semantic_equivalence'] is False for r in rows))
    def test_consciousness_not_resonance(self):
        c=self.lex.get('Consciousness'); r=self.lex.get('Resonance'); self.assertIn(r.term_id,c.raw['not_equivalent_to'])
    def test_intention_not_aboutness(self):
        i=self.lex.get('Intention'); a=self.lex.get('Intentionality / Aboutness'); self.assertIn(a.term_id,i.raw['not_equivalent_to'])

if __name__=='__main__': unittest.main()
