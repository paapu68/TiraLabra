#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Density functional theory (DFT) without orbitals.
In this module we define a computational grids and some of its functions
"""

import numpy as np
class Gridi(object):
    """Laskentagridiä esittävä luokka
    
    Parametrit:
    
    nx : int 
         number of grid points in x direction
    ny : int 
         number of grid points in y direction
    nz : int 
         number of grid points in z direction
     h : float
         grid spacing (in atomic units)
    """

    def __init__(self, nx=11, ny=11, nz=0, h=0.1, init_value=0.0):
        self.nx = nx
        self.ny = ny
        self.nz = nz
        self.h = h
        if (nz == 0): #2d
            self.gridi = np.empty( (nx,ny,1) )
            self.gridi[:, :, :] = 0.0 # zero boundary condition
            self.gridi[1:nx-1, 1:ny-1, 0] = init_value
        elif (ny == 0): #2d
            self.gridi = np.empty( (nx,1,nz) )
            self.gridi[:, :, :] = 0.0 # zero boundary condition
            self.gridi[1:nx-1, 0, 1:nz-1] = init_value
        elif (nx == 0): #2d
            self.gridi = np.empty( (1,ny,nz) )
            self.gridi[:, :, :] = 0.0 # zero boundary condition
            self.gridi[0, 1:ny-1, 1:nz-1] = init_value
        else: #3d
            self.gridi = np.empty( (nx,ny,nz) )
            self.gridi[:, :, :] = 0.0 # zero boundary condition
            self.gridi[1:nx-1, 1:ny-1, 1:nz-1] = init_value

        print "grid", self.gridi.shape

    def to_1d_list(self):
        return self.gridi.ravel().tolist()

    def get_number_of_boxes(self):
        return (self.nx-1)*(self.ny-1)*(self.nz-1)

    def get_volume_of_a_box(self):
        return self.h * self.h * self.h

    def get_volume(self):
        return self.h * self.h * self.h * self.get_number_of_boxes()

    def get_grid_step(self):
        return self.h
