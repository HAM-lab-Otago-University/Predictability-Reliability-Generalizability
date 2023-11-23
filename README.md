# Predictability-Reliability-Generalizability

Benchmark Machine-Learning Based Multimodal MRI to Capture Cognitive Abilities across the Lifespan: Predictability, Reliability and Generalisability

Abstract

Across the lifespan, people differ in their cognitive abilities, and these individual differences may be indicative of neurological/psychiatric issues. Having a neuroimaging-based biomarker that can capture the individual differences in cognitive abilities may allow us to early detect or trace neurological/psychiatric issues. As with any robust biomarker, a neuroimaging based biomarker needs to have good psychometric properties: predictability (i.e., predicting cognitive abilities of persons outside of the model-building processes), reliability (i.e., having stable ranks across time), and generalisability (i.e., predicting cognitive abilities across datasets). Here, we benchmarked these abilities for MRI of different types to capture cognitive abilities across the lifespan. We took three MRI databases (Human Connectome Project Young Adults (HCP-YA), Human Connectome Project Aging (HCP-A), Dunedin Study (DUD)), covering 2,131 people from 22 to almost 100 years old. Each database consists of multiple MRI types: structural, resting state and fMRI during several tasks. We combined different MRI measures together using a stacking approach and Elastic Net to predict cognitive abilities. Stacking led to good prediction across datasets: HCP-YA (r = 0.60), HCP-A (r=0.61), DUD (r=0.55). Similarly, stacking also led to excellent test-retest reliability in HCP-YA (ICC = 0.79) and DUD (ICC= 0.89). For generalisability, we could only combine non-task MRI types (i.e., structural MRI and resting state fMRI) together, given that different studies used different tasks. We found non-task stacking led to modest generalisability across datasets with mean r=0.25, compared to prediction within-datasets mean r=0.40. Thus, multimodal MRI could capture cognitive abilities with good predictability and reliability and modest generalizability.




For reproducibility purposes, we provided all scripts we used in this study as well as supplementary files here.
Note users will need to edit these scripts so that the designated folders and files match with their local settings.

The data for this article was extensively preprocessed within previous projects as: https://github.com/HAM-lab-Otago-University/HCP for HCP Young Adults dataset, https://github.com/HAM-lab-Otago-University/HCP-Aging_commonality for HCP Aging dataset, and https://dunedinstudy.otago.ac.nz/ for the Dunedin Study dataset.
Some files, if not placed in this directory, can be found in our aforementioned github projects.

Common abbreviations within scripts:

HCP-YA, hcp-ya, hcp_ya, ya - HCP Young Adults dataset,

HCP-A, hcp-a, hcp_a, a - HCP Aging dataset,

DUD, DUD45, DUD_ch, DUD_res, dud, d - Dunedin Study dataset (with next extension: 45 - scanned at age 45 years old; ch - observed or tested at childhood age (7-11 years old), res - residuals)



The directory contains the following files and folders:


/1_Preprocessing/hcp_ya/

01_fMRIPrep – folder contains slurm scripts for running fMRIPrep preprocessing script on resting state and task data of HCP-YA,

02_XCP-D – folder contains slurm scripts for running XCP-D cleaning script on resting state and task data of HCP-YA,

03_HCP-YA_New_rest-state_extraction_from_cifti_to_table.ipynb, 04_HCP-YA_New_rest-state_extraction_from_cifti_to_table-RETEST.ipynb, 05_HCP-YA_TASK_FC.ipynb, 06_HCP-YA_TASK_FC_retest.ipynb – scripts assembles atlas-based csv tables from CIFTI files from the previous step,

07_HCP-YA_ENet_Stacked_cognition_norace_pca75_noRestMov_AgeADJ_manyCon_NEW_ADJ_TYPE_OneTrain_stackSTD_5cv_new enhanced.ipynb – this script does fold-wise brain feature and target table adjustment (by residualising) to biological sex and/or age before main machine learning script; it also makes Elastic Net machine learning.


/1_Preprocessing/hcp_a/

01_HCP-A_ENet_Stacked_COG_pca75_ALLADJ_trainAdj_OneTrain_StackSTD_5cv.ipynb – the script does fold-wise brain feature and target table adjustment (by residualising) to biological sex and/or age before main machine learning script; it also makes Elastic Net machine learning.


/1_Preprocessing/dud/

01 dud tables clenup (only the same parameters as in hcp).ipynb, 02 dud tables clenup (only the same parameters as in hcp)-retest set.ipynb, 03 dud tables clenup (task FC tables).ipynb, 04 dud tables clenup (task FC tables)-retest set.ipynb – these scripts checks provided Dunedin Study tables for missiong values and reorganize in the same structure as in other two datasets;

05 DUD_StackedML_ElasticNet_cognition_pca75_task-FC-unstd_iq45_NewADJ_OneTrain_stackSTD_5cv_new type of iq res.ipynb – the script does fold-wise brain feature and target table adjustment (by residualising) to biological sex and/or age before main machine learning script; it also makes Elastic Net machine learning;

06 IQ resuduals calculation.ipynb – the script does fold-wise total cognitive score adjustment (adult to childhood).


2_Modelling/01_NESI_ML/ – the folder contains the main machine learning scripts, adapted to the super computer calculations (on NeSI). The ML parameters for 4 algorithms can be found at params.py script. The calculations can be launched through train_*.py scripts for the single modality level and train_layer2_*.py for the stacked level;

/2_Modelling/02_slurm_launch/ – the folder contains the slurm files helping to launch previous step;

/2_Modelling/03_Generalizability/LS_3dataset_ElasticNet_cognition_NonTask_AgeSexAdj_New_version_stacked.ipynb – the script does the machine learning rounds for the generalizability modelling;

/2_Modelling/04_HCP_YA_models/

01_HCP-YA_ENet_Stacked_cognition_pca75_noRestMov_AgeADJ_manyCon_NEW_ADJ_TYPE_OneTrain_stackSTD_5cv_Feature_Importance_new_enhanced_sets.ipynb – the script runs one-fold machine learning Elastic Net round for getting a feature importance (elastic net weights);

02_HCP-YA_RETEST_ElasticNet_cognition_pca75_taskFC_NewADJ_OneTrain_stackSTD_5cv_new_enhanced_sets.ipynb – the script runs a one-fold machine learning Elastic Net round with 2 testing sets for test-retest reliability.

/2_Modelling/05_HCP_A_models/01_HCP-A_ENet_Stacked_COG_pca75_ALLADJ_trainAdj_OneTrain_StackSTD_5cv_Feature_Importance_short.ipynb – the script runs one-fold machine learning Elastic Net round for getting a feature importance (elastic net weights). 

/2_Modelling/06_DUD_models/

01_DUD_StackedML_ElasticNet_cognition_pca75_task-FC-unstd_iq45_NewADJ_OneTrain_stackSTD_5cv_Feature Importance.ipynb - the script runs one-fold machine learning Elastic Net round for getting a feature importance (elastic net weights);

02_DUD_RETEST_ElasticNet_cognition_pca75_taskFC_NewADJ_OneTrain_stackSTD_5cv.ipynb – the script runs a one-fold machine learning Elastic Net round with 2 testing sets for test-retest reliability.


