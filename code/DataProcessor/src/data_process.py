# -*- coding: utf-8 -*-
"""
    Created by: Andrés Segura-Tinoco
    Version: 0.1.0
    Created on: May 13, 2022
    Updated on: May 13, 2022
    Description: Data processing module
"""

# Import Python base libraries
import pandas as pd

# Pre-processing dataset from JSON to CSV
def pre_process_dataset(in_dataset:list, language:str) -> list:
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
    df = pd.DataFrame(out_dataset, columns=header)
    return df

# Post-processing dataset from CSV to CSV
def post_process_dataset(in_dataset:list, language:str) -> list:
    out_dataset = []
    
    # Return outcome
    return out_dataset