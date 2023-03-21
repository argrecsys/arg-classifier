# -*- coding: utf-8 -*-
"""
    Created by: Andrés Segura-Tinoco
    Version: 1.1.0
    Created on: Jun 28, 2022
    Updated on: Mar 21, 2023
    Description: Manages ML engine auditing
"""

import logging
from datetime import datetime

# Machine Learning Logging class
class MLLog:
    
    # Constructor
    def __init__(self, verbose=False):
        self.log_path = '../log/log_file.log'
        self.verbose = verbose
        
        # Create logger
        self.logger = logging.getLogger('ml_logger')
        self.logger.setLevel(logging.DEBUG)
        
        # Create file handler which logs even debug messages
        fh = logging.FileHandler(self.log_path)
        fh.setLevel(logging.DEBUG)
        
        # Create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)
        
        # Add the handlers to the logger
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
        
        # Otherwise root logger prints things again
        self.logger.propagate = False
    
    # Log a debug message
    def log_debug(self, msg:str):
        full_msg = msg + ' - ' + str(datetime.now())
        self.logger.debug(full_msg)
        if self.verbose:
            print(full_msg)
    
    # Log an info message
    def log_info(self, msg:str):
        msg = msg if type(msg) == "str" else str(msg)
        full_msg = msg + ' - ' + str(datetime.now())
        self.logger.info(full_msg)
        if self.verbose:
            print(full_msg)
    
    # Log an error message
    def log_error(self, msg:str):
        full_msg = msg + ' - ' + str(datetime.now())
        self.logger.error(full_msg)
        if self.verbose:
            print(full_msg)
