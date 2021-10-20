# -*- coding: utf-8 -*-
"""
    Created by: Andres Segura Tinoco
    Version: 0.2.0
    Created on: Oct 19, 2021
    Updated on: Oct 20, 2021
    Description: ML engine utility functions.
"""

# Import Custom libraries
import util_lib as cul
from ml.constant import TaskType

# Import Python base libraries
import pandas as pd

# Import ML libraries
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score, recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import roc_auc_score

# Util function - Transform labels
def get_label_dict(task_type:str, label_list:list) -> dict:
    
    # Update label field
    label_dict = {}
    if task_type == TaskType.IDENTIFICATION.value:
        # Labels: non-argumentative or argumentative
        label_dict = { 0: "no", 1: "yes" }
        label_list = [0 if item == "-" else 1 for item in label_list]
        
    elif task_type == TaskType.CLASSIFICATION.value:
        label_dict = cul.convert_categ_to_num(label_list)
        label_list = [label_dict[item] for item in label_list]
        label_dict = {v: k for k, v in label_dict.items()}
    
    return label_dict, label_list

# Util function - Convert a list of values to a feature vector
def value_to_features(values:list, prefix:str):
    key_words = []
    
    if len(values):
        for kw in values:
            kw_name = prefix + "_" + kw.lower().replace(" ", "_")
            key_words.append(kw_name)
    else:
        kw_name = prefix + "_none"
        key_words.append(kw_name)

    return key_words

# Core function - Calculate difference between real and predicted
def calculate_errors(task_type:str, y_real:pd.Series, y_pred:pd.Series, verbose:bool) -> tuple:
    conf_mx = confusion_matrix(y_real, y_pred)
    accuracy = accuracy_score(y_real, y_pred)
    
    if task_type == TaskType.IDENTIFICATION.value:
        precision = precision_score(y_real, y_pred)
        recall = recall_score(y_real, y_pred)
        f1 = f1_score(y_real, y_pred)
        roc_score = roc_auc_score(y_real, y_pred)
        
    elif task_type == TaskType.CLASSIFICATION.value:
        precision = precision_score(y_real, y_pred, average='micro')
        recall = recall_score(y_real, y_pred, average='micro')
        f1 = f1_score(y_real, y_pred, average='micro')
        roc_score= 0
        
    if verbose:
        print(conf_mx)
        print("accuracy:", accuracy, ", precision:", precision, ", recall:", recall, ", f1-score:", f1, ", roc_curve:", roc_score)
        #cpl.plot_confusion_matrix(conf_mx)
    
    return accuracy, precision, recall, f1, roc_score
