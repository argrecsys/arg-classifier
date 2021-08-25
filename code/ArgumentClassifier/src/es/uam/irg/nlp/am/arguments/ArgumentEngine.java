/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package es.uam.irg.nlp.am.arguments;

import edu.stanford.nlp.pipeline.*;
import es.uam.irg.ml.Constants;
import java.io.*;
import java.util.*;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author ansegura
 */
public class ArgumentEngine {
    
    // Class members
    private String language;
    private Properties props;
    
    /**
     * Class constructor.
     * 
     * @param lang
     */
    public ArgumentEngine(String lang) {
        this.language = lang;
        setProperties();
    }
    
    /**
     * 
     * @param docText
     * @return 
     */
    public CoreDocument createCoreNlpDocument(String docText) {
        StanfordCoreNLP pipeline = new StanfordCoreNLP(this.props);
        CoreDocument document = pipeline.processToCoreDocument(docText);
        return document;
    }
    
    /**
     *
     * @return
     */
    public String getCurrentLanguage() {
        return this.language;
    }
    
    /**
     * Divides a paragraph into sentences.
     * 
     * @param docText a string representing the text of a document (a paragraph).
     * @return 
     */
    public List<String> getSentences(String docText) {
        List<String> sentences = new ArrayList<>();
        
        CoreDocument nlpDoc = createCoreNlpDocument(docText);
        nlpDoc.sentences().forEach(sent -> {
            sentences.add(sent.text());
        });
        
        return sentences;
    }
    
    /**
     * Configures CoreNLP properties according to the specified language.
     */
    private void setProperties() {
        this.props = new Properties();
        
        try {
            if (language.equals(Constants.LANG_EN)) {
                this.props.setProperty("annotators", "tokenize, ssplit, pos, lemma, ner, parse, dcoref, sentiment");
            }
            else if (language.equals(Constants.LANG_ES)) {
                this.props.load(new FileInputStream(Constants.SPANISH_PROPERTIES));
            }
            
        } catch (FileNotFoundException ex) {
            Logger.getLogger(ArgumentEngine.class.getName()).log(Level.SEVERE, null, ex);
        } catch (IOException ex) {
            Logger.getLogger(ArgumentEngine.class.getName()).log(Level.SEVERE, null, ex);
        }
    }
    
}
