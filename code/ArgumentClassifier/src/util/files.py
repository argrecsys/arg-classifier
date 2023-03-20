# -*- coding: utf-8 -*-
"""
    Created by: Andrés Segura-Tinoco
    Version: 1.7.0
    Created on: Oct 06, 2021
    Updated on: Mar 16, 2023
    Description: Files library with utility functions
"""

# Import Python base libraries
import os
import csv
import json
import yaml
import pandas as pd

# Read a list of objects from a folder
# Supported extensions: csv, json, jsonl, txt
def get_dict_from_folder(folder_path:str, extension:str, encoding:str="utf-8") -> dict:
    result = {}
    
    try:
        file_ext = "." + extension.lower()
        
        for file in os.listdir(folder_path):
            if file.endswith(file_ext):
                filepath = os.path.join(folder_path, file)
                file_data = None
                
                if file_ext == ".csv":
                    file_data = get_list_from_csv(filepath, encoding)
                
                elif file_ext == ".json":
                    file_data = get_dict_from_json(filepath, encoding)
                
                elif file_ext == ".jsonl":
                    file_data = get_list_from_jsonl(filepath, encoding)
                
                elif file_ext == ".txt":
                    file_data = get_list_from_plain_file(filepath, encoding)
                    
                if file_data:
                    file_name = file.replace(file_ext,  "")
                    result[file_name] = file_data
                
    except Exception as e:
        print(e)
        
    return result

# Read a dict from a JSON file
def get_dict_from_json(json_path:str, encoding:str="utf-8") -> dict:
    result = {}
    
    try:
        with open(json_path, mode="r", encoding=encoding) as file:
            result = json.load(file)
        
    except Exception as e:
        print(e)
        
    return result

# Read a dict from YAML file
def get_dict_from_yaml(yaml_path:str, encoding:str="utf-8") -> dict:
    result = {}
    
    try:
        with open(yaml_path, mode="r", encoding=encoding) as file:
            yaml_file = file.read()
            result = yaml.load(yaml_file, Loader=yaml.FullLoader)
        
    except Exception as e:
        print(e)
        
    return result

# Read a pandas DataFrame from CSV file
def get_df_from_csv(csv_path:str, delimiter:str=",", encoding:str="utf-8") -> pd.DataFrame:
    result = None
    
    try:
        result = pd.read_csv(csv_path, sep=delimiter, encoding=encoding)
        
    except Exception as e:
        print(e)
        
    return result

# Read a list from a CSV file
def get_list_from_csv(csv_path:str, encoding:str="utf-8") -> list:
    result = []
    
    try:
        with open(csv_path, mode="r", encoding=encoding) as file:
            csvreader = csv.reader(file)
            result = [row for row in csvreader]
            
    except Exception as e:
        print(e)
            
    return result

# Read a list of dict from JSON file
def get_list_from_json(json_path:str, encoding:str="utf-8") -> list:
    result = []
    
    try:
        with open(json_path, mode="r", encoding=encoding) as file:
            result = json.load(file)
        
    except Exception as e:
        print(e)
        
    return result

# Read a list of dict from a JSONL (json lines format) file
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

# Read a list from plain file
def get_list_from_plain_file(file_path:str, encoding:str="utf-8") -> list:
    result = []
    
    try:
        with open(file_path, mode="r", encoding=encoding) as file:
            result = file.readlines()
        
    except Exception as e:
        print(e)
    
    return result

# Save or update a CSV data
def save_csv_data(file_path:str, header:list, data:list, mode:str="w", encoding:str="utf-8") -> bool:
    df = pd.DataFrame(data, columns=header)
    result = save_df_to_csv(df, file_path, False, mode, encoding)
    return result

# Save dataframe to CSV file
def save_df_to_csv(df:pd.DataFrame, file_path:str, index=False, mode:str="w", encoding:str="utf-8") -> bool:
    result = False
    
    try:
        hdr = (mode == "w") or (not os.path.isfile(file_path))
        df.to_csv(file_path, index=index, mode=mode, encoding=encoding, header=hdr)
        result = True
        
    except Exception as e:
        print(e)
    
    return result
