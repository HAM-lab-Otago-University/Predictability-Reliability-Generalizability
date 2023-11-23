# Predictability-Reliability-Generalizability

Benchmark Machine-Learning Based Multimodal MRI to Capture Cognitive Abilities across the Lifespan: Predictability, Reliability and Generalisability

Abstract

Across the lifespan, people differ in their cognitive abilities, and these individual differences may be indicative of neurological/psychiatric issues. Having a neuroimaging-based biomarker that can capture the individual differences in cognitive abilities may allow us to early detect or trace neurological/psychiatric issues. As with any robust biomarker, a neuroimaging based biomarker needs to have good psychometric properties: predictability (i.e., predicting cognitive abilities of persons outside of the model-building processes), reliability (i.e., having stable ranks across time), and generalisability (i.e., predicting cognitive abilities across datasets). Here, we benchmarked these abilities for MRI of different types to capture cognitive abilities across the lifespan. We took three MRI databases (Human Connectome Project Young Adults (HCP-YA), Human Connectome Project Aging (HCP-A), Dunedin Study (DUD)), covering 2,131 people from 22 to almost 100 years old. Each database consists of multiple MRI types: structural, resting state and fMRI during several tasks. We combined different MRI measures together using a stacking approach and Elastic Net to predict cognitive abilities. Stacking led to good prediction across datasets: HCP-YA (r = 0.60), HCP-A (r=0.61), DUD (r=0.55). Similarly, stacking also led to excellent test-retest reliability in HCP-YA (ICC = 0.79) and DUD (ICC= 0.89). For generalisability, we could only combine non-task MRI types (i.e., structural MRI and resting state fMRI) together, given that different studies used different tasks. We found non-task stacking led to modest generalisability across datasets with mean r=0.25, compared to prediction within-datasets mean r=0.40. Thus, multimodal MRI could capture cognitive abilities with good predictability and reliability and modest generalizability.




For reproducibility purposes, we provided all scripts we used in this study as well as supplementary files here.
Note users will need to edit these scripts so that the designated folders and files match with their local settings.

The data for this article was extensively preprocessed within previous projects as: https://github.com/HAM-lab-Otago-University/HCP for HCP Young Adults dataset, https://github.com/HAM-lab-Otago-University/HCP-Aging_commonality for HCP Aging dataset, and https://dunedinstudy.otago.ac.nz/ for the Dunedin Study dataset.
Some files, if not placed in this directory, can be found in our aforementioned github projects.

The directory contains the following files and folders:


