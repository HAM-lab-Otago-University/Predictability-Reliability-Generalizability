#!/bin/bash -e
#SBATCH --job-name=fp_w_aroma
#SBATCH --time=120:00:00
#SBATCH --mem=80000MB
#SBATCH --cpus-per-task=12
#SBATCH --account=your_account
#SBATCH --profile task
#SBATCH --output=/hpc/scratch/your_account/sing/HCP/logs/%x/%x_%j_%a.out

#SBATCH --mail-user=your@email.address
#SBATCH --mail-type=ALL

#SBATCH --array=0-827

module load Singularity

echo HCP 
echo 0-827

subjects_string=`cat /hpc/scratch/your_account/sing/HCP/subjects/subjects.csv`

IFS=',' read -r -a array <<< "$subjects_string"

participant_id="${array[${SLURM_ARRAY_TASK_ID}]}"

echo "participant id $participant_id"

work_dir_abs_path="/hpc/scratch/your_account/sing/work_dir/fmriprep_working_dir_$participant_id"

export SINGULARITY_BIND="/hpc/scratch/your_account/sing:/scratch/"

image_path="/hpc/scratch/your_account/sing/images/fmriprep-23.0.0.simg"

bids_path="/scratch/data/HCP"

out_path="/scratch/data/HCP/derivatives/fmriprep"

work_dir_path="/scratch/work_dir/fmriprep_working_dir_$participant_id"

license_path="/scratch/fs_licence/license.txt"

fs_sub_dir="/scratch/data/HCP/derivatives/freesurfer/"

rm -rf ${work_dir_abs_path}
mkdir ${work_dir_abs_path}

trap "rm -rf $work_dir_abs_path" EXIT

singularity run --cleanenv ${image_path} \
${bids_path}  \
${out_path} \
participant --participant_label ${participant_id} \
--write-graph \
--notrack \
--nthreads 12 \
--omp-nthreads 12 \
--mem_mb 80000 \
--skip_bids_validation \
--fs-license-file ${license_path} \
--work-dir ${work_dir_path} \
--cifti-output \
--ignore slicetiming \
--fs-subjects-dir ${fs_sub_dir} \
--use-aroma

echo "finished $participant_id , with aroma"

echo "finished $participant_id , removing working directory"
rm -rf ${work_dir_abs_path}
