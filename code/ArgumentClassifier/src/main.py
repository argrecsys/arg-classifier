# -*- coding: utf-8 -*-
"""
    Created by: Andres Segura Tinoco
    Version: 0.1.0
    Created on: Aug 27, 2021
    Updated on: Oct 06, 2021
    Description: Main class of the argument classifier.
"""

# Import Python base libraries
import util_lib as ul
import pandas as pd
from datetime import datetime

# Import ML libraries
from sklearn.feature_extraction.text import CountVectorizer

######################
### CORE FUNCTIONS ###
######################

# Read data configuration
def read_data_setup() -> dict:
    filepath = "config/config.json"
    setup = ul.get_dict_from_json(filepath)
    return setup

# Read JSON file of features
def read_feature_file(filepath:str) -> dict:
    features = ul.get_dict_from_json(filepath, "utf-8")
    return features

# Read CSV file of labels
def read_label_file(filepath:str) -> dict:
    labels = {}
    lines = ul.get_list_from_plain_file(filepath, "utf-8")
    
    if len(lines) > 1:
        for line in lines[1:]:
            data = line.split(",")
            n = len(data)
            
            # Save data
            prop_id = data[0]+"-"+data[1]
            linker = data[n-3]
            category = data[n-2]
            sub_category = data[n-1]
            labels[prop_id] = {"linker": linker, "category": category, "sub_category": sub_category}
    
    return labels

# Create dataset
def create_dataset(features:dict, labels:dict, setup:dict, lower:bool=True) -> list:
    corpus = []
    text_length = []
    avg_word_length = []
    number_punct_marks = []
    parse_tree_depth = []
    number_sub_clauses = []
    label_list = []
    
    for k, v in features.items():
        label = labels.get(k, None)
        
        if label is not None:
            
            # Add vocabulary
            feat_data = []
            feat_data += v["unigrams"] if setup["unigrams"] and len(v["unigrams"]) > 0 else []
            feat_data += v["bigrams"] if setup["bigrams"] and len(v["bigrams"]) > 0 else []
            feat_data += v["trigrams"] if setup["trigrams"] and len(v["trigrams"]) > 0 else []
            feat_data += v["adverbs"] if setup["adverbs"] and len(v["adverbs"]) > 0 else []
            feat_data += v["verbs"] if setup["verbs"] and len(v["verbs"]) > 0 else []
            feat_data += v["modal_aux"] if setup["modal_aux"] and len(v["modal_aux"]) > 0 else []
            feat_data += v["word_couples"] if setup["word_couples"] and len(v["word_couples"]) > 0 else []
            feat_data += v["punctuation"] if setup["punctuation"] and len(v["punctuation"]) > 0 else []
            feat_data += v["key_words"] if setup["key_words"] and len(v["key_words"]) > 0 else []
            
            # Transform to lower case and save vocabulary
            feat_data = [ele.lower() if lower else ele for ele in feat_data]
            corpus.append(feat_data)
            
            if setup["stats"]:
                text_length.append(v["text_length"])
                avg_word_length.append(v["avg_word_length"])
                number_punct_marks.append(v["number_punct_marks"])
                parse_tree_depth.append(v["parse_tree_depth"])
                number_sub_clauses.append(v["number_sub_clauses"])
            
            label_list.append(label["category"])
        else:
            print('Missing label:', k)
        
    # Word vectorization
    vectorizer = CountVectorizer(analyzer=lambda x: x)
    data = vectorizer.fit_transform(corpus).toarray()
    columns = vectorizer.get_feature_names()
    
    # Create dataframe
    df = pd.DataFrame(data, columns=columns)
    
    # Add extra columns
    if setup["stats"]:
        df["text_length"] = text_length
        df["avg_word_length"] = avg_word_length
        df["number_punct_marks"] = number_punct_marks
        df["parse_tree_depth"] = parse_tree_depth
        df["number_sub_clauses"] = number_sub_clauses
    
    # Added label column
    df["label"] = label_list
    
    return df

#####################
### START PROGRAM ###
#####################
if __name__ == "__main__":
    print('>> START PROGRAM:', str(datetime.now()))
    
    # 0. Program variables
    output_path = "../../../dataset/"
    data_setup = read_data_setup()
    
    # 1. Create dataset
    filepath = output_path + "features.json"
    features = read_feature_file(filepath)
    
    filepath = output_path + "propositions.csv"
    labels = read_label_file(filepath)
    
    dataset = create_dataset(features, labels, data_setup)
    
    # 2. Export dataset
    filepath = output_path + "dataset.csv"
    dataset.to_csv(filepath, index=False)
    
    print(">> END PROGRAM:", str(datetime.now()))
#####################
#### END PROGRAM ####
#####################
