# -*- coding: utf-8 -*-
"""
    Created by: Andres Segura Tinoco
    Version: 0.1.0
    Created on: May 11, 2022
    Updated on: May 11, 2022
    Description: Input data processing module.
"""

# Import Custom libraries
from util import files as fl

# Import Python base libraries
from datetime import datetime

######################
### CORE FUNCTIONS ###
######################

# Read data configuration
def read_app_setup() -> dict:
    filepath = "../config/config.json"
    setup = fl.get_dict_from_json(filepath)
    return setup

# Read JSON input dataset
def read_input_dataset(folder_path:str) -> dict:
    filepath = folder_path + "annotations.jsonl"
    dataset = fl.get_list_from_jsonl(filepath)
    return dataset

# Save CSV output dataset
def save_output_dataset(folder_path:str, header:list, dataset:list) -> bool:
    filepath = folder_path + "sentences.csv"
    result = fl.save_csv_data(filepath, header, dataset)
    return result

# Processing dataset from JSON to CSV
def process_dataset(in_dataset:list, language:str) -> list:
    out_dataset = []
    header = ["sent_id", "sent_text", "sent_label"]
    
    # Method constants
    DOT_MARK = '.'
    VALID_SENT_SIZE = 3
    LABEL_SPAM = 'SPAM'
    
    # for-in loop
    comment_id = '0'
    comment_id = '0'
    for row in in_dataset:
        
        # Read basic info
        if 'proposal_id' in row:
            proposal_id = row['proposal_id']
        elif 'comment_id' in row:
            comment_id = row['comment_id']
        text = row['text']
        tokens = row['tokens']
        spans = row['spans']
        
        # Identify dot marks
        dot_marks = [token for token in tokens if token['text'] == DOT_MARK]
        if len(dot_marks) == 0:
            dot_marks = [{'text': '.', 'start': 0, 'end': len(text), 'id': len(tokens), 'ws': True, 'disabled': False}]
            
        # Annotate sentences
        sent_id = 0
        sent_text = ''
        ix_start = 0
        for dot in dot_marks:
            ix_end = dot['end']
            sent_text = text[ix_start : ix_end]
            sent_text = sent_text.strip()
            
            # It is a valid sentence
            if len(sent_text) >= VALID_SENT_SIZE: 
                labels = []
                
                for span in spans:
                    if span['start'] >= ix_start and span['end'] <= ix_end:
                        label = span['label']
                        if label not in labels and label != "LINKER":
                            labels.append(label)
                
                if len(labels) == 0:
                    labels.append(LABEL_SPAM)
                
                # Save outcome
                for i, label in enumerate(labels):
                    record_id = proposal_id + "-" + comment_id + "-" + str(sent_id) + "-" + str(i)
                    out_dataset.append([record_id, sent_text, label])
                    
                # Update sentence number
                sent_id += 1
            
            # Update start index
            ix_start = ix_end + 1
    
    # Return outcome
    return out_dataset, header

# Start application
def start_app():
    app_setup = read_app_setup()
    
    if len(app_setup):
        
        # 0. Program variables
        language = app_setup["language"]
        data_folder = app_setup["data_folder"]
        
        # 1. Read JSON input dataset
        json_dataset = read_input_dataset(data_folder)
        print(" - Total number of records read:", len(json_dataset))
        
        # 2. Processing dataset
        csv_dataset, header = process_dataset(json_dataset, language)
        
        # 3. Save CSV output dataset
        result = save_output_dataset(data_folder, header, csv_dataset)
        print(" - Total number of records saved:", len(csv_dataset))
        
        if result:
            print(" - Successful transformation")
        
    else:
        print(">> ERROR - The application configuration could not be read.", str(datetime.now()))

#####################
### START PROGRAM ###
#####################
if __name__ == "__main__":
    print('>> START DATA PROCESSOR:', str(datetime.now()))
    start_app()    
    print(">> END DATA PROCESSOR:", str(datetime.now()))
#####################
#### END PROGRAM ####
#####################
