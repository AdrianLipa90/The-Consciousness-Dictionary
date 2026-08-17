import json, unittest
from pathlib import Path
from consciousness_dictionary.registry import Lexicon
from consciousness_dictionary.validate import validate

ROOT=Path(__file__).resolve().parents[1]
class RegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.lex=Lexicon.load(ROOT/'ontology/registry/v0_2',ROOT/'ontology/relations/extra_relations.jsonl')
    def test_large_dictionary(self): self.assertGreaterEqual(len(self.lex.terms),500)
    def test_core_terms(self):
        for name in ['Consciousness','Qualia','Mineness','Interoception','Meaning','Intention','PhaseNav 36-Mode Embedding','Falsification Criterion']:
            self.assertTrue(self.lex.get(name).term_id.startswith('CLX2-'))
    def test_compact_registry_integrity(self):
        import hashlib
        reg=ROOT/'ontology/registry/v0_2'
        idx=json.loads((reg/'index.json').read_text())
        self.assertEqual(idx['term_count'],548)
        self.assertEqual(sum(x['count'] for x in idx['shards']),548)
        for shard in idx['shards']:
            digest=hashlib.sha256((reg/shard['path']).read_bytes()).hexdigest()
            self.assertEqual(digest,shard['sha256'],shard['path'])
    def test_no_self_negative_edges(self):
        for t in self.lex.terms.values():
            self.assertNotIn(t.term_id,t.raw.get('not_equivalent_to',[]),t.term_id)
    def test_validation(self):
        formulas={x['formula_id'] for x in json.loads((ROOT/'ontology/formulas/formulas.json').read_text())['formulas']}
        report=validate(self.lex,formulas); self.assertEqual(report['status'],'PASS',report)

if __name__=='__main__': unittest.main()
