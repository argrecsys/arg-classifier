# -*- coding: utf-8 -*-
"""
    Created by: Andrés Segura-Tinoco
    Version: 0.6.0
    Created on: Oct 19, 2021
    Updated on: Mar 22, 2023
    Description: ML engine contants.
"""

# Import Python base libraries
import enum

# Using enum class create the task type enumeration
class TaskType(enum.Enum):
    ARG_DETECTION = 'arg-detection'
    ARG_CLASSIFICATION = 'arg-classification'
    REL_CLASSIFICATION = 'rel-classification'
    
    def __str__(self):
        return self.value

# Using enum class create the model type enumeration
class ModelType(enum.Enum):
    LOG_REG = "logistic-regression"
    NAIVE_BAYES = "naive-bayes"
    SVM = "support-vector-machine"
    GRADIENT_BOOSTING = "gradient-boosting"
    
    def __str__(self):
        return self.value

# Using enum class create the data scale algorithms enumeration
class ScaleData(enum.Enum):
    NORMALIZE = "normalize"
    STANDARDIZE = "standardize"
    
    def __str__(self):
        return self.value
    
# Using enum class create the dimensionality reduction algorithms enumeration
class DimReduction(enum.Enum):
    LDA = "lda"
    PCA = "pca"
    SVD = "svd"
    
    def __str__(self):
        return self.value
