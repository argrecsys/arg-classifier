# -*- coding: utf-8 -*-
"""
    Created by: Andrés Segura-Tinoco
    Version: 1.0.0
    Created on: Oct 06, 2021
    Updated on: May 13, 2022
    Description: Files library with utility functions
"""

# Import Python base libraries
import os
import csv
import json
import yaml
import pandas as pd

# Read list from JSONL (json lines format) file
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

# Save or update a CSV data
def save_csv_data(file_path:str, header:list, data:list, mode:str="w", encoding:str="utf-8") -> bool:
    result = False
    
    try:    
        with open(file_path, mode, newline="", encoding=encoding) as f:
            write = csv.writer(f)
            if not os.path.exists(file_path) or mode == "w":
                write.writerow(header)
            for row in data:
                write.writerow(row)
            result = True
    
    except Exception as e:
        print("Error:", e)
    
    return result

# Save dataframe to CSV file
def save_df_to_csv(df:pd.DataFrame, file_path:str, index=False, encoding:str="utf-8") -> bool:
    result = False
    
    try: 
        df.to_csv(file_path, index=index, encoding=encoding)
        result = os.path.exists(file_path)
        
    except Exception as e:
        print("Error:", e)
    
    return result
