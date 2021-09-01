/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package es.uam.irg.nlp.am;

/**
 *
 * @author ansegura
 */
public class Program {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // TODO code application logic here
        System.out.println(">> FEAT-EXTRACTOR BEGINS");
        
        // Program hyperparameters with default values
        String language = Constants.LANG_ES;
        String extractionMode = FeatureExtractor.Mode.ARG_DET.name();
        boolean createDataset = false;
        
        // Read input parameters
        if (args.length > 0) {
            language = args[0].toLowerCase();
            
            if (args.length > 1) {
                extractionMode = args[1].toUpperCase();
                
                if (args.length > 2) {
                    createDataset = Boolean.parseBoolean(args[2]);
                }
            }
        }
        System.out.format(">> Language selected: %s, extraction mode: %s and create dataset: %s\n", 
                language, extractionMode, createDataset);
        
        // Run program
        FeatureExtractor miner = new FeatureExtractor(language, createDataset);
        boolean result = miner.runProgram(extractionMode);
        
        if (result) {
            System.out.println(">> The Feature Extractor engine was executed correctly.");
        }
        else {
            System.err.println(">> The Feature Extractor engine had an unexpected error.");
        }
        
        System.out.println(">> FEAT-EXTRACTOR ENDS");
    }
    
}
