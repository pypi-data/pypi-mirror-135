module methods

  use, intrinsic :: iso_fortran_env, only : output_unit, error_unit

  implicit none

  integer, parameter, public :: lt = -1, gt = 1 ! Options for j_range
  integer, public :: ncoll
  
contains

  subroutine run(r, v, sigma, box, dt, nsteps, coltime, partner)
    double precision, intent(inout)    :: r(:,:)
    double precision, intent(inout)    :: v(:,:)
    double precision, intent(in)       :: sigma(:)
    double precision, intent(in)       :: box        ! Box length (in units where sigma=1)
    double precision, intent(in)       :: dt         ! Time step
    integer,          intent(in)    :: nsteps     ! 
    double precision, intent(inout) :: coltime(:) ! Time to next collision (n)
    integer,          intent(inout) :: partner(:) ! Collision partner (n)

    double precision :: vir        ! Total collisional virial
    double precision :: kin        ! Kinetic energy
    double precision :: temp_kinet ! Temperature (conserved)

    integer            :: i, j, k, col_sum, blk, stp, nblock, nstep, ioerr
    double precision               :: tij, t_now, vir_sum
    double precision, dimension(3) :: vcm

    r(:,:) = r(:,:) / box                                     ! Convert positions to box=1 units
    r(:,:) = r(:,:) - anint(r(:,:))                    ! Periodic boundaries

    if (nsteps == 0) then
       ncoll = 0
       vcm(:) = sum(v(:,:), dim=2) / size(r,2)              ! Centre-of mass velocity
       v(:,:) = v(:,:) - spread(vcm(:), dim=2, ncopies=size(r,2)) ! Set COM velocity to zero
       kin        = 0.5 * sum(v**2)
       temp_kinet = 2.0 * kin / (3*(size(r,2)-1))
       v          = v / sqrt(temp_kinet) ! We fix the temperature to be 1.0
       kin        = 0.5 * sum(v**2)
       temp_kinet = 2.0 * kin / (3*(size(r,2)-1))
       !write(unit=output_unit, fmt='(a,t40,f15.6)') 'Temperature', temp_kinet
       !write(unit=output_unit, fmt='(f15.6,f15.6,f15.6)') sum(v(:,:), dim=2) / size(r,2)              ! Centre-of mass velocity
    end if
    
    ! Initial overlap check
    if (overlap(r, sigma, box)) then
       write (unit=error_unit, fmt='(a)') 'Particle overlap in initial configuration'
       stop 'Error in md_nve_hs'
    end if
    
    ! Initial search for collision partners >i
    if (nsteps == 0) then
       coltime(:) = huge(1.0)
       partner(:) = size(r,2)
       do i = 1, size(r,2)
          call update(r, v, sigma, coltime, partner, i, box, gt) 
       end do
       r(:,:) = r(:,:) * box  ! Convert back
       return
    end if

    do stp = 1, nsteps ! Begin loop over steps
       vir_sum = 0.0 ! Zero collisional virial accumulator for this step
       col_sum = 0   ! Zero collision counter for this step
       t_now   = 0.0 ! Keep track of time within this step
       do ! Loop over collisions within this step
          i   = minloc(coltime, dim=1)    ! Locate minimum collision time
          j   = partner(i)                ! Collision partner
          tij = coltime(i)                ! Time to collision
          
          if (t_now + tij > dt) then
             call advance(dt - t_now, t_now, r, v, box, coltime, partner)     ! Advance to end of time step
             exit
          end if

          call advance(tij, t_now, r, v, box, coltime, partner) ! Advance to time of next collision
          call collide(r, v, sigma, i, j, box, vir)    ! Compute collision dynamics
          col_sum = col_sum + 1           ! Increment collision counter
          vir_sum = vir_sum + vir         ! Increment collisional virial accumulator

          ! Update collision lists
          do k = 1, size(r,2)
             if (k==i .or. k==j .or. partner(k) == i .or. partner(k) == j)  then
                call update(r, v, sigma, coltime, partner, k, box, gt) ! Search for partners >k
             end if
          end do
          call update(r, v, sigma, coltime, partner, i, box, lt)   ! Search for partners <i
          call update(r, v, sigma, coltime, partner, j, box, lt)   ! Search for partners <j
       end do

       ncoll = ncoll + col_sum
    end do
    
    if (overlap(r, sigma, box)) stop 'Particle overlap in final configuration'
    r(:,:) = r(:,:) * box  ! Convert back
  end subroutine run
  
  subroutine advance(t, t_now, r, v, box, coltime, partner)
    double precision,    intent(inout) :: r(:,:)
    double precision,    intent(in)    :: v(:,:)
    double precision,    intent(in)    :: box
    double precision,    intent(inout) :: coltime(:) ! Time to next collision (n)
    integer,             intent(inout) :: partner(:) ! Collision partner (n)
    double precision,    intent(in) :: t ! Time interval over which to advance configuration
    double precision,    intent(inout) :: t_now
    
    ! Guard against going back in time
    if (t < 0.0) then ! should never happen
       write (unit=error_unit, fmt='(a,f15.6)') 'Negative time step', t
       stop 'Error in md_nve_hs/advance'
    end if

    t_now      = t_now + t                 ! Advance current time by t
    coltime(:) = coltime(:) - t            ! Reduce times to next collision by t
    r(:,:)     = r(:,:) + t * v(:,:) / box ! Advance all positions by t (box=1 units)
    r(:,:)     = r(:,:) - anint(r(:,:))    ! Apply periodic boundaries
  end subroutine advance
  
  ! If j_range == gt, this routine loops over j > i seeking collisions at times shorter than coltime(i)
  ! Note that coltime(i) is set to a large value at the start, in this case
  ! If j_range == lt, the loop is over j < i, and the comparison is with coltime(j) in each case
  ! We use this approach so as to store information about each collision once only
  ! using the lower of the two indices
  subroutine update(r, v, sigma, coltime, partner, i, box, j_range)
    double precision,    intent(in)    :: r(:,:), v(:,:), sigma(:)
    double precision,    intent(inout) :: coltime(:) ! Time to next collision (n)
    integer, intent(inout) :: partner(:) ! Collision partner (n)
    integer, intent(in) :: i       ! Index of atom of interest
    double precision,    intent(in) :: box     ! Simulation box length
    integer, intent(in) :: j_range ! Range of j to be considered

    integer            :: j, j1, j2, k
    double precision, dimension(3) :: rij, vij
    double precision               :: rijsq, vijsq, bij, tij, discr, sigsq

    select case (j_range)
    case (lt) ! j < i
       j1 = 1
       j2 = i-1
    case (gt) ! j > i
       j1 = i+1
       j2 = size(r, 2)
       coltime(i) = huge(1.0)
    case default ! should never happen
       write(unit = error_unit, fmt='(a,i10)') 'j_range error ', j_range
       stop 'Impossible error in update'
    end select

    do j = j1, j2 ! Loop over specified range of partners
       rij(:) = r(:,i) - r(:,j)
       rij(:) = rij(:) - anint(rij(:))
       rij(:) = rij(:) * box ! Now in sigma=1 units
       vij(:) = v(:,i) - v(:,j)
       bij    = DOT_product(rij, vij)

       if (bij < 0.0) then ! Test if collision is possible
          rijsq = sum(rij**2)
          vijsq = sum(vij**2)
          sigsq = ((sigma(i) + sigma(j)) / 2)**2
          !discr = bij ** 2 - vijsq * (rijsq - 1.0) ! sigma**2 = 1.0
          discr = bij ** 2 - vijsq * (rijsq - sigsq) ! sigma**2 = 1.0
          if (discr > 0.0) then ! Test if collision is happening
             tij = (-bij - sqrt(discr)) / vijsq
             k = min(i, j)
             if (tij < coltime(k)) then ! Test if collision needs storing
                coltime(k) = tij
                partner(k) = max(i,j)
             end if
          end if
       end if
    end do
  end subroutine update

  function overlap(r, sigma, box)
    logical          :: overlap ! Returns flag indicating any pair overlaps
    double precision, intent(in) :: r(:,:)     ! Simulation box length
    double precision, intent(in) :: sigma(:), box     ! Simulation box length

    integer            :: i, j
    double precision, dimension(3) :: rij
    double precision               :: rij_sq, box_sq, rij_mag, sig_sq

    overlap = .false.
    box_sq  = box**2
    do i = 1, size(r,2) - 1
       do j = i + 1, size(r,2)
          rij(:) = r(:,i) - r(:,j)
          rij(:) = rij(:) - anint(rij(:))
          rij_sq = sum(rij**2)  ! squared distance
          rij_sq = rij_sq * box_sq ! now in sigma=1 units
          sig_sq = ((sigma(i) + sigma(j)) / 2)**2
          !if (rij_sq < 1.0) then
          if (rij_sq < sig_sq) then
             rij_mag = sqrt(rij_sq)
             !write(unit=error_unit, fmt='(a,2i5,f15.8)') 'Warning: i,j,rij = ', i, j, rij_mag
             overlap = .true.
          end if
       end do
    end do
  end function overlap

  ! This routine implements collision dynamics, updating the velocities
  ! The colliding pair (i,j) is assumed to be in contact already
  subroutine collide(r, v, sigma, i, j, box, virial)
    double precision,    intent(in)  :: r(:,:), sigma(:)
    double precision,    intent(inout)  :: v(:,:)
    integer, intent(in)  :: i, j   ! Colliding atom indices
    double precision,    intent(in)  :: box    ! Simulation box length
    double precision,    intent(out) :: virial ! Collision contribution to pressure

    double precision, dimension(3) :: rij, vij
    double precision               :: factor, sig_sq
    
    rij(:) = r(:,i) - r(:,j)
    rij(:) = rij(:) - anint(rij(:)) ! Separation vector
    rij(:) = rij(:) * box              ! Now in sigma=1 units
    vij(:) = v(:,i) - v(:,j)           ! Relative velocity

    sig_sq = ((sigma(i) + sigma(j)) / 2)**2
    factor = DOT_product(rij, vij) / sig_sq
    vij    = -factor * rij

    v(:,i) = v(:,i) + vij
    v(:,j) = v(:,j) - vij
    virial = DOT_product(vij, rij) / 3.0
  end subroutine collide

end module methods
