# -*- coding: utf-8 -*-
"""
    Created by: Andres Segura Tinoco
    Version: 0.3.0
    Created on: Aug 27, 2021
    Updated on: Oct 08, 2021
    Description: Main class of the argument classifier.
"""

# Import Custom libraries
import util_lib as cul
import ml_engine as eng

# Import Python base libraries
from datetime import datetime

######################
### CORE FUNCTIONS ###
######################

# Read data configuration
def read_app_setup() -> dict:
    filepath = "../config/config.json"
    setup = cul.get_dict_from_json(filepath)
    return setup

# Start application
def start_app():
    app_setup = read_app_setup()
    
    if len(app_setup):
        
        # 1. Program variables
        force_create_dataset = app_setup["force_create_dataset"]
        data_setup = app_setup["data"]
        model_state = app_setup["model_state"]
        output_path = app_setup["output_path"]
        perc_test = app_setup["perc_test"]
        task_type = app_setup["task"]
        y_label = app_setup["y_label"]
        engine = eng.MLEngine(task_type=task_type, verbose=True)
        
        # 2. Read dataset
        dataset, label_dict = engine.create_dataset(output_path, force_create_dataset, y_label, data_setup)
        
        # 3. Split dataset
        X_train, X_test, y_train, y_test = engine.split_dataset(dataset,perc_test, model_state)
        
        # 4. Train model
        clf = engine.create_model("nb", X_train, y_train, model_state)
        
        # 5. Test model
        engine.test_model(clf, X_train, y_train)
        
    else:
        print(">> ERROR - The application configuration could not be read.", str(datetime.now()))

#####################
### START PROGRAM ###
#####################
if __name__ == "__main__":
    print('>> START PROGRAM:', str(datetime.now()))
    start_app()    
    print(">> END PROGRAM:", str(datetime.now()))
#####################
#### END PROGRAM ####
#####################
