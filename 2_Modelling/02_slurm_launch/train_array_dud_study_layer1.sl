#!/bin/bash -e

#SBATCH --job-name=dud_study_layer1_v5
#SBATCH --time=24:00:00
#SBATCH --mem-per-cpu=2048MB
#SBATCH --cpus-per-task=4
#SBATCH --account=your_account
#SBATCH --profile task
#SBATCH --output=/hpc/scratch/your_account/Dunedin-MRI-Study-Array/slurm_outputs/%x/%x_%j_%a.out

#SBATCH --mail-user=your@email.address
#SBATCH --mail-type=ALL

#SBATCH --array=0-2183

module load Dunedin-MRI-Study

python ../train_dud_study.py "${SLURM_ARRAY_TASK_ID}"
