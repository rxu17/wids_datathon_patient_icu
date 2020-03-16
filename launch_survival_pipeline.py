# -*- coding: utf-8 -*-
'''
Description: Used to transform icu health data
Contents:
Arguments:
How To Use: python launch_survival_pipeline.py 
Contributors: rxu17
'''

import re
import time
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as pyplot
import seaborn as sb
import yaml
from getpass import getuser


def get_pipeline_process():
    steps = {1: "data_intake",
             2: "data_prep",
             3: "modeling",
             4: "model_evaluation",
             5: "model_deployment"}


def get_current_repo():
    ''' 
    Returns the repo location for the code that is currently running.
    '''
    import __main__
    try:
        this_dir = os.path.realpath(__main__.__file__).strip(".py")
    except Exception:
        this_dir = os.getcwd()
        assert '/wids_datathon_patient_survival' in this_dir, \
            "ERROR: code run interactively must be run from a repo sub-directory"
    repo_len = len("/wids_datathon_patient_survival") + 1
    end_repo_name = this_dir.find("/wids_datathon_patient_survival")+repo_len
    code_repo = this_dir[:end_repo_name].rstrip(
        '/')  # slice and remove trailing slash
    return(code_repo)


def get_path(main_process = None, step = None):
    ''' Gets the full filepath for a given process name and step
        
        Args: 
            main_process - str, see survival_paths.yaml for possible 
                    values, process names
            step - str, see survival_paths.yaml for possible 
                    values, step names
    '''
    path_file = get_current_repo() + "/survival_paths.yaml"
    with open(path_file) as data_file:
        parameter_dict = yaml.load(data_file)
    if main_process not in list(parameter_dict.keys()):
        raise LookupError("Could not find specified main process, "
                          "{}, in list of parameters".format(main_process))
    if step is None:
        pass
    if step not in list(parameter_dict[main_process].keys()):
        raise LookupError("Could not find specified step, "
                          "{}, in list of parameters".format(step))
    return(parameter_dict[main_process][step])


def launch(process_ids, remove_outliers, impute_missing):
    '''

    '''
    #cmd = ' '.join(["bash", shell_path, self.script])
    pp = get_pipeline_process()
    for process_id in process_ids:
        if not(remove_outliers):
            pass
        if not(impute_missing):
            pass
        script = get_path(pp[process_id].keys())
        cmd = ['python ' + script]
        subprocess.call(cmd, shell = False)


def get_args():
    # Parse arguments
    parser = argparse.ArgumentParser(
        description='Run specified processes')
    parser.add_argument('-mp', '--main_process_ids', type=int,
                        default=[1, 2, 3, 4, 5],
                        nargs='*',
                        help=('List of main processes you wish to run'))
    parser.add_argument('-reout', '--remove_outliers', type=utils.str2bool,
                        default=True,
                        nargs='?',
                        help=('Run outlier removal process'))
    parser.add_argument('-imp', '--impute_missing', type=utils.str2bool,
                        default=True,
                        nargs='?',
                        help=('Run imputation process on missing data'))

def main():
    args = get_args()
    launch(args.main_process_ids, args.remove_outliers, args.impute_missing)


if __name__ == "__main__":
    main()
