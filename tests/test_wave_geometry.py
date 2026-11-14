import math, unittest
from core.abom_v8.wave_geometry import *

class WaveGeometryTests(unittest.TestCase):
    def test_interference_extrema(self):
        self.assertAlmostEqual(equal_wave_intensity(2,0),16,places=12)
        self.assertAlmostEqual(equal_wave_intensity(2,math.pi),0,places=12)
        self.assertAlmostEqual(equal_wave_intensity(2,2*math.pi),16,places=12)
    def test_general_two_wave_formula(self):
        a,b,d=2+0j,3+0j,.7
        self.assertAlmostEqual(two_wave_intensity(a,b,d),intensity(a+b*complex(math.cos(d),math.sin(d))),places=12)
    def test_plane_wave_superposition(self):
        a=PlaneWave(1+0j,(2.,),3.)
        b=PlaneWave(1+0j,(2.,),3.,math.pi)
        self.assertAlmostEqual(abs(superpose((a,b),(.4,),.2)),0,places=12)
    def test_path_phase_and_fringe_spacing(self):
        self.assertAlmostEqual(phase_from_path_difference(.5,1),math.pi)
        self.assertAlmostEqual(fringe_spacing(500e-9,2,1e-3),1e-3)
    def test_dirichlet_boundary_normalization_orthogonality(self):
        L=3.
        for n in (1,2,3):
            self.assertAlmostEqual(dirichlet_mode(n,0,L),0,places=12)
            self.assertAlmostEqual(dirichlet_mode(n,L,L),0,places=12)
            self.assertAlmostEqual(inner_product(lambda x,L:dirichlet_mode(n,x,L),lambda x,L:dirichlet_mode(n,x,L),L),1,places=7)
        for n,m in ((1,2),(1,3),(2,4)):
            self.assertAlmostEqual(inner_product(lambda x,L:dirichlet_mode(n,x,L),lambda x,L:dirichlet_mode(m,x,L),L),0,places=7)
    def test_neumann_modes(self):
        L=4.
        self.assertAlmostEqual(neumann_mode(0,0,L),.5)
        self.assertAlmostEqual(inner_product(lambda x,L:neumann_mode(0,x,L),lambda x,L:neumann_mode(0,x,L),L),1,places=7)
        self.assertAlmostEqual(inner_product(lambda x,L:neumann_mode(1,x,L),lambda x,L:neumann_mode(2,x,L),L),0,places=7)
    def test_mode_frequency(self):
        self.assertAlmostEqual(mode_angular_frequency(2,3,4),1.5*math.pi,places=12)
    def test_invalid_inputs(self):
        calls=(lambda:fringe_spacing(1,0,1),lambda:phase_from_path_difference(1,0),lambda:dirichlet_mode(0,.5,1),lambda:dirichlet_mode(1,1.1,1),lambda:neumann_mode(-1,.5,1),lambda:mode_angular_frequency(1,-1,1),lambda:PlaneWave(1+0j,(),1))
        for call in calls:
            with self.assertRaises(ValueError): call()

if __name__=="__main__": unittest.main()
