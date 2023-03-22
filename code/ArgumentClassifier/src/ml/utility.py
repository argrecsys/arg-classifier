# -*- coding: utf-8 -*-
"""
    Created by: Andrés Segura-Tinoco
    Version: 0.11.0
    Created on: Oct 19, 2021
    Updated on: Mar 22, 2023
    Description: ML engine utility functions.
"""

# Import Custom libraries
from ml.constant import TaskType
from util import ml as uml

# Import Python base libraries
import numpy as np
import pandas as pd

# Import ML librarie
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import roc_auc_score
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler

######################
### UTIL FUNCTIONS ###
######################

# Util function - Transform labels
def get_label_dict(task_type:str, labels:list) -> dict:
    label_dict = {}
    label_list = []
    
    # Update label field
    if task_type == TaskType.ARG_DETECTION.value:
        # Labels: non-argumentative or argumentative
        label_dict = { 0: "no", 1: "yes" }
        label_list = [0 if item == "no" else 1 for item in labels]
        
    elif task_type == TaskType.ARG_CLASSIFICATION.value or task_type == TaskType.REL_CLASSIFICATION.value:
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

# Util function - Apply dimensionality reduction
def apply_dim_reduction(X:np.ndarray, method:str, n:float, y:np.ndarray=None) -> np.ndarray:
    x_reduced = []
    variance = []
    method = method.upper()
    
    # Create a DataFrame from DR
    if method == "PCA":
        model = PCA(n_components=n)
        x_reduced = model.fit_transform(X)
        variance = model.explained_variance_ratio_
    
    elif mehtod == "SVD":
        model = TruncatedSVD(n_components=n)
        x_reduced = model.fit_transform(X)
        variance = model.explained_variance_ratio_

    elif method == "lda":
        model = LDA(n_components=n)
        x_reduced = model.fit_transform(X, y)
        variance = model.explained_variance_ratio_
    
    return x_reduced, variance

# Util function - Calculates basic dataframe column stats
def get_df_col_stats(df:pd.DataFrame, col_name:str) -> pd.DataFrame:
    data = df[col_name]
    df_new = pd.concat([data.value_counts(), data.value_counts(normalize=True).mul(100)], 
                   axis=1, keys=('counts', 'percentage'))
    return df_new

######################
### CORE FUNCTIONS ###
######################

# Core function - Calculate difference between real and predicted
def calculate_errors(task_type:str, y_real:list, y_pred:list, target_names:list, avg_type:str="") -> tuple:
    
    # Calculate model metrics
    conf_mx = confusion_matrix(y_real, y_pred)
    report = classification_report(y_real, y_pred, target_names=target_names)
    output = classification_report(y_real, y_pred, output_dict=True)
    
    # Get model metrics
    accuracy = output['accuracy']
    weighted_avg = output['weighted avg']
    precision = weighted_avg['precision']
    recall = weighted_avg['recall']
    f1_score = weighted_avg['f1-score']
    roc_score = 0
    if task_type == TaskType.ARG_DETECTION.value:
        roc_score = roc_auc_score(y_real, y_pred)
    
    # Return model metrics
    return conf_mx, accuracy, precision, recall, f1_score, roc_score, report

# Core function - Calculates mislabeled records
def calc_mislabeled_records(y_real, y_pred):
    records = {"t1_error":[], "t2_error":[]}
        
    for ix, (real, pred) in enumerate(zip(y_real, y_pred)):
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
