# 
# This script is used to calculate the Kramers-Kronig (KK) forward and reverse
# transfroms using Python code.
# 
# Original script was done in FORTRAN by Jochen Autschbach.
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

def kkmaclaurin(wave,points,p):
	h = abs(points[0][0]-points[1][0])
	trans = np.zeros((len(points),2))
	if wave:
		a = -1.0
	else:
		a = 1.0
	for i in range(len(points)):
		if i%2 == 0:
			j = 1
		else:
			j = 0
		sum = 0.0
		vj = points[i][0]
		while j < len(points):
			if i == j:
				j += 2
			rj = points[j][1]
			vi = points[j][0]
			fj = rj / (vi * (vi*vi - vj*vj))
			sum += fj
			j += 2
		trans[i][0] = points[i][0]
		trans[i][1] = a * 2.0/mt.pi * (vj*vj) * (2.0*h) * sum
	return trans

def kkreversemaclaurin(wave,points,p):
	h = abs(points[0][0]-points[1][0])
	trans = np.zeros((len(points),2))
	if wave:
		a = -1
	else:
		a = 1
	for i in range(len(points)):
		if i%2 == 0:
			j = 1
		else:
			j = 0
		sum = 0.0
		vj = points[i][0]
		while j < len(points):
			if i == j:
				j += 2
			rj = points[j][1]
			vi = points[j][0]
			fj = rj / (vi*vi * (vi*vi - vj*vj))
			sum += fj
			j += 2
		trans[i][0] = points[i][0]
		trans[i][1] = -a * 2.0/mt.pi * (vj*vj*vj) * (2.0*h) * sum
	return trans
