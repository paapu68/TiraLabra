#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Tässä moduulissa laskentaan liittyviä funktioita. Esim. 
ratkaistaan hartree potentiaali  """

def tee_gauss_seidel_yksi_askel(gridi, varaus, dx, dy, dz):
    """ Iteroidaan Poissonin yhtälön (nabla²=-4*pi*rho)
    ratkaisua yksi askel:
    http://en.wikipedia.org/wiki/Discrete_Poisson_equation
    Ratkaisun pitäisi olla Hartree potentiaali.
    Käytetään Gauss-Seidel iteraatiota:
    http://en.wikipedia.org/wiki/Gauss%E2%80%93Seidel_method
    """
    from math import pi
    imax = gridi.shape[0]
    jmax = gridi.shape[1]
    kmax = gridi.shape[2]
    #2d
    if kmax < 2:
        k=0
        for i in range(0, imax-1):
            for j in range(0, jmax-1):
                gridi[i,j,k] = \
                    gridi[i-1,j,k]*0.25 + \
                    gridi[i+1,j,k]*0.25 + \
                    gridi[i,j-1,k]*0.25 + \
                    gridi[i,j+1,k]*0.25 + \
                    pi * varaus[i,j,k] * dx * dy
    #3d
    #3d
    else:
        for i in range(0, imax-1):
            for j in range(0, jmax-1):
                for k in range(0, kmax-1):
                    gridi[i,j,k] = \
                        gridi[i,j,k-1]/6 + \
                        gridi[i,j,k+1]/6 + \
                        gridi[i-1,j,k]/6 + \
                        gridi[i+1,j,k]/6 + \
                        gridi[i,j-1,k]/6 + \
                        gridi[i,j+1,k]/6 + \
                        2 / 3 * pi * varaus[i,j,k] * dx * dy * dz
