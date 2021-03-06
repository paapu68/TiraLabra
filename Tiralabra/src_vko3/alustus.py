#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" DFT ilman atomiorbitaaleja. Tässä moduulissa alustetaan laskenta gridi """

import numpy as np

def tee_gridi(nx, ny, nz):
    """ luodaan tyhjä gridi laskentaa varten """
    return np.empty( (ny,nx,nz) )

def aseta_gridin_alkuarvo(arvo, gridi):
    """ asetetaan gridiin vakioarvo """
    tmp = gridi.copy()
    tmp[:, :, :] = arvo
    return tmp

