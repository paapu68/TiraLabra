#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Tässä moduulissa laskentaan liittyviä funktioita. Esim. 
ratkaistaan hartree potentiaali  """

import numpy as np
import energiat

def tee_gauss_seidel_yksi_askel(V_hartree, varaus):
    """ Iteroidaan Poissonin yhtälön (nabla²=-4*pi*rho)
    ratkaisua yksi askel:
    http://en.wikipedia.org/wiki/Discrete_Poisson_equation
    Ratkaisun pitäisi olla Hartree potentiaali.
    Käytetään Gauss-Seidel iteraatiota:
    http://en.wikipedia.org/wiki/Gauss%E2%80%93Seidel_method

    xxx: parannus ks.
    http://wiki.scipy.org/PerformancePython
    """
    from math import pi
    gridi = V_hartree.gridi
    h = V_hartree.get_grid_step()
    imax = gridi.shape[0]
    jmax = gridi.shape[1]
    kmax = gridi.shape[2]
    #2d
    if kmax < 2:
        k=0
        for i in range(1, imax-1):
            for j in range(1, jmax-1):
                gridi[i,j,k] = \
                    gridi[i-1,j,k]*0.25 + \
                    gridi[i+1,j,k]*0.25 + \
                    gridi[i,j-1,k]*0.25 + \
                    gridi[i,j+1,k]*0.25 + \
                    pi * varaus.gridi[i,j,k] * h * h
    #3d
    #3d
    else:
        #print "3d", varaus
        for i in range(1, imax-1):
            for j in range(1, jmax-1):
                for k in range(1, kmax-1):
                    gridi[i,j,k] = \
                        gridi[i,j,k-1]/6 + \
                        gridi[i,j,k+1]/6 + \
                        gridi[i-1,j,k]/6 + \
                        gridi[i+1,j,k]/6 + \
                        gridi[i,j-1,k]/6 + \
                        gridi[i,j+1,k]/6 + \
                        2. / 3. * pi * varaus.gridi[i,j,k] * h * h * h



def monte_carlo_yksi_askel_kaikki(elektroni_tiheys, V_hartree,
                                  ydin_tiheys,
                                  tiheydenmuutos=0.1, T=100):
    """ muutetaan varaustiheyttä ja hyväksytään tai hylätään siirto 
    hyväksytään siirto== muutetaan uuteen tiheyteen
    hylätään siirto== ei muuteta tiheyttä.
    Koko varaustiheys muutetaan kerralla (jotta elektronimäärä säilyy)
    """
    import math
    kb = 3.1668114e-6  #Bolztmannin vakio atomiyksiköissä

    def onko_pariton(num):
        return bool(num % 2)

    #lasketaan kokonaisenergia vanhalla elektronitiheydellä
    print "vanha",
    e_vanha = energiat.E_tot(elektroni_tiheys, V_hartree, ydin_tiheys)

    # alkuvarausmuutos, kerrotaan 1-x ja 1+x jossa x muutos (aluksi 10%)
    size = elektroni_tiheys.gridi.size
    positiiviset = np.ones(size/2)*(1.+tiheydenmuutos)
    negatiiviset = np.ones(size/2)*(1.-tiheydenmuutos)
    #print size
    #print "POS",positiiviset
    #print "NEG",negatiiviset    
    yrite = np.concatenate([positiiviset, negatiiviset])
    if onko_pariton(size):
        yksi = np.ones(1)
        yrite = np.concatenate([yrite, yksi])
    np.random.shuffle(yrite)
    #print "elektronitiheyden muutos", yrite
    elektroni_tiheys_vanha = elektroni_tiheys.gridi
    yrite = yrite.reshape(elektroni_tiheys.gridi.shape)
    #print "elektroni_tiheys_vanha", elektroni_tiheys_vanha
    #print "elektroni_tiheys muutos", yrite
    elektroni_tiheys.gridi = elektroni_tiheys.gridi * yrite
    #skaalataan elektronien lukumäärä takaisin alkuperäiseen
    elektroni_tiheys.gridi = elektroni_tiheys.gridi * \
        elektroni_tiheys.get_summa_mennyt() / \
        elektroni_tiheys.get_summa_nykyinen()

    #print "elektroni_tiheys uusi", elektroni_tiheys.to_1d_list()
    #print "elektronitiheys uusi", elektroni_tiheys.gridi
    print "uusi",
    e_uusi = energiat.E_tot(elektroni_tiheys, V_hartree, ydin_tiheys)
    e_diff = e_uusi - e_vanha
    print "ediff", e_diff
    if e_uusi > e_vanha:
        print "eksponenetti", math.exp(-(e_diff)/(kb*T)), e_diff
        #print 
        if np.random.random_sample() > math.exp(-(e_diff)/(kb*T)):
            #hylätään uusi 
            elektroni_tiheys.gridi = elektroni_tiheys_vanha
            #print "eksponenetti", math.exp(-(e_diff)/(kb*T))
            print "MC hylätty"
        else:
            print "MC hyväksytty YLÄMÄKEEN"
    else:
        print "MC hyväksytty"
    

