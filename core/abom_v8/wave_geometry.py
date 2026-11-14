"""Analytic classical wave/interference reference for Motion-to-Form research.

Separate from QWAVE SI metadata and the hydrogen stationary-state baseline.
Implements classical monochromatic superposition and 1D interval modes; not a
quantum solver, spacetime model, or claim about matter formation.
"""
from __future__ import annotations
import cmath, math
from dataclasses import dataclass
from typing import Iterable

def _finite(name, value):
    value=float(value)
    if not math.isfinite(value): raise ValueError(f"{name} must be finite")
    return value

@dataclass(frozen=True)
class PlaneWave:
    amplitude: complex
    wavevector: tuple[float, ...]
    angular_frequency: float
    phase: float=0.0
    def __post_init__(self):
        if not self.wavevector: raise ValueError("wavevector must have at least one dimension")
        if not all(math.isfinite(float(v)) for v in self.wavevector): raise ValueError("wavevector must be finite")
        if not math.isfinite(self.angular_frequency) or self.angular_frequency<=0: raise ValueError("angular_frequency must be positive and finite")
        if not math.isfinite(self.phase): raise ValueError("phase must be finite")
        if not (math.isfinite(self.amplitude.real) and math.isfinite(self.amplitude.imag)): raise ValueError("amplitude must be finite")
    def evaluate(self, position: Iterable[float], time=0.0):
        point=tuple(float(v) for v in position)
        if len(point)!=len(self.wavevector): raise ValueError("position and wavevector dimensions must match")
        if not all(math.isfinite(v) for v in point): raise ValueError("position must be finite")
        argument=sum(k*x for k,x in zip(self.wavevector,point))-self.angular_frequency*_finite("time",time)+self.phase
        return self.amplitude*cmath.exp(1j*argument)

def superpose(waves, position, time=0.0):
    wave_list=tuple(waves)
    if not wave_list: raise ValueError("at least one wave is required")
    return sum((w.evaluate(position,time) for w in wave_list),0j)

def intensity(field):
    if not (math.isfinite(field.real) and math.isfinite(field.imag)): raise ValueError("field must be finite")
    return abs(field)**2

def two_wave_intensity(a1, a2, phase_difference):
    if not all(math.isfinite(z.real) and math.isfinite(z.imag) for z in (a1,a2)): raise ValueError("amplitudes must be finite")
    return intensity(a1+a2*cmath.exp(1j*_finite("phase_difference",phase_difference)))

def equal_wave_intensity(amplitude, phase_difference):
    a=_finite("amplitude",amplitude); d=_finite("phase_difference",phase_difference)
    return 4*a*a*math.cos(d/2)**2

def phase_from_path_difference(path_difference,wavelength):
    dr=_finite("path_difference",path_difference); lam=_finite("wavelength",wavelength)
    if lam<=0: raise ValueError("wavelength must be positive")
    return 2*math.pi*dr/lam

def fringe_spacing(wavelength,screen_distance,source_separation):
    lam=_finite("wavelength",wavelength); distance=_finite("screen_distance",screen_distance); separation=_finite("source_separation",source_separation)
    if min(lam,distance,separation)<=0: raise ValueError("all dimensions must be positive")
    return lam*distance/separation

def dirichlet_mode(mode,x,length):
    if isinstance(mode,bool) or not isinstance(mode,int) or mode<1: raise ValueError("mode must be a positive integer")
    x=_finite("x",x); L=_finite("length",length)
    if L<=0 or not 0<=x<=L: raise ValueError("require length > 0 and x in [0,length]")
    return math.sqrt(2/L)*math.sin(mode*math.pi*x/L)

def neumann_mode(mode,x,length):
    if isinstance(mode,bool) or not isinstance(mode,int) or mode<0: raise ValueError("mode must be a nonnegative integer")
    x=_finite("x",x); L=_finite("length",length)
    if L<=0 or not 0<=x<=L: raise ValueError("require length > 0 and x in [0,length]")
    return (1/math.sqrt(L) if mode==0 else math.sqrt(2/L))*math.cos(mode*math.pi*x/L)

def mode_angular_frequency(mode,wave_speed,length):
    if isinstance(mode,bool) or not isinstance(mode,int) or mode<1: raise ValueError("mode must be a positive integer")
    c=_finite("wave_speed",wave_speed); L=_finite("length",length)
    if c<=0 or L<=0: raise ValueError("wave_speed and length must be positive")
    return c*mode*math.pi/L

def inner_product(left,right,length,samples=20000):
    L=_finite("length",length)
    if L<=0 or isinstance(samples,bool) or not isinstance(samples,int) or samples<2: raise ValueError("invalid integration domain or sample count")
    dx=L/samples
    return sum(left((i+.5)*dx,L)*right((i+.5)*dx,L) for i in range(samples))*dx
