#
# This is a script that will take a list of zeropoints for either tyhe MSKK or
# CDKK methods to be used in kk-inter and will fit those points to the closest
# points in a given set of data.
# This script will only do so with the frequency\wavelike variables.
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

def fit(p,n,freq,zerolist):
	cddiff = np.zeros((len(freq),len(zerolist)+1))
	anchors = np.zeros((len(zerolist),2))
	n = int(len(zerolist))
	for i in range(n):
		for j in range(len(freq)):
			cddiff[j][i] = freq[j] - zerolist[i]
	for i in range(len(freq)):
		cddiff[i][n] = freq[i]
	for j in range(n):
		for k in range(len(freq)-1):
			if abs(cddiff[k][j]) < abs(cddiff[k+1][j]):
				if abs(cddiff[k-1][j]) < abs(cddiff[k+1][j]):
					low = cddiff[k-1][n]
				else:
					low = cddiff[k+1][n]
				if k%2 != 0:
					anchors[j][0] = cddiff[k][n]
					anchors[j][1] = low
				else:
					anchors[j][0] = low
					anchors[j][1] = cddiff[k][n]
				break
	return anchors
