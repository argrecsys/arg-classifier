/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package es.uam.irg.nlp.am;

import es.uam.irg.io.Dataset;
import edu.stanford.nlp.pipeline.CoreDocument;
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
    private boolean datasetExists;
    
    /**
     * Class constructor.
     * 
     * @param language
     * @param datasetExists
     */
    public FeatureExtractor(String language, boolean datasetExists) {
        this.argEngine = new ArgumentEngine(language);
        this.datasetExists = datasetExists;
    }
    
    /**
     *
     * @param mode
     * @return 
     */
    public boolean runProgram(String mode) {
        boolean result = false;
        
        // ML pipeline
        try {
            List<TextFeature> features = null;
            List<Proposition> rawData;
            
            // 1. Create/get data (raw dataset)
            Dataset ds = new Dataset(this.argEngine);
            if (this.datasetExists) {
                rawData = ds.getDataset();
            }
            else {
                rawData = ds.createDataset();
            }
            System.out.println(">> N proposition: " + rawData.size());
            
            // 2. Extract features (temp dataset)
            if (mode.equals(Mode.ARG_DET.name())) {
                System.out.println(">> Argument detection features");
                features = extractArgumentDetectionFeatures(rawData);
            }
            else if (mode.equals(Mode.ARG_CLF.name())) {
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
            CoreDocument nlpDoc = this.argEngine.createCoreNlpDocument(prop.getText());
            TextFeature tf = new TextFeature(nlpDoc, true);
            
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
