"""
This file is used for setting params that will be used across all runs.
"""

# this is the run name that should be given to all layer1 istances.
# this saves time in organising runs after updating training scripts
run_name = "sep_2023_rerun_v5"

# dict of params that should be passed to all layer1 job instances
layer1_params_dict = {
                     "skip_existing": False,

}

# dict of params that should be passed to all layer2 job instances
layer2_params_dict ={
                     "skip_existing": False,

}
