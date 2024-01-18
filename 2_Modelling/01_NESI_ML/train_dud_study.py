from params import get_all_modas
from regressors import fit_model_layer1
from pathlib import Path
import sys
from train_params import run_name, layer1_params_dict
from utils import get_base_path

if __name__ == "__main__":
    
    dataset_name = "dud_study" # declaring dataset name
    
    base_path= get_base_path()
    
    base_out_path = base_path / run_name / dataset_name # setting base out path for datset and run name
    
    array_job = False
    
    # loading command line argument, will be the SLURM_ARRAY_TASK_ID
    if len(sys.argv) > 1:
        arg_num = int(sys.argv[1])
        array_job = True
    
    
    regs = ["eNet", "rf", "xgb", 'svr'] # declaring all regressors to train on
    
    folds = [f"Fold_{i}" for i in range(7)] # all folds for dud_study datset
    
    modas = get_all_modas(dataset_name=dataset_name) # loading all moda names for dataset
    
    # declaring all targets for datset
    targets = ["IQ45_adj", "IQ45_raw", "IQch_adj", "IQch_raw", "IQres_adj", "IQres_raw"]
    
    args = []
    
    # creating list of different job arguments needed for fitting the whole array job
    for reg in regs: 
        for fold in folds:
            for moda in modas:
                for target_name in targets:
                    args.append({"dataset_name":dataset_name, "target_name":target_name, "reg":reg,"moda":moda, "fold":fold, "base_out_path":base_out_path, **layer1_params_dict})
    
    if array_job:
        # if array job on nesi loading the singular set of arguments for this array task by using
        # given SLURM_ARRAY_TASK_ID to index into list of arguments
        # array job is executed in embarrasingly parallel style
        print(f"executing {arg_num} of {len(args)}")          
        arg = args[arg_num]
        print(arg)
        fit_model_layer1(**arg)
    else:
        # if not an array job running each argument consecutively
        # this is for easier use debugging locally
        print(f"{len(args)}")
        for arg in args:
            fit_model_layer1(**arg)
    
    
