import unittest
from consciousness_dictionary.rifc import AffectiveField,RelationalQualiaState,phenomenal_discrepancy,weighted_discrepancy

class RIFCTests(unittest.TestCase):
    def test_discrepancy_is_vector_valued(self):
        a=RelationalQualiaState((0,1),(0,0),AffectiveField(0,0,0,0,0,0),0,(1,0))
        b=RelationalQualiaState((1,1),(0,1),AffectiveField(1,0,0,0,0,0),0.5,(0,1))
        d=phenomenal_discrepancy(a,b); self.assertEqual(len(d.vector()),5); self.assertGreater(d.affect,0)
    def test_scalarization_requires_weights(self):
        a=RelationalQualiaState((0,),(0,),AffectiveField(0,0,0,0,0,0),0,(0,))
        d=phenomenal_discrepancy(a,a)
        with self.assertRaises(ValueError): weighted_discrepancy(d,[1,1])

if __name__=='__main__': unittest.main()
