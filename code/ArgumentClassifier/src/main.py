# -*- coding: utf-8 -*-
"""
    Created by: Andrés Segura-Tinoco
    Version: 0.8.8
    Created on: Aug 27, 2021
    Updated on: May 25, 2022
    Description: Main class of the argument classifier.
"""

# Import Custom libraries
from util import files as ufl
import ml.engine as mle
from ml.constant import ModelType, TaskType

# Import Python base libraries
import json
from datetime import datetime
from itertools import product

######################
### CORE FUNCTIONS ###
######################

# Read data configuration
def read_app_setup() -> dict:
    filepath = "../config/config.json"
    setup = ufl.get_dict_from_json(filepath)
    return setup

# Return current dataset name composed by a coding map
def get_curr_dataset_name(feat_setup:dict) -> str:
    ds_name = "ds_"
    
    for v in feat_setup.values():
        ds_name += str(int(v))
    
    return ds_name

# Save error analysis
def save_error_ids(error_ids, X_test):
    
    for k, v in error_ids.items():
        print(k, ':', v)
        #for rid in v:
        #    print(rid, X_test.loc[rid])

# Save model result
def save_results(result_folder:str, data:list, task:str, ml_ngx:mle.MLEngine) -> int:
    filepath = result_folder + "metrics.csv"
    model_id = ml_ngx.get_next_model_id(filepath)
    header = ["id", "task", "dataset", "configuration", "method", "params", "accuracy", "precision", "recall", "f1-score", "roc-score", "datestamp"]
    data = [[model_id, task] + row for row in data]
    result = ufl.save_csv_data(filepath, header, data, mode="a")
    
    if not result:
        model_id = 0
    return model_id

# Start application
def start_app(task_type:str, ml_algo:str):
    app_setup = read_app_setup()
    
    if len(app_setup):
        
        # 0. Program variables
        feat_setup = app_setup["features"]
        create_dataset = app_setup["create_dataset"]
        cv_k = app_setup["cv_k"]
        data_folder = app_setup["data_folder"]
        language = app_setup["language"]
        model_folder = app_setup["model_folder"]
        model_state = app_setup["model_state"]
        perc_test = app_setup["perc_test"]
        result_folder = app_setup["result_folder"]
        y_label = "sent_label1" if task_type == "detection" else "sent_label2"
        
        # 1. Machine Learning engine object
        ml_ngx = mle.MLEngine(language=language, task_type=task_type, verbose=True)
        
        # 2. Read dataset
        dataset, label_dict = ml_ngx.create_dataset(data_folder, y_label, create_dataset, feat_setup)
        
        # 3. Split dataset
        X_train, X_test, y_train, y_test = ml_ngx.split_dataset(dataset,perc_test, model_state)
        
        # 4. Train or calibrate model
        clf, params = ml_ngx.create_model(ml_algo, X_train, y_train, model_state)
        # clf, params = ml_ngx.create_and_fit_model(ml_algo, X_train, y_train, model_state, cv_k)
        
        # 5. Validate model - Estimating model performance
        metrics_val = ml_ngx.validate_model(clf, X_train, y_train, cv_k)
        
        # 6. Test model
        metrics_test = ml_ngx.test_model(clf, X_test, y_test)
        
        # 7. Error analysis
        error_ids = ml_ngx.get_mislabeled_records()
        save_error_ids(error_ids, X_test)
        
        # 8. Save model params and results
        results = []
        dataset_name = get_curr_dataset_name(feat_setup)
        results.append([dataset_name, "validation", ml_algo, json.dumps(params), *metrics_val, datetime.now()])
        results.append([dataset_name, "test", ml_algo, json.dumps(params), *metrics_test, datetime.now()])
        model_id = save_results(result_folder, results, task_type, ml_ngx)
        
        # 9. Create and save model
        if model_id > 0:
            fnl_clf = ml_ngx.create_save_model(model_folder, model_id, ml_algo, dataset, model_state)
            
            #  10. Make predictions
        
    else:
        print(">> ERROR - The application configuration could not be read.", str(datetime.now()))

#####################
### START PROGRAM ###
#####################
if __name__ == "__main__":
    print('>> START PROGRAM:', str(datetime.now()))
    tasks = [TaskType.DETECTION.value, TaskType.CLASSIFICATION.value]
    algos = [ModelType.NAIVE_BAYES.value, ModelType.GRADIENT_BOOSTING.value]
    for task, algo in list(product(tasks, algos)):
        print("\n>> %s (%s) - %s:" % (task.title(), algo, str(datetime.now())))
        start_app(task, algo)
    print(">> END PROGRAM:", str(datetime.now()))
#####################
#### END PROGRAM ####
#####################
