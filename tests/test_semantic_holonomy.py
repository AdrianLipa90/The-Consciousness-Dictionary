import cmath
import math
import unittest

from consciousness_dictionary.phasenav_native import (
    inner_product,
    semantic_holonomy_coupling,
    u1_semantic_holonomy_phase,
    u1_semantic_transport,
    vector_from_index,
)


class SemanticHolonomyTests(unittest.TestCase):
    def test_transport_is_unit_modulus_and_additive(self):
        a=(0.20,-0.35)
        b=(0.80,0.10)
        self.assertAlmostEqual(abs(u1_semantic_transport(a+b)),1.0,places=12)
        self.assertAlmostEqual(
            abs(u1_semantic_transport(a+b)-u1_semantic_transport(a)*u1_semantic_transport(b)),
            0.0,places=12,
        )

    def test_open_path_gauge_covariance(self):
        edges=(0.25,-0.40,0.75)
        chi=(0.10,0.55,-0.20,0.35)
        shifted=tuple(edges[k]+chi[k+1]-chi[k] for k in range(len(edges)))
        expected=cmath.exp(1j*(chi[-1]-chi[0]))*u1_semantic_transport(edges)
        self.assertAlmostEqual(abs(u1_semantic_transport(shifted)-expected),0.0,places=12)

    def test_closed_loop_gauge_invariance(self):
        edges=(0.25,-0.40,0.75)
        chi=(0.10,0.55,-0.20)
        shifted=tuple(
            edges[k]+chi[(k+1)%len(chi)]-chi[k]
            for k in range(len(edges))
        )
        self.assertAlmostEqual(
            abs(u1_semantic_transport(shifted)-u1_semantic_transport(edges)),
            0.0,places=12,
        )

    def test_semantic_coupling_preserves_strength_and_adds_phase(self):
        left=vector_from_index(3)
        right=vector_from_index(47)
        edges=(0.17,0.29,-0.08)
        z=inner_product(left,right)
        c=semantic_holonomy_coupling(left,right,edges)
        self.assertAlmostEqual(abs(c),abs(z),places=12)
        if abs(z)>1e-15:
            self.assertAlmostEqual(
                abs(c/z-u1_semantic_transport(edges)),0.0,places=12
            )
        self.assertAlmostEqual(
            cmath.phase(u1_semantic_transport(edges)),
            u1_semantic_holonomy_phase(edges),
            places=12,
        )


if __name__=="__main__":
    unittest.main()
