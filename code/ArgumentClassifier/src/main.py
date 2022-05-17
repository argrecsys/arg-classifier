# -*- coding: utf-8 -*-
"""
    Created by: Andrés Segura-Tinoco
    Version: 0.7.0
    Created on: Aug 27, 2021
    Updated on: May 16, 2022
    Description: Main class of the argument classifier.
"""

# Import Custom libraries
from util import files as ufl
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
    setup = ufl.get_dict_from_json(filepath)
    return setup

# Return current dataset name composed by a coding map
def get_curr_dataset_name(setup:dict) -> str:
    ds_name = "ds"
    
    ds_name += "-0" if setup["remove_stopwords"] else ""
    ds_name += "-1" if setup["punctuation"] else ""
    ds_name += "-2" if setup["unigrams"] else ""
    ds_name += "-3" if setup["bigrams"] else ""
    ds_name += "-4" if setup["trigrams"] else ""
    ds_name += "-5" if setup["word_couples"] else ""
    ds_name += "-6" if setup["adverbs"] else ""
    ds_name += "-7" if setup["verbs"] else ""
    ds_name += "-8" if setup["key_words"] else ""
    ds_name += "-9" if setup["text_stats"] else ""
    
    return ds_name

# Save error analysis
def save_error_ids(error_ids, X_test):
    
    for k, v in error_ids.items():
        print(k, ':', v)
        #for rid in v:
        #    print(rid, X_test.loc[rid])

# Save model result
def save_results(result_folder:str, data:list, ml_ngx:mle.MLEngine) -> int:
    filepath = result_folder + "metrics.csv"
    model_id = ml_ngx.get_next_model_id(filepath)
    header = ["id", "dataset", "configuration", "method", "params", "accuracy", "precision", "recall", "f1-score", "roc-score", "datestamp"]
    data = [[model_id] + row for row in data]
    result = ufl.save_csv_data(filepath, header, data, mode="a")
    
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
        data_folder = app_setup["data_folder"]
        language = app_setup["language"]
        model_state = app_setup["model_state"]
        model_folder = app_setup["model_folder"]
        result_folder = app_setup["result_folder"]
        perc_test = app_setup["perc_test"]
        task_type = app_setup["task"]
        curr_dataset = get_curr_dataset_name(data_setup)
        y_label = app_setup["y_label"]
        
        # 1. Machine Learning engine object
        ml_ngx = mle.MLEngine(language=language, task_type=task_type, verbose=True)
        
        # 2. Read dataset
        dataset, label_dict = ml_ngx.create_dataset(data_folder, y_label, data_setup)
        
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
        results.append([curr_dataset, "validation", ml_algo, json.dumps(params), *metrics_val, datetime.now()])
        results.append([curr_dataset, "test", ml_algo, json.dumps(params), *metrics_test, datetime.now()])
        model_id = save_results(result_folder, results, ml_ngx)
        
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
