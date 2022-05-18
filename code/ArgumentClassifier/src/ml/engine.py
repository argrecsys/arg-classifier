# -*- coding: utf-8 -*-
"""
    Created by: Andrés Segura-Tinoco
    Version: 0.8.0
    Created on: Oct 07, 2021
    Updated on: May 18, 2022
    Description: ML engine class.
"""

# Import Custom libraries
from util import files as ufl
from util import ml as uml
import ml.utility as mlu
from ml.constant import ModelType

# Import Python base libraries
import os
import pandas as pd
import joblib as jl
from nltk.corpus import stopwords

# Import ML libraries
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import GridSearchCV

# Machine Learning API class
class MLEngine:
    
    # Constructor
    def __init__(self, language:str, task_type:str, verbose:bool=True):
        self.encoding = "utf-8"
        self.label_column = "label"
        self.language = language
        self.task_type = task_type
        self.verbose = verbose
        self.cv_value = 5
        self.mislabeled_records = {"t1_error":[], "t2_error":[]}
        
    ######################
    ### UTIL FUNCTIONS ###
    ######################
    
    # Read JSON file of features
    def __read_feature_file(self, data_path:str) -> dict:
        filepath = data_path + "features.json"
        features = ufl.get_dict_from_json(filepath, self.encoding)
        return features
    
    # Read CSV file of labels
    def __read_label_file(self, data_path:str) -> dict:
        labels = {}
        
        filepath = data_path + "propositions.csv"
        lines = ufl.get_list_from_plain_file(filepath, self.encoding)
        
        if len(lines) > 1:
            for line in lines[1:]:
                data = line.split(",")
                n = len(data)
                
                # Save data
                prop_id = data[0]
                label1 = data[n-2]
                label2 = data[n-1][:-1]
                labels[prop_id] = {"sent_label1": label1, "sent_label2": label2}
        
        return labels
    
    # Core function - Create dataset
    def __create_dataset(self, features:dict, labels:dict, y_label:str, setup:dict) -> pd.DataFrame:
        
        # Temp variables
        vcb_corpus = []
        punct_mtx = []
        adverbs_mtx = []
        verbs_mtx = []
        key_words_mtx = []
        modal_auxiliary = []
        text_length = []
        avg_word_length = []
        number_punct_marks = []
        parse_tree_depth = []
        number_sub_clauses = []
        label_list = []
        
        # Create dictionary of stopwords
        set_stopwords = set(stopwords.words(self.language))
        
        # Create corpus
        for k, v in features.items():
            label_data = labels.get(k, None)
            
            if label_data is not None:
                
                # Add vocabulary (steps -1, -2, -3, -4)
                feat_data = []
                feat_data += v["unigrams"] if setup["unigrams"] and len(v["unigrams"]) > 0 else []
                feat_data += v["bigrams"] if setup["bigrams"] and len(v["bigrams"]) > 0 else []
                feat_data += v["trigrams"] if setup["trigrams"] and len(v["trigrams"]) > 0 else []
                feat_data += v["word_couples"] if setup["word_couples"] and len(v["word_couples"]) > 0 else []
                
                # Transform words to lower case, remove stopwords and save vocabulary (step -0)
                vocabulary = [ele.lower() for ele in feat_data]
                if setup["remove_stopwords"] and len(set_stopwords):
                    vocabulary = [ele for ele in vocabulary if ele not in set_stopwords]
                vcb_corpus.append(vocabulary)
                
                # Punctuation matrix (step -5)
                if setup["punctuation"]:
                    punct_mtx.append(mlu.value_to_features(v["punctuation"], "pm"))
                
                # Adverbs matrix (step -6)
                if setup["adverbs"]:
                    adverbs_mtx.append(mlu.value_to_features(v["adverbs"], "avb"))
                
                # Verbs matrix (step -7)
                if setup["verbs"]:
                    verbs_mtx.append(mlu.value_to_features(v["verbs"], "vb"))
                
                # Keyword matrix (step -8)
                if setup["key_words"]:
                    key_words_mtx.append(mlu.value_to_features(v["key_words"], "kw"))
                
                # Save text statistics (step -9)
                if setup["text_stats"]:
                    modal_auxiliary.append(len(v["modal_aux"]))
                    text_length.append(v["text_length"])
                    avg_word_length.append(v["avg_word_length"])
                    number_punct_marks.append(v["number_punct_marks"])
                    parse_tree_depth.append(v["parse_tree_depth"])
                    number_sub_clauses.append(v["number_sub_clauses"])
                
                # Save label
                label_list.append(label_data[y_label].lower())
            else:
                print('Missing label:', k)
        
        # Create main dataframe
        df = uml.create_df_from_sparse_matrix(vcb_corpus)
        
        # Add adverbs matrix to main df
        if setup["punctuation"]:
            df_punct = uml.create_df_from_sparse_matrix(punct_mtx)
            df = pd.concat([df, df_punct], axis=1)
        
        # Add adverbs matrix to main df
        if setup["adverbs"]:
            df_adv = uml.create_df_from_sparse_matrix(adverbs_mtx)
            df = pd.concat([df, df_adv], axis=1)
        
        # Add verbs matrix to main df
        if setup["verbs"]:
            df_vb = uml.create_df_from_sparse_matrix(verbs_mtx)
            df = pd.concat([df, df_vb], axis=1)
        
        # Add keywords matrix to main df
        if setup["key_words"]:
            df_kw = uml.create_df_from_sparse_matrix(key_words_mtx)
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
        df_sparsity = uml.calc_df_sparsity(df)
        print('DataFrame sparsity:', df_sparsity)
        
        return df
    
    ###########################
    ### ML PUBLIC FUNCTIONS ###
    ###########################
    
    # ML function - Create dataset
    def create_dataset(self, data_path:str, y_label:str, data_setup:dict) -> tuple:
        dataset = None
        label_dict = {}
        force_create_dataset = data_setup.get("force_create", False)
        df_filepath = data_path + "dataset.csv"
        
        if force_create_dataset or not os.path.exists(df_filepath):
            features = self.__read_feature_file(data_path)
            labels = self.__read_label_file(data_path)
            dataset = self.__create_dataset(features, labels, y_label, data_setup)
            dataset.to_csv(df_filepath, index=False)
        else:
            dataset = ufl.get_df_from_csv(df_filepath)
        
        if dataset is not None:
            label_dict, label_list = mlu.get_label_dict(self.task_type, dataset[self.label_column].tolist())
            dataset[self.label_column] = label_list
            print(label_dict)
            print(dataset.groupby([self.label_column])[self.label_column].count())
        
        return dataset, label_dict
    
    # ML function - Split dataset into train/test
    def split_dataset(self, dataset:pd.DataFrame, perc_test:float, model_state:int) -> tuple:
        X = dataset.loc[:, ~dataset.columns.isin([self.label_column])]
        y = dataset[self.label_column]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=perc_test, random_state=model_state)
        
        return X_train, X_test, y_train, y_test
    
    # ML function - Create model with default params
    def create_model(self, algorithm:str, X_train:pd.DataFrame, y_train:pd.Series, model_state:int):
        clf = None
        params = {}
        
        if algorithm == ModelType.NAIVE_BAYES.value:
            # Naive Bayes
            clf = MultinomialNB()
            clf.fit(X_train, y_train)
        
        elif algorithm == ModelType.GRADIENT_BOOSTING.value:
            # Gradient Boosting
            params = {'learning_rate': 0.01, 'n_estimators': 100, 'max_depth': 5, 'min_samples_leaf': 5, 'random_state': model_state}
            clf = GradientBoostingClassifier(**params)
            clf.fit(X_train, y_train)
        
        # Return model and model params
        return clf, params
    
    # ML function - Create and fit (with grid search) model
    def create_and_fit_model(self, algorithm:str, X_train:pd.DataFrame, y_train:pd.Series, model_state:int):
        clf = None
        params = {}
        
        if algorithm == ModelType.NAIVE_BAYES.value:
            # Naive Bayes
            clf = MultinomialNB()
            clf.fit(X_train, y_train)
        
        elif algorithm == ModelType.GRADIENT_BOOSTING.value:
            # Gradient Boosting
            space = {'learning_rate': [0.15, 0.1, 0.05, 0.01, 0.005],
                     'n_estimators': [50, 75, 100, 125, 150],
                     'max_depth': [3, 4, 5, 6, 7],
                     'min_samples_leaf': [1, 2, 5, 7, 10]}
            tuning = GridSearchCV(estimator=GradientBoostingClassifier(random_state=model_state), 
                                  param_grid=space, scoring='accuracy', cv=self.cv_value)
            tuning.fit(X_train, y_train)
            params = tuning.best_params_
            clf = tuning.best_estimator_
        
        # Return model and model params
        return clf, params
    
    # ML function - Validate model
    def validate_model(self, clf, X_train, y_train):
        print("- Validating model:")
        y_train_pred = cross_val_predict(clf, X_train, y_train, cv=self.cv_value)
        return mlu.calculate_errors(self.task_type, y_train, y_train_pred, self.verbose)
    
    # ML function - Test model
    def test_model(self, clf, X_test, y_test):
        print("- Testing model:")
        y_test_pred = clf.predict(X_test)
        
        # Calculate mislabeled records
        self.mislabeled_records = mlu.calc_mislabeled_records(X_test.index, y_test, y_test_pred)
        
        return mlu.calculate_errors(self.task_type, y_test, y_test_pred, self.verbose)
    
    # ML function - Get ids of mislabeled records
    def get_mislabeled_records(self) -> dict:
        return self.mislabeled_records
    
    # ML function - Creates and save final model
    def create_save_model(self, model_folder:str, model_id:int, algorithm:str, dataset:pd.DataFrame, model_state:int):
        filepath = model_folder + algorithm.replace(" ", "_") + "_model_" + str(model_id) + ".joblib"
        X = dataset.loc[:, ~dataset.columns.isin([self.label_column])]
        y = dataset[self.label_column]
        
        # Create final model
        clf = self.create_model(algorithm, X, y, model_state)
        
        # Model persistence
        jl.dump(clf, filepath) 
        if not os.path.exists(filepath):
            clf = None
        
        return clf
    
    # ML function - Returns the next model id (current + 1)
    def get_next_model_id(self, filepath:str) -> int:
        max_value = 0
        
        df = ufl.get_df_from_csv(filepath)
        if df is not None:
            max_value = df["id"].max()
        max_value += 1
        
        return max_value
