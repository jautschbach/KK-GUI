module mskk
! 
! This script is used to calculate the Multiply Subtractive KK (MSKK) method
! to perform the transformation on optical data. This method was proposed by
! Palmer,Williams,Budde.
! 
! Original script was done in Fortran by Mark Rudolph.
! 
! Reference:
! Palmer KF, Williams MZ, Budde BA. Multiply Subtractive Kramers-Kronig analysis
!     of optical data. Appl Opt 1998;37:2660-2673.
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
!initialization of variables======================================================
   implicit none
   integer :: i,j,k,l,m,time(3),counter,time_count(3),time_end(3)
   double precision :: rj, vi, vj, sum, fj, rtemp, phisum, phiprod, phiprod_sub, &
     & intprod, inner_intprod, outer_intprod, outer_intprod_sub, phi, h, a
   double precision, parameter :: tiny = 1d-10, zero = 0d0, one = 1d0, two = 2d0, &
     & pi = 3.1415926535897932385d0
!=================================================================================
   
   contains
   
   subroutine gskk(np,na,wave,points,anchors,transform)
   implicit none
   integer, intent(in) :: np,na,wave
   double precision, intent(in) :: points(:,:), anchors(:,:)
   double precision, intent(out) :: transform(np,2)
   call itime(time)
   write(*,1001) time(1),time(2),time(3)
1001 format ( 'PROCESS STARTED AT: ',I2.2,':',I2.2,':',I2.2)
   h = abs(points(1,1)-points(2,1))
   if (wave.eq.0) then
      a = 1.0d0
   else
      a = -1.0d0
   end if
   counter = 5
   do i=1,np
         if (i.eq.int(np*counter/100)) then
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
1501 format(' ',I3.3,'% COMPLETE...........TIME ELAPSED: ',I2.2,':',I2.2,':',I2.2)
         end if
      if (mod(i,2).eq.0) then
         j = 1
         m = 1
      else
         j = 2
         m = 2
      end if
      sum = zero
      vj = points(i,1)
      do while (j <= np)
         if (i == j) then
            j = j+2
            cycle
         end if
         rj = points(j,2)
         vi = points(j,1)
         phi = 0d0
         phisum = 0d0
         do k=1,na
            phi = anchors(k,3)
            phiprod_sub = 0d0
            phiprod = 1d0
               do l=1,na
                  if (l.eq.k) then
                     cycle
                  else
                     phiprod_sub = (vj*vj - anchors(l,m)*anchors(l,m)) / &
                           & (anchors(k,m)*anchors(k,m) - anchors(l,m)*anchors(l,m))
                     phiprod = phiprod * phiprod_sub
                  end if
               end do
            phisum = phisum + (phi * phiprod)
         end do

         intprod = 1d0
         do k=1,na
            inner_intprod = vi*vi - anchors(k,m)*anchors(k,m)
            intprod = intprod * inner_intprod
         end do
         
         outer_intprod = 1d0
         do k=1,na
            outer_intprod_sub = vj*vj - anchors(k,m)*anchors(k,m)
            outer_intprod = outer_intprod * outer_intprod_sub
         end do
         rtemp = (vi*vi - vj*vj) 
         if (abs(rtemp) <= tiny) then
            write(*,*) 'Division by zero', j,k,rtemp
         end if
         fj = (rj*vi) / (rtemp * intprod)
         sum = sum + fj
         j = j+2
      end do
      transform(i,1) = points(i,1)
      transform(i,2) = phisum+a*(two/pi)*(two*h)*sum*outer_intprod
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
   end subroutine gskk

   subroutine reversegskk(np,na,wave,points,anchors,transform)
   implicit none
   integer, intent(in) :: np,na,wave
   double precision, intent(in) :: points(:,:), anchors(:,:)
   double precision, intent(out) :: transform(np,2)
   call itime(time)
   write(*,1000) time(1),time(2),time(3)
1000 format ( 'PROCESS STARTED AT: ',I2.2,':',I2.2,':',I2.2)
   h = abs(points(1,1)-points(2,1))
   if (wave.eq.0) then
      a = 1.0d0
   else
      a = -1.0d0
   end if
   counter = 5
   do i=1,np
         if (i.eq.int(np*counter/100)) then
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
      if (mod(i,2).eq.0) then
         j = 1
         m = 1
      else
         j = 2
         m = 2
      end if
      sum = zero
      vj = points(i,1)
      do while (j <= np)
         if (i == j) then
            j = j+2
            cycle
         end if
         rj = points(j,2)
         vi = points(j,1)
         phi = 0d0
         phisum = 0d0
         do k=1,na
            phi = anchors(k,3)
            phiprod_sub = 0d0
            phiprod = 1d0
               do l=1,na
                  if (l.eq.k) then
                     cycle
                  else
                     phiprod_sub = (vj*vj - anchors(l,m)*anchors(l,m)) / &
                           & (anchors(k,m)*anchors(k,m) - anchors(l,m)*anchors(l,m))
                     phiprod = phiprod * phiprod_sub
                  end if
               end do
            phisum = phisum + (phi * phiprod)
         end do
         intprod = 1d0
         do k=1,na
            inner_intprod = vi*vi - anchors(k,m)*anchors(k,m)
            intprod = intprod * inner_intprod
         end do
         outer_intprod = 1d0
         do k=1,na
            outer_intprod_sub = vj*vj - anchors(k,m)*anchors(k,m)
            outer_intprod = outer_intprod * outer_intprod_sub
         end do
         rtemp = (vi*vi - vj*vj) 
         if (abs(rtemp) <= tiny) then
            write(*,*) 'Division by zero', j,k,rtemp
         end if
         fj = (rj) / (rtemp * intprod)
         sum = sum + fj
         j = j+2
      end do
      transform(i,1) = points(i,1)
      transform(i,2) = phisum+a*(-two/pi)*vj*(two*h)*sum*outer_intprod
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
   end subroutine reversegskk

end module mskk
