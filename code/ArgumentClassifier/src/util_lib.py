# -*- coding: utf-8 -*-
"""
    Created by: Andres Segura Tinoco
    Version: 1.0.0
    Created on: Oct 06, 2021
    Updated on: Oct 19, 2021
    Description: Library with utility functions
"""

# Import Python base libraries
import os
import csv
import json
import yaml
import pandas as pd

# Import ML libraries
from sklearn.feature_extraction.text import CountVectorizer

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
    result = dict()

    try:
        with open(json_path, mode="r", encoding=encoding) as file:
            result = json.load(file)
    except Exception as e:
        print(e)
        
    return result

# File function - Read dict from YAML file
def get_dict_from_yaml(yaml_path:str, encoding:str="utf-8") -> dict:
    result = dict()
    
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
def save_append_csv_data(filepath:str, header:list, data:list, encoding:str="utf-8") -> bool:
    result = False
    mode = "a" if os.path.exists(filepath) else "w"
    
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

# Util function - Convert the values of a dict of dicts to a list
def convert_dict_dict_to_list(dict_dict:dict, key:str) -> list:
    values = []
    
    for k, v in dict_dict.items():
        value = v.get(key, "")
        values.append(value)
    
    return values
        
# Util function - Transform a categorical list to a numeric list
def convert_categ_to_num(catg_list:list) -> dict:
    label_dict = {}
    
    for value in catg_list:
        value = value.lower()
        if not value in label_dict:
            label_dict[value] = len(label_dict)
    
    return label_dict

# Util function - Calculate DataFrame sparsity
def calc_df_sparsity(df:pd.DataFrame) -> float:
    sparsity = (df.to_numpy() == 0).mean()
    return sparsity

# Util function - Creates a DataFrame from a sparse matrix using CountVectorizer data structure
def create_df_from_sparse_matrix(matrix:list) -> pd.DataFrame:
    
    # Word vectorization
    vectorizer = CountVectorizer(analyzer=lambda x: x)
    data = vectorizer.fit_transform(matrix).toarray()
    columns = vectorizer.get_feature_names()
        
    # Create dataframe
    df = pd.DataFrame(data, columns=columns)
    
    return df
