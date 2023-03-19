# -*- coding: utf-8 -*-
"""
    Created by: Andrés Segura-Tinoco
    Version: 0.10.0
    Created on: May 13, 2022
    Updated on: Mar 19, 2023
    Description: Data processing module
"""

# Import Python base libraries
import pandas as pd
import spacy
from typing import Final

# Class constants basic
BREAK_MARKS: Final[set] = {".", ";"}
VALID_SENT_SIZE: Final[int] = 3

# Class constants label 1
LABEL_YES: Final[str] = "YES"
LABEL_NO: Final[str] = "NO"

# Class constants label 2
LABEL_MAJOR_CLAIM: Final[str] = "MAJOR_CLAIM"
LABEL_CLAIM: Final[str] = "CLAIM"
LABEL_PREMISE: Final[str] = "PREMISE"
LABEL_SPAM: Final[str] = "SPAM"
LABEL_LINKER: Final[str] = "LINKER"

# Class constants label 2
LABEL_INTENTS: Final[set] = {"SUPPORT", "ATTACK", "LINKS"}
LABEL_NONE: Final[str] = "NONE"

# spaCy Spanish large model
spacy_nlp = spacy.load("es_core_news_lg")

# Validates whether a statement is valid or not
def __is_valid_sentence(sent_text:str) -> bool:
    n_tokens = len(sent_text.split(" "))
    if (len(sent_text) >= VALID_SENT_SIZE) and (any(c.isalpha() for c in sent_text)) and (n_tokens >= 2):
        return True
    return False

# Find the (ARGAEL) relation category between the claim and the premise and its main intent
def __find_argael_relation(ac_id:str, relations:list, rel_type:str) -> str:
    rel_categories = []
    
    for rel in relations:
        ac_id2 = rel[2]
        rel_name = rel[3]
        if ac_id == ac_id2:
            rel_categories.append(rel_name)
    
    rel_category = LABEL_NONE
    if len(rel_categories):
        tokens = rel_categories[0].upper().split(":")
        if rel_type == "CATEGORY":
            rel_category = tokens[0]
        else:
            rel_category = tokens[1].strip()
    
    return rel_category

# Find the (Prodigy) relation category between the claim and the premise and its main intent
def __find_prodigy_relation(label2:str, lbl_start:int, lbl_end:int, relations:list) -> str:
    rel_categories = []
    
    if label2 == LABEL_PREMISE:
        for rel in relations:
            source = rel["head_span"] if rel["head_span"]["label"] == LABEL_PREMISE else rel["child_span"]
            
            if source["start"] == lbl_start and source["end"] == lbl_end:
                label = rel["label"]
                if label not in LABEL_INTENTS:
                    rel_categories.append(label)
    
    rel_category = LABEL_NONE
    if len(rel_categories):
        rel_category = rel_categories[0]
    
    return rel_category

# Pre-processing dataset from a list of CSV files to an unique CSV file
def pre_process_argael_dataset(proposals:list, annotations:dict, language:str) -> list:
    dataset = []
    header = ["sent_id", "sent_text", "sent_label1", "sent_label2", "sent_label3"]
    
    for doc_id in annotations.keys():        
        doc_id = str(doc_id)
        proposal = proposals[doc_id]
        annotation = annotations[doc_id]
        arg_comps = annotation["comp"]
        arg_rels = annotation["rel"]
        
        # for-in loop
        proposal_id = "0"
        comment_id = "0"
        for row in proposal:
        
            # Read basic info
            if "proposal_id" in row:
                proposal_id = row["proposal_id"]
            elif "comment_id" in row:
                comment_id = row["comment_id"]
            text = row["text"].strip()
            
            # Use spaCy to split sentences
            sp_doc = spacy_nlp(text)
            sentences = sp_doc.sents
            
            # Annotate sentences
            sent_text = ""
            sent_id = 0
            
            for sent_text in sentences:
                record_id = proposal_id + "-" + comment_id + "-" + str(sent_id)
                sent_text = str(sent_text).strip()
                sent_len = len(sent_text)
                
                # If it is a valid sentence
                if __is_valid_sentence(sent_text):
                    
                    # Select candidate labels
                    sent_labels = []
                    for ac in arg_comps:
                        ac_id = ac[0]
                        ac_text = ac[1]
                        ac_type = ac[2]
                        
                        # If a statement wraps a span or if a span wraps a statement...
                        label2 = LABEL_SPAM
                        if (sent_text in ac_text) or (ac_text in sent_text):
                            label2 = ac_type.upper().replace(" ", "_")
                            label1 = LABEL_NO if label2 == LABEL_SPAM else LABEL_YES
                            label2 = LABEL_CLAIM if label2 == LABEL_MAJOR_CLAIM else label2
                            label3 = __find_argael_relation(ac_id, arg_rels, "SUB_CATEGORY")
                            labels = {"label1": label1, "label2": label2, "label3": label3, "len": len(ac_text)}
                            sent_labels.append(labels)
                    
                    if len(sent_labels) == 0:
                        labels = {"label1": LABEL_NO, "label2": LABEL_SPAM, "label3": LABEL_NONE, "len": sent_len}
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
                    dataset.append([record_id, sent_text, label1, label2, label3])
                    
                    # Update sentence number
                    sent_id += 1
                    
                else:
                    # Invalid sentence
                    print(" - Invalid:", record_id, sent_text)

    # Return outcome
    df = pd.DataFrame(dataset, columns=header)
    return df

# Pre-processing dataset from a list of JSON files to an unique CSV file
def pre_process_prodigy_dataset(annotations:list, language:str) -> list:
    dataset = []
    header = ["sent_id", "sent_text", "sent_label1", "sent_label2", "sent_label3"]
    
    # for-in loop
    proposal_id = "0"
    comment_id = "0"
    for row in annotations:
        
        # Read basic info
        if "proposal_id" in row:
            proposal_id = row["proposal_id"]
        elif "comment_id" in row:
            comment_id = row["comment_id"]
        text = row["text"].strip()
        tokens = row["tokens"]
        spans = row["spans"]
        relations = row["relations"]
        
        # Identify break marks
        break_marks = [token for token in tokens if token["text"] in BREAK_MARKS]
        if len(break_marks) == 0:
            break_marks = [{"text": ".", "start": 0, "end": len(text), "id": len(tokens), "ws": True, "disabled": False}]
        elif tokens[-1]["text"] not in BREAK_MARKS:
            break_marks.append({"text": "", "start": len(text)-1, "end": len(text), "id": len(tokens), "ws": True, "disabled": False})
        
        # Annotate sentences
        sent_text = ""
        sent_id = 0
        ix_start = 0
        
        for mark in break_marks:
            record_id = proposal_id + "-" + comment_id + "-" + str(sent_id)
            ix_end = mark["end"]
            sent_text = text[ix_start : ix_end]
            sent_text = sent_text.strip()
            sent_len = ix_end - ix_start
            
            # If it is a valid sentence
            if __is_valid_sentence(sent_text):
                
                # Select candidate labels
                sent_labels = []
                for span in spans:
                    lbl_start = span["start"]
                    lbl_end = span["end"]
                    
                    # If a statement wraps a span or if a span wraps a statement...
                    if (lbl_start >= ix_start and lbl_end <= ix_end) or (ix_start >= lbl_start and ix_end <= lbl_end):
                        label2 = span["label"]
                        
                        if label2 != LABEL_LINKER:
                            label1 = LABEL_NO if label2 == LABEL_SPAM else LABEL_YES
                            label2 = LABEL_CLAIM if label2 == LABEL_MAJOR_CLAIM else label2
                            label3 = __find_prodigy_relation(label2, lbl_start, lbl_end, relations)
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
                dataset.append([record_id, sent_text, label1, label2, label3])
                
                # Update sentence number
                sent_id += 1
                
            else:
                # Invalid sentence
                print(" - Invalid:", record_id, sent_text)
                
            # Update start index
            ix_start = ix_end + 1
    
    # Return outcome
    df = pd.DataFrame(dataset, columns=header)
    return df

# Post-processing dataset from CSV to CSV
def post_process_dataset(in_dataset:list, language:str) -> list:
    out_dataset = []
    
    # Return outcome
    return out_dataset
