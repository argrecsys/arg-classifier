# -*- coding: utf-8 -*-
"""
    Created by: Andrés Segura-Tinoco
    Version: 0.4.0
    Created on: Oct 19, 2021
    Updated on: May 23, 2022
    Description: ML engine utility functions.
"""

# Import Custom libraries
from ml.constant import TaskType
from util import ml as uml

# Import Python base libraries
import pandas as pd

# Import ML libraries
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score, recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler

# Util function - Transform labels
def get_label_dict(task_type:str, labels:list) -> dict:
    label_dict = {}
    label_list = []
    
    # Update label field
    if task_type == TaskType.DETECTION.value:
        # Labels: non-argumentative or argumentative
        label_dict = { 0: "no", 1: "yes" }
        label_list = [0 if item == "no" else 1 for item in labels]
        
    elif task_type == TaskType.CLASSIFICATION.value:
        label_dict = uml.convert_categ_to_num(labels)
        label_list = [label_dict[item] for item in labels]
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
    
    if task_type == TaskType.DETECTION.value:
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

# Core function - Calculates mislabeled records
def calc_mislabeled_records(index, y_real, y_pred):
    records = {"t1_error":[], "t2_error":[]}
        
    for ix, real, pred in zip(index, y_real, y_pred):
        if real == 1 and pred == 0:
            records["t2_error"].append(ix)
        elif real == 0 and pred == 1:
            records["t1_error"].append(ix)
    
    return records

# Core function - Normalize numeric values of a dataframe
def normalize_df(df:pd.DataFrame) -> pd.DataFrame:
    scaler = MinMaxScaler()
    df_new = pd.DataFrame(scaler.fit_transform(df.values), columns=df.columns, index=df.index)
    return df_new

# Core function - Standardize numeric values of a dataframe
def standardize_df(df:pd.DataFrame) -> pd.DataFrame:
    scaler = StandardScaler()
    df_new = pd.DataFrame(scaler.fit_transform(df.values), columns=df.columns, index=df.index)
    return df_new
