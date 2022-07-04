/**
 * Copyright 2022
 * Andrés Segura-Tinoco
 * Information Retrieval Group at Universidad Autonoma de Madrid
 *
 * This is free software: you can redistribute it and/or modify it under the
 * terms of the GNU General Public License as published by the Free Software
 * Foundation, either version 3 of the License, or (at your option) any later
 * version.
 *
 * This software is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 * FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along with
 * the current software. If not, see <http://www.gnu.org/licenses/>.
 */
package es.uam.irg.nlp.am;

import es.uam.irg.utils.InitParams;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.HashSet;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * Alternative starting point of the argument mining module.
 */
public class SimpleProgram {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // TODO code application logic here
        System.out.println(">> SIMPLE FEAT-EXTRACTION BEGINS");

        // Program hyperparameters from JSON config file
        Map<String, Object> params = InitParams.readInitParams();
        String language = (String) params.get("language");
        Map<String, HashSet<String>> linkers = (Map<String, HashSet<String>>) params.get("linkers");
        HashSet<String> validLinkers = linkers.get("validLinkers");
        HashSet<String> invalidLinkers = linkers.get("invalidLinkers");
        System.out.format(">> Analysis language: %s, Valid linkers: %s, Invalid linkers: %s\n",
                language, validLinkers, invalidLinkers);

        // Run program
        FeatureExtractor miner = new FeatureExtractor(language, validLinkers, invalidLinkers);
        String inputText = getInputText();
        String resultText = miner.simpleFeatExtraction(inputText);

        if (!resultText.isEmpty()) {
            System.out.println(String.format(">> Text Features: \n%s", resultText));
        } else {
            System.err.println(">> The Feature Extractor engine had an unexpected error.");
        }

        System.out.println(">> SIMPLE FEAT-EXTRACTION ENDS");
    }

    /**
     *
     * @return
     */
    private static String getInputText() {
        String text = "";
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        try {
            System.out.println(">> Enter the input text: ");
            text = br.readLine();
        } catch (IOException ex) {
            Logger.getLogger(SimpleProgram.class.getName()).log(Level.SEVERE, null, ex);
        }
        return text;
    }

}
