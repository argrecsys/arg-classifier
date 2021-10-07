# -*- coding: utf-8 -*-
"""
    Created by: Andres Segura Tinoco
    Version: 0.1.0
    Created on: Aug 27, 2021
    Updated on: Oct 06, 2021
    Description: Main class of the argument classifier.
"""

# Import Custom libraries
import util_lib as cul
import plot_lib as cpl

# Import Python base libraries
import pandas as pd
from datetime import datetime

# Import ML libraries
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score, recall_score
from sklearn.metrics import f1_score

######################
### CORE FUNCTIONS ###
######################

# Read data configuration
def read_data_setup() -> dict:
    filepath = "config/config.json"
    setup = cul.get_dict_from_json(filepath)
    return setup

# Read JSON file of features
def read_feature_file(output_path:str) -> dict:
    filepath = output_path + "features.json"
    features = cul.get_dict_from_json(filepath, "utf-8")
    return features

# Read CSV file of labels
def read_label_file(output_path:str) -> dict:
    labels = {}
    
    filepath = output_path + "propositions.csv"
    lines = cul.get_list_from_plain_file(filepath, "utf-8")
    
    if len(lines) > 1:
        for line in lines[1:]:
            data = line.split(",")
            n = len(data)
            
            # Save data
            prop_id = data[0] + "-" + data[1]
            linker = data[n-3]
            category = data[n-2]
            sub_category = data[n-1]
            labels[prop_id] = {"linker": linker, "category": category, "sub_category": sub_category}
    
    return labels

# Core function - Transform labels
def get_label_dict(labels:dict, y_label:str) -> dict:
    catg_list = cul.convert_dict_dict_to_list(labels, y_label)
    return cul.convert_categ_to_num(catg_list)

# Core function - Create dataset
def create_dataset(features:dict, labels:dict, y_label:str, setup:dict, lower:bool=True) -> list:
    corpus = []
    text_length = []
    avg_word_length = []
    number_punct_marks = []
    parse_tree_depth = []
    number_sub_clauses = []
    label_list = []
    
    for k, v in features.items():
        label_data = labels.get(k, None)
        
        if label_data is not None:
            
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
            
            label_list.append(label_data[y_label])
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
    y_label = "category"
    data_setup = read_data_setup()
    
    # 1. Create dataset
    features = read_feature_file(output_path)
    labels = read_label_file(output_path)
    label_dict = get_label_dict(labels, y_label)
    
    dataset = create_dataset(features, labels, y_label, data_setup)
    filepath = output_path + "dataset.csv"
    dataset.to_csv(filepath, index=False)
    
    # 2. Split dataset into train/test (0.8/0.2)
    perc_train = 0.8
    state = 42
    X = dataset.loc[:, ~dataset.columns.isin(["label"])]
    y = pd.Series([label_dict[l] for l in dataset["label"]])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=(1-perc_train), random_state=state)
    
    # 3. Train model
    nv_clf = MultinomialNB()
    nv_clf.fit(X_train, y_train)
    
    # 4. Test model
    cv_result = cross_val_score(nv_clf, X_train, y_train, cv=5, scoring="accuracy")
    print(cv_result)
    
    y_train_pred = cross_val_predict(nv_clf, X_train, y_train, cv=5)
    conf_mx = confusion_matrix(y_train, y_train_pred)
    cpl.plot_confusion_matrix(conf_mx)
    print(conf_mx)
    
    m_precision = precision_score(y_train, y_train_pred, average='micro')
    m_recall = recall_score(y_train, y_train_pred, average='micro')
    m_f1 = f1_score(y_train, y_train_pred, average='micro')
    print("precision:", m_precision, ", recall:", m_recall, ", f1-score:", m_f1)
    
    print(">> END PROGRAM:", str(datetime.now()))
#####################
#### END PROGRAM ####
#####################
