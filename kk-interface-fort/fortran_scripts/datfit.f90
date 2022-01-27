module fit_data
!
! This is a script that will take a list of zeropoints for either tyhe MSKK or
! CDKK methods to be used in kk-inter and will fit those points to the closest
! points in a given set of data.
! This script will only do so with the frequency\wavelike variables.
!
!    This file is part of kk-interiface-fort
!
!    kk-interface-fort is free software: you can redistribute it and/or modify
!    it under the terms of the GNU General Public License as published by
!    the Free Software Foundation, either version 3 of the License, or
!    (at your option) any later version.
!
!    kk-interface-fort is distributed in the hope that it will be useful,
!    but WITHOUT ANY WARRANTY; without even the implied warranty of
!    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
!    GNU General Public License for more details.
!
!    You should have received a copy of the GNU General Public License
!    along with kk-interface-fort.  If not, see <http://www.gnu.org/licenses/>.
!
!=================================================================================
   implicit none
   integer :: i,j,k,l,m
   double precision, allocatable :: cddiff(:,:)
   double precision :: low
!=================================================================================

   contains
   subroutine fit(np,n,freq,zerolist,anchors)
   implicit none
   integer, intent(in) :: np,n
   double precision, intent(in) :: freq(:),zerolist(:)
   double precision, intent(out) :: anchors(n,2)
   allocate (cddiff(np,n+1))
   do i=1,n
      do j=1,np
         cddiff(j,i) = freq(j) - zerolist(i)
      end do
   end do
   cddiff(:,n+1) = freq(:)
   do j=1,n
      do k=1,np-1
         if (abs(cddiff(k,j)).lt.abs(cddiff(k+1,j))) then
            if (abs(cddiff(k-1,j)).lt.abs(cddiff(k+1,j))) then
               low = cddiff(k-1,n+1)
            else
               low = cddiff(k+1,n+1)
            end if
            if (mod(k,2).eq.0) then
               anchors(j,1) = cddiff(k,n+1)
               anchors(j,2) = low
            else
               anchors(j,1) = low
               anchors(j,2) = cddiff(k,n+1)
            end if
            goto 200
         end if
      end do
      200 continue
   end do
   deallocate (cddiff)
   end subroutine fit

end module fit_data
