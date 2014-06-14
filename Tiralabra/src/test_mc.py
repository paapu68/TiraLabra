#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" DFT ilman atomiorbitaaleja. 
Tässä moduulissa kokeillaan metodien toimivuutta 
elektronitiheys on positiivinen luku
"""

import numpy as np
from scipy.optimize import fmin_powell, fmin, anneal
from gridi import *
from energiat import E_tot
import laskentaa
import piirtoa
import string




# yritetään lukea alkuarvot filestä alkuarvot.txt
# muutetaan siten että x->y ja y->x 
# eli input tiedossa y tulee ensin koska se on matriisin 1. dimensio
# tämä gridin koon määrittelyssä ja ytimien paikkoken määrittelyssä
#try:
if True:
    infile=open('alkuarvot.txt','r')
    ny=int(infile.readline().strip())
    nx=int(infile.readline().strip())
    nz=int(infile.readline().strip())
    elektroni_lkm=float(infile.readline().strip())
    elektroni_tiheys = Gridi(nx=nx,ny=ny,nz=nz,init_value=elektroni_lkm)
    V_hartree = Gridi(nx=nx,ny=ny,nz=nz,init_value=0)
    ydin_tiheys = Gridi(nx=nx,ny=ny,nz=nz,init_value=0)
    ytimien_lkm=int(infile.readline().strip())
    for i_ydin in range(ytimien_lkm):
        line=infile.readline()
        col=string.split(line)
        iy=int(col[0])
        ix=int(col[1])
        iz=int(col[2])
        z =float(col[3])
        ydin_tiheys.gridi[ix,iy,iz]=1.0/ydin_tiheys.get_volume_of_a_box()


#except: # mennään oletusinputeilla
#    print "tiedoston luku tiedosta 'alkuarvot.txt' EI onnistunut"
#    print "käytetään oletusarvoja"
#    V_hartree = Gridi(init_value=0)
#    ydin_tiheys = Gridi(init_value=0)
#    elektroni_tiheys = Gridi(init_value=2.0)
#    ydin_tiheys.gridi[2,2,0]=1.0/ydin_tiheys.get_volume_of_a_box()
#    ydin_tiheys.gridi[12,3,0]=1.0/ydin_tiheys.get_volume_of_a_box()

#elektroni_tiheys.gridi[:,:,:]=1.0/elektroni_tiheys.get_volume()
print elektroni_tiheys.get_volume()
print elektroni_tiheys.gridi
print elektroni_tiheys.to_1d_list()

print "ydintiheys",ydin_tiheys.gridi
#Elektronien määrä on vakio
elektroni_tiheys.set_summa()
ntot = np.sum(elektroni_tiheys.gridi)*V_hartree.get_volume_of_a_box()
print "elektronien kokonaisvaraus", ntot, elektroni_tiheys.get_summa_mennyt()

# otetaan tavoitteeksi että siirto hyväksytään joka viides kerta
# silloin on sopivasti riskiä yrityksessä
n_hyvaksytty = 0
n_hylatty = 0
tiheydenmuutos = 0.1
outfile = open('energiat.txt', 'w')
count = 0
for step in range(10):
    for step2 in range(100):
        count = count + 1
        hyvaksytty = laskentaa.monte_carlo_yksi_askel_kaikki(
            elektroni_tiheys, V_hartree,
            ydin_tiheys,
            tiheydenmuutos)
        if hyvaksytty:
            n_hyvaksytty =n_hyvaksytty+1
        else:
            n_hylatty = n_hylatty+1
        print "hyv/hyl", n_hyvaksytty, n_hylatty
        if n_hyvaksytty > 5 and n_hylatty==0:
            #hyvaksytaan liian usein
            tiheydenmuutos = tiheydenmuutos * 1.1
            n_hyvaksytty = 0
            n_hylatty = 0
        elif n_hylatty > 5 and n_hyvaksytty==0:
            #hylataan liian usein
            tiheydenmuutos = tiheydenmuutos * 0.9
            n_hyvaksytty = 0
            n_hylatty = 0
        elif (n_hyvaksytty > 0): 
            #hylataan liian usein
            if (n_hylatty/n_hyvaksytty > 10.0):
                tiheydenmuutos = tiheydenmuutos * 0.9
                n_hyvaksytty = 0
                n_hylatty = 0
        elif (n_hylatty > 0): 
            #hylataan liian usein
            if (n_hyvaksytty/n_hylatty > 10.0):
                tiheydenmuutos = tiheydenmuutos * 1.1
                n_hyvaksytty = 0
                n_hylatty = 0
        else:
            #ollaan ok alueella
            pass
            

        outfile.write(str(count)+'  '+str(E_tot(elektroni_tiheys, V_hartree, ydin_tiheys))+'  '+str( tiheydenmuutos)+'\n')

    piirtoa.plot2d_simple(elektroni_tiheys)
outfile.close()


