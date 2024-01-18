from collections import defaultdict
from pathlib import Path
import pandas as pd
import numpy as np
from train_params import run_name
from params import get_all_modas, get_moda_stacks

def get_base_path():
    """
    This function will return the base path. The base path always maps to the globus endpoint
    /media/hcs-sci-psy-narun/Nesi/Bryn
    or
    the scratch-nobackup location on the high performance computing (hpc) cluster
    /nesi/nobackup/uoo03493/Bryn
    
    This function is to make paths agnostic to file system.
    
    Returns:
        Path : Base path for project data on current file system
    """
    nesi_path = Path("/hpc/scratch/your_account")
    
    if nesi_path.exists():
        return nesi_path
    else:
        return Path("/media/username")
    
    
def dd(): # function for recursive default dict
    return defaultdict(dd)


def default_to_regular(d): # converting recursive default dict to normal dict
    if isinstance(d, defaultdict):
        d = {k: default_to_regular(v) for k, v in d.items()}
    return d

def load_y(dataset_name : str, target_name : str, splits=None, fold=None,):
    """
    This function will load target data for a given dataset, target name, data split and fold
    
    Args:
        dataset_name (str): dataset string for target dataset, valid options are : {"dud_study", "hcp_aging", "hcp_ya"} 
        target_name (str): target variable. must relate to the given dataset. No validity checking
        splits (list, optional): List of data splits to load. Defaults to ['train1, 'test'].
        fold (string, optional): string name of fold to load e.g Fold_0. If none is provided all folds relating to given dataset are loaded

    Raises:
        ValueError: if dataset_name is invalid

    Returns:
        dict : returns dictonary of loaded target data in format [fold][split]: np.array of target values
    """
    
    if dataset_name not in {"hcp_aging", "dud_study", "hcp_ya"}:
        raise ValueError(f"{dataset_name} is invalid dataset name")
    
    if not splits:
        splits = ["train1", "test"]

    
    base_path = get_base_path() # getting base path
    
    path_dict = {"hcp_aging":base_path / "data/HCPAging_v5/cognition" / target_name,
                "dud_study":base_path / "data/Dunedin_study_v5/main_set" / target_name,
                "hcp_ya":base_path / "data/HCP_YA_v5/main_set" / target_name}
    
    target_path = path_dict[dataset_name] # getting relative target path for given dataset

    out_dict = dd()
    
    if not fold: # if no folds provided loading all folds for given dataset
        
        folds_dict = {"hcp_aging":[f"Fold_{i}" for i in range(5)],
                    "dud_study": [f"Fold_{i}" for i in range(7)],
                    "hcp_ya":[f"Fold_{i}" for i in range(8)]}
        
        folds = folds_dict[dataset_name]     
        
        for fold in folds:
            for split in splits: # loading target data into dict
                out_dict[fold][split] = pd.read_csv(target_path/fold/f"target_y_{split}.csv", header=None,skiprows=[0]).iloc[:,1].values
    
    else:
        for split in splits: # loading target data into dict
            out_dict[fold][split] = pd.read_csv(target_path/fold/f"target_y_{split}.csv", header=None,skiprows=[0]).iloc[:,1].values

    return default_to_regular(out_dict) # coverting recursive default dict to dict before returning


def load_data(modas, dataset_name : str, splits=None, folds=None,):
    """
    Loading data relating to list of modalities and dataset.

    Args:
        modas (list): list of names of modalities to load
        dataset_name (str): name of dataset to load modality data for
        splits (list, optional): List of data splits to load. Defaults to ['train1, 'test'].
        fold (string, optional): string name of fold to load e.g Fold_0. If none is provided all folds relating to given dataset are loaded

    Raises:
        ValueError: if dataset_name is invalid

    Returns:
        dict : returns dictonary of loaded target data in format [moda][fold][split]: np.array of target values
    """
    
    if dataset_name not in {"hcp_aging", "dud_study", "hcp_ya"}:
        raise ValueError(f"{dataset_name} is invalid dataset name")
    
    if not splits:
        splits = ["train1", "test"]

    
    base_path = get_base_path() # getting base path
    
    path_dict = {"hcp_aging":base_path / "data/HCPAging_v5/cognition" / "ML_modalities",
                "dud_study":base_path / "data/Dunedin_study_v5/main_set" / "ML_modalities",
                "hcp_ya":base_path / "data/HCP_YA_v5/main_set" / "ML_modalities"}
    
    target_path = path_dict[dataset_name] # getting relative path for given dataset

    out_dict = dd() # recursive default dict
    
    if not folds: # if no folds provided loading all folds for given dataset
        
        folds_dict = {"hcp_aging":[f"Fold_{i}" for i in range(5)],
                    "dud_study": [f"Fold_{i}" for i in range(7)],
                    "hcp_ya":[f"Fold_{i}" for i in range(8)]}
        
        folds = folds_dict[dataset_name]
    
    for split in splits:
        for moda in modas:
            for fold in folds: # loading modality data into default dict
                
                # loading data from csv into dataframe. then extract array of values ignoring index column and header row
                out_dict[moda][fold][split] = pd.read_csv(target_path/fold/f"{moda}_{split}.csv", header=None,skiprows=[0]).iloc[:,1:].values 

    return default_to_regular(out_dict) # converting default dict to dict before returning


def load_data_layer2(set_name : str, reg : str, dataset_name : str, target_name : str,splits=None, folds=None,):
    
    
    base_path = get_base_path() / run_name
    
    if dataset_name not in {"hcp_aging", "dud_study", "hcp_ya"}:
        raise ValueError(f"{dataset_name} is invalid dataset name")
    
    modas = get_moda_stacks(dataset_name=dataset_name, set_name=set_name)
    
    if not splits:
        splits = ["train1", "test"]
    
    
    
    if not folds:
        if dataset_name == "hcp_aging":
            folds= [f"Fold_{i}" for i in range(5)]
        
        if dataset_name == "dud_study":
            folds= [f"Fold_{i}" for i in range(7)]
    
    target_path = base_path / dataset_name / "results"/ target_name / "layer1" / reg 
    
    out_dict = dd()
    
    for fold in folds:
        for split in splits:
            split_dict = {moda : pd.read_csv(target_path/moda/fold/f"{split}_results.csv")["results"].values for moda in modas}
            split_df = pd.DataFrame.from_dict(split_dict)
            split_values = split_df.iloc[:,1:].values
            
            out_dict[fold][split] = split_values
        
    return default_to_regular(out_dict)


if __name__ == "__main__":
    dataset_name = "dud_study"
    target_name = "IQ45_adj"
    
    modas = ["brainVol", "cort"]
    
    data = load_data(modas, dataset_name=dataset_name)
    y = load_y(dataset_name=dataset_name, target_name=target_name)
    
    print('asd')
