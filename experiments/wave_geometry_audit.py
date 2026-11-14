"""Deterministic classical wave geometry audit."""
import math
from core.abom_v8.wave_geometry import dirichlet_mode,equal_wave_intensity,fringe_spacing,inner_product,mode_angular_frequency,phase_from_path_difference

def main():
    constructive=equal_wave_intensity(1,0); destructive=equal_wave_intensity(1,math.pi)
    phase=phase_from_path_difference(.5,1); spacing=fringe_spacing(500e-9,2,1e-3)
    norm=inner_product(lambda x,L:dirichlet_mode(3,x,L),lambda x,L:dirichlet_mode(3,x,L),2)
    orth=inner_product(lambda x,L:dirichlet_mode(2,x,L),lambda x,L:dirichlet_mode(3,x,L),2)
    omega=mode_angular_frequency(3,2,4)
    assert math.isclose(constructive,4,abs_tol=1e-12) and math.isclose(destructive,0,abs_tol=1e-12)
    assert math.isclose(phase,math.pi,abs_tol=1e-12) and math.isclose(spacing,1e-3,rel_tol=1e-12)
    assert math.isclose(norm,1,abs_tol=1e-7) and math.isclose(orth,0,abs_tol=1e-7)
    assert math.isclose(omega,1.5*math.pi,abs_tol=1e-12)
    print("wave geometry audit: PASS")
    print(f"constructive={constructive}; destructive={destructive}; phase={phase:.12g} rad")
    print(f"Young fringe spacing={spacing:.12g} m; mode-3 norm={norm:.12g}; mode-2/3 inner product={orth:.12g}")
    print(f"mode-3 angular frequency={omega:.12g} rad/s")
    print("scope: classical scalar waves and 1D interval eigenmodes only")

if __name__=="__main__": main()
