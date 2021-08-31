/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package es.uam.irg.nlp.am;

import es.uam.irg.io.Dataset;
import es.uam.irg.io.IOManager;
import es.uam.irg.nlp.am.arguments.ArgumentEngine;
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
    
    /**
     * Class constructor.
     * 
     * @param language
     * @param createDataset
     */
    public FeatureExtractor(String language, boolean createDataset) {
        this.argEngine = new ArgumentEngine(language);
        this.createDataset = createDataset;
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
            
            // 1. Create/get data (raw dataset)
            Dataset ds = new Dataset(this.argEngine);
            if (this.createDataset) {
                rawData = ds.createDataset();
            }
            else {
                rawData = ds.getDataset();
            }
            System.out.println(">> N proposition: " + rawData.size());
            
            // 2. Extract features (temp dataset)
            if (extractionMode.equals(Mode.ARG_DET.name())) {
                System.out.println(">> Argument detection features");
                features = extractArgumentDetectionFeatures(rawData);
            }
            else if (extractionMode.equals(Mode.ARG_CLF.name())) {
                System.out.println(">> Argument classification features");
                features = extractArgumentClassificationFeatures(rawData);
            }
            
            // 3. Save results (final dataset)
            if (features != null) {
                result = IOManager.saveTextFeatures(Constants.FEATURES_FILEPATH, features);
            }
        }
        catch (Exception ex) {
            Logger.getLogger(FeatureExtractor.class.getName()).log(Level.SEVERE, null, ex);
        }
        
        return result;
    }
    
    /**
     * 
     * @param rawData
     * @return 
     */
    private List<TextFeature> extractArgumentClassificationFeatures(List<Proposition> rawData) {
        return null;
    }

    /**
     * 
     * @param rawData
     * @return 
     */
    private List<TextFeature> extractArgumentDetectionFeatures(List<Proposition> rawData) {
        List<TextFeature> features = new ArrayList<>();
        int i = 0;
        for (Proposition prop : rawData) {
            if (i == 5) {
                break;
            }
            i++;
            
            TextFeature tf = new TextFeature(this.argEngine, prop.getText());
            
            tf.extraction();
            if (tf.isValid()) {
                features.add(tf);
            }
        }
        
        System.out.println(">> Total propositions: " + rawData.size());
        System.out.println(">> Total propositions with features: " + features.size());
        return features;
    }
    
    public static enum Mode {
        ARG_DET,
        ARG_CLF
    }
    
}
