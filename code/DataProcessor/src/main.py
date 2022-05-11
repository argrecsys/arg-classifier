# -*- coding: utf-8 -*-
"""
    Created by: Andres Segura Tinoco
    Version: 0.1.0
    Created on: May 11, 2022
    Updated on: May 11, 2022
    Description: Input data processing module.
"""

# Import Custom libraries
import util_lib as cul

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

# Read JSON input dataset
def read_input_dataset(folder_path:str) -> dict:
    filepath = folder_path + "annotations.jsonl"
    dataset = cul.get_list_from_jsonl(filepath)
    return dataset

# Processing dataset from JSON to CSV
def process_dataset(in_dataset:list) -> list:
    out_dataset = []
    
    return out_dataset

# Save CSV output dataset
def save_output_dataset(dataset:list, folder_path:str) -> bool:
    result = False
    filepath = folder_path + "input_data.jsonl"
    
    return result

# Start application
def start_app():
    app_setup = read_app_setup()
    
    if len(app_setup):
        
        # 0. Program variables
        language = app_setup["language"]
        data_folder = app_setup["data_folder"]
        
        # 1. Read JSON input dataset
        json_dataset = read_input_dataset(data_folder)
        print(" - Total number of records read:", len(json_dataset))
        
        # 2. Processing dataset
        csv_dataset = process_dataset(json_dataset)
        
        # 3. Save CSV output dataset
        result = save_output_dataset(csv_dataset, data_folder)
        
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
