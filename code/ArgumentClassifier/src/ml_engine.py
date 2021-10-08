# -*- coding: utf-8 -*-
"""
    Created by: Andres Segura Tinoco
    Version: 0.5.0
    Created on: Oct 07, 2021
    Updated on: Oct 08, 2021
    Description: ML engine class.
"""

# Import Custom libraries
import util_lib as cul
#import plot_lib as cpl

# Import Python base libraries
import os
import enum
import numpy as np
import pandas as pd

# Import ML libraries
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score, recall_score, f1_score

# Using enum class create the task type enumeration
class TaskType(enum.Enum):
    IDENTIFICATION = 'identification'
    CLASSIFICATION = 'classification'
    
    def __str__(self):
        return self.value

# Machine Learning class
class MLEngine:
    
    # Constructor
    def __init__(self, task_type:str, verbose:bool=True):
        self.encoding = "utf-8"
        self.label_column = "label"
        self.task_type = task_type
        self.verbose = verbose
        
    ######################
    ### UTIL FUNCTIONS ###
    ######################
    
    # Read JSON file of features
    def __read_feature_file(self, output_path:str) -> dict:
        filepath = output_path + "features.json"
        features = cul.get_dict_from_json(filepath, self.encoding)
        return features
    
    # Read CSV file of labels
    def __read_label_file(self, output_path:str) -> dict:
        labels = {}
        
        filepath = output_path + "propositions.csv"
        lines = cul.get_list_from_plain_file(filepath, self.encoding)
        
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
    
    # Core function - Create dataset
    def __create_dataset(self, features:dict, labels:dict, y_label:str, setup:dict) -> pd.DataFrame:
        corpus = []
        text_length = []
        avg_word_length = []
        number_punct_marks = []
        parse_tree_depth = []
        number_sub_clauses = []
        label_list = []
        lower_case = True
        
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
                feat_data = [ele.lower() if lower_case else ele for ele in feat_data]
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
        
        # Calculate DataFrame sparsity
        df_sparsity = cul.calc_df_sparsity(df)
        print('DataFrame sparsity:', df_sparsity)
        
        # Added label column
        df[self.label_column] = label_list
        
        return df
    
    # Core function - Transform labels
    def __get_label_dict(self, label_list:list) -> dict:
        
        # Update label field
        label_dict = {}
        if self.task_type == TaskType.IDENTIFICATION.value:
            label_dict = { 0: "no", 1: "yes" }
            label_list = [0 if item == "-" else 1 for item in label_list]
            
        elif self.task_type == TaskType.CLASSIFICATION.value:
            label_dict = cul.convert_categ_to_num(label_list)
            label_list = [label_dict[item] for item in label_list]
            label_dict = {v: k for k, v in label_dict.items()}
        
        return label_dict, label_list
    
    ####################
    ### ML FUNCTIONS ###
    ####################
    
    # ML function - Create dataset
    def create_dataset(self, output_path:str, force_create_dataset:bool, y_label:str, data_setup:dict) -> tuple:
        dataset = None
        label_dict = {}
        df_filepath = output_path + "dataset.csv"
        
        if force_create_dataset or not os.path.exists(df_filepath):
            features = self.__read_feature_file(output_path)
            labels = self.__read_label_file(output_path)
            dataset = self.__create_dataset(features, labels, y_label, data_setup)
            dataset.to_csv(df_filepath, index=False)
        else:
            dataset = pd.read_csv(df_filepath)
        
        if dataset is not None:
            label_dict, label_list = self.__get_label_dict(dataset[self.label_column].tolist())
            dataset[self.label_column] = label_list
        
        return dataset, label_dict
    
    # ML function - Split dataset into train/test
    def split_dataset(self, dataset:pd.DataFrame, perc_test:float, model_state:int) -> tuple:
        X = dataset.loc[:, ~dataset.columns.isin([self.label_column])]
        y = dataset[self.label_column]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=perc_test, random_state=model_state)
        
        return X_train, X_test, y_train, y_test
    
    # ML function - Create model
    def create_model(self, algorithm:str, X_train:pd.DataFrame, y_train:pd.Series, model_state:int):
        clf = None
        
        if algorithm == "nb":
            # Naive Bayes
            clf = MultinomialNB()
            clf.fit(X_train, y_train)
        
        elif algorithm == "gb":
            # Gradient Boosting
            clf = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=2, random_state=model_state)
            clf.fit(X_train, y_train)
        
        return clf
    
    # ML function - Test model
    def test_model(self, clf, X_train, y_train):
        cv_result = cross_val_score(clf, X_train, y_train, cv=5, scoring="accuracy")
        accuracy = np.mean(cv_result)
        
        y_train_pred = cross_val_predict(clf, X_train, y_train, cv=5)
        conf_mx = confusion_matrix(y_train, y_train_pred)
        
        if self.task_type == TaskType.IDENTIFICATION.value:
            m_precision = precision_score(y_train, y_train_pred)
            m_recall = recall_score(y_train, y_train_pred)
            m_f1 = f1_score(y_train, y_train_pred)
            
        elif self.task_type == TaskType.CLASSIFICATION.value:
            m_precision = precision_score(y_train, y_train_pred, average='micro')
            m_recall = recall_score(y_train, y_train_pred, average='micro')
            m_f1 = f1_score(y_train, y_train_pred, average='micro')
        
        if self.verbose:
            print(cv_result)
            #cpl.plot_confusion_matrix(conf_mx)
            print(conf_mx)
            print("accuracy:", accuracy, ", precision:", m_precision, ", recall:", m_recall, ", f1-score:", m_f1)
        
        return m_precision, m_recall, m_f1
