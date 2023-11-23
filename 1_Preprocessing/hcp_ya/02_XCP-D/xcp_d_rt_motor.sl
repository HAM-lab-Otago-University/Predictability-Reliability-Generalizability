#!/bin/bash -e
##SBATCH --partition large,hugemem,bigmem
##SBATCH --partition milan
#SBATCH --job-name=XCP_D_MTR_RT
#SBATCH --time=30:00:00
#SBATCH --mem=40GB
#SBATCH --cpus-per-task=2
#SBATCH --account=your_account
#SBATCH --profile task
#SBATCH --output=/hpc/scratch/your_account/sing/HCP/logs/%x/%x_%j_%a.out

#SBATCH --mail-user=your@email.address
#SBATCH --mail-type=ALL

#SBATCH --array=0-33

module load Singularity

echo HCP-acompcor-RT_MTR
echo 0-44

subjects_string=`cat /hpc/scratch/your_account/sing/HCP/subjects/subjects-XCP_d-retest.csv`

IFS=',' read -r -a array <<< "$subjects_string"

participant_id="${array[${SLURM_ARRAY_TASK_ID}]}"

echo "participant id $participant_id"

work_dir_abs_path="/hpc/scratch/your_account/sing/work_dir/XCP_D_MTR_working_dir_$participant_id"

export SINGULARITY_BIND="/hpc/scratch/your_account/sing:/sing/,/hpc/scratch/your_account/TEMP/tmp_${SLURM_JOB_ID}:/tmp/"

image_path="/hpc/scratch/your_account/sing/images/xcp_d-0.4.0rc2+16.g6109c09.simg"

in_path="/sing/data/HCP-RT/derivatives/fmriprep"

out_path="/sing/data/HCP-RT/derivatives/xcp_d-0.4.0rc2+16"

work_dir_path="/sing/work_dir/XCP_D_MTR_working_dir_$participant_id"

custom_confounds="/sing/data/HCP-RT/derivatives/custom_confounds"

rm -rf ${work_dir_abs_path}
mkdir ${work_dir_abs_path}

trap "rm -rf $work_dir_abs_path" EXIT

singularity run --cleanenv ${image_path} \
${in_path}  \
${out_path} \
participant --participant_label ${participant_id} \
--clean-workdir \
--input-type fmriprep \
--cifti \
--smoothing 0 \
--task-id MOTOR \
--despike \
--nuisance-regressors acompcor \
--custom_confounds ${custom_confounds} \
--dummy-scans auto \
--disable-bandpass-filter \
--fd-thresh 0.5 \
--dcan-qc \
--notrack \
--nthreads 2 \
--omp-nthreads 2 \
--mem_gb 40 \
-w ${work_dir_path}

echo "finished $participant_id , with xcp_d_compcor_MTR_RT"

echo "finished $participant_id , removing working directory"
rm -rf ${work_dir_abs_path}
echo "finished $participant_id , removing temp directory"
rm -rf $TMPDIR
