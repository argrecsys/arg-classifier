/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package es.uam.irg.ml;

import edu.stanford.nlp.pipeline.CoreDocument;
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
public class ArgumentClassifier {
    
    // Class members
    private boolean verbose = true;
    private ArgumentEngine argEngine;
    
    public static enum Mode {
        ARG_DET, 
        ARG_CLF
    }
    
    /**
     * Class constructor.
     * 
     * @param language
     * @param verbose 
     */
    public ArgumentClassifier(String language, boolean verbose) {
        this.argEngine = new ArgumentEngine(language);
        this.verbose = verbose;
    }
    
    /**
     *
     * @return 
     */
    public boolean runProgram(String mode) {
        boolean result = false;
        
        // ML pipeline
        try {
            // 1. Get raw dataset
            Dataset ds = new Dataset(this.argEngine, this.verbose);
            List<Proposition> rawData = ds.getDataset();
            System.out.println(">> N proposition: " + rawData.size());
            // System.out.println(rawData);
            
            // 2. Create model
            Object model = null;
            if (mode.equals(Mode.ARG_DET.name())) {
                System.out.println(">> Argument Detection");
                model = createArgumentDetectionModel(rawData);
            }
            else if (mode.equals(Mode.ARG_CLF.name())) {
                System.out.println(">> Argument Classification");
                model = createArgumentClassificationModel(rawData);
            }
            
            // 3. Train ML model
            //var classifier = createClassifier();
            
            // 4. Evaluate it
            
            result = true;
        }
        catch (Exception ex) {
            Logger.getLogger(ArgumentClassifier.class.getName()).log(Level.SEVERE, null, ex);
        }
        
        return result;
    }
    
    /**
     * 
     * @param rawData
     * @return 
     */
    private Object createArgumentClassificationModel(List<Proposition> rawData) {
        throw new UnsupportedOperationException("Not supported yet."); //To change body of generated methods, choose Tools | Templates.
    }

    /**
     * 
     * @param rawData
     * @return 
     */
    private Object createArgumentDetectionModel(List<Proposition> rawData) {
        List<TextFeature> features = new ArrayList<>();
        
        for (Proposition prop : rawData) {
            CoreDocument nlpDoc = this.argEngine.createCoreNlpDocument(prop.getText());
            TextFeature tf = new TextFeature(nlpDoc);
            tf.process();
            
            if (tf.isValid()) {
                features.add(tf);
            }
        }
        
        System.out.println("Total propositions: " + rawData.size());
        System.out.println("Total propositions with features: " + features.size());
        
        return null;
    }
    
}
