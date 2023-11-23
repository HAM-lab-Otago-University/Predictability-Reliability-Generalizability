from params import hcp_aging_moda_stack_dict
from regressors import fit_model_layer2
from pathlib import Path
import sys
from train_params import run_name, layer2_params_dict
from utils import get_base_path

if __name__ == "__main__":
    
    dataset_name = "hcp_aging"
    
    base_path= get_base_path()
    
    base_out_path = base_path / run_name / dataset_name
    
    array_job = False
    
    if len(sys.argv) > 1:
        arg_num = int(sys.argv[1])
        array_job = True
    
    
    fir_regs = ["eNet", "rf", "xgb", 'svr']
    sec_regs = ["eNet", "rf", "xgb", 'svr']
    
    folds = [f"Fold_{i}" for i in range(5)]
    
    sets = hcp_aging_moda_stack_dict.keys() 
    
    targets = ["totalIQ"]
    
    args = []
    
    for fir_reg in fir_regs:
        for sec_reg in sec_regs:
            for fold in folds:
                for set_name in sets:
                    for target_name in targets:
                        args.append({"dataset_name":dataset_name, "target_name":target_name, "fir_reg":fir_reg,"sec_reg":sec_reg, "set_name":set_name, "fold":fold, "base_out_path":base_out_path, **layer2_params_dict})
            
    
    
    if array_job:
        print(f"executing {arg_num} of {len(args)}")          
        arg = args[arg_num]
        print(arg)
        fit_model_layer2(**arg)
    else:
        print(dataset_name)
        print(f"{len(args)}")
        for arg in args:
            fit_model_layer2(**arg)