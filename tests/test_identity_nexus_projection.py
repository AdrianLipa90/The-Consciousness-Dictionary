import math
import unittest

from consciousness_dictionary.registry import Lexicon
from consciousness_dictionary.phasenav_native import PhaseState
from consciousness_dictionary.query import external_phase_projection


def term(term_id: str, name: str, definition: str, phase_index: int) -> dict:
    return {
        "term_id": term_id,
        "canonical_name": name,
        "definition": definition,
        "formal_class": "concept",
        "epistemic_status": "DEFINITION",
        "phase_index": phase_index,
        "category": "Meta-formal primitives",
        "dependencies": [],
        "not_equivalent_to": [],
    }


class IdentityNexusProjectionTests(unittest.TestCase):
    def setUp(self):
        self.lexicon = Lexicon([
            term("T-A", "Alpha", "first canonical state", 1),
            term("T-B", "Beta", "second canonical state", 2),
            term("T-C", "Gamma", "third canonical state", 3),
        ])

    def test_exact_term_vector_ranks_same_term_first(self):
        t = self.lexicon.get("T-A")
        q = PhaseState.from_term(t.term_id, t.phase_index, t.raw).vector
        rows = external_phase_projection(self.lexicon, q, limit=3)
        self.assertEqual(rows[0]["term_id"], "T-A")
        self.assertAlmostEqual(rows[0]["coherence"], 1.0, places=12)
        self.assertAlmostEqual(rows[0]["informational_action"], 0.0, places=9)
        self.assertFalse(rows[0]["semantic_equivalence"])
        self.assertFalse(rows[0]["authority_grant"])

    def test_limit_is_bounded_and_deterministic(self):
        t = self.lexicon.get("T-B")
        q = PhaseState.from_term(t.term_id, t.phase_index, t.raw).vector
        a = external_phase_projection(self.lexicon, q, limit=2)
        b = external_phase_projection(self.lexicon, q, limit=2)
        self.assertEqual(a, b)
        self.assertEqual(len(a), 2)

    def test_wrong_dimension_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "36 components"):
            external_phase_projection(self.lexicon, [0.0] * 35)

    def test_nonfinite_fails_closed(self):
        q = [0.0] * 36
        q[7] = math.nan
        with self.assertRaisesRegex(ValueError, "non-finite"):
            external_phase_projection(self.lexicon, q)

    def test_nonpositive_limit_is_quiet(self):
        self.assertEqual(external_phase_projection(self.lexicon, [0.0] * 36, limit=0), [])


if __name__ == "__main__":
    unittest.main()
