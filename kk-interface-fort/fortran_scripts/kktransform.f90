module kk_m_trans
! 
! This script is used to calculate the Kramers-Kronig (KK) forward and reverse
! transfroms.
! 
! Original script was done in Fortran by Jochen Autschbach.
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
   double precision :: sum, vj, rj, vi, rtemp, fj, h
   integer :: i,j,k,time(3),counter,time_count(3),time_end(3)
   real :: a
   double precision, parameter :: tiny = 1d-10, zero = 0d0, two = 2d0, &
       & pi = 3.1415926535897932385d0
!=================================================================================

   contains
 
   subroutine kkmaclaurin(wave,points,np,transform)
      implicit none
      integer, intent(in) :: np, wave
      double precision, intent(in) :: points(:,:)
      double precision, intent(out) :: transform(np,2)
   call itime(time)
   write(*,1001) time(1),time(2),time(3)
1001 format ( 'PROCESS STARTED AT: ',I2.2,':',I2.2,':',I2.2)
      h = abs(points(1,1) - points(2,1))
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
1501 format(' ',i3.3,'% COMPLETE...........TIME ELAPSED: ',i2.2,':',i2.2,':',i2.2)
         end if
         if (wave == 1) then
            a = -1.0d0
         else
            a = 1.0d0
         end if
         if (mod(i,2) .eq.0) then
            j = 1
         else
            j = 2
         end if
         sum = zero
         vj = points(i,1)
         do while (j < np+1)
            if (i == j) then
               j = j+2
               cycle
            end if
            rj = points(j,2)
            vi = points(j,1)
            rtemp = (vi * (vi*vi - vj*vj))
            if (abs(rtemp) <= tiny) then
               write(*,*) 'Division by zero',i,j,rtemp
            end if
            fj = rj / rtemp
            sum = sum + fj
            j = j + 2
         end do
         transform(i,1) = points(i,1)
         transform(i,2) = a * two/pi * (vj*vj) * (two*h) * sum
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
   end subroutine kkmaclaurin


   subroutine kkreversemaclaurin(wave,points,np,transform)
      implicit none
      integer, intent(in) :: np, wave
      double precision, intent(in) :: points(:,:)
      double precision, intent(out) :: transform(np,2)
   call itime(time)
   write(*,1000) time(1),time(2),time(3)
1000 format ( 'PROCESS STARTED AT: ',I2.2,':',I2.2,':',I2.2)
      h = abs(points(1,1) - points(2,1))
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
         if (wave == 1) then
            a = -1.0d0
         else
            a = 1.0d0
         end if
         if (mod(i,2) .eq.0) then
            j = 1
         else
            j = 2
         end if 
         sum = zero
         vj = points(i,1)
         do while (j < np+1)
            if (i == j) then
               j = j+2
               cycle
            end if
            rj = points(j,2)
            vi = points(j,1)
            rtemp = (vi*vi * (vi*vi - vj*vj))
            if (abs(rtemp) <= tiny) then
               write(*,*) 'Division by zero',i,j,rtemp
            end if
            fj = rj / rtemp
            sum = sum + fj
            j = j+2
         end do
         transform(i,1) = points(i,1)
         transform(i,2) = -a * two/pi * (vj*vj*vj) * (two*h) * sum
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
   end subroutine kkreversemaclaurin

end module kk_m_trans
