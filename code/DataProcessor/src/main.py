# -*- coding: utf-8 -*-
"""
    Created by: Andrés Segura-Tinoco
    Version: 0.3.0
    Created on: May 11, 2022
    Updated on: May 13, 2022
    Description: Main module.
"""

# Import Custom libraries
from util import files as fl
import data_process as dp

# Import Python base libraries
from datetime import datetime

######################
### CORE FUNCTIONS ###
######################

# Read data configuration
def read_app_setup() -> dict:
    filepath = "../config/config.json"
    setup = fl.get_dict_from_json(filepath)
    return setup

# Data pre-processing module
def data_preprocessing(language:str, folder_path:str) -> bool:
    result = False
    
    # 1. Read JSON input dataset
    in_filepath = folder_path + "annotations.jsonl"
    json_dataset = fl.get_list_from_jsonl(in_filepath)
    print(" - Total number of records read:", len(json_dataset))
    
    # 2. Processing dataset
    df = dp.pre_process_dataset(json_dataset, language)
    print(df)
    
    # 3. Save dataframe to CSV file
    out_filepath = folder_path + "propositions.csv"
    result = fl.save_df_to_csv(df, out_filepath)
    print(" - Total number of records saved:", len(df))
    
    return result

# Data post-processing module
def data_postprocessing(language:str, folder_path:str) -> bool:
    result = False
    
    return result

# Start application
def start_app():
    app_setup = read_app_setup()
    
    if len(app_setup):
        result = False
        
        # 0. Program variables
        data_folder = app_setup["data_folder"]
        language = app_setup["language"]
        task = app_setup["task"]
        
        # Task to be exeuted
        if task == "preprocessing":
            result = data_preprocessing(language, data_folder)
            
        elif task == "postprocessing":
            result = data_postprocessing(language, data_folder)
        
        if result:
            print(" - Successful transformation")
        
    else:
        print(">> ERROR - The application configuration could not be read.", str(datetime.now()))

#####################
### START PROGRAM ###
#####################
if __name__ == "__main__":
    print('>> START DATA PROCESSOR:', str(datetime.now()))
    start_app()    
    print(">> END DATA PROCESSOR:", str(datetime.now()))
#####################
#### END PROGRAM ####
#####################
