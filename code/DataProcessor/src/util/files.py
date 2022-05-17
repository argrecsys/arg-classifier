# -*- coding: utf-8 -*-
"""
    Created by: Andrés Segura-Tinoco
    Version: 1.1.0
    Created on: Oct 06, 2021
    Updated on: May 16, 2022
    Description: Files library with utility functions
"""

# Import Python base libraries
import os
import json
import yaml
import pandas as pd

# Read list (of dict) from JSONL (json lines format) file
def get_list_from_jsonl(json_path:str, encoding:str="utf-8") -> list:
    result = []
    
    try:
        json_list = []
        with open(json_path, mode="r", encoding=encoding) as file:
            json_list = list(file)
        
        result = [json.loads(jline) for jline in json_list]
        
    except Exception as e:
        print(e)
        
    return result

# Read list from plain file
def get_list_from_plain_file(file_path:str, encoding:str="utf-8") -> list:
    result = []
    
    try:
        with open(file_path, mode="r", encoding=encoding) as file:
            result = file.readlines()
        
    except Exception as e:
        print(e)
    
    return result

# Read dict from JSON file
def get_dict_from_json(json_path:str, encoding:str="utf-8") -> dict:
    result = {}

    try:
        with open(json_path, mode="r", encoding=encoding) as file:
            result = json.load(file)
        
    except Exception as e:
        print(e)
        
    return result

# Read dict from YAML file
def get_dict_from_yaml(yaml_path:str, encoding:str="utf-8") -> dict:
    result = {}
    
    try:
        with open(yaml_path, mode="r", encoding=encoding) as file:
            yaml_file = file.read()
            result = yaml.load(yaml_file, Loader=yaml.FullLoader)
        
    except Exception as e:
        print(e)
        
    return result

# Read pandas DataFrame from CSV file
def get_df_from_csv(filepath:str, delimiter:str=",", encoding:str="utf-8") -> pd.DataFrame:
    df = None
    
    if os.path.exists(filepath):
        df = pd.read_csv(filepath, sep=delimiter, encoding=encoding)

    return df

# Save or update a CSV data
def save_csv_data(file_path:str, header:list, data:list, mode:str="w", encoding:str="utf-8") -> bool:
    df = pd.DataFrame(data, columns=header)
    result = save_df_to_csv(df, file_path, False, mode, encoding)
    return result

# Save dataframe to CSV file
def save_df_to_csv(df:pd.DataFrame, file_path:str, index=False, mode:str="w", encoding:str="utf-8") -> bool:
    result = False
    
    try: 
        df.to_csv(file_path, index=index, mode=mode, encoding=encoding)
        result = os.path.exists(file_path)
        
    except Exception as e:
        print(e)
    
    return result
