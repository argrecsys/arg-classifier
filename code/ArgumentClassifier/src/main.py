# -*- coding: utf-8 -*-
"""
    Created by: Andres Segura Tinoco
    Version: 0.4.0
    Created on: Aug 27, 2021
    Updated on: Oct 18, 2021
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

# Save model result
def save_results(result_folder:str, data:list) -> bool:
    filepath = result_folder + "metrics.csv"
    header = ["dataset", "configuration", "method", "accuracy", "precision", "recall", "f1-score", "roc-score", "datestamp"]
    result = cul.save_append_csv_data(filepath, header, data)
    return result

# Start application
def start_app():
    app_setup = read_app_setup()
    
    if len(app_setup):
        
        # 1. Program variables
        ml_algo = "gb"
        data_setup = app_setup["data"]
        model_state = app_setup["model_state"]
        model_folder = app_setup["model_folder"]
        output_folder = app_setup["output_folder"]
        result_folder = app_setup["result_folder"]
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
        metrics_val = ml_ngx.validate_model(clf, X_train, y_train)
        
        # 6. Test model
        metrics_test = ml_ngx.test_model(clf, X_test, y_test)
        
        # 7. Create and save model
        ml_ngx.create_save_model(model_folder, ml_algo, dataset, model_state)
        
        # 8. Save model params and results
        results = []
        results.append(["dataset 1", "validation", ml_algo, *metrics_val, datetime.now()])
        results.append(["dataset 1", "test", ml_algo, *metrics_test, datetime.now()])
        save_results(result_folder, results)
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
