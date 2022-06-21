# -*- coding: utf-8 -*-
"""
    Created by: Andrés Segura-Tinoco
    Version: 0.3.0
    Created on: Oct 19, 2021
    Updated on: Jun 21, 2022
    Description: ML engine contants.
"""

# Import Python base libraries
import enum

# Using enum class create the task type enumeration
class TaskType(enum.Enum):
    DETECTION = 'detection'
    CLASSIFICATION = 'classification'
    
    def __str__(self):
        return self.value

# Using enum class create the model type enumeration
class ModelType(enum.Enum):
    NAIVE_BAYES = "naive-bayes"
    GRADIENT_BOOSTING = "gradient-boosting"
    SVM = "support-vector-machine"
    
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
    
    def __str__(self):
        return self.value
