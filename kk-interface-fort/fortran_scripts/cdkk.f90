module cdkk_mod
!
! This is a script that implements the Chained Doubly-Subtractive KK (CDKK) method 
! into the program kk-interface-fort.
! The idea for this script is based off the idea for the CDKK by Rudolph and 
! Autschbach. 
! Code is similar to the one used for the Multiply Subtractive KK (MSKK) method
! by Mark Rudolph.
!
! Reference:
! Rudolph M, Autschbach J. Fast Generation of Nonresonant and Resonant Optical
!     Rotatory Dispersion Curves with the Help of Circular Dichroism Calculations
!     and Kramers-Kronig Transformations. Chirality 2008;20:995-1008.
!
!    This file is part of kk-interface-fort
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
!initialization of variables================================================
   implicit none
   integer :: i,j,k,l,m,n,time(3),counter,time_count(3),time_end(3)
   real :: a
   double precision :: sum,vj, rj, vi, rtemp, fj, h, phi, phisum, phiprod, &
    & phiprod_sub, intprod, inner_intprod, outer_intprod, outer_intprod_sub 
   double precision, parameter :: pi=3.1415926535897932385d0, zero = 0d0, &
                             & two = 2d0, tiny = 1d-6
   double precision, allocatable :: anchors(:,:)
   integer, allocatable :: cdkkinter(:)
!===========================================================================

   contains
   subroutine cdkk(np,na,wave,points,anchorfile,transform)
!variables from program=====================================================
   implicit none
   integer, intent(in) :: np,na,wave
   double precision, intent(in) :: points(:,:), anchorfile(:,:)
   double precision, intent(out) :: transform(np,2)
!assumes the chebyshev nodes inputted have been fitted to the data==========
   call itime(time)
   write(*,1001) time(1),time(2),time(3)
1001 format ( 'Process started at: ',I2.2,':',I2.2,':',I2.2)
   allocate(cdkkinter(na),anchors(na,3))
   h = abs(points(1,1) - points(2,1))
   if (wave == 1) then !changes sign if the variable is wavelike
      a = -1d0
   else
      a = 1d0
   end if
   anchors = anchorfile
!finds where the nodes are close to the data and sets the indeces===========
!that will be used for the integration bounds===============================
   do i=1,na
      do j=2,np+1,2
         if (abs(points(j,1) - anchors(i,1)) <= tiny) then
            cdkkinter(i) = j
            goto 200
         end if
      end do
      stop 'ERROR in difference calculation'
      200 continue
   end do
   cdkkinter(1) = 1
   cdkkinter(na) = np+1
   counter = 5
!doubly-subtractive method (similar to mskk.f90 script)=====================
   do i=1,na-1
      do j=cdkkinter(i),cdkkinter(i+1)-1 !integrate between anchor pnts.
         if (j.eq.int(np*counter/100)) then
            call itime(time_count)
            time_count(:) = [time_count(1)-time(1),time_count(2)-time(2), &
                                               & time_count(3)-time(3)]
            if (time_count(3) < 0) then
               time_count(2) = time_count(2) - 1
               time_count(3) = time_count(3) + 60
            end if
            if (time_count(2) < 0) then
               time_count(1) = time_count(1) - 1
               time_count(2) = time_count(2) + 60
            end if
            write(*,1501) counter,time_count(1),time_count(2),time_count(3)
            counter = counter + 5
1501 format(' ',i3.3,'% COMPLETE...........TIME ELAPSED: ',i2.2,':',i2.2,':',i2.2)
         end if
         if (mod(j,2).eq.0) then
            k = 1
            m = 1
         else
            k = 2
            m = 2
         end if
         sum = zero
         vj = points(j,1)
         do while (k <= np)
            if (k.eq.j) then
               k = k+2
               cycle
            end if
            rj = points(k,2)
            vi = points(k,1)
            phi = 0d0
            phisum = 0d0
            do l=i,i+1
               phi = anchors(l,3)
               phiprod_sub = 0d0
               phiprod = 1d0
               do n=i,i+1
                  if (n.eq.l) then
                     cycle
                  else
                     phiprod_sub = (vj*vj - anchors(n,m)*anchors(n,m)) / &
                          & (anchors(l,m)*anchors(l,m) - anchors(n,m)*anchors(n,m))
                     phiprod = phiprod * phiprod_sub
                  end if
               end do
               phisum = phisum + (phi * phiprod)
            end do
            intprod = 1d0
            do l=i,i+1
               inner_intprod = vi*vi - anchors(l,m)*anchors(l,m)
               intprod = intprod * inner_intprod
            end do
            outer_intprod = 1d0
            do l=i,i+1
               outer_intprod_sub = vj*vj - anchors(l,m)*anchors(l,m)
               outer_intprod = outer_intprod * outer_intprod_sub
            end do
            rtemp = (vi*vi - vj*vj)
            if (abs(rtemp) <= tiny) then
               write(*,*) 'Division by zero', j,k,rtemp
            end if
            fj = (rj*vi) / (rtemp * intprod)
            sum = sum + fj
            k = k+2
         end do
         transform(j,1) = points(j,1)
         transform(j,2) = phisum+a*(two/pi)*(two*h)*sum*outer_intprod
      end do
   end do
   call itime(time_end)
   time_end(:) = [time_end(1)-time(1),time_end(2)-time(2), &
                                     & time_end(3)-time(3)]
      if (time_end(3) < 0) then
         time_end(2) = time_end(2) - 1
         time_end(3) = time_end(3) + 60
      end if
      if (time_end(2) < 0) then
         time_end(1) = time_end(1) - 1
         time_end(2) = time_end(2) + 60
      end if
      write(*,2001) time_end(1),time_end(2),time_end(3)
2001 format('PROCESS COMPLETE.........TIME ELAPSED: ',i2.2,':',i2.2,':',i2.2)
   deallocate(cdkkinter,anchors)
   end subroutine cdkk

   subroutine reversecdkk(np,na,wave,points,anchorfile,transform)
!variables from program=====================================================
   implicit none
   integer, intent(in) :: np,na,wave
   double precision, intent(in) :: points(:,:), anchorfile(:,:)
   double precision, intent(out) :: transform(np,2)
!assumes the chebyshev nodes inputted have been fitted to the data==========
   call itime(time)
   write(*,1000) time(1),time(2),time(3)
1000 format ( 'PROCESS STARTED AT: ',I2.2,':',I2.2,':',I2.2)
   allocate(cdkkinter(na), anchors(na,3))
   h = abs(points(1,1) - points(2,1))
   if (wave == 1) then !changes sign when integrating with wave-like variables
      a = -1d0
   else
      a = 1d0
   end if
   anchors = anchorfile
!finds where the nodes are close to the data and sets the indeces===========
!that will be used for the integration bounds===============================
   do i=1,na
      do j=2,np+1,2
         if (abs(points(j,1) - anchors(i,1)) <= tiny) then
            cdkkinter(i) = j
            goto 200
         end if
      end do
      stop 'ERROR in difference calculation'
      200 continue
   end do
   cdkkinter(1) = 1
   cdkkinter(na) = np+1
   counter = 5
!doubly-subtractive method (similar to mskk.f90 script)=====================
   do i=1,na-1
      do j=cdkkinter(i),cdkkinter(i+1)-1 !integrate between anchor pnts.
         if (j.eq.int(np*counter/100)) then
            call itime(time_count)
            time_count(:) = [time_count(1)-time(1),time_count(2)-time(2), &
                                               & time_count(3)-time(3)]
            if (time_count(3) < 0) then
               time_count(2) = time_count(2) - 1
               time_count(3) = time_count(3) + 60
            end if
            if (time_count(2) < 0) then
               time_count(1) = time_count(1) - 1
               time_count(2) = time_count(2) + 60
            end if
            write(*,1500) counter,time_count(1),time_count(2),time_count(3)
            counter = counter + 5
1500 format(' ',i3.3,'% COMPLETE...........TIME ELAPSED: ',i2.2,':',i2.2,':',i2.2)
         end if
         if (mod(j,2).eq.0) then
            k = 1
            m = 1
         else
            k = 2
            m = 2
         end if
         sum = zero
         vj = points(j,1)
         do while (k <= np)
            if (k.eq.j) then
               k = k+2
               cycle
            end if
            rj = points(k,2)
            vi = points(k,1)
            phi = 0d0
            phisum = 0d0
            do l=i,i+1
               phi = anchors(l,3)
               phiprod_sub = 0d0
               phiprod = 1d0
               do n=i,i+1
                  if (n.eq.l) then
                     cycle
                  else
                     phiprod_sub = (vj*vj - anchors(n,m)*anchors(n,m)) / &
                          & (anchors(l,m)*anchors(l,m) - anchors(n,m)*anchors(n,m))
                     phiprod = phiprod * phiprod_sub
                  end if
               end do
               phisum = phisum + (phi * phiprod)
            end do
            intprod = 1d0
            do l=i,i+1
               inner_intprod = vi*vi - anchors(l,m)*anchors(l,m)
               intprod = intprod * inner_intprod
            end do
            outer_intprod = 1d0
            do l=i,i+1
               outer_intprod_sub = vj*vj - anchors(l,m)*anchors(l,m)
               outer_intprod = outer_intprod * outer_intprod_sub
            end do
            rtemp = (vi*vi - vj*vj)
            if (abs(rtemp) <= tiny) then
               write(*,*) 'Division by zero', j,k,rtemp
            end if
            fj = (rj) / (rtemp * intprod)
            sum = sum + fj
            k = k+2
         end do
         transform(j,1) = points(j,1)
         transform(j,2) = phisum+a*(-two/pi)*vj*(two*h)*sum*outer_intprod
      end do
   end do
   call itime(time_end)
   time_end(:) = [time_end(1)-time(1),time_end(2)-time(2), &
                                     & time_end(3)-time(3)]
      if (time_end(3) < 0) then
         time_end(2) = time_end(2) - 1
         time_end(3) = time_end(3) + 60
      end if
      if (time_end(2) < 0) then
         time_end(1) = time_end(1) - 1
         time_end(2) = time_end(2) + 60
      end if
      write(*,2000) time_end(1),time_end(2),time_end(3)
2000 format('PROCESS COMPLETE.........TIME ELAPSED: ',i2.2,':',i2.2,':',i2.2)
   deallocate(cdkkinter,anchors)
   end subroutine reversecdkk

end module cdkk_mod
