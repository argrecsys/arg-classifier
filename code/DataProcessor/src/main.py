# -*- coding: utf-8 -*-
"""
    Created by: Andrés Segura-Tinoco
    Version: 0.10.0
    Created on: May 11, 2022
    Updated on: Mar 19, 2023
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
def data_preprocessing(language:str, folder_path:str, anno_tool:str) -> bool:
    result = False
    
    if anno_tool == "argael":
        
        # 1. Read raw documents (from JSON files)
        filepath = folder_path + "proposals"
        proposals = fl.get_dict_from_folder(filepath, "jsonl")
        print(" - Total number of proposals:", len(proposals))
        
        # 2. Read annotation dataset (from CSV files)
        filepath = folder_path + "annotations"
        set_annotations = fl.get_dict_from_folder(filepath, "csv")
        
        # 3. Preprocessing annotations
        annotations = {}
        for key, value in set_annotations.items():
            tokens = key.split("_")
            if len(tokens) == 3:
                file_name = tokens[0]
                file_type = tokens[2]
                doc = annotations.get(file_name, {})
                doc[file_type] = value
                annotations[file_name] = doc
        print(" - Total number of annotations:", len(annotations))
        
        # 4. Processing dataset
        df = dp.pre_process_argael_dataset(proposals, annotations, language)
        print(df)
        
    elif anno_tool == "prodigy":
        
        # 1. Read annotation dataset (from JSONL file)
        filepath = folder_path + "annotations.jsonl"
        annotations = fl.get_list_from_jsonl(filepath)
        print(" - Total number of annotations:", len(annotations))
        
        # 2. Processing dataset
        df = dp.pre_process_prodigy_dataset(annotations, language)
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
        anno_tool = app_setup["anno_tool"]
        data_folder = app_setup["data_folder"]
        language = app_setup["language"]
        task = app_setup["task"]
        
        # Task to be exeuted
        if task == "preprocessing":
            result = data_preprocessing(language, data_folder, anno_tool)
            
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
    print(">> START DATA PROCESSOR:", str(datetime.now()))
    start_app()    
    print(">> END DATA PROCESSOR:", str(datetime.now()))
#####################
#### END PROGRAM ####
#####################
