/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package es.uam.irg.clf;

import es.uam.irg.ml.Dataset;
import es.uam.irg.nlp.am.arguments.Proposition;
import java.util.List;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author ansegura
 */
public class ArgumentClassifier {
    
    // Class members
    private String language;
    private boolean verbose = true;
    // private Map<String, Object> mdbSetup;
    // private Map<String, Object> msqlSetup;
    
    /**
     * Class constructor.
     * 
     * @param language
     * @param verbose 
     */
    public ArgumentClassifier(String language, boolean verbose) {
        this.language = language;
        this.verbose = verbose;
        // this.mdbSetup = FunctionUtils.getDatabaseConfiguration(Constants.MONGO_DB);
        // this.msqlSetup = FunctionUtils.getDatabaseConfiguration(Constants.MYSQL_DB);
    }
    
    /**
     * 
     * @return 
     */
    public boolean runProgram() {
        boolean result = false;
        
        // ML pipeline
        try {
            // 1. Get raw dataset
            Dataset ds = new Dataset(this.verbose);
            ds.createDataset();
            List<Proposition> rawData = ds.getDataset();
            System.out.println(rawData);
            
            // 2. Transform dataset
            //var data = processDataset();
            
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
    
}
