# -*- coding: utf-8 -*-
"""
    Created by: Andres Segura Tinoco
    Version: 0.1.0
    Created on: Oct 19, 2021
    Updated on: Oct 19, 2021
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
    NAIVE_BAYES = "naive bayes"
    GRADIENT_BOOSTING = "gradient boosting"
    
    def __str__(self):
        return self.value
