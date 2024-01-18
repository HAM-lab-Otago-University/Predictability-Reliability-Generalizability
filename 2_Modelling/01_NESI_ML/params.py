"""
This file is for holding the hyper parameter grids for gridsearching between layers1 and layers2 for the Dunedin MRI Study.
"""


import numpy as np

# hyper param dict containing hyper parameters for grid search
hyper_param_dict = {


        'svr': {'kernel' : ['rbf'],#poly,'sigmoid'], # 1
                 'gamma' : ['scale','auto', 1e-08, 1e-07, 1e-06, 1e-05, 1e-04, 1e-03, 3e-08, 3e-07, 3e-06, 3e-05, 3e-04, 3e-03,6e-08, 6e-07, 6e-06, 6e-05, 6e-04, 6e-03], # 20
                 'C': [1,6,9,10,12,15,20,50], # 8
                 "epsilon":np.arange(0.02, 0.22, 0.02) # 10
                },
  
        'eNet': {'alpha': np.logspace(-1, 2, 70), #70
                    'l1_ratio':np.linspace(0,1,25), #25
                    'max_iter': [1000], # 1
                },
 
        'xgb':{  'booster': ['gbtree'], 
                        'n_jobs': [1], 
                        #'eta':[0.03,0.06,0.1], 
                        'max_depth':list(range(1,9)),
                        'subsample':np.arange(0.5, 1.0, 0.1),
                        "gamma":np.array([1.00076853e-05,9.34881588e-05, 8.80749768e-04, 8.08577330e-03, 7.43272907e-02,  6.96351591e-01]),
                        "learning_rate":np.logspace(-5, -0.1, 5)
                        },

        'rf':{'n_estimators': [5000], # 1
                'max_depth':list(range(1,11)), # 10
                'max_features':['auto','sqrt','log2'], # 3
                'n_jobs': [1] # not for parameter seach, just setting to run on single core
                }
     
}

# hyper param dict using only one target in grid. For use in estimating resource usage
single_hyper_param_dict = {


        'svr': {'kernel' : ['rbf'],#poly,'sigmoid'], # 1
                 'gamma' : ['scale','auto', 1e-08, 1e-07, 1e-06, 1e-05, 1e-04, 1e-03, 3e-08, 3e-07, 3e-06, 3e-05, 3e-04, 3e-03,6e-08, 6e-07, 6e-06, 6e-05, 6e-04, 6e-03], # 20
                 'C': [1,6,9,10,12,15,20,50], # 8
                 "epsilon":np.arange(0.02, 0.22, 0.02) # 10
                },
  
        'eNet': {'alpha': np.logspace(-1, 2, 70), #70
                    'l1_ratio':np.linspace(0,1,25), #25
                    'max_iter': [1000], # 1
                },
 
        'xgb':{  'booster': ['gbtree'], 
                        'tree_method':['hist',],
                        'n_jobs': [1], 
                        #'eta':[0.03,], 
                        'max_depth':[1],
                        'subsample':[0.5],
                        "gamma":np.array([1.00076853e-05,]),
                        "learning_rate":[np.logspace(-5, -0.1, 10)[2]]
                        },

        'rf':{'n_estimators': [5000], # 1
                'max_depth':list(range(1,11)), # 10
                'max_features':['auto','sqrt','log2'], # 3
                'n_jobs': [1] # not for parameter seach, just setting to run on single core
                }
}


def get_all_folds(dataset_name : str):
        
        folds_dict = {"hcp_aging":[f"Fold_{i}" for i in range(5)],
                    "dud_study": [f"Fold_{i}" for i in range(7)],
                    "hcp_ya":[f"Fold_{i}" for i in range(8)]}
        
        return folds_dict[dataset_name] 


def get_all_sets(dataset_name : str):
        """
        Convenience function for getting all set names relating to a dataset
        
        Args:
            dataset_name (str): valid dataset string, one of {"dud_study", "hcp_aging", "hcp_ya"}

        Raises:
            ValueError: If dataset name is invalid

        Returns:
            list : list of set names 
        """
        
        if dataset_name not in {"dud_study", "hcp_aging", "hcp_ya"}:
                raise ValueError(f"{dataset_name} not valid name")
        
        out_dict = {"dud_study":[f"set{i}" for i in range(1,9)],
        "hcp_aging":[f"set{i}" for i in range(1,9)],
        "hcp_ya":[f"set{i}" for i in range(1,9)]
        }
        return out_dict[dataset_name]
        


def get_all_modas(dataset_name : str):
        """
        Convenience function for getting all modas relating to a dataset

        Args:
            dataset_name (str): valid dataset string, one of {"dud_study", "hcp_aging", "hcp_ya"}

        Raises:
            ValueError: If dataset name is invalid

        Returns:
            list : list of modality names 
        """
        
        if dataset_name not in {"dud_study", "hcp_aging", "hcp_ya"}:
                raise ValueError(f"{dataset_name} not valid name")
        out_dict = {"dud_study":dud_study_moda_stack_dict['set1'],
        "hcp_aging":hcp_aging_moda_stack_dict['set1'],
        "hcp_ya":hcp_ya_moda_stack_dict['set1']
        }
        return out_dict[dataset_name]
        
dud_study_moda_stack_dict = dict(
                                set1 = ['brainVol', 'cort', 'facename', 'facename_FC_PCA75', 'faces', 'faces_FC_PCA75', 'mid', 'mid_FC_PCA75', 'rest_PCA75', 'stroop', 'stroop_FC_PCA75', 'subc', 'surf'],
                                set2 = ['stroop', 'faces', 'facename', 'mid'],
                                set3 = ['cort', 'surf', 'subc','brainVol', 'rest_PCA75'],
                                set4 = ['stroop_FC_PCA75', 'faces_FC_PCA75', 'facename_FC_PCA75', 'mid_FC_PCA75'],
                                set5 = ['stroop', 'faces', 'facename', 'mid', 'stroop_FC_PCA75', 'faces_FC_PCA75', 'facename_FC_PCA75', 'mid_FC_PCA75'],
                                set6 = ['stroop', 'faces', 'facename', 'mid', 'cort', 'surf', 'subc','brainVol', 'rest_PCA75'],
                                set7 = ['stroop_FC_PCA75', 'faces_FC_PCA75', 'facename_FC_PCA75', 'mid_FC_PCA75', 'cort', 'surf', 'subc','brainVol', 'rest_PCA75'],
                                set8 = ['stroop_FC_PCA75', 'faces_FC_PCA75', 'facename_FC_PCA75', 'mid_FC_PCA75', 'rest_PCA75'])

hcp_aging_moda_stack_dict = dict(
                                set1 = ['VolBrain','carit1', 'carit_FC_PCA75', 'cort', 'face4', 'face5', 'face6', 'face_FC_PCA75', 'rest_PCA75', 'subc', 'surf', 'vism', 'vism_FC_PCA75'],
				set2 = ['carit1', 'face4','face5', 'face6','vism'],
				set3 = ['cort', 'subc', 'surf', 'rest_PCA75', 'VolBrain'],
				set4 = ['carit_FC_PCA75', 'face_FC_PCA75', 'vism_FC_PCA75'],
				set5 = ['carit1', 'face4','face5', 'face6', 'vism', 'carit_FC_PCA75', 'face_FC_PCA75', 'vism_FC_PCA75'],
				set6 = ['carit1', 'face4','face5', 'face6', 'vism', 'cort', 'subc', 'surf', 'rest_PCA75', 'VolBrain'],
				set7 = ['carit_FC_PCA75', 'face_FC_PCA75', 'vism_FC_PCA75', 'cort', 'subc', 'surf', 'rest_PCA75', 'VolBrain'],
				set8 = ['carit_FC_PCA75', 'face_FC_PCA75', 'vism_FC_PCA75', 'rest_PCA75'])

hcp_ya_moda_stack_dict = dict(
                             set1 = ['emo', 'gam', 'lan', 'mot', 'rel', 'soc', 'wm', 'gam_FC_PCA75', 'lan_FC_PCA75', 'mot_FC_PCA75', 'rel_FC_PCA75', 'soc_FC_PCA75', 'wm_FC_PCA75', 'cort', 'subc', 'surf', 'VolBrain', 'rest_PCA75'],
                             set2 = ['emo', 'gam', 'lan', 'mot', 'rel', 'soc', 'wm'],
                             set3 = ['cort', 'subc', 'surf', 'rest_PCA75', 'VolBrain'],
                             set4 = ['gam_FC_PCA75', 'lan_FC_PCA75', 'mot_FC_PCA75', 'rel_FC_PCA75', 'soc_FC_PCA75', 'wm_FC_PCA75'],
                             set5 = ['emo', 'gam', 'lan', 'mot', 'rel', 'soc', 'wm', 'gam_FC_PCA75', 'lan_FC_PCA75', 'mot_FC_PCA75', 'rel_FC_PCA75', 'soc_FC_PCA75', 'wm_FC_PCA75'],
                             set6 = ['emo', 'gam', 'lan', 'mot', 'rel', 'soc', 'wm', 'cort', 'subc', 'surf', 'rest_PCA75', 'VolBrain'],
                             set7 = ['gam_FC_PCA75', 'lan_FC_PCA75', 'mot_FC_PCA75', 'rel_FC_PCA75', 'soc_FC_PCA75', 'wm_FC_PCA75', 'cort', 'subc', 'surf', 'rest_PCA75', 'VolBrain'],
                             set8 = ['gam_FC_PCA75', 'lan_FC_PCA75', 'mot_FC_PCA75', 'rel_FC_PCA75', 'soc_FC_PCA75', 'wm_FC_PCA75', 'rest_PCA75'])

def get_moda_stacks(dataset_name : str, set_name : str):
        """
        Convenice function to get list of layer2 modalites relating to given set number

        Args:
            dataset_name (str): dataset name for target modalities
            set_name (str): set name for layer2, e.g set1 

        Returns:
            _type_: _description_
        """
        
        if dataset_name == "hcp_aging":
                return hcp_aging_moda_stack_dict[set_name]

        if dataset_name == "dud_study":
                return dud_study_moda_stack_dict[set_name]
        
        if dataset_name == "hcp_ya":
                return hcp_ya_moda_stack_dict[set_name]


if __name__ == "__main__":
        
        xgb_dict = hyper_param_dict["xgb"]
        
        count = 1
        
        for v in xgb_dict.values():
                print(v)
                count *= len(v)
                print(count)
        print(count)
