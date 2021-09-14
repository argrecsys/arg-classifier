/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package es.uam.irg.nlp.am;

import es.uam.irg.io.Dataset;
import es.uam.irg.io.IOManager;
import es.uam.irg.nlp.am.arguments.ArgumentEngine;
import es.uam.irg.nlp.am.arguments.ArgumentLinker;
import es.uam.irg.nlp.am.arguments.ArgumentLinkerManager;
import es.uam.irg.nlp.am.arguments.Proposition;
import java.util.ArrayList;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author ansegura
 */
public class FeatureExtractor {
    
    // Class members
    private final ArgumentEngine argEngine;
    private boolean createDataset;
    private ArgumentLinkerManager lnkManager;
    
    /**
     * Class constructor.
     * 
     * @param language
     * @param createDataset
     */
    public FeatureExtractor(String language, boolean createDataset) {
        this.argEngine = new ArgumentEngine(language);
        this.createDataset = createDataset;
        this.lnkManager = createLinkerManager(language);
    }
    
    /**
     *
     * @param extractionMode
     * @return 
     */
    public boolean runProgram(String extractionMode) {
        boolean result = false;
        
        // ML pipeline
        try {
            List<TextFeature> features = null;
            List<Proposition> rawData;
            
            // 1. Get lexicon of linkers
            List<ArgumentLinker> lexicon = this.lnkManager.getLexicon(true);
            
            // 2. Create/get data (raw dataset)
            Dataset ds = new Dataset(this.argEngine, lexicon);
            if (this.createDataset) {
                rawData = ds.createDataset();
            }
            else {
                rawData = ds.getDataset();
            }
            System.out.println(">> Total propositions: " + rawData.size());
            
            // 3. Extract features (temp dataset)
            if (extractionMode.equals(Mode.ARG_DET.name())) {
                System.out.println(">> Argument detection features");
                features = extractArgumentDetectionFeatures(rawData, lexicon);
            }
            else if (extractionMode.equals(Mode.ARG_CLF.name())) {
                System.out.println(">> Argument classification features");
                features = extractArgumentClassificationFeatures(rawData, lexicon);
            }
            
            // 4. Save results (final dataset)
            if (features != null) {
                System.out.println(">> Total propositions with features: " + features.size());
                result = IOManager.saveTextFeatures(Constants.FEATURES_FILEPATH, features);
            }
        }
        catch (Exception ex) {
            Logger.getLogger(FeatureExtractor.class.getName()).log(Level.SEVERE, null, ex);
        }
        
        return result;
    }
    
    /**
     * Create the linker manager object.
     *
     * @param lang
     * @param verbose
     * @return
     */
    private ArgumentLinkerManager createLinkerManager(String lang) {
        return IOManager.readLinkerTaxonomy(lang, true);
    }
    
    /**
     * 
     * @param rawData
     * @return 
     */
    private List<TextFeature> extractArgumentClassificationFeatures(List<Proposition> rawData, List<ArgumentLinker> lexicon) {
        return null;
    }

    /**
     * 
     * @param rawData
     * @return 
     */
    private List<TextFeature> extractArgumentDetectionFeatures(List<Proposition> rawData, List<ArgumentLinker> lexicon) {
        List<TextFeature> features = new ArrayList<>();
        
        for (Proposition prop : rawData) {
            TextFeature tf = new TextFeature(this.argEngine, lexicon, prop.getText());
            
            tf.extraction();
            if (tf.isValid()) {
                features.add(tf);
            }
        }
        
        return features;
    }
    
    public static enum Mode {
        ARG_DET,
        ARG_CLF
    }
    
}
