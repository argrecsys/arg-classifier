/**
 * Copyright 2021
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
package es.uam.irg.io;

import es.uam.irg.nlp.am.arguments.ArgumentEngine;
import es.uam.irg.nlp.am.arguments.ArgumentLinker;
import es.uam.irg.nlp.am.arguments.Proposition;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Creates and returns the main dataset of the ML pipeline.
 */
public class Dataset {

    // Class constants
    private static final String DATASET_FILEPATH = "../../data/sentences.csv";

    // Class members
    private ArgumentEngine argEngine;
    private List<ArgumentLinker> lexicon;

    /**
     * Class constructor
     *
     * @param argEngine
     */
    public Dataset(ArgumentEngine argEngine) {
        this.argEngine = argEngine;
    }

    /**
     *
     * @return
     */
    public List<Proposition> getDataset() {
        List<Proposition> dataset = IOManager.readDatasetFromCsvFile(DATASET_FILEPATH);
        return dataset;
    }

    /**
     *
     * @return
     */
    private Map<Integer, Map<Integer, ArgumentLinker>> getSentencesWithArguments() {
        Map<Integer, Map<Integer, ArgumentLinker>> sentWithArgs = new HashMap<>();

//        try {
//            
//            Map<Integer, Argument> sentences = IOManager.readArgumentList();
//            System.out.println(">> Total sentences with arguments: " + sentences.size());
//
//            // Temp variables
//            String[] tokens;
//            int nTokens;
//            ArgumentLinker linker;
//
//            for (Document doc : sentences) {
//                tokens = doc.getString("argumentID").split("-");
//                nTokens = tokens.length;
//                linker = new ArgumentLinker(doc.get("linker", Document.class));
//
//                if (nTokens > 2) {
//                    int docID = Integer.parseInt(tokens[nTokens - 3]);
//                    int sentID = Integer.parseInt(tokens[nTokens - 2]);
//
//                    if (!sentWithArgs.containsKey(docID)) {
//                        sentWithArgs.put(docID, new HashMap<>());
//                    }
//                    if (!sentWithArgs.get(docID).containsKey(sentID)) {
//                        sentWithArgs.get(docID).put(sentID, linker);
//                    }
//                } else {
//                    System.out.println("-- ERROR!");
//                }
//            }
//        } catch (NumberFormatException ex) {
//            Logger.getLogger(FeatureExtractor.class.getName()).log(Level.SEVERE, null, ex);
//        }
        return sentWithArgs;
    }

}
