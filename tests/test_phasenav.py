import math, unittest
from consciousness_dictionary.phasenav_native import *

class PhaseNavTests(unittest.TestCase):
    def test_vector_shape_and_range(self):
        v=vector_from_index(1); self.assertEqual(len(v),36); self.assertTrue(all(0<=x<TAU for x in v))
    def test_self_coherence(self):
        v=vector_from_index(11); self.assertAlmostEqual(relational_coherence(v,v),1.0,places=10)
    def test_symmetry(self):
        a=vector_from_index(3); b=vector_from_index(47); self.assertAlmostEqual(relational_coherence(a,b),relational_coherence(b,a),places=12)
    def test_delta_antisymmetry(self):
        a=vector_from_index(9); b=vector_from_index(18); d1=relation_delta(a,b); d2=relation_delta(b,a); self.assertTrue(all(abs(x+y)<1e-10 for x,y in zip(d1,d2)))
    def test_semantic_mass_is_implementation_quantity(self):
        self.assertGreater(semantic_mass(5),0.0)

if __name__=='__main__': unittest.main()
