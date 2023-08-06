module methods

  implicit none

  integer, parameter :: dp = selected_real_kind(12)

  !private
  !public :: evolve_velocity_verlet

contains

  subroutine pbc_local(r,box,hbox)
    double precision, intent(inout) :: r(:)
    double precision, intent(in)    :: box(:),hbox(:)
    where (abs(r) > hbox)
       r = r - sign(box,r)
    end where
  end subroutine pbc_local

  subroutine pbc(r,box,hbox)
    double precision, intent(inout) :: r(:,:)
    double precision, intent(in)    :: box(:),hbox(:)
    integer :: i
    do i = 1,size(r,2)
       where (abs(r(:,i)) > hbox(:))
          r(:,i) = r(:,i) - sign(box(:),r(:,i))
       end where
    end do
  end subroutine pbc

  subroutine fix_cm(dr)
    double precision, intent(inout) :: dr(:,:)
    double precision :: drcm(size(dr,1))
    integer :: i
    drcm = sum(dr(:,:), dim=2) / size(dr,2)
    do i = 1,size(dr,2)
       dr(:,i) = dr(:,i) - drcm
    end do
  end subroutine fix_cm
       
  subroutine evolve_velocity_verlet(step, dt, forces, box, pos, pos_unf, vel, ids, mass)
    double precision, intent(in)       :: box(:), dt, mass(:,:)
    double precision, intent(inout)    :: forces(:,:), pos(:,:), pos_unf(:,:), vel(:,:)
    integer, intent(in)        :: step, ids(:)
    double precision                   :: dr(size(pos,1),size(pos,2))
    integer :: i
    if (step == 1) then
       dr = vel / mass * dt + 0.5 * forces / mass * dt**2
       pos = pos + dr
       pos_unf = pos_unf + dr
       vel = vel + 0.5 * forces / mass * dt
       do i = 1,size(pos,2) 
          call pbc_local(pos(:,i), box, box/2)
       end do       
    else if (step == 2) then
       vel = vel + 0.5 * forces / mass * dt
    end if
  end subroutine evolve_velocity_verlet

  subroutine evolve_nose_poincare(step, dt, forces, epot, epot_old, T, s, pi, Q, H_0, box, pos, pos_unf, vel, ids, mass)
    integer, intent(in)             :: step, ids(:)
    double precision, intent(in)    :: dt,box(:),mass(:,:),Q,H_0
    double precision, intent(inout) :: forces(:,:)
    double precision, intent(in)    :: T
    double precision, intent(inout) :: s,pi
    double precision, intent(inout) :: pos(:,:),pos_unf(:,:),vel(:,:)
    double precision                :: dr(size(pos,1),size(pos,2))
    double precision                :: epot_old, s_old, pimm, ekin, epot
    integer                         :: i, ndim, ndf
    ! Some constants
    ndim = size(pos,1)
    ndf = size(pos,2) - 1  ! assume cm is fixed (if (vcm_fix) ndf = ndf-1)

    if (step == 1) then
       ! First step of nose poincare
       s_old = s
       s = s * (1 + pi/(4*Q)*dt)**2
       pi = pi / (1 + pi/(4*Q)*dt)
       vel = vel * s_old / s
       vel = vel + forces / mass * dt / 2
       dr = vel * dt
       pos = pos + dr
       pos_unf = pos_unf + dr
       do i = 1,size(pos,2) 
          call pbc_local(pos(:,i),box,box/2)
       end do
    else if (step == 2) then
       ! Second step of nose poincare
       ekin = sum([(sum(mass(:,i) * vel(:,i)**2) / 2, i=1,size(pos,2))])
       s_old = s
       pimm = pi + dt * (ekin - (epot_old+epot)/2 + (H_0 - ndim*ndf*T*(log(s)+1)))
       s = s * (1+pimm/(4*Q)*dt)**2
       pi = pimm / (1+pimm/(4*Q)*dt)
       vel = vel + forces / mass * dt / 2
       vel = vel * s_old / s
    end if
  end subroutine evolve_nose_poincare
  
end module methods
