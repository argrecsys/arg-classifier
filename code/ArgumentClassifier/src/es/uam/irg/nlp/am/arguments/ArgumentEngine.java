/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package es.uam.irg.nlp.am.arguments;

import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.pipeline.*;
import edu.stanford.nlp.util.CoreMap;
import es.uam.irg.clf.Constants;
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
     * Divides a paragraph into sentences.
     * 
     * @param docText a string representing the text of a document (a paragraph).
     * @return 
     */
    public List<String> getSentences(String docText) {
        List<String> sentences = new ArrayList<>();
        
        StanfordCoreNLP pipeline = new StanfordCoreNLP(this.props);
        Annotation annotation = new Annotation(docText);
        pipeline.annotate(annotation);
        
        List<CoreMap> coreSents = annotation.get(CoreAnnotations.SentencesAnnotation.class);
        for (int i = 0; i < coreSents.size(); i++) {
            CoreMap sentence = coreSents.get(i);
            String sentenceText = sentence.toString();
            sentences.add(sentenceText);
        }
        
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
