/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package es.uam.irg.nlp.am;

import es.uam.irg.utils.FeatureUtils;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.pipeline.CoreDocument;
import edu.stanford.nlp.trees.Tree;
import es.uam.irg.nlp.am.arguments.ArgumentEngine;
import es.uam.irg.nlp.am.arguments.ArgumentLinker;
import es.uam.irg.nlp.am.arguments.Phrase;
import es.uam.irg.utils.FunctionUtils;
import java.util.ArrayList;
import java.util.List;

/**
 *
 * @author ansegura
 */
public class TextFeature {
    
    // Class contants
    public final static int MIN_LENGTH = 3;
    
    // Class variables
    private List<String> adverbs;    
    private ArgumentEngine argEngine;
    private int avgWordLength;
    private List<String> bigrams;
    private String id;
    private boolean isValid;
    private List<String> keyWords;
    private List<ArgumentLinker> lexicon;
    private List<String> modalAuxs;
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
     * @param argEngine
     * @param lexicon
     * @param text
     */
    public TextFeature(ArgumentEngine argEngine, List<ArgumentLinker> lexicon, String id, String text) {
        this.argEngine = argEngine;
        this.lexicon = lexicon;
        this.id = id;
        this.text = text;
        this.unigrams = new ArrayList<>();
        this.bigrams = new ArrayList<>();
        this.trigrams = new ArrayList<>();
        this.adverbs = new ArrayList<>();
        this.verbs = new ArrayList<>();
        this.modalAuxs = new ArrayList<>();
        this.wordCouples = new ArrayList<>();
        this.punctuation = new ArrayList<>();
        this.keyWords = new ArrayList<>();
        this.textLength = text.length();
        this.avgWordLength = 0;
        this.numberPunctMarks = 0;
        this.parseTreeDepth = 0;
        this.numberSubclauses = 0;
        this.isValid = false;
    }
    
    /**
     * 
     */
    public void extraction() {
        
        // NLP-processing
        if (this.textLength >= MIN_LENGTH) {
            extractFeatures();
        }
    }
    
    public String getID() {
        return this.id;
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
     * @return 
     */
    @Override
    public String toString() {
        String str = "{\"unigrams\": %s, \"bigrams\": %s, \"trigrams\": %s, \"adverbs\": %s, \"verbs\": %s, \"modal_aux\": %s,"
                   + " \"word_couples\": %s, \"punctuation\": %s, \"key_words\": %s, \"text_length\": %d, \"avg_word_length\": %d,"
                   + " \"number_punct_marks\": %d, \"parse_tree_depth\": %d, \"number_sub_clauses\": %d}";
        str = String.format(str, listToString(unigrams), listToString(bigrams), listToString(trigrams), listToString(adverbs), 
                listToString(verbs), listToString(modalAuxs), listToString(wordCouples), listToString(punctuation), 
                listToString(keyWords), textLength, avgWordLength, numberPunctMarks, parseTreeDepth, numberSubclauses);
        return str;
    }
    
    /**
     * 
     */
    private void extractFeatures() {
        CoreDocument nlpDoc = this.argEngine.createCoreNlpDocument(this.text);
        String currWord;
        String posTag;
        
        // 1. Split sentences into words
        for (CoreLabel token : nlpDoc.tokens()) {
            currWord = token.word();
            posTag = token.tag();
            
            // Adding words
            if (posTag.equals("PUNCT") || currWord.equals("'")) {
                this.punctuation.add(currWord);
            }
            else {
                this.unigrams.add(currWord);
                this.avgWordLength += currWord.length();
                
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
            }
        }
        
        // 2. If the sentence has valid words...
        if (this.unigrams.size() > 0) {
            this.avgWordLength /= this.unigrams.size();
            this.numberPunctMarks = this.punctuation.size();
            
            // 2.1 Group them into n-grams
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
            
            // 2.2. Create the parse tree
            List<Phrase> phraseList = getPhraseList();
            
            for (Phrase frase : phraseList) {
                if (frase.depth > this.parseTreeDepth) {
                    this.parseTreeDepth = frase.depth;
                }
            }
            this.numberSubclauses = phraseList.size();
            
            // 2.3. Group them into couple-of-words
            String[] tokens = this.unigrams.toArray(new String[0]);
            this.wordCouples = FeatureUtils.getWordCouples(tokens);
            
            // 2.4. Get list of keywords
            this.keyWords = FeatureUtils.getUsedLinkerList(tokens, this.lexicon);
            
            // 2.5. Save state
            this.isValid = true;
        }
        
    }
    
    /**
     * Get phrase list.
     * @return 
     */
    private List<Phrase> getPhraseList() {
        Tree tree = this.argEngine.getTree(this.text);
        List<Phrase> phraseList = this.argEngine.getPhraseList(tree);
        return phraseList;
    }
    
    /**
     * 
     * @param list
     * @return 
     */
    private String listToString(List<String> list) {
        String separator = "\"";
        String result = FunctionUtils.listToString(list, separator);
        if (result.equals("\"\"")) {
            result = "";
        }
        return "[" + result + "]";
    }
    
}
