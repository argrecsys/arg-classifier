/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package es.uam.irg.utils;

import es.uam.irg.nlp.am.arguments.ArgumentEngine;
import es.uam.irg.nlp.am.arguments.ArgumentLinker;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author ansegura
 */
public class FeatureUtils {

    public static final String NGRAMS_DELIMITER = "-";

    /**
     *
     * @param vocabulary
     * @param lexicon
     * @return
     */
    public static List<String> getUsedLinkerList(List<String> vocabulary, List<ArgumentLinker> lexicon) {
        Set<String> linkers = new HashSet<>();
        String[] tokens = vocabulary.toArray(new String[0]);
        String nGram;

        for (int i = 0; i < tokens.length; i++) {
            for (ArgumentLinker linker : lexicon) {
                nGram = getNGram(tokens, i, i + linker.nTokens);

                if (linker.isEquals(nGram)) {
                    linkers.add(linker.linker);
                    i += linker.nTokens - 1;
                    break;
                }
            }
        }

        // Convert map keys to arraylist
        return FunctionUtils.listFromSet(linkers);
    }

    /**
     *
     * @param vocabulary
     * @return
     */
    public static List<String> getWordCouples(List<String> vocabulary) {
        Set<String> wordCouples = new HashSet<>();
        String wordPairs;

        for (int i = 0; i < vocabulary.size() - 1; i++) {
            for (int j = i + 1; j < vocabulary.size(); j++) {
                wordPairs = vocabulary.get(i) + "-" + vocabulary.get(j);
                wordCouples.add(wordPairs);
            }
        }

        // Convert map keys to arraylist
        return FunctionUtils.listFromSet(wordCouples);
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
                nGram = FunctionUtils.arrayToString(subList, NGRAMS_DELIMITER);
            }
        } catch (Exception ex) {
            Logger.getLogger(ArgumentEngine.class.getName()).log(Level.SEVERE, null, ex);
        }

        return nGram.toLowerCase();
    }

}
