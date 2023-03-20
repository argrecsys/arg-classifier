# -*- coding: utf-8 -*-
"""
    Created by: Andrés Segura-Tinoco
    Version: 0.3.0
    Created on: May 11, 2022
    Updated on: Mar 20, 2023
    Description: ML library with utility functions
"""

# Import Python base libraries
import pandas as pd

# Import ML libraries
from sklearn.feature_extraction.text import CountVectorizer

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
    columns = vectorizer.get_feature_names_out()
        
    # Create dataframe
    df = pd.DataFrame(data, columns=columns)
    
    return df
