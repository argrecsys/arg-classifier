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
import ml.engine as eng

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
        ml_algo = "nb"
        data_setup = app_setup["data"]
        model_state = app_setup["model_state"]
        model_folder = app_setup["model_folder"]
        output_folder = app_setup["output_folder"]
        perc_test = app_setup["perc_test"]
        task_type = app_setup["task"]
        y_label = app_setup["y_label"]
        ml_ngx = eng.MLEngine(task_type=task_type, verbose=True)
        
        # 2. Read dataset
        dataset, label_dict = ml_ngx.create_dataset(output_folder, y_label, data_setup)
        
        # 3. Split dataset
        X_train, X_test, y_train, y_test = ml_ngx.split_dataset(dataset,perc_test, model_state)
        
        # 4. Train model
        clf = ml_ngx.create_model(ml_algo, X_train, y_train, model_state)
        
        # 5. Validate model - Estimating model performance
        ml_ngx.validate_model(clf, X_train, y_train)
        
        # 6. Test model
        ml_ngx.test_model(clf, X_test, y_test)
        
        # 7. Create and save model
        ml_ngx.create_save_model(model_folder, ml_algo, dataset, model_state)
        
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
