# -*- coding: utf-8 -*-
"""
    Created by: Andres Segura Tinoco
    Version: 0.6.0
    Created on: Oct 07, 2021
    Updated on: Oct 18, 2021
    Description: ML engine class.
"""

# Import Custom libraries
import util_lib as cul
#import plot_lib as cpl

# Import Python base libraries
import os
import enum
import pandas as pd
import joblib as jl

# Import ML libraries
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score, recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import roc_auc_score

# Using enum class create the task type enumeration
class TaskType(enum.Enum):
    IDENTIFICATION = 'identification'
    CLASSIFICATION = 'classification'
    
    def __str__(self):
        return self.value

# Machine Learning API class
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
    
    # Core function - Convert a list of values to a feature vector
    def __value_to_features(self, values, prefix):
        key_words = []
        
        if len(values):
            for kw in values:
                kw_name = prefix + "_" + kw.lower().replace(" ", "_")
                key_words.append(kw_name)
        else:
            kw_name = prefix + "_none"
            key_words.append(kw_name)
    
        return key_words
    
    # Core function - Create dataset
    def __create_dataset(self, features:dict, labels:dict, y_label:str, setup:dict) -> pd.DataFrame:
        
        # Temp variables
        vcb_corpus = []
        adverbs_mtx = []
        verbs_mtx = []
        key_words_mtx = []
        text_length = []
        modal_auxiliary = []
        avg_word_length = []
        number_punct_marks = []
        parse_tree_depth = []
        number_sub_clauses = []
        label_list = []
        
        # Create corpus
        for k, v in features.items():
            label_data = labels.get(k, None)
            
            if label_data is not None:
                
                # Add vocabulary
                feat_data = []
                feat_data += v["unigrams"] if setup["unigrams"] and len(v["unigrams"]) > 0 else []
                feat_data += v["bigrams"] if setup["bigrams"] and len(v["bigrams"]) > 0 else []
                feat_data += v["trigrams"] if setup["trigrams"] and len(v["trigrams"]) > 0 else []
                feat_data += v["word_couples"] if setup["word_couples"] and len(v["word_couples"]) > 0 else []
                feat_data += v["punctuation"] if setup["punctuation"] and len(v["punctuation"]) > 0 else []
                
                # Transform to lower case and save vocabulary
                feat_data = [ele.lower() for ele in feat_data]
                vcb_corpus.append(feat_data)
                
                # Adverbs matrix
                if setup["adverbs"]:
                    adverbs_mtx.append(self.__value_to_features(v["adverbs"], "avb"))
                
                # Verbs matrix
                if setup["verbs"]:
                    verbs_mtx.append(self.__value_to_features(v["verbs"], "vb"))
                
                # Keyword matrix
                if setup["key_words"]:
                    key_words_mtx.append(self.__value_to_features(v["key_words"], "kw"))
                
                # Save text statistics
                if setup["text_stats"]:
                    modal_auxiliary.append(len(v["modal_aux"]))
                    text_length.append(v["text_length"])
                    avg_word_length.append(v["avg_word_length"])
                    number_punct_marks.append(v["number_punct_marks"])
                    parse_tree_depth.append(v["parse_tree_depth"])
                    number_sub_clauses.append(v["number_sub_clauses"])
                
                # Save label
                label_list.append(label_data[y_label])
            else:
                print('Missing label:', k)
        
        # Create main dataframe
        df = cul.create_df_from_sparse_matrix(vcb_corpus)
        
        # Add adverbs matrix to main df
        if setup["adverbs"]:
            df_adv = cul.create_df_from_sparse_matrix(adverbs_mtx)
            df = pd.concat([df, df_adv], axis=1)
        
        # Add verbs matrix to main df
        if setup["verbs"]:
            df_vb = cul.create_df_from_sparse_matrix(verbs_mtx)
            df = pd.concat([df, df_vb], axis=1)
        
        # Add keywords matrix to main df
        if setup["key_words"]:
            df_kw = cul.create_df_from_sparse_matrix(key_words_mtx)
            df = pd.concat([df, df_kw], axis=1)
        
        # Add extra columns - text stats
        if setup["text_stats"]:
            df["stats_modal_auxiliary"] = modal_auxiliary
            df["stats_text_length"] = text_length
            df["stats_avg_word_length"] = avg_word_length
            df["stats_number_punct_marks"] = number_punct_marks
            df["stats_parse_tree_depth"] = parse_tree_depth
            df["stats_number_sub_clauses"] = number_sub_clauses
        
        # Added label column
        df[self.label_column] = label_list
        
        # Calculate DataFrame sparsity
        df_sparsity = cul.calc_df_sparsity(df)
        print('DataFrame sparsity:', df_sparsity)
        
        return df
    
    # Core function - Calculate difference between real and predicted
    def __calculate_errors(self, y_real, y_pred) -> tuple:
        conf_mx = confusion_matrix(y_real, y_pred)
        accuracy = accuracy_score(y_real, y_pred)
        
        if self.task_type == TaskType.IDENTIFICATION.value:
            precision = precision_score(y_real, y_pred)
            recall = recall_score(y_real, y_pred)
            f1 = f1_score(y_real, y_pred)
            roc_score = roc_auc_score(y_real, y_pred)
            
        elif self.task_type == TaskType.CLASSIFICATION.value:
            precision = precision_score(y_real, y_pred, average='micro')
            recall = recall_score(y_real, y_pred, average='micro')
            f1 = f1_score(y_real, y_pred, average='micro')
            roc_score= 0
            
        if self.verbose:
            print(conf_mx)
            print("accuracy:", accuracy, ", precision:", precision, ", recall:", recall, ", f1-score:", f1, ", roc_curve:", roc_score)
            #cpl.plot_confusion_matrix(conf_mx)
        
        return accuracy, precision, recall, f1, roc_score 
    
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
    
    ###########################
    ### ML PUBLIC FUNCTIONS ###
    ###########################
    
    # ML function - Create dataset
    def create_dataset(self, output_folder:str, y_label:str, data_setup:dict) -> tuple:
        dataset = None
        label_dict = {}
        force_create_dataset = data_setup.get("force_create", False)
        df_filepath = output_folder + "dataset.csv"
        
        if force_create_dataset or not os.path.exists(df_filepath):
            features = self.__read_feature_file(output_folder)
            labels = self.__read_label_file(output_folder)
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
    
    # ML function - Validate model
    def validate_model(self, clf, X_train, y_train):
        print("- Validating model:")
        y_train_pred = cross_val_predict(clf, X_train, y_train, cv=5)
        return self.__calculate_errors(y_train, y_train_pred)
    
    # ML function - Test model
    def test_model(self, clf, X_test, y_test):
        print("- Testing model:")
        y_test_pred = clf.predict(X_test)
        return self.__calculate_errors(y_test, y_test_pred)
    
    # ML function - Creates and save final model
    def create_save_model(self, model_folder:str, algorithm:str, dataset:pd.DataFrame, model_state:int) -> bool:
        result = False
        filepath = model_folder + algorithm + "_model.joblib"
        X = dataset.loc[:, ~dataset.columns.isin([self.label_column])]
        y = dataset[self.label_column]
        
        clf = self.create_model(algorithm, X, y, model_state)
        
        # Model persistence
        jl.dump(clf, filepath) 
        result = os.path.exists(filepath)
        
        return result
    