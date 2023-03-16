# -*- coding: utf-8 -*-
"""
    Created by: Andrés Segura-Tinoco
    Version: 0.9.2
    Created on: May 13, 2022
    Updated on: Mar 16, 2023
    Description: Data processing module
"""

# Import Python base libraries
import pandas as pd
from typing import Final

# Class constants basic
BREAK_MARKS: Final[set] = {'.', ';'}
VALID_SENT_SIZE: Final[int] = 3

# Class constants label 1
LABEL_YES: Final[str] = 'YES'
LABEL_NO: Final[str] = 'NO'

# Class constants label 2
LABEL_MAJOR_CLAIM: Final[str] = 'MAJOR_CLAIM'
LABEL_CLAIM: Final[str] = 'CLAIM'
LABEL_PREMISE: Final[str] = 'PREMISE'
LABEL_SPAM: Final[str] = 'SPAM'
LABEL_LINKER: Final[str] = 'LINKER'

# Class constants label 2
LABEL_INTENTS: Final[set] = {'SUPPORT', 'ATTACK', 'LINKS'}
LABEL_NONE: Final[str] = 'NONE'

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
                if label not in LABEL_INTENTS:
                    rel_categories.append(label)
    
    rel_category = 'NONE'
    if len(rel_categories):
        rel_category = rel_categories[0]
    
    return rel_category

# Pre-processing dataset from a list of CSV files to an unique CSV file
def pre_process_argael_dataset(raw_text:list, in_dataset:dict, language:str) -> list:
    out_dataset = []
    header = ["sent_id", "sent_text", "sent_label1", "sent_label2", "sent_label3"]
    
    doc_ids = in_dataset.keys()
    print(len(doc_ids))
    print(doc_ids)
    
    # Return outcome
    df = pd.DataFrame(out_dataset, columns=header)
    return df

# Pre-processing dataset from a list of JSON files to an unique CSV file
def pre_process_prodigy_dataset(in_dataset:list, language:str) -> list:
    out_dataset = []
    header = ["sent_id", "sent_text", "sent_label1", "sent_label2", "sent_label3"]
    
    # for-in loop
    proposal_id = '0'
    comment_id = '0'
    for row in in_dataset:
        
        # Read basic info
        if 'proposal_id' in row:
            proposal_id = row['proposal_id']
        elif 'comment_id' in row:
            comment_id = row['comment_id']
        text = row['text'].strip()
        tokens = row['tokens']
        spans = row['spans']
        relations = row['relations']
        
        # Identify break marks
        break_marks = [token for token in tokens if token['text'] in BREAK_MARKS]
        if len(break_marks) == 0:
            break_marks = [{'text': '.', 'start': 0, 'end': len(text), 'id': len(tokens), 'ws': True, 'disabled': False}]
        elif tokens[-1]['text'] not in BREAK_MARKS:
            break_marks.append({'text': '', 'start': len(text)-1, 'end': len(text), 'id': len(tokens), 'ws': True, 'disabled': False})
        
        # Annotate sentences
        sent_text = ''
        sent_id = 0
        ix_start = 0
        
        for mark in break_marks:
            record_id = proposal_id + "-" + comment_id + "-" + str(sent_id)
            ix_end = mark['end']
            sent_text = text[ix_start : ix_end]
            sent_text = sent_text.strip()
            sent_len = ix_end - ix_start
            
            # If it is a valid sentence
            if __is_valid_sentence(sent_text):
                
                # Select candidate labels
                sent_labels = []
                for span in spans:
                    lbl_start = span['start']
                    lbl_end = span['end']
                    
                    # If a statement wraps a span or if a span wraps a statement...
                    if (lbl_start >= ix_start and lbl_end <= ix_end) or (ix_start >= lbl_start and ix_end <= lbl_end):
                        label2 = span['label']
                        
                        if label2 != LABEL_LINKER:
                            label1 = LABEL_NO if label2 == LABEL_SPAM else LABEL_YES
                            label2 = LABEL_CLAIM if label2 == LABEL_MAJOR_CLAIM else label2
                            label3 = __find_relations(label2, lbl_start, lbl_end, relations)
                            labels = {"label1": label1, "label2": label2, "label3": label3, "len": (lbl_end - lbl_start)}
                            sent_labels.append(labels)
                
                if len(sent_labels) == 0:
                    labels = {"label1": LABEL_NO, "label2": LABEL_SPAM, "label3": LABEL_NONE, "len": (ix_end - ix_start)}
                    sent_labels.append(labels)
                
                # Select more representative label
                sent_label = {}
                sent_share = {}
                max_share = 0
                for label in sent_labels:
                    curr_label = label["label2"]
                    curr_share = sent_share.get(curr_label, 0) + (label["len"] / sent_len)
                    sent_share[curr_label] = curr_share
                    
                    if curr_share > max_share:
                        max_share = curr_share
                        sent_label = label
                
                # Save outcome
                label1 = sent_label["label1"]
                label2 = sent_label["label2"]
                label3 = sent_label["label3"]
                out_dataset.append([record_id, sent_text, label1, label2, label3])
                
                # Update sentence number
                sent_id += 1
                
            else:
                # Invalid sentence
                print(" - Invalid:", record_id, sent_text)
                
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
