# -*- coding: utf-8 -*-
"""
    Created by: Andrés Segura-Tinoco
    Version: 0.6.0
    Created on: May 13, 2022
    Updated on: Jun 2, 2022
    Description: Data processing module
"""

# Import Python base libraries
import pandas as pd
from typing import Final

# Class constants
BREAK_MARKS: Final[set] = {'.', ';'}
LABEL_INTENTS: Final[set] = {'SUPPORT', 'ATTACK'}
LABEL_LINKS: Final[str] = 'LINKS'
LABEL_MAJOR_CLAIM: Final[str] = 'MAJOR_CLAIM'
LABEL_NO: Final[str] = 'NO'
LABEL_NONE: Final[str] = 'NONE'
LABEL_PREMISE: Final[str] = 'PREMISE'
LABEL_SPAM: Final[str] = 'SPAM'
LABEL_YES: Final[str] = 'YES'
VALID_SENT_SIZE: Final[int] = 3

# Validates whether a statement is valid or not
def __is_valid_sentence(sent_text:str) -> bool:
    result = (len(sent_text) >= VALID_SENT_SIZE) and (any(c.isalpha() for c in sent_text))
    return result

# Find the relation category between the claim and the premise and its main intent
def __find_relations(label2:str, lbl_start:int, lbl_end:int, relations:list) -> str:
    rel_categories = []
    
    if label2 == LABEL_PREMISE:
        for rel in relations:
            source = rel['head_span'] if rel['head_span']['label'] == LABEL_PREMISE else rel['child_span']
            
            if source['start'] == lbl_start and source['end'] == lbl_end:
                label = rel['label']
                if (label not in LABEL_INTENTS) and (label != LABEL_LINKS):
                    rel_categories.append(label)
    
    rel_category = 'NONE'
    if len(rel_categories):
        rel_category = rel_categories[0]
    
    return rel_category

# Pre-processing dataset from JSON to CSV
def pre_process_dataset(in_dataset:list, language:str) -> list:
    out_dataset = []
    header = ["sent_id", "sent_text", "sent_label1", "sent_label2", "sent_label3"]
    
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
        relations = row['relations']
        
        # Identify break marks
        break_marks = [token for token in tokens if token['text'] in BREAK_MARKS]
        if len(break_marks) == 0:
            break_marks = [{'text': '.', 'start': 0, 'end': len(text), 'id': len(tokens), 'ws': True, 'disabled': False}]
            
        # Annotate sentences
        sent_id = 0
        sent_text = ''
        ix_start = 0
        for mark in break_marks:
            ix_end = mark['end']
            sent_text = text[ix_start : ix_end]
            sent_text = sent_text.strip()
            
            # It is a valid sentence
            if __is_valid_sentence(sent_text):
                labels = []
                cache = []
                
                for span in spans:
                    lbl_start = span['start']
                    lbl_end = span['end']
                    
                    if lbl_start >= ix_start and lbl_end <= ix_end:
                        label2 = span['label']
                        if label2 not in cache and label2 != "LINKER":
                            label3 = __find_relations(label2, lbl_start, lbl_end, relations)
                            labels.append((label2, label3))
                            cache.append(label2)
                
                if len(labels) == 0:
                    labels.append((LABEL_SPAM, LABEL_NONE))
                
                # Save outcome
                for i, label in enumerate(labels):
                    label2, label3 = label
                    
                    if label2 != LABEL_MAJOR_CLAIM:
                        record_id = proposal_id + "-" + comment_id + "-" + str(sent_id) + "-" + str(i)
                        label1 = LABEL_NO if label2 == LABEL_SPAM else LABEL_YES
                        out_dataset.append([record_id, sent_text, label1, label2, label3])
                
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
