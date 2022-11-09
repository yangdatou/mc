#!/bin/bash                                                                          
#SBATCH --partition=debug
#SBATCH --time=01:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=3
#SBATCH --job-name=mc-ising
#SBATCH --mem=0

module purge
module load gcc/9.2.0
module load binutils/2.26
module load cmake-3.6.2 

source /home/yangjunjie/intel/oneapi/setvars.sh --force;
export LD_LIBRARY_PATH=$MKLROOT/lib:$LD_LIBRARY_PATH
export PYTHONPATH=/home/yangjunjie/packages/pyscf/pyscf-main
export PYSCF_TMPDIR=/scratch/global/yangjunjie/

export CC=icc
export FC=ifort
export CXX=icpc

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK;
export PYSCF_MAX_MEMORY=$SLURM_MEM_PER_NODE;
echo SLURM_CPUS_PER_TASK = $SLURM_CPUS_PER_TASK;
echo SLURM_MEM_PER_NODE  = $SLURM_MEM_PER_NODE;

python mc.py 0.5 &
python mc.py 1.0 &
python mc.py 2.0

