from params import get_all_modas
from regressors import fit_model_layer1
from pathlib import Path
import sys
from train_params import run_name, layer1_params_dict
from utils import get_base_path

if __name__ == "__main__":
    
    dataset_name = "hcp_aging"
    
    base_path= get_base_path()
    
    base_out_path = base_path / run_name / dataset_name
    
    array_job = False
    
    if len(sys.argv) > 1:
        arg_num = int(sys.argv[1])
        array_job = True
    
    
    
    regs = ["eNet", "rf", "xgb", 'svr']
    
    folds = [f"Fold_{i}" for i in range(5)]
    
    modas = get_all_modas(dataset_name=dataset_name) ### need to implement this
    
    targets = ["totalIQ"]
    
    args = []
    
    for reg in regs: ## This needs updating!!
        for fold in folds:
            for moda in modas:
                for target_name in targets:
                    args.append({"dataset_name":dataset_name, "target_name":target_name, "reg":reg,"moda":moda, "fold":fold, "base_out_path":base_out_path, **layer1_params_dict})
            
    
    
    if array_job:
        print(f"executing {arg_num} of {len(args)}")          
        arg = args[arg_num]
        print(arg)
        fit_model_layer1(**arg)
    else:
        print(f"{len(args)}")
        for arg in args:
            fit_model_layer1(**arg)
    
    