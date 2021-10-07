# -*- coding: utf-8 -*-
"""
    Created by: Andres Segura Tinoco
    Version: 0.2.0
    Created on: Aug 27, 2021
    Updated on: Oct 07, 2021
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
    filepath = "config/config.json"
    setup = cul.get_dict_from_json(filepath)
    return setup

#####################
### START PROGRAM ###
#####################
if __name__ == "__main__":
    print('>> START PROGRAM:', str(datetime.now()))
    
    # 0. Read app configuration
    app_setup = read_app_setup()
    
    if len(app_setup):
        
        # 1. Program variables
        output_path = "../../../dataset/"
        task = app_setup["task"]
        data_setup = app_setup["data"]
        perc_test = app_setup["perc_test"]
        model_state = app_setup["model_state"]
        y_label = app_setup["y_label"]
        
        # 2. Read dataset
        dataset, label_dict = eng.create_dataset(output_path, y_label, data_setup)
        filepath = output_path + "dataset.csv"
        dataset.to_csv(filepath, index=False)
        
        # 3. Split dataset
        X_train, X_test, y_train, y_test = eng.split_dataset(dataset, label_dict, perc_test, model_state)
        
        # 4. Train model
        clf = eng.create_model("nb", X_train, y_train)
        
        # 5. Test model
        eng.test_model(clf, X_train, y_train, True)
        
    else:
        print(">> ERROR - The application configuration could not be read.", str(datetime.now()))
        
    print(">> END PROGRAM:", str(datetime.now()))
#####################
#### END PROGRAM ####
#####################
