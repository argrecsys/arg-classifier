# -*- coding: utf-8 -*-
"""
    Created by: Andrés Segura-Tinoco
    Version: 1.2.3
    Created on: Aug 27, 2021
    Updated on: Mar 24, 2023
    Description: Main class of the argument classifier.
"""

# Import Custom libraries
from util import files as ufl
import ml.engine as mle
import ml.logging as mll
from ml.constant import TaskType

# Import Python base libraries
import time
import json
from datetime import datetime

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
        if type(v) is bool:
            ds_name += str(int(v))
    
    return ds_name

# Return the target label from the current task
def get_target_label(task_name:str) -> str:
    target_label = ""
    if task_name == TaskType.ARG_DETECTION.value:
        target_label = "sent_label1"
    elif task_name == TaskType.ARG_CLASSIFICATION.value:
        target_label = "sent_label2"
    elif task_name == TaskType.REL_CLASSIFICATION.value:
        target_label = "sent_label3"
    return target_label

# Save error analysis
def save_error_ids(error_ids, X_test):
    
    for k, v in error_ids.items():
        print(k, ":", v)
        #for rid in v:
        #    print(rid, X_test[rid])

# Save model metrics
def save_metrics(task_type:str, dataset_name:str, configuration:str, pipeline_setup:dict, params:dict, metrics:tuple, elapsed_time:float):
    result = []
    if metrics:
        result = [task_type, dataset_name, configuration, json.dumps(pipeline_setup), json.dumps(params), *metrics, elapsed_time, datetime.now()]
    return result

# Save model results
def save_results(result_folder:str, data:list, ml_ngx:mle.MLEngine) -> int:
    filepath = result_folder + "metrics.csv"
    model_id = ml_ngx.get_next_model_id(filepath)
    header = ["id", "task", "dataset", "configuration", "pipeline", "params", "accuracy", "precision", "recall", "f1-score", "roc-score", "elapsed_time", "datestamp"]
    data = [[model_id] + data]
    result = ufl.save_csv_data(filepath, header, data, mode="a")
    
    if not result:
        model_id = 0
    return model_id

# Create a valid and descriptive model file path
def create_model_filename(folder_path:str, model_id:str, ml_algo:str) -> str:
    model_ext = "joblib"
    file_path = folder_path + "model-" + str(model_id) + "-" + ml_algo.replace(" ", "-") + "." + model_ext
    return file_path

# Start application
def start_app(logger:mll.MLLog, app_setup:dict):
    tasks = app_setup["tasks"]
    
    for task in tasks:
        start_time = time.time()
        logger.log_info("\n>> Scenario begins")
    
        # 0. Program variables
        feat_setup = app_setup["features"]
        pipeline_setup = app_setup["pipeline"]
        train_setup = app_setup["train"]
        create_dataset = app_setup["create_dataset"]
        data_folder = app_setup["data_folder"]
        language = app_setup["language"]
        model_folder = app_setup["model_folder"]
        result_folder = app_setup["result_folder"]
        dr_algo = pipeline_setup["dim_red_algo"]
        ml_algo = pipeline_setup["ml_algo"]
        model_state = train_setup["model_state"]
        y_label = get_target_label(task)
        logger.log_info("- %s (%s - %s):" % (task.title(), ml_algo, dr_algo))
        
        # 1. Machine Learning engine object
        ml_ngx = mle.MLEngine(language=language, task_type=task, logger=logger)
        
        # 2. Read dataset
        dataset, label_dict = ml_ngx.create_dataset(data_folder, y_label, create_dataset, feat_setup)
        model_classes = [*label_dict.values()]
        
        # 3. Split dataset
        X_train, X_test, y_train, y_test = ml_ngx.split_dataset(dataset, train_setup)
        
        # 4. Create or fit model pipeline
        if train_setup["hp_tuning"]:
            clf, params = ml_ngx.create_and_fit_model(pipeline_setup, X_train, y_train, model_classes, model_state, train_setup)
        else:
            clf, params = ml_ngx.create_and_train_model(pipeline_setup, X_train, y_train, model_classes, model_state)
        
        # 5. Test model
        metrics_test = ml_ngx.test_model(clf, X_test, y_test, model_classes)
        elapsed_time = (time.time() - start_time)
        
        # 6. Error analysis
        error_ids = ml_ngx.get_mislabeled_records()
        save_error_ids(error_ids, X_test)
        
        # 7. Save model params and results
        dataset_name = get_curr_dataset_name(feat_setup)
        results = save_metrics(task, dataset_name, "test", pipeline_setup, params, metrics_test, elapsed_time)
        model_id = save_results(result_folder, results, ml_ngx)
        
        # 8. Create final model and save it
        if model_id > 0:
            filepath = create_model_filename(model_folder, model_id, ml_algo)
            fnl_clf = ml_ngx.create_and_save_model(filepath, dataset, pipeline_setup, model_classes, model_state)
            
            #  9. Use model (make predictions)
            pass
    
        logger.log_info(">> Scenario ends")
        logger.log_info("- Elapsed time: %s seconds" % (time.time() - start_time))

#####################
### START PROGRAM ###
#####################
from itertools import product

if __name__ == "__main__":
    logger = mll.MLLog(verbose=True)
    logger.log_info("\n>> START PROGRAM")
    app_setup = read_app_setup()
    
    if len(app_setup):
        start_app(logger, app_setup)
    else:
        logger.log_error(">> ERROR - The application configuration could not be read.")
    
    logger.log_info(">> END PROGRAM")
    logger = None
#####################
#### END PROGRAM ####
#####################
