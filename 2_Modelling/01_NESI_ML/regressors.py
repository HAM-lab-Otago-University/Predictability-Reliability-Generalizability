import xgboost as xgb
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import ElasticNet
from sklearn.model_selection import GridSearchCV
from params import hyper_param_dict, single_hyper_param_dict
from pathlib import Path
from utils import load_data, load_y, dd, default_to_regular, load_data_layer2
import pickle
import pandas as pd


def get_params(reg_name : str):
    """
    Convenience function to get hyper params relating to a regressor
    """
    return hyper_param_dict[reg_name]


def get_single_params(reg_name : str):
    return single_hyper_param_dict[reg_name]


def get_reg(reg_name : str):
    """
    Function will map a reggressor name to a class

    Args:
        reg_name (str): string relating to a valid regressor type

    Returns:
        regressor : regressor class compatible with sklearn gridsearchcv class
    """
    reg_dict = {"xgb":xgb.XGBRegressor,
                "eNet":ElasticNet,
                "rf":RandomForestRegressor,
                "svr": SVR,}
    return reg_dict[reg_name]()


def get_search(reg_name : str):
    """
    function will return an initialized GridSearchCV class with regressor and
    hyper param grid relating to given regressor string

    Args:
        reg_name (str): name of regressor to initialize search grid for 

    Returns:
        GridSearchCV : initialized GridSearchCV
    """
    params = get_params(reg_name)
    reg = get_reg(reg_name)
    
    search = GridSearchCV(reg, params, cv=5, n_jobs = -1, verbose = 0)
    
    return search


def get_single_search(reg_name : str):
    params = get_single_params(reg_name)
    reg = get_reg(reg_name)
    
    search = GridSearchCV(reg, params, cv=5, n_jobs = -1, verbose = 0)
    
    return search


def fit_model_layer1(dataset_name : str, target_name :str, reg : str, moda : str, fold : str, base_out_path : Path, skip_existing=True):
    """
    This function will can be mapped to a list of arguements relating to the dataset, target variables and regressor to
    complete hyper parameter tuning using a existing parameter grid in params.py and output the predictions from 
    the final model to the results path. The predictions can then be used as input for layer2 training.

    Args:
        dataset_name (str): dataset string for target dataset, valid options are : {"dud_study", "hcp_aging", "hcp_ya"} 
        target_name (str): target variable. must relate to the given dataset. No validity checking
        reg (str): name of regressor to fit. must be one of {rf, eNet, xgb, svr}
        moda (str): name of data modality to use as predictor in training a regressor
        fold (str): name of data fold to use as prediction e.g Fold_0
        base_out_path (Path): base path for output. results will go to base_out_path/"results"/target_name/"layer1"/reg/moda/fold
        skip_existing (bool, optional): Whether to skip this job if there is already a results outfile. Defaults to True.
    """
    
    results_out_path = base_out_path/"results"/target_name/"layer1"/reg/moda/fold
    
    for split in ['train1', 'test']: # checking if files are existing and skipping job if so
        
        results_out_file = results_out_path/f"{split}_results.csv"
        
        if results_out_file.exists() and skip_existing: # skip if file already exists
            print(f"{results_out_file} skipping as already exists")
            return
        
    model_out_path = base_out_path/"models"/target_name/"layer1"/reg/moda/fold
    model_out_file = model_out_path/f"train1_model.pkl"
    
    moda_data = load_data(dataset_name=dataset_name, modas=[moda], folds=[fold]) # loading modality data 
    
    target_data = load_y(dataset_name=dataset_name, target_name=target_name, fold=fold) # loading target data
    
    # indexing into moda data dict and target dict to retreive X and y arrays for fitting model
    X_train = moda_data[moda][fold]['train1']
    y_train = target_data[fold]["train1"]
    X_test = moda_data[moda][fold]['test']
        
    search = get_search(reg) # getting gridsearch instance
    search.fit(X_train,y_train) # fitting gridsearch
    
    train_preds = search.predict(X_train) # getting predictions from best gridsearch model
    test_preds = search.predict(X_test)
    
    Path.mkdir(results_out_path, exist_ok=True, parents=True) # making output directories
    Path.mkdir(model_out_path, exist_ok=True, parents=True)
    
    train_preds_df = pd.DataFrame({"results":train_preds}) # converting results into dataframes
    test_preds_df = pd.DataFrame({"results":test_preds})
    
    train_preds_df.to_csv(results_out_path/f"train1_results.csv") # saving dataframes as csv
    test_preds_df.to_csv(results_out_path/f"test_results.csv")
        
    with open(model_out_file, "wb") as f: # saving gridsearch model as pickle
        pickle.dump(search, f)
        
    print(f"{dataset_name} {target_name} {reg}   {moda}  {fold} finished")
    

def fit_model_layer2(dataset_name : str, target_name :str, fir_reg : str, sec_reg : str, set_name : str, fold : str, base_out_path : Path, skip_existing=True):
    
    results_out_path = base_out_path/"results"/target_name/"layer2"/fir_reg/sec_reg/set_name/fold
    
    for split in ['train1', 'test']:
        
        results_out_file = results_out_path/f"{split}_results.csv"
        
        if results_out_file.exists() and skip_existing: # skip if file already exists
            print(f"{results_out_file} skipping as already exists")
            return
        
    model_out_path = base_out_path/"models"/target_name/"layer2"/fir_reg/sec_reg/set_name/fold
    model_out_file = model_out_path/f"train1_model.pkl"
    stand_model_out_file = model_out_path/f"stand1_model.pkl"
    
    layer1_results = load_data_layer2(set_name=set_name, reg=fir_reg, dataset_name=dataset_name, target_name=target_name, folds=[fold])
    target_data = load_y(dataset_name=dataset_name, target_name=target_name, fold=fold)

    X_train = layer1_results[fold]['train1']
    y_train = target_data[fold]["train1"]
    X_test = layer1_results[fold]['test']

    #Standartize X_train
    std_model = StandardScaler()
    std_model.fit(X_train)
    X_train = std_model.transform(X_train)
    X_test = std_model.transform(X_test)

    search = get_search(sec_reg)
    search.fit(X_train,y_train)
    
    train_preds = search.predict(X_train)
    test_preds = search.predict(X_test)
    
    Path.mkdir(results_out_path, exist_ok=True, parents=True)
    Path.mkdir(model_out_path, exist_ok=True, parents=True)
    
    train_preds_df = pd.DataFrame({"results":train_preds})
    test_preds_df = pd.DataFrame({"results":test_preds})
    
    train_preds_df.to_csv(results_out_path/f"train1_results.csv")
    test_preds_df.to_csv(results_out_path/f"test_results.csv")
        
    with open(model_out_file, "wb") as f:
        pickle.dump(search, f)

    with open(stand_model_out_file, "wb") as g:
        pickle.dump(std_model, g)

    print(f"{dataset_name} {target_name} {fir_reg} {sec_reg}  {set_name}  {fold} finished")
    
