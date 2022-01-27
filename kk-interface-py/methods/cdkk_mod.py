#
# This script calculates the Kramers-Kronig transforms using the CDKK method with
# Python code.
# The idea for this script is based off that given by Rudolph and Autschbach
# Code is similar to that in the MSKK method by Mark Rudolph
#
# Reference:
# Rudolph M, Autschbach J. Fast Generation of Nonresonant and Resonant Optical
#     Rotatory Dispersion Curves with the Help of Circular Dichroism Calculations
#     and Kramers-Kronig Transformations. Chirality 2008;20:995-1008.
#
#    This file is part of kk-interface-python
#
#    kk-interface-python is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    kk-interface-python is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with kk-interface-python.  If not, see <http://www.gnu.org/licenses/>.
#
import numpy as np
import math as mt

def cdkk(a,p,wave,points,anchors):
    cdkkinter = np.zeros(len(anchors))
    transform = np.zeros((len(points),2))
    h = abs(points[0][0] - points[1][0])
    if wave:
        a = -1.0
    else:
        a = 1.0
    for i in range(len(anchors)):
        for j in range(1,len(points),2):
            if abs(points[j][0] - anchors[i][0]) <= 1.0e-6:
                cdkkinter[i] = j
                break
    cdkkinter[0] = 1
    cdkkinter[-1] = len(points)
    
    for i in range(len(anchors)-1):
        for j in range(int(cdkkinter[i]),int(cdkkinter[i+1])):
            if j%2 == 0:
                k = 1
                m = 1
            else:
                k = 0
                m = 0
            sum = 0.
            vj = points[j][0]
            while k < len(points):
                if k == j:
                    k += 2
                    continue
                rj = points[k][1]
                vi = points[k][0]
                phi = 0.0
                phisum = 0.0
                for l in range(i,i+2):
                    phi = anchors[l][2]
                    phiprod_sub = 0.0
                    phiprod = 1.0
                    for n in range(i,i+2):
                        if n == l:
                            continue
                        else:
                            phiprod_sub = (vj*vj - anchors[n][m]* \
                                                                 anchors[n][m]) / \
                                   (anchors[l][m]*anchors[l][m] - \
                                                  anchors[n][m]*anchors[n][m])
                            phiprod = phiprod * phiprod_sub
                    phisum = phisum + (phi * phiprod)
                intprod = 1.0
                for l in range(i,i+2):
                    inner_intprod = vi*vi - anchors[l][m]*anchors[l][m]
                    intprod = intprod * inner_intprod
                outer_intprod = 1.0
                for l in range(i,i+2):
                    outer_intprod_sub = vj*vj - anchors[l][m]*anchors[l][m]
                    outer_intprod = outer_intprod * outer_intprod_sub
                fj = (rj * vi) / ((vi*vi - vj*vj) * intprod)
                sum += fj
                k += 2
            transform[j][0] = points[j][0]
            transform[j][1] = phisum+a*(2.0/mt.pi)*(2.0*h)*sum*outer_intprod
    return transform
            
def reversecdkk(a,p,wave,points,anchors):
    cdkkinter = np.zeros(len(anchors))
    transform = np.zeros((len(points),2))
    h = abs(points[0][0] - points[1][0])
    if wave:
        a = -1.0
    else:
        a = 1.0
    for i in range(len(anchors)):
        for j in range(1,len(points),2):
            if abs(points[j][0] - anchors[i][0]) <= 1.0e-6:
                cdkkinter[i] = j
                break
    cdkkinter.sort()
    cdkkinter[0] = 0
    cdkkinter[-1] = len(points)
    for i in range(len(anchors)-1):
        for j in range(int(cdkkinter[i]),int(cdkkinter[i+1])):
            if j%2 == 0:
                k = 1
                m = 1
            else:
                k = 0
                m = 0
            sum = 0.0
            vj = points[j][0]
            while k < len(points):
                if k == j:
                    k += 2
                    continue
                rj = points[k][1]
                vi = points[k][0]
                phi = 0.0
                phisum = 0.0
                for l in range(i,i+2):
                    phi = anchors[l][2]
                    phiprod_sub = 0.0
                    phiprod = 1.0
                    for n in range(i,i+2):
                        if n == l:
                            continue
                        else:
                            phiprod_sub = (vj*vj - anchors[n][m]* \
                                                    anchors[n][m]) / \
                            (anchors[l][m]*anchors[l][m] - \
                                        anchors[n][m]*anchors[n][m])
                            phiprod = phiprod * phiprod_sub
                    phisum = phisum + (phi * phiprod)
                intprod = 1.0
                for l in range(i,i+2):
                    inner_intprod = vi*vi - anchors[l][m]*anchors[l][m]
                    intprod = intprod * inner_intprod
                outer_intprod = 1.0
                for l in range(i,i+2):
                    outer_intprod_sub = vj*vj - anchors[l][m]*anchors[l][m]
                    outer_intprod = outer_intprod * outer_intprod_sub
                fj = (rj) / ((vi*vi - vj*vj) * intprod)
                sum += fj
                k += 2
            transform[j][0] = points[j][0]
            transform[j][1] = phisum+a*(-2.0/mt.pi)*vj*(2.0*h)*sum*outer_intprod
    return transform

