# -*- coding: utf-8 -*-
"""
    Created by: Andres Segura Tinoco
    Version: 1.0.0
    Created on: Oct 06, 2021
    Updated on: Oct 06, 2021
    Description: Library with utility functions
"""

# Import Python
import json
import yaml

# Util function - Read list from plain file
def get_list_from_plain_file(filepath:str, encoding:str="utf-8") -> list:
    lines = []
    
    try:
        with open(filepath, "r", encoding=encoding) as file:
            lines = file.readlines()
    except Exception as e:
        print(e)
    
    return lines

# Util function - Read dict from JSON file
def get_dict_from_json(json_path:str, encoding:str="utf-8") -> dict:
    result = dict()

    try:
        with open(json_path, "r", encoding=encoding) as f:
            result = json.load(f)
    except Exception as e:
        print(e)
        
    return result

# Util function - Read dict from YAML file
def get_dict_from_yaml(yaml_path:str, encoding:str="utf-8") -> dict:
    result = dict()
    
    try:
        with open(yaml_path, "r", encoding=encoding) as f:
            yaml_file = f.read()
            result = yaml.load(yaml_file, Loader=yaml.FullLoader)
    except Exception as e:
        print(e)
        
    return result
