# -*- coding: utf-8 -*-
"""
    Created by: Andres Segura Tinoco
    Version: 0.5.5
    Created on: Aug 27, 2021
    Updated on: Oct 25, 2021
    Description: Main class of the argument classifier.
"""

# Import Custom libraries
import util_lib as cul
import ml.engine as mle
from ml.constant import ModelType

# Import Python base libraries
import json
from datetime import datetime

######################
### CORE FUNCTIONS ###
######################

# Read data configuration
def read_app_setup() -> dict:
    filepath = "../config/config.json"
    setup = cul.get_dict_from_json(filepath)
    return setup

# Save error analysis
def save_error_ids(error_ids, X_test):
    
    for k, v in error_ids.items():
        print(k, ':', v)
        #for rid in v:
        #    print(rid, X_test.loc[rid])

# Save model result
def save_results(result_folder:str, data:list) -> int:
    filepath = result_folder + "metrics.csv"
    model_id = cul.get_max_value_from_csv_file(filepath, "id") + 1
    header = ["id", "dataset", "configuration", "method", "params", "accuracy", "precision", "recall", "f1-score", "roc-score", "datestamp"]
    data = [[model_id] + row for row in data]
    result = cul.save_append_csv_data(filepath, header, data)
    
    if not result:
        model_id = 0
    return model_id

# Start application
def start_app():
    app_setup = read_app_setup()
    
    if len(app_setup):
        
        # 0. Program variables
        ml_algo = ModelType.GRADIENT_BOOSTING.value
        data_setup = app_setup["data"]
        language = app_setup["language"]
        model_state = app_setup["model_state"]
        model_folder = app_setup["model_folder"]
        output_folder = app_setup["output_folder"]
        result_folder = app_setup["result_folder"]
        perc_test = app_setup["perc_test"]
        task_type = app_setup["task"]
        y_label = app_setup["y_label"]
        
        # 1. Machine Learning engine object
        ml_ngx = mle.MLEngine(language=language, task_type=task_type, verbose=True)
        
        # 2. Read dataset
        dataset, label_dict = ml_ngx.create_dataset(output_folder, y_label, data_setup)
        
        # 3. Split dataset
        X_train, X_test, y_train, y_test = ml_ngx.split_dataset(dataset,perc_test, model_state)
        
        # 4. Train model
        clf, params = ml_ngx.create_model(ml_algo, X_train, y_train, model_state)
        # clf, params = ml_ngx.create_and_fit_model(ml_algo, X_train, y_train, model_state)
        
        # 5. Validate model - Estimating model performance
        metrics_val = ml_ngx.validate_model(clf, X_train, y_train)
        
        # 6. Test model
        metrics_test = ml_ngx.test_model(clf, X_test, y_test)
        
        # 7. Error analysis
        error_ids = ml_ngx.get_mislabeled_records()
        save_error_ids(error_ids, X_test)
        
        # 8. Save model params and results
        results = []
        results.append(["dataset 1", "validation", ml_algo, json.dumps(params), *metrics_val, datetime.now()])
        results.append(["dataset 1", "test", ml_algo, json.dumps(params), *metrics_test, datetime.now()])
        model_id = save_results(result_folder, results)
        
        # 9. Create and save model
        if model_id > 0:
            fnl_clf = ml_ngx.create_save_model(model_folder, model_id, ml_algo, dataset, model_state)
        
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
