# -*- coding: utf-8 -*-
"""
    Created by: Andrés Segura-Tinoco
    Version: 0.9.12
    Created on: Oct 07, 2021
    Updated on: Jun 16, 2022
    Description: ML engine class.
"""

# Import Custom libraries
from util import files as ufl
from util import ml as uml
import ml.utility as mlu
from ml.constant import ModelType, DimReduction, ScaleData

# Import Python base libraries
import os
import numpy as np
import pandas as pd
import joblib as jl

# Import ML libraries
from nltk.stem import SnowballStemmer
from sklearn.model_selection import train_test_split, StratifiedShuffleSplit
from sklearn.model_selection import GridSearchCV

# Import data transformers
from sklearn.preprocessing import Binarizer
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA

# Import ML algorithms
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import GradientBoostingClassifier

# Machine Learning API class
class MLEngine:
    
    # Constructor
    def __init__(self, language:str, task_type:str, verbose:bool=True):
        self.encoding = "utf-8"
        self.label_column = "label"
        self.metric_avg = "micro"
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
        label_pattern = "sent_label"
        filepath = data_path + "propositions.csv"
        lines = ufl.get_list_from_plain_file(filepath, self.encoding)
        
        if len(lines) > 1:
            header = lines[0].replace("\n", "").split(",")
            n_labels = sum([1 if col_name.startswith(label_pattern) else 0 for col_name in header])
            
            for line in lines[1:]:
                data = line.replace("\n", "").split(",")
                n_cols = len(data)
                
                # Save data
                label = {"id": data[0]}
                for i in range(0, n_labels):
                    ix = n_cols - n_labels + i
                    label[label_pattern+str(i+1)] = data[ix]
                labels.append(label)
        
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
            print("- The length of the data and the labels is different")
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
        
        # Added label column
        df[self.label_column] = label_list
        
        return df
    
    # Core function - Create model pipeline with default params
    def __create_model(self, pipeline_setup:dict, model_params:dict, model_classes) -> Pipeline:
        ml_algo = pipeline_setup["ml_algo"]
        data_scale_algo = pipeline_setup["data_scale_algo"]
        dim_red_algo = pipeline_setup["dim_red_algo"]
        
        # Adding pipeline steps
        estimators = []
        if ml_algo == ModelType.NAIVE_BAYES.value:
            estimators.append(('binarizer', Binarizer()))
            estimators.append(('model', MultinomialNB()))
            
        else:
            # 1. Add data scaler
            if data_scale_algo == ScaleData.NORMALIZE.value:
                estimators.append(("scaler", MinMaxScaler()))
                
            elif data_scale_algo == ScaleData.STANDARDIZE.value:
                estimators.append(("scaler", StandardScaler()))
            
            # 2. Add dim reducer
            if dim_red_algo == DimReduction.PCA.value:
                n_comp = 300
                estimators.append(("reducer", PCA(n_components=n_comp)))
                
            elif dim_red_algo == DimReduction.LDA.value:
                n_comp = len(model_classes) - 1
                estimators.append(("reducer", LDA(n_components=n_comp)))
                
            # 3. Add model
            estimators.append(('model', GradientBoostingClassifier(**model_params)))
        
        # Create model pipeline
        pipe = Pipeline(estimators)
        print(pipe)
        
        # Return model and model params
        return pipe
    
    # Core function - Calculate model errors
    def __calculate_model_errors(self, y_real:list, y_pred:list, model_classes:list, avg_type:str) -> tuple:
        results = mlu.calculate_errors(self.task_type, y_real, y_pred, model_classes, avg_type)
        conf_mx, accuracy, precision, recall, f1_score, roc_score, report = results
    
        if self.verbose:
            print(conf_mx)
            print(report)
            print("accuracy: %0.2f, precision: %0.2f, recall: %0.2f, f1-score: %0.2f, roc-curve: %0.2f \n" % (accuracy, precision, recall, f1_score, roc_score))
        
        return accuracy, precision, recall, f1_score, roc_score
    
    ###########################
    ### ML PUBLIC FUNCTIONS ###
    ###########################
    
    # ML function - Create dataset
    def create_dataset(self, data_path:str, y_label:str, force_create_dataset:bool, feat_setup:dict) -> tuple:
        dataset = None
        label_dict = {}
        df_filepath = data_path + "dataset.csv"
        
        if force_create_dataset or not os.path.exists(df_filepath):
            
            # Creation of initial dataset
            features = self.__read_feature_file(data_path)
            labels = self.__read_label_file(data_path)
            stopwords = self.__read_stopword_list(data_path)
            dataset = self.__create_dataset(features, labels, y_label, feat_setup, stopwords)
            
            # Save it to disk
            dataset.to_csv(df_filepath, index=False)
        else:
            # Or, read it from disk
            dataset = ufl.get_df_from_csv(df_filepath)
        
        # Final formatting
        if dataset is not None:
            label_dict, label_list = mlu.get_label_dict(self.task_type, dataset[self.label_column].tolist())
            dataset[self.label_column] = label_list
            
            if self.verbose:
                # Calculate dataset sparsity
                ds_sparsity = uml.calc_df_sparsity(dataset)
                print('- Original dataset sparsity:', ds_sparsity)
                
                # Show dataset labels info
                print('- Dataset labels info:')
                print(label_dict)
                print(mlu.get_df_col_stats(dataset, self.label_column))
                print('\n', dataset)
        
        return dataset, label_dict
    
    # ML function - Split dataset into train/test
    def split_dataset(self, dataset:pd.DataFrame, train_setup:dict) -> tuple:
        cv_stratified = train_setup["cv_stratified"]
        perc_test = train_setup["perc_test"]
        model_state = train_setup["model_state"]
        
        # Features (X) and labels (y)
        X = dataset.drop(self.label_column, axis=1).values
        y = dataset[self.label_column].values
        
        if cv_stratified:
            sss = StratifiedShuffleSplit(n_splits=1, test_size=perc_test, random_state=model_state)
            
            for train_index, test_index in sss.split(X, y):
                X_train, X_test = X[train_index], X[test_index]
                y_train, y_test = y[train_index], y[test_index]
            
        else:
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=perc_test, random_state=model_state)
        
        return X_train, X_test, y_train, y_test
    
    # ML function - Create and train model
    def create_and_train_model(self, pipeline_setup:dict, X_train:np.ndarray, y_train:np.ndarray, model_classes, model_state:int) -> tuple:
        
        # Create model pipeline
        print("- Creating model:")
        # params = {'learning_rate': 0.1, 'n_estimators': 150, 'max_depth': 5, 'min_samples_leaf': 1, 'min_samples_split': 2, 'random_state': model_state}
        params = {'learning_rate': 0.1, 'n_estimators': 200, 'max_depth': 3, 'min_samples_leaf': 5, 'min_samples_split': 2, 'random_state': model_state}
        clf = self.__create_model(pipeline_setup, params, model_classes)
        
        # Train model with train data
        print("- Training model:")
        clf.fit(X_train, y_train)
        
        # Return model and model params
        return clf, params
    
    # ML function - Create and fit model
    def create_and_fit_model(self, pipeline_setup:dict, X_train:np.ndarray, y_train:np.ndarray, model_classes, model_state:int, train_setup:dict) -> tuple:
        
        # Create model pipeline
        print("- Creating model:")
        params = {'random_state': model_state}
        clf = self.__create_model(pipeline_setup, params, model_classes)
        scores = ()
        
        # Fit model with train data
        print("- Fitting model:")
        ml_algo = pipeline_setup["ml_algo"]
        cv_k = train_setup["cv_k"]
        
        if ml_algo == ModelType.GRADIENT_BOOSTING.value:
            
            # GB hyper-params space
            space = {'model__learning_rate': [0.15, 0.1, 0.05, 0.01, 0.005],
                     'model__n_estimators': [75, 100, 125, 150, 200],
                     'model__max_depth': [3, 4, 5, 6, 7],
                     'model__min_samples_leaf': [1, 2, 5, 7, 11],
                     'model__min_samples_split': [2, 3, 4, 5]}
            
            # Gradient Boosting tuning
            metric = "f1_" + self.metric_avg
            tuning = GridSearchCV(estimator=clf, param_grid=space, scoring=metric, cv=cv_k, n_jobs=8, refit=True)
            tuning.fit(X_train, y_train)
            
            # Keep the best
            clf = tuning.best_estimator_
            params = tuning.best_params_
            scores = tuning.cv_results_['mean_test_score'][0], tuning.cv_results_['std_test_score'][0]
        
        if self.verbose:
            print(params)
            print(scores)
        
        # Return model and model params
        return clf, params
    
    # ML function - Test model
    def test_model(self, clf, X_test:np.ndarray, y_test:np.ndarray, model_classes:list) -> tuple:
        print("- Testing model:")
        y_test_pred = clf.predict(X_test)
        
        # Calculate mislabeled records
        self.mislabeled_records = mlu.calc_mislabeled_records(y_test, y_test_pred)
        
        # Calculate and return error metrics
        return self.__calculate_model_errors(y_test, y_test_pred, model_classes, self.metric_avg)
    
    # ML function - Get ids of mislabeled records
    def get_mislabeled_records(self) -> dict:
        return self.mislabeled_records
    
    # ML function - Creates and save final model
    def create_and_save_model(self, filepath:str, dataset:pd.DataFrame, pipeline_setup:dict, model_classes, model_state:int):
        
        # Features (X) and labels (y)
        X = dataset.drop(self.label_column, axis=1).values
        y = dataset[self.label_column].values
        
        # Create final model
        clf, params = self.create_and_train_model(pipeline_setup, X, y, model_classes, model_state)
        
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
