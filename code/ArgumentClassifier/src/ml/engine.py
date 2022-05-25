# -*- coding: utf-8 -*-
"""
    Created by: Andrés Segura-Tinoco
    Version: 0.8.10
    Created on: Oct 07, 2021
    Updated on: May 25, 2022
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

# Import ML libraries
from nltk.stem import SnowballStemmer
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
        self.mislabeled_records = {"t1_error":[], "t2_error":[]}
        
    ######################
    ### UTIL FUNCTIONS ###
    ######################
    
    # Read JSON file of features
    def __read_feature_file(self, data_path:str) -> list:
        filepath = data_path + "features.json"
        features = ufl.get_list_from_json(filepath, self.encoding)
        return features
    
    # Read CSV file of labels
    def __read_label_file(self, data_path:str) -> list:
        labels = []
        
        filepath = data_path + "propositions.csv"
        lines = ufl.get_list_from_plain_file(filepath, self.encoding)
        
        if len(lines) > 1:
            for line in lines[1:]:
                data = line.replace("\n", "").split(",")
                n = len(data)
                
                # Save data
                prop_id = data[0]
                label1 = data[n-2]
                label2 = data[n-1]
                labels.append({"id": prop_id, "sent_label1": label1, "sent_label2": label2})
        
        return labels
    
    # Read text plain file of stopwords
    def __read_stopword_list(self, data_path:str) -> set:
        filepath = data_path + "stopwords/" + self.language + ".txt"
        stopwords = set(ufl.get_list_from_plain_file(filepath))
        return stopwords
    
    # Core function - Create dataset
    def __create_dataset(self, features:list, labels:list, y_label:str, feat_setup:dict, set_stopwords:set) -> pd.DataFrame:
        
        # Validation
        if len(features) != len(labels):
            print(" - The length of the data and the labels is different")
            return None
        
        # Temp variables
        vcb_corpus = []
        ent_mtx = []
        adverbs_mtx = []
        verbs_mtx = []
        nouns_mtx = []
        punct_mtx = []
        key_words_mtx = []
        modal_auxiliary = []
        text_length = []
        text_position = []
        token_count = []
        avg_word_length = []
        punct_marks_count = []
        parse_tree_depth = []
        sub_clauses_count = []
        label_list = []
        
        # Create stemmer
        stemmer = SnowballStemmer(self.language)
        
        # Create corpus
        for v, l in zip(features, labels):
            label_data = l
                
            # Add vocabulary - BoW and PoS
            feat_data = []
            feat_data += v["bow_unigrams"] if feat_setup["bow_unigrams"] and len(v["bow_unigrams"]) > 0 else []
            feat_data += v["bow_bigrams"] if feat_setup["bow_bigrams"] and len(v["bow_bigrams"]) > 0 else []
            feat_data += v["bow_trigrams"] if feat_setup["bow_trigrams"] and len(v["bow_trigrams"]) > 0 else []
            feat_data += v["pos_unigrams"] if feat_setup["pos_unigrams"] and len(v["pos_unigrams"]) > 0 else []
            feat_data += v["pos_bigrams"] if feat_setup["pos_bigrams"] and len(v["pos_bigrams"]) > 0 else []
            feat_data += v["word_couples"] if feat_setup["word_couples"] and len(v["word_couples"]) > 0 else []
            
            # Transform words to lower case, remove stopwords and save vocabulary (step -0)
            vocabulary = [ele.lower() for ele in feat_data]
            if feat_setup["remove_stopwords"] and set_stopwords:
                vocabulary = [ele for ele in vocabulary if ele not in set_stopwords]
            vcb_corpus.append(vocabulary)
            
            # Entities matrix
            if feat_setup["entities"]:
                ent_mtx.append(mlu.value_to_features(v["entities"], "ent"))
            
            # Adverbs matrix
            if feat_setup["adverbs"]:
                tokens = [stemmer.stem(ele) for ele in v["adverbs"]]
                adverbs_mtx.append(mlu.value_to_features(tokens, "avb"))
            
            # Verbs matrix
            if feat_setup["verbs"]:
                tokens = [stemmer.stem(ele) for ele in v["verbs"]]
                verbs_mtx.append(mlu.value_to_features(tokens, "vb"))
            
            # Nouns matrix
            if feat_setup["nouns"]:
                nouns_mtx.append(mlu.value_to_features(v["nouns"], "nns"))
            
            # Punctuation matrix
            if feat_setup["punctuation"]:
                punct_mtx.append(mlu.value_to_features(v["punctuation"], "pm"))
            
            # Keyword matrix (step -8)
            if feat_setup["key_words"]:
                key_words_mtx.append(mlu.value_to_features(v["key_words"], "kw"))
            
            # Save structural features
            if feat_setup["struc_stats"]:
                modal_auxiliary.append(len(v["modal_auxs"]))
                text_length.append(v["text_length"])
                text_position.append(v["text_position"])
                token_count.append(v["token_count"])
                avg_word_length.append(v["avg_word_length"])
                punct_marks_count.append(v["punct_marks_count"])
                
            # Save syntactic features
            if feat_setup["synt_stats"]:
                parse_tree_depth.append(v["parse_tree_depth"])
                sub_clauses_count.append(v["sub_clauses_count"])
            
            # Save label
            label_list.append(label_data[y_label].lower())
        
        # Create main dataframe
        df = uml.create_df_from_sparse_matrix(vcb_corpus)
        
        # Add entities matrix to main df
        if feat_setup["entities"]:
            df_ent = uml.create_df_from_sparse_matrix(ent_mtx)
            df = pd.concat([df, df_ent], axis=1)
        
        # Add adverbs matrix to main df
        if feat_setup["adverbs"]:
            df_adv = uml.create_df_from_sparse_matrix(adverbs_mtx)
            df = pd.concat([df, df_adv], axis=1)
        
        # Add verbs matrix to main df
        if feat_setup["verbs"]:
            df_vb = uml.create_df_from_sparse_matrix(verbs_mtx)
            df = pd.concat([df, df_vb], axis=1)
        
        # Add verbs matrix to main df
        if feat_setup["nouns"]:
            df_nns = uml.create_df_from_sparse_matrix(nouns_mtx)
            df = pd.concat([df, df_nns], axis=1)
        
        # Add punctuation matrix to main df
        if feat_setup["punctuation"]:
            df_punct = uml.create_df_from_sparse_matrix(punct_mtx)
            df = pd.concat([df, df_punct], axis=1)
        
        # Add keywords matrix to main df
        if feat_setup["key_words"]:
            df_kw = uml.create_df_from_sparse_matrix(key_words_mtx)
            df = pd.concat([df, df_kw], axis=1)
        
        # Add extra columns - structural stats
        if feat_setup["struc_stats"]:
            df["struc_modal_auxiliary"] = modal_auxiliary
            df["struc_text_length"] = text_length
            df["struc_text_position"] = text_position
            df["struc_token_count"] = token_count
            df["struc_avg_word_length"] = avg_word_length
            df["struc_punct_marks_count"] = punct_marks_count
            
        # Add extra columns - syntactic stats
        if feat_setup["synt_stats"]:
            df["synt_parse_tree_depth"] = parse_tree_depth
            df["synt_sub_clauses_count"] = sub_clauses_count
        
        # Scale final dataframe
        if feat_setup["scale_data"]:
            df = mlu.normalize_df(df)
        
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
    def create_dataset(self, data_path:str, y_label:str, force_create_dataset:bool, feat_setup:dict) -> tuple:
        dataset = None
        label_dict = {}
        df_filepath = data_path + "dataset.csv"
        
        if force_create_dataset or not os.path.exists(df_filepath):
            
            # Creation
            features = self.__read_feature_file(data_path)
            labels = self.__read_label_file(data_path)
            stopwords = self.__read_stopword_list(data_path)
            dataset = self.__create_dataset(features, labels, y_label, feat_setup, stopwords)
            
            # Dimensionality reduction
            if feat_setup["dim_reduction"]:
                n_comp = 0.95
                dataset, pca_variance = mlu.apply_dim_reduction(dataset, 'PCA', n_comp)
                print('Explained Variance Ratio:', sum(pca_variance) * 100)
            
            # Save it to disk
            dataset.to_csv(df_filepath, index=False)
        else:
            # Read it from disk
            dataset = ufl.get_df_from_csv(df_filepath)
        
        # Final formatting
        if dataset is not None:
            label_dict, label_list = mlu.get_label_dict(self.task_type, dataset[self.label_column].tolist())
            dataset[self.label_column] = label_list
            
            if self.verbose:
                print(label_dict)
                print(dataset.groupby([self.label_column])[self.label_column].count())
                print(dataset)
        
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
            params = {'learning_rate': 0.1, 'n_estimators': 150, 'max_depth': 5, 'min_samples_leaf': 1, 'min_samples_split': 2, 'random_state': model_state}
            clf = GradientBoostingClassifier(**params)
            clf.fit(X_train, y_train)
        
        # Return model and model params
        return clf, params
    
    # ML function - Create and fit (with grid search) model
    def create_and_fit_model(self, algorithm:str, X_train:pd.DataFrame, y_train:pd.Series, model_state:int, cv_k:int) -> tuple:
        clf = None
        params = {}
        
        if algorithm == ModelType.NAIVE_BAYES.value:
            # Naive Bayes
            clf = MultinomialNB()
            clf.fit(X_train, y_train)
        
        elif algorithm == ModelType.GRADIENT_BOOSTING.value:
            # GB hyper-params space
            space = {'learning_rate': [0.15, 0.1, 0.05, 0.01, 0.005],
                     'n_estimators': [50, 75, 100, 125, 150],
                     'max_depth': [3, 4, 5, 6, 7],
                     'min_samples_split': [2, 3, 4, 5],
                     'min_samples_leaf': [1, 2, 5, 7, 11]}
            
            # Gradient Boosting tuning
            tuning = GridSearchCV(estimator=GradientBoostingClassifier(random_state=model_state), 
                                  param_grid=space, scoring='accuracy', cv=cv_k, n_jobs=8)
            tuning.fit(X_train, y_train)
            
            # Keep the best
            clf = tuning.best_estimator_
            params = tuning.best_params_
        
        # Return model and model params
        return clf, params
    
    # ML function - Validate model
    def validate_model(self, clf, X_train:pd.DataFrame, y_train:pd.Series, cv_k:int) -> tuple:
        print("- Validating model:")
        y_train_pred = cross_val_predict(clf, X_train, y_train, cv=cv_k)
        return mlu.calculate_errors(self.task_type, y_train, y_train_pred, self.verbose)
    
    # ML function - Test model
    def test_model(self, clf, X_test:pd.DataFrame, y_test:pd.Series) -> tuple:
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
