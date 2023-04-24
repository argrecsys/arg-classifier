# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 23:27:29 2023

@author: Usuario
"""

# Import Custom libraries
from util import files as ufl

# Import ML libraries
import pandas as pd
import numpy as np
import optuna
import lightgbm as lgb
import sklearn.metrics
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

def load_dataset():
    filepath = "../../../data/dataset.csv"
    label_column = "label"
    dataset = ufl.get_df_from_csv(filepath)
    print("len:", len(dataset))
    
    # Features (X) and labels (y)
    X = dataset.drop(label_column, axis=1).values
    y_cat = dataset[label_column].values
    
    # Encoding categorical data into numerical data
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y_cat)
    
    return X, y

def objective(trial):
    data, target = load_dataset()
    
    train_x, valid_x, train_y, valid_y = train_test_split(data, target, test_size=0.2)
    dtrain = lgb.Dataset(train_x, label=train_y)

    param = {
        "objective": "binary",
        "metric": "binary_logloss",
        "verbosity": -1,
        "boosting_type": "gbdt",
        "lambda_l1": trial.suggest_float("lambda_l1", 1e-8, 10.0, log=True),
        "lambda_l2": trial.suggest_float("lambda_l2", 1e-8, 10.0, log=True),
        "num_leaves": trial.suggest_int("num_leaves", 2, 256),
        "feature_fraction": trial.suggest_float("feature_fraction", 0.4, 1.0),
        "bagging_fraction": trial.suggest_float("bagging_fraction", 0.4, 1.0),
        "bagging_freq": trial.suggest_int("bagging_freq", 1, 7),
        "min_child_samples": trial.suggest_int("min_child_samples", 5, 100),
    }

    gbm = lgb.train(param, dtrain)
    preds = gbm.predict(valid_x)
    pred_labels = np.rint(preds)
    accuracy = sklearn.metrics.accuracy_score(valid_y, pred_labels)
    
    return accuracy

if __name__ == "__main__":
    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=100)

    print("Number of finished trials: {}".format(len(study.trials)))

    print("Best trial:")
    trial = study.best_trial

    print("  Value: {}".format(trial.value))

    print("  Params: ")
    for key, value in trial.params.items():
        print("    {}: {}".format(key, value))