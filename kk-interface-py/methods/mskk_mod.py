# 
# This script is used to calculate the Multiply Subtractive KK (MSKK) method
# to perform the transformation on optical data. This method was proposed by
# Palmer,Williams,Budde using Python code.
# 
# Original script was done in FORTNAN by Mark Rudolph.
# 
# Reference:
# Palmer KF, Williams MZ, Budde BA. Multiply Subtractive Kramers-Kronig analysis
#     of optical data. Appl Opt 1998;37:2660-2673.
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

def gskk(p,a,wave,points,anchors):
	h = abs(points[0][0]-points[1][0])
	trans = np.zeros((len(points),2))
	if wave:
		a = -1.0
	else:
		a = 1.0
	for i in range(len(points)):
		if i%2 == 0:
			j = 1
			m = 1
		else:
			j = 0
			m = 0
		sum = 0.0
		vj = points[i][0]
		while j < len(points):
			if i == j:
				j += 2
				continue
			rj = points[j][1]
			vi = points[j][0]
			phi = 0.0
			phisum = 0.0
			for k in range(len(anchors)):
				phi = anchors[k][2]
				phiprod_sub = 0.0
				phiprod = 1.0
				for l in range(len(anchors)):
					if l == k:
						continue
					phiprod_sub = (vj*vj - anchors[l][m]*anchors[l][m]) / \
						(anchors[k][m]*anchors[k][m] - anchors[l][m]*anchors[l][m])
					phiprod = phiprod * phiprod_sub
				phisum += (phi*phiprod)

			intprod = 1.0
			for k in range(len(anchors)):
				inner_intprod = vi*vi - anchors[k][m]*anchors[k][m]
				intprod = intprod * inner_intprod

			outer_intprod = 1.0
			for k in range(len(anchors)):
				outer_intprod_sub = vj*vj - anchors[k][m]*anchors[k][m]
				outer_intprod = outer_intprod * outer_intprod_sub

			fj = (rj*vi) / ((vi*vi - vj*vj) * intprod)
			sum += fj
			j += 2
		trans[i][0] = points[i][0]
		trans[i][1] = phisum+a*(2/mt.pi)*(2*h)*sum*outer_intprod
	return trans

def reversegskk(p,a,wave,points,anchors):
	h = abs(points[0][0]-points[1][0])
	trans = np.zeros((len(points),2))
	if wave:
		a = -1.0
	else:
		a = 1.0
	for i in range(len(points)):
		if i%2 == 0:
			j = 1
			m = 1
		else:
			j = 0
			m = 0
		sum = 0.0
		vj = points[i][0]
		while j < len(points):
			if i == j:
				j += 2
				continue
			rj = points[j][1]
			vi = points[j][0]
			phi = 0.0
			phisum = 0.0
			for k in range(len(anchors)):
				phi = anchors[k][2]
				phiprod_sub = 0.0
				phiprod = 1.0
				for l in range(len(anchors)):
					if l == k:
						#print l,k
						continue
						#print 1
					else:
						#print 2,l,k
						phiprod_sub = (vj*vj - anchors[l][m]*anchors[l][m]) / \
								(anchors[k][m]*anchors[k][m] - anchors[l][m]*anchors[l][m])
						phiprod = phiprod * phiprod_sub
				phisum += (phi*phiprod)

			intprod = 1.0
			for k in range(len(anchors)):
				inner_intprod = vi*vi - anchors[k][m]*anchors[k][m]
				intprod = intprod * inner_intprod

			outer_intprod = 1.0
			for k in range(len(anchors)):
				outer_intprod_sub = vj*vj - anchors[k][m]*anchors[k][m]
				outer_intprod = outer_intprod * outer_intprod_sub

			fj = (rj) / ((vi*vi - vj*vj) * intprod)
			sum += fj
			j += 2
		trans[i][0] = points[i][0]
		trans[i][1] = phisum+a*(-2/mt.pi)*vj*(2*h)*sum*outer_intprod
	return trans

