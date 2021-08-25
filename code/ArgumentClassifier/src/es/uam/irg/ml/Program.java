/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package es.uam.irg.ml;

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
        System.out.println(">> ARG-CLASSIFIER BEGINS");
        
        // Program hyperparameters with default values
        String language = Constants.LANG_ES;
        String mode = ArgumentClassifier.Mode.ARG_DET.name();
        
        // Read input parameters
        if (args.length > 0) {
            language = args[0].toLowerCase();
            
            if (args.length > 1) {
                mode = args[1].toUpperCase();
            }
        }
        System.out.format(">> Language selected: %s\n", language);
        
        // Run program
        ArgumentClassifier miner = new ArgumentClassifier(language, true);
        boolean result = miner.runProgram(mode);
        
        if (result) {
            System.out.println(">> The Argument Classifier engine was executed correctly.");
        }
        else {
            System.err.println(">> The Argument Classifier engine had an unexpected error.");
        }
        
        System.out.println(">> ARG-CLASSIFIER ENDS");
    }
    
}
