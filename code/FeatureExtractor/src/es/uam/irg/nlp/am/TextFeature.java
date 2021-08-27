/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package es.uam.irg.nlp.am;

import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.pipeline.CoreDocument;
import es.uam.irg.utils.FunctionUtils;
import java.util.ArrayList;
import java.util.List;

/**
 *
 * @author ansegura
 */
public class TextFeature {
    
    public final static int MIN_LENGTH = 3;
    
    // Class variables
    private List<String> adverbs;    
    private int avgWordLength;
    private List<String> bigrams;
    private boolean isValid;
    private List<String> keyWords;
    private List<String> modalAuxs;
    private CoreDocument nlpDoc;
    private int numberPunctMarks;
    private int numberSubclauses;
    private int parseTreeDepth;
    private List<String> punctuation;
    private String text;
    private int textLength;
    private List<String> trigrams;
    private List<String> unigrams;
    private List<String> verbs;
    private List<String> wordCouples;
    
    /**
     * 
     * @param nlpDoc 
     */
    public TextFeature(CoreDocument nlpDoc) {
        this.nlpDoc = nlpDoc;
        this.text = this.nlpDoc.text();
        this.textLength = this.text.length();
        this.unigrams = new ArrayList<>();
        this.bigrams = new ArrayList<>();
        this.trigrams = new ArrayList<>();
        this.adverbs = new ArrayList<>();
        this.verbs = new ArrayList<>();
        this.modalAuxs = new ArrayList<>();
        this.wordCouples = new ArrayList<>();
        this.punctuation = new ArrayList<>();
        this.keyWords = new ArrayList<>();
        this.isValid = false;
    }
    
    /**
     * 
     * @return 
     */
    public boolean isValid() {
        return this.isValid;
    }
    
    /**
     * 
     */
    public void process() {
        
        // NLP-processing
        if (this.textLength >= MIN_LENGTH) {
            extractFeatures();            
            this.isValid = true;
        }
    }
    
    /**
     * 
     * @return 
     */
    @Override
    public String toString() {
        String str = "{'unigrams': %s, 'bigrams': %s, 'trigrams': %s, 'adverbs': %s, 'verbs': %s, 'modal_aux': %s,"
                   + " 'word_couples': %s, 'punctuation': %s, 'key_words': %s, 'text_length': %d, 'avg_word_length': %d,"
                   + " 'number_punct_marks': %d, 'parse_tree_depth': %d, 'number_sub_clauses': %d}";
        str = String.format(str, listToString(unigrams), listToString(bigrams), listToString(trigrams), listToString(adverbs), 
                listToString(verbs), listToString(modalAuxs), listToString(wordCouples), listToString(punctuation), 
                listToString(keyWords), textLength, avgWordLength, numberPunctMarks, parseTreeDepth, numberSubclauses);
        return str;
    }
    /**
     * 
     */
    private void extractFeatures() {
        String currWord;
        String posTag;
        
        for (CoreLabel token : this.nlpDoc.tokens()) {
            currWord = token.word();
            posTag = token.tag();
            
            // Adding words
            if (!posTag.equals("PUNCT")) {
                this.unigrams.add(currWord);
                this.avgWordLength += currWord.length();
            }
            
            // Adding POS tags
            if (posTag.equals("ADV")) {
                this.adverbs.add(currWord);
            }
            else if (posTag.equals("VERB")) {
                this.verbs.add(currWord);
            }
            else if (posTag.equals("AUX")) {
                this.modalAuxs.add(currWord);
            }
            else if (posTag.equals("PUNCT")) {
                this.punctuation.add(currWord);
            }
        }
        
        if (this.unigrams.size() > 0) {
            this.avgWordLength /= this.unigrams.size();
            this.numberPunctMarks = this.punctuation.size();
            
            String bigram;
            String trigram;
            String wordN_1 = "";
            String wordN_2 = "";
            for (String word : this.unigrams) {

                if (!wordN_1.equals("")) {
                    bigram = wordN_1 + "-" + word;
                    this.bigrams.add(bigram);

                    if (!wordN_2.equals("")) {
                        trigram = wordN_2 + "-" + wordN_1 + "-" + word;
                        this.trigrams.add(trigram);
                    }
                }
                wordN_2 = wordN_1;
                wordN_1 = word;
            }
        }
        
    }
    
    /**
     * 
     * @param list
     * @return 
     */
    private String listToString(List<String> list) {
        return "[" + FunctionUtils.listToString(list) + "]";
    }
    
}
