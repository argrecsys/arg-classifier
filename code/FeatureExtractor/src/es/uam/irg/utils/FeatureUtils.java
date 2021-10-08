/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package es.uam.irg.utils;

import es.uam.irg.nlp.am.Constants;
import es.uam.irg.nlp.am.arguments.ArgumentEngine;
import es.uam.irg.nlp.am.arguments.ArgumentLinker;
import java.util.ArrayList;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author ansegura
 */
public class FeatureUtils {
    
    /**
     * 
     * @param tokens
     * @param lexicon
     * @return 
     */
    public static List<String> getUsedLinkerList(String[] tokens, List<ArgumentLinker> lexicon) {
        List<String> linkers = new ArrayList<>();
        String nGram;
        
        for (int i = 0; i < tokens.length; i++) {
            for (ArgumentLinker linker : lexicon) {
                nGram = getNGram(tokens, i, i + linker.nTokens);
                
                if (linker.isEquals(nGram) && !linkers.contains(linker.linker)) {
                    linkers.add(linker.linker);
                    i += linker.nTokens - 1;
                    break;
                }
            }
        }
        
        return linkers;
    }
    
    /**
     * 
     * @param tokens
     * @return 
     */
    public static List<String> getWordCouples(String[] tokens) {
        List<String> wordCouples = new ArrayList<>();
        
        return wordCouples;
    }
    
        /**
     * 
     * @param tokens
     * @param ixStart
     * @param nTokens
     * @return 
     */
    private static String getNGram(String[] tokens, int ixStart, int nTokens) {
        String nGram = "";
        
        try {
            if (tokens.length > 0) {
                String[] subList = FunctionUtils.getSubArray(tokens, ixStart, nTokens);
                nGram = FunctionUtils.arrayToString(subList, Constants.NGRAMS_DELIMITER);
            }
        }
        catch (Exception ex) {
            Logger.getLogger(ArgumentEngine.class.getName()).log(Level.SEVERE, null, ex);
        }
        
        return nGram.toLowerCase();
    }
    
}