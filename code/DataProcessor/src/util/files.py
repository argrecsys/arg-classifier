# -*- coding: utf-8 -*-
"""
    Created by: Andres Segura Tinoco
    Version: 1.0.0
    Created on: Oct 06, 2021
    Updated on: May 11, 2022
    Description: Files library with utility functions
"""

# Import Python base libraries
import os
import csv
import json
import yaml
import pandas as pd

# File function - Read list from plain file
def get_list_from_plain_file(filepath:str, encoding:str="utf-8") -> list:
    lines = []
    
    try:
        with open(filepath, mode="r", encoding=encoding) as file:
            lines = file.readlines()
    except Exception as e:
        print(e)
    
    return lines

# File function - Read dict from JSON file
def get_dict_from_json(json_path:str, encoding:str="utf-8") -> dict:
    result = {}

    try:
        with open(json_path, mode="r", encoding=encoding) as file:
            result = json.load(file)
    except Exception as e:
        print(e)
        
    return result

def get_list_from_jsonl(json_path:str, encoding:str="utf-8") -> dict:
    result = {}

    try:
        json_list = []
        with open(json_path, mode="r", encoding=encoding) as file:
            json_list = list(file)
        
        result = [json.loads(jline) for jline in json_list]
        
    except Exception as e:
        print(e)
        
    return result

# File function - Read dict from YAML file
def get_dict_from_yaml(yaml_path:str, encoding:str="utf-8") -> dict:
    result = {}
    
    try:
        with open(yaml_path, mode="r", encoding=encoding) as file:
            yaml_file = file.read()
            result = yaml.load(yaml_file, Loader=yaml.FullLoader)
    except Exception as e:
        print(e)
        
    return result

# File function - Get max value from column from CSV file
def get_max_value_from_csv_file(filepath:str, column:str) -> int:
    max_value = 0
    
    if os.path.exists(filepath):
        df = pd.read_csv(filepath)
        max_value = df["id"].max()
    
    return max_value

# File function - Save or update CSV data
def save_csv_data(filepath:str, header:list, data:list, mode:str="w", encoding:str="utf-8") -> bool:
    result = False
    
    try:    
        with open(filepath, mode, newline="", encoding=encoding) as f:
            write = csv.writer(f)
            if mode == "w":
                write.writerow(header)
            for row in data:
                write.writerow(row)
        result = True
    
    except Exception as e:
        print("Error:", e)
    
    return result
