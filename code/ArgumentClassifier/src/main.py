# -*- coding: utf-8 -*-
"""
    Created by: Andres Segura Tinoco
    Version: 0.1.0
    Created on: Aug 27, 2021
    Updated on: Oct 05, 2021
    Description: Main class of the argument classifier.
"""

# Import Python
import json

######################
### CORE FUNCTIONS ###
######################

# Read JSON file of features
def read_feature_file(filepath:str, encoding:str="utf-8") -> dict:
    features = {}
    
    with open(filepath, "r", encoding=encoding) as file:
        json_data = file.read()
        features = json.loads(json_data)
    
    return features

# Read CSV file of labels
def read_labels_file(filepath:str, encoding:str="utf-8") -> dict:
    labels = {}
    lines = []
    
    with open(filepath, "r", encoding=encoding) as file:
        lines = file.readlines()
    
    if len(lines) > 1:
        for line in lines[1:]:
            data = line.split(",")
            n = len(data)
            
            # Save data
            prop_id = data[0]+"-"+data[1]
            linker = data[n-3]
            category = data[n-3]
            sub_category = data[n-3]
            labels[prop_id] = {"linker": linker, "category": category, "sub_category": sub_category}
    
    return labels

# Create dataset
def create_dataset(features:dict, labels:dict) -> list:
    dataset = []
    
    return dataset

#####################
### START PROGRAM ###
#####################
if __name__ == "__main__":
    
    # 0. Program variables
    
    # 1. Create dataset
    filepath = "../../../dataset/features.json"
    features = read_feature_file(filepath)
    
    filepath = "../../../dataset/propositions.csv"
    labels = read_labels_file(filepath)
    
    dataset = create_dataset(features, labels)
    
#####################
#### END PROGRAM ####
#####################
