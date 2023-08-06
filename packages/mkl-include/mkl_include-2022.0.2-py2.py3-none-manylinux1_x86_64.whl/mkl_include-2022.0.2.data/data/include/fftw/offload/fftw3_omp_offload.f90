!===============================================================================
! Copyright 2021 Intel Corporation.
!
! This software and the related documents are Intel copyrighted  materials,  and
! your use of  them is  governed by the  express license  under which  they were
! provided to you (License).  Unless the License provides otherwise, you may not
! use, modify, copy, publish, distribute,  disclose or transmit this software or
! the related documents without Intel's prior written permission.
!
! This software and the related documents  are provided as  is,  with no express
! or implied  warranties,  other  than those  that are  expressly stated  in the
! License.
!===============================================================================

! Content:
!    Intel(R) oneAPI Math Kernel Library (Intel(R) oneMKL)
!    FFTW3 Fortran OpenMP Offload Interfaces
!*****************************************************************************

MODULE PREC
  INTEGER, PARAMETER :: FFTW_SPKP = SELECTED_REAL_KIND(6,37)
  INTEGER, PARAMETER :: FFTW_DPKP = SELECTED_REAL_KIND(15,307)
END MODULE PREC

MODULE FFTW3_OMP_OFFLOAD

  INTERFACE
    SUBROUTINE dfftw_plan_dft_1d_omp_offload_lp64(p, n, in, out, s, flags)
      USE PREC
      INTEGER*8 :: p
      INTEGER(4) :: n, s, flags
      COMPLEX(FFTW_DPKP), INTENT(IN), DIMENSION(*) :: in
      COMPLEX(FFTW_DPKP), INTENT(OUT), DIMENSION(*) :: out
    END SUBROUTINE dfftw_plan_dft_1d_omp_offload_lp64

    SUBROUTINE dfftw_plan_dft_1d_omp_offload_ilp64(p, n, in, out, s, flags)
      USE PREC
      INTEGER*8 :: p
      INTEGER(8) :: n, s, flags
      COMPLEX(FFTW_DPKP), INTENT(IN), DIMENSION(*) :: in
      COMPLEX(FFTW_DPKP), INTENT(OUT), DIMENSION(*) :: out
    END SUBROUTINE dfftw_plan_dft_1d_omp_offload_ilp64

    SUBROUTINE dfftw_plan_dft_2d_omp_offload_lp64(p, nx, ny, in, out, s, flags)
      USE PREC
      INTEGER*8 :: p
      INTEGER(4) :: nx, ny, s, flags
      COMPLEX(FFTW_DPKP), INTENT(IN), DIMENSION(..) :: in
      COMPLEX(FFTW_DPKP), INTENT(OUT), DIMENSION(..) :: out
    END SUBROUTINE dfftw_plan_dft_2d_omp_offload_lp64

    SUBROUTINE dfftw_plan_dft_2d_omp_offload_ilp64(p, nx, ny, in, out, s, flags)
      USE PREC
      INTEGER*8 :: p
      INTEGER(8) :: nx, ny, s, flags
      COMPLEX(FFTW_DPKP), INTENT(IN), DIMENSION(..) :: in
      COMPLEX(FFTW_DPKP), INTENT(OUT), DIMENSION(..) :: out
    END SUBROUTINE dfftw_plan_dft_2d_omp_offload_ilp64

    SUBROUTINE dfftw_plan_dft_3d_omp_offload_lp64(p, nx, ny, nz, in, out, s, flags)
      USE PREC
      INTEGER*8 :: p
      INTEGER(4) :: nx, ny, nz, s, flags
      COMPLEX(FFTW_DPKP), INTENT(IN), DIMENSION(..) :: in
      COMPLEX(FFTW_DPKP), INTENT(OUT), DIMENSION(..) :: out
    END SUBROUTINE dfftw_plan_dft_3d_omp_offload_lp64

    SUBROUTINE dfftw_plan_dft_3d_omp_offload_ilp64(p, nx, ny, nz, in, out, s, flags)
      USE PREC
      INTEGER*8 :: p
      INTEGER(8) :: nx, ny, nz, s, flags
      COMPLEX(FFTW_DPKP), INTENT(IN), DIMENSION(..) :: in
      COMPLEX(FFTW_DPKP), INTENT(OUT), DIMENSION(..) :: out
    END SUBROUTINE dfftw_plan_dft_3d_omp_offload_ilp64

    SUBROUTINE dfftw_plan_many_dft_omp_offload_lp64(p, rank, n, howmany, in, inembed, istride, idist, out, onembed, ostride, odist, s, flags)
      USE PREC
      INTEGER*8 :: p
      INTEGER(4) :: rank, howmany, istride, idist, ostride, odist, s, flags
      INTEGER(4), DIMENSION(*) :: n, inembed, onembed
      COMPLEX(FFTW_DPKP), INTENT(IN), DIMENSION(..) :: in
      COMPLEX(FFTW_DPKP), INTENT(OUT), DIMENSION(..) :: out
    END SUBROUTINE dfftw_plan_many_dft_omp_offload_lp64

    SUBROUTINE dfftw_plan_many_dft_omp_offload_ilp64(p, rank, n, howmany, in, inembed, istride, idist, out, onembed, ostride, odist, s, flags)
      USE PREC
      INTEGER*8 :: p
      INTEGER(8) :: rank, howmany, istride, idist, ostride, odist, s, flags
      INTEGER(8), DIMENSION(*) :: n, inembed, onembed
      COMPLEX(FFTW_DPKP), INTENT(IN), DIMENSION(..) :: in
      COMPLEX(FFTW_DPKP), INTENT(OUT), DIMENSION(..) :: out
    END SUBROUTINE dfftw_plan_many_dft_omp_offload_ilp64

    SUBROUTINE dfftw_execute_omp_offload(p)
      INTEGER*8 :: p
    END SUBROUTINE dfftw_execute_omp_offload

    SUBROUTINE dfftw_execute(p)
      INTEGER*8 :: p
      !$omp  declare variant( dfftw_execute:dfftw_execute_omp_offload ) match( construct={target variant dispatch}, device={arch(gen)} )
    END SUBROUTINE dfftw_execute

    SUBROUTINE dfftw_execute_dft_omp_offload(p, in, out)
      USE PREC
      INTEGER*8 :: p
      COMPLEX(FFTW_DPKP), INTENT(IN), DIMENSION(..) :: in
      COMPLEX(FFTW_DPKP), INTENT(OUT), DIMENSION(..) :: out
    END SUBROUTINE dfftw_execute_dft_omp_offload

  END INTERFACE

  INTERFACE dfftw_execute_dft
    SUBROUTINE dfftw_execute_dft_cpu(p, in, out)
      USE PREC
      INTEGER*8 :: p
      COMPLEX(FFTW_DPKP), INTENT(IN), DIMENSION(..) :: in
      COMPLEX(FFTW_DPKP), INTENT(OUT), DIMENSION(..) :: out
      !$omp  declare variant( dfftw_execute_dft_cpu:dfftw_execute_dft_omp_offload ) match( construct={target variant dispatch}, device={arch(gen)} )
    END SUBROUTINE dfftw_execute_dft_cpu
  END INTERFACE

  INTERFACE dfftw_plan_dft_1d
    SUBROUTINE dfftw_plan_dft_1d_cpu_lp64(p, n, in, out, s, flags)
      USE PREC
      INTEGER*8 :: p
      INTEGER(4) :: n, s, flags
      COMPLEX(FFTW_DPKP), INTENT(IN), DIMENSION(*) :: in
      COMPLEX(FFTW_DPKP), INTENT(OUT), DIMENSION(*) :: out
      !$omp  declare variant( dfftw_plan_dft_1d_cpu_lp64:dfftw_plan_dft_1d_omp_offload_lp64 ) match( construct={target variant dispatch}, device={arch(gen)} )
    END SUBROUTINE dfftw_plan_dft_1d_cpu_lp64

    SUBROUTINE dfftw_plan_dft_1d_cpu_ilp64(p, n, in, out, s, flags)
      USE PREC
      INTEGER*8 :: p
      INTEGER(8) :: n, s, flags
      COMPLEX(FFTW_DPKP), INTENT(IN), DIMENSION(*) :: in
      COMPLEX(FFTW_DPKP), INTENT(OUT), DIMENSION(*) :: out
      !$omp  declare variant( dfftw_plan_dft_1d_cpu_ilp64:dfftw_plan_dft_1d_omp_offload_ilp64 ) match( construct={target variant dispatch}, device={arch(gen)} )
    END SUBROUTINE dfftw_plan_dft_1d_cpu_ilp64
   END INTERFACE dfftw_plan_dft_1d

   INTERFACE dfftw_plan_dft_2d
    SUBROUTINE dfftw_plan_dft_2d_cpu_lp64(p, nx, ny, in, out, s, flags)
      USE PREC
      INTEGER*8 :: p
      INTEGER(4) :: nx, ny, s, flags
      COMPLEX(FFTW_DPKP), INTENT(IN), DIMENSION(..) :: in
      COMPLEX(FFTW_DPKP), INTENT(OUT), DIMENSION(..) :: out
      !$omp  declare variant( dfftw_plan_dft_2d_cpu_lp64:dfftw_plan_dft_2d_omp_offload_lp64 ) match( construct={target variant dispatch}, device={arch(gen)} )
    END SUBROUTINE dfftw_plan_dft_2d_cpu_lp64

      SUBROUTINE dfftw_plan_dft_2d_cpu_ilp64(p, nx, ny, in, out, s, flags)
      USE PREC
      INTEGER*8 :: p
      INTEGER(8) :: nx, ny, s, flags
      COMPLEX(FFTW_DPKP), INTENT(IN), DIMENSION(..) :: in
      COMPLEX(FFTW_DPKP), INTENT(OUT), DIMENSION(..) :: out
      !$omp  declare variant( dfftw_plan_dft_2d_cpu_ilp64:dfftw_plan_dft_2d_omp_offload_ilp64 ) match( construct={target variant dispatch}, device={arch(gen)} )
    END SUBROUTINE dfftw_plan_dft_2d_cpu_ilp64

   END INTERFACE dfftw_plan_dft_2d

  INTERFACE dfftw_plan_dft_3d
    SUBROUTINE dfftw_plan_dft_3d_cpu_lp64(p, nx, ny, nz, in, out, s, flags)
      USE PREC
      INTEGER*8 :: p
      INTEGER(4) :: nx, ny, nz, s, flags
      COMPLEX(FFTW_DPKP), INTENT(IN), DIMENSION(..) :: in
      COMPLEX(FFTW_DPKP), INTENT(OUT), DIMENSION(..) :: out
      !$omp  declare variant( dfftw_plan_dft_3d_cpu_lp64:dfftw_plan_dft_3d_omp_offload_lp64 ) match( construct={target variant dispatch}, device={arch(gen)} )
    END SUBROUTINE dfftw_plan_dft_3d_cpu_lp64

   SUBROUTINE dfftw_plan_dft_3d_cpu_ilp64(p, nx, ny, nz, in, out, s, flags)
      USE PREC
      INTEGER*8 :: p
      INTEGER(8) :: nx, ny, nz, s, flags
      COMPLEX(FFTW_DPKP), INTENT(IN), DIMENSION(..) :: in
      COMPLEX(FFTW_DPKP), INTENT(OUT), DIMENSION(..) :: out
      !$omp  declare variant( dfftw_plan_dft_3d_cpu_ilp64:dfftw_plan_dft_3d_omp_offload_ilp64 ) match( construct={target variant dispatch}, device={arch(gen)} )
    END SUBROUTINE dfftw_plan_dft_3d_cpu_ilp64
   END INTERFACE dfftw_plan_dft_3d

   INTERFACE dfftw_plan_many_dft
    SUBROUTINE dfftw_plan_many_dft_cpu_lp64(p, rank, n, howmany, in, inembed, istride, idist, out, onembed, ostride, odist, s, flags)
      USE PREC
      INTEGER*8 :: p
      INTEGER(4) :: rank, howmany, istride, idist, ostride, odist, s, flags
      INTEGER(4), DIMENSION(*) :: n, inembed, onembed
      COMPLEX(FFTW_DPKP), INTENT(IN), DIMENSION(..) :: in
      COMPLEX(FFTW_DPKP), INTENT(OUT), DIMENSION(..) :: out
      !$omp  declare variant( dfftw_plan_many_dft_cpu_lp64:dfftw_plan_many_dft_omp_offload_lp64 ) match( construct={target variant dispatch}, device={arch(gen)} )
    END SUBROUTINE dfftw_plan_many_dft_cpu_lp64

    SUBROUTINE dfftw_plan_many_dft_cpu_ilp64(p, rank, n, howmany, in, inembed, istride, idist, out, onembed, ostride, odist, s, flags)
      USE PREC
      INTEGER*8 :: p
      INTEGER(8) :: rank, howmany, istride, idist, ostride, odist, s, flags
      INTEGER(8), DIMENSION(*) :: n, inembed, onembed
      COMPLEX(FFTW_DPKP), INTENT(IN), DIMENSION(..) :: in
      COMPLEX(FFTW_DPKP), INTENT(OUT), DIMENSION(..) :: out
      !$omp  declare variant( dfftw_plan_many_dft_cpu_ilp64:dfftw_plan_many_dft_omp_offload_ilp64 ) match( construct={target variant dispatch}, device={arch(gen)} )
    END SUBROUTINE dfftw_plan_many_dft_cpu_ilp64
   END INTERFACE

   INTERFACE
    SUBROUTINE sfftw_plan_dft_1d_omp_offload_lp64(p, n, in, out, s, flags)
      USE PREC
      INTEGER*8 :: p
      INTEGER(4) :: n, s, flags
      COMPLEX(FFTW_SPKP), INTENT(IN), DIMENSION(*) :: in
      COMPLEX(FFTW_SPKP), INTENT(OUT), DIMENSION(*) :: out
    END SUBROUTINE sfftw_plan_dft_1d_omp_offload_lp64

    SUBROUTINE sfftw_plan_dft_1d_omp_offload_ilp64(p, n, in, out, s, flags)
      USE PREC
      INTEGER*8 :: p
      INTEGER(8) :: n, s, flags
      COMPLEX(FFTW_SPKP), INTENT(IN), DIMENSION(*) :: in
      COMPLEX(FFTW_SPKP), INTENT(OUT), DIMENSION(*) :: out
    END SUBROUTINE sfftw_plan_dft_1d_omp_offload_ilp64

    SUBROUTINE sfftw_plan_dft_2d_omp_offload_lp64(p, nx, ny, in, out, s, flags)
      USE PREC
      INTEGER*8 :: p
      INTEGER(4) :: nx, ny, s, flags
      COMPLEX(FFTW_SPKP), INTENT(IN), DIMENSION(..) :: in
      COMPLEX(FFTW_SPKP), INTENT(OUT), DIMENSION(..) :: out
    END SUBROUTINE sfftw_plan_dft_2d_omp_offload_lp64

    SUBROUTINE sfftw_plan_dft_2d_omp_offload_ilp64(p, nx, ny, in, out, s, flags)
      USE PREC
      INTEGER*8 :: p
      INTEGER(8) :: nx, ny, s, flags
      COMPLEX(FFTW_SPKP), INTENT(IN), DIMENSION(..) :: in
      COMPLEX(FFTW_SPKP), INTENT(OUT), DIMENSION(..) :: out
    END SUBROUTINE sfftw_plan_dft_2d_omp_offload_ilp64

    SUBROUTINE sfftw_plan_dft_3d_omp_offload_lp64(p, nx, ny, nz, in, out, s, flags)
      USE PREC
      INTEGER*8 :: p
      INTEGER(4) :: nx, ny, nz, s, flags
      COMPLEX(FFTW_SPKP), INTENT(IN), DIMENSION(..) :: in
      COMPLEX(FFTW_SPKP), INTENT(OUT), DIMENSION(..) :: out
    END SUBROUTINE sfftw_plan_dft_3d_omp_offload_lp64

    SUBROUTINE sfftw_plan_dft_3d_omp_offload_ilp64(p, nx, ny, nz, in, out, s, flags)
      USE PREC
      INTEGER*8 :: p
      INTEGER(8) :: nx, ny, nz, s, flags
      COMPLEX(FFTW_SPKP), INTENT(IN), DIMENSION(..) :: in
      COMPLEX(FFTW_SPKP), INTENT(OUT), DIMENSION(..) :: out
    END SUBROUTINE sfftw_plan_dft_3d_omp_offload_ilp64

    SUBROUTINE sfftw_plan_many_dft_omp_offload_lp64(p, rank, n, howmany, in, inembed, istride, idist, out, onembed, ostride, odist, s, flags)
      USE PREC
      INTEGER*8 :: p
      INTEGER(4) :: rank, howmany, istride, idist, ostride, odist, s, flags
      INTEGER(4), DIMENSION(*) :: n, inembed, onembed
      COMPLEX(FFTW_SPKP), INTENT(IN), DIMENSION(..) :: in
      COMPLEX(FFTW_SPKP), INTENT(OUT), DIMENSION(..) :: out
    END SUBROUTINE sfftw_plan_many_dft_omp_offload_lp64

    SUBROUTINE sfftw_plan_many_dft_omp_offload_ilp64(p, rank, n, howmany, in, inembed, istride, idist, out, onembed, ostride, odist, s, flags)
      USE PREC
      INTEGER*8 :: p
      INTEGER(8) :: rank, howmany, istride, idist, ostride, odist, s, flags
      INTEGER(8), DIMENSION(*) :: n, inembed, onembed
      COMPLEX(FFTW_SPKP), INTENT(IN), DIMENSION(..) :: in
      COMPLEX(FFTW_SPKP), INTENT(OUT), DIMENSION(..) :: out
    END SUBROUTINE sfftw_plan_many_dft_omp_offload_ilp64

    SUBROUTINE sfftw_execute_omp_offload(p)
      INTEGER*8 :: p
    END SUBROUTINE sfftw_execute_omp_offload

    SUBROUTINE sfftw_execute(p)
      INTEGER*8 :: p
      !$omp  declare variant( sfftw_execute:sfftw_execute_omp_offload ) match( construct={target variant dispatch}, device={arch(gen)} )
    END SUBROUTINE sfftw_execute

    SUBROUTINE sfftw_execute_dft_omp_offload(p, in, out)
      USE PREC
      INTEGER*8 :: p
      COMPLEX(FFTW_SPKP), INTENT(IN), DIMENSION(..) :: in
      COMPLEX(FFTW_SPKP), INTENT(OUT), DIMENSION(..) :: out
    END SUBROUTINE sfftw_execute_dft_omp_offload

  END INTERFACE

  INTERFACE sfftw_execute_dft
    SUBROUTINE sfftw_execute_dft_cpu(p, in, out)
      USE PREC
      INTEGER*8 :: p
      COMPLEX(FFTW_SPKP), INTENT(IN), DIMENSION(..) :: in
      COMPLEX(FFTW_SPKP), INTENT(OUT), DIMENSION(..) :: out
      !$omp  declare variant( sfftw_execute_dft_cpu:sfftw_execute_dft_omp_offload ) match( construct={target variant dispatch}, device={arch(gen)} )
    END SUBROUTINE sfftw_execute_dft_cpu
   END INTERFACE

   INTERFACE sfftw_plan_dft_1d
    SUBROUTINE sfftw_plan_dft_1d_cpu_lp64(p, n, in, out, s, flags)
      USE PREC
      INTEGER*8 :: p
      INTEGER(4) :: n, s, flags
      COMPLEX(FFTW_SPKP), INTENT(IN), DIMENSION(*) :: in
      COMPLEX(FFTW_SPKP), INTENT(OUT), DIMENSION(*) :: out
      !$omp  declare variant( sfftw_plan_dft_1d_cpu_lp64:sfftw_plan_dft_1d_omp_offload_lp64 ) match( construct={target variant dispatch}, device={arch(gen)} )
    END SUBROUTINE sfftw_plan_dft_1d_cpu_lp64

    SUBROUTINE sfftw_plan_dft_1d_cpu_ilp64(p, n, in, out, s, flags)
      USE PREC
      INTEGER*8 :: p
      INTEGER(8) :: n, s, flags
      COMPLEX(FFTW_SPKP), INTENT(IN), DIMENSION(*) :: in
      COMPLEX(FFTW_SPKP), INTENT(OUT), DIMENSION(*) :: out
      !$omp  declare variant( sfftw_plan_dft_1d_cpu_ilp64:sfftw_plan_dft_1d_omp_offload_ilp64 ) match( construct={target variant dispatch}, device={arch(gen)} )
    END SUBROUTINE sfftw_plan_dft_1d_cpu_ilp64
   END INTERFACE

   INTERFACE sfftw_plan_dft_2d
    SUBROUTINE sfftw_plan_dft_2d_cpu_lp64(p, nx, ny, in, out, s, flags)
      USE PREC
      INTEGER*8 :: p
      INTEGER(4) :: nx, ny, s, flags
      COMPLEX(FFTW_SPKP), INTENT(IN), DIMENSION(..) :: in
      COMPLEX(FFTW_SPKP), INTENT(OUT), DIMENSION(..) :: out
      !$omp  declare variant( sfftw_plan_dft_2d_cpu_lp64:sfftw_plan_dft_2d_omp_offload_lp64 ) match( construct={target variant dispatch}, device={arch(gen)} )
    END SUBROUTINE sfftw_plan_dft_2d_cpu_lp64

    SUBROUTINE sfftw_plan_dft_2d_cpu_ilp64(p, nx, ny, in, out, s, flags)
      USE PREC
      INTEGER*8 :: p
      INTEGER(8) :: nx, ny, s, flags
      COMPLEX(FFTW_SPKP), INTENT(IN), DIMENSION(..) :: in
      COMPLEX(FFTW_SPKP), INTENT(OUT), DIMENSION(..) :: out
      !$omp  declare variant( sfftw_plan_dft_2d_cpu_ilp64:sfftw_plan_dft_2d_omp_offload_ilp64 ) match( construct={target variant dispatch}, device={arch(gen)} )
    END SUBROUTINE sfftw_plan_dft_2d_cpu_ilp64
   END INTERFACE

   INTERFACE sfftw_plan_dft_3d
    SUBROUTINE sfftw_plan_dft_3d_cpu_lp64(p, nx, ny, nz, in, out, s, flags)
      USE PREC
      INTEGER*8 :: p
      INTEGER(4) :: nx, ny, nz, s, flags
      COMPLEX(FFTW_SPKP), INTENT(IN), DIMENSION(..) :: in
      COMPLEX(FFTW_SPKP), INTENT(OUT), DIMENSION(..) :: out
      !$omp  declare variant( sfftw_plan_dft_3d_cpu_lp64:sfftw_plan_dft_3d_omp_offload_lp64 ) match( construct={target variant dispatch}, device={arch(gen)} )
    END SUBROUTINE sfftw_plan_dft_3d_cpu_lp64

    SUBROUTINE sfftw_plan_dft_3d_cpu_ilp64(p, nx, ny, nz, in, out, s, flags)
      USE PREC
      INTEGER*8 :: p
      INTEGER(8) :: nx, ny, nz, s, flags
      COMPLEX(FFTW_SPKP), INTENT(IN), DIMENSION(..) :: in
      COMPLEX(FFTW_SPKP), INTENT(OUT), DIMENSION(..) :: out
      !$omp  declare variant( sfftw_plan_dft_3d_cpu_ilp64:sfftw_plan_dft_3d_omp_offload_ilp64 ) match( construct={target variant dispatch}, device={arch(gen)} )
    END SUBROUTINE sfftw_plan_dft_3d_cpu_ilp64
   END INTERFACE

   INTERFACE sfftw_plan_many_dft
    SUBROUTINE sfftw_plan_many_dft_cpu_lp64(p, rank, n, howmany, in, inembed, istride, idist, out, onembed, ostride, odist, s, flags)
      USE PREC
      INTEGER*8 :: p
      INTEGER(4) :: rank, howmany, istride, idist, ostride, odist, s, flags
      INTEGER(4), DIMENSION(*) :: n, inembed, onembed
      COMPLEX(FFTW_SPKP), INTENT(IN), DIMENSION(..) :: in
      COMPLEX(FFTW_SPKP), INTENT(OUT), DIMENSION(..) :: out
      !$omp  declare variant( sfftw_plan_many_dft_cpu_lp64:sfftw_plan_many_dft_omp_offload_lp64 ) match( construct={target variant dispatch}, device={arch(gen)} )
    END SUBROUTINE sfftw_plan_many_dft_cpu_lp64

    SUBROUTINE sfftw_plan_many_dft_cpu_ilp64(p, rank, n, howmany, in, inembed, istride, idist, out, onembed, ostride, odist, s, flags)
      USE PREC
      INTEGER*8 :: p
      INTEGER(8) :: rank, howmany, istride, idist, ostride, odist, s, flags
      INTEGER(8), DIMENSION(*) :: n, inembed, onembed
      COMPLEX(FFTW_SPKP), INTENT(IN), DIMENSION(..) :: in
      COMPLEX(FFTW_SPKP), INTENT(OUT), DIMENSION(..) :: out
      !$omp  declare variant( sfftw_plan_many_dft_cpu_ilp64:sfftw_plan_many_dft_omp_offload_ilp64 ) match( construct={target variant dispatch}, device={arch(gen)} )
    END SUBROUTINE sfftw_plan_many_dft_cpu_ilp64
   END INTERFACE

END MODULE FFTW3_OMP_OFFLOAD
