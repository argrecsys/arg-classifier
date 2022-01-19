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
package es.uam.irg.nlp.am;

import es.uam.irg.io.Dataset;
import es.uam.irg.io.IOManager;
import es.uam.irg.nlp.am.arguments.ArgumentEngine;
import es.uam.irg.nlp.am.arguments.ArgumentLinker;
import es.uam.irg.nlp.am.arguments.ArgumentLinkerManager;
import es.uam.irg.nlp.am.arguments.Proposition;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author ansegura
 */
public class FeatureExtractor {
    
    // Class constants
    private static final String ARG_CLF = "classification";
    private static final String ARG_DET = "detection";
    private static final String FEATURES_FILEPATH = "../../dataset/features.json";
    private static final boolean VERBOSE = true;

    // Class members
    private final ArgumentEngine argEngine;
    private final boolean createDataset;
    private final ArgumentLinkerManager lnkManager;

    /**
     * Class constructor.
     *
     * @param language
     * @param createDataset
     * @param validLinkers
     * @param invalidLinkers
     */
    public FeatureExtractor(String language, boolean createDataset, HashSet<String> validLinkers, HashSet<String> invalidLinkers) {
        this.argEngine = new ArgumentEngine(language);
        this.createDataset = createDataset;
        this.lnkManager = createLinkerManager(language, validLinkers, invalidLinkers);
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

            // 1. Get lexicon of linkers
            List<ArgumentLinker> lexicon = this.lnkManager.getLexicon(true);

            // 2. Create/get data (raw dataset)
            Dataset ds = new Dataset(this.argEngine, lexicon);
            if (this.createDataset) {
                rawData = ds.createDataset();
            } else {
                rawData = ds.getDataset();
            }
            System.out.println(">> Total propositions: " + rawData.size());

            // 3. Extract features (temp dataset)
            if (extractionMode.equals(ARG_DET)) {
                System.out.println(">> Argument detection features");
                features = extractArgumentDetectionFeatures(rawData, lexicon);
            } else if (extractionMode.equals(ARG_CLF)) {
                System.out.println(">> Argument classification features");
                features = extractArgumentClassificationFeatures(rawData, lexicon);
            }

            // 4. Save results (final dataset)
            if (features != null) {
                System.out.println(">> Total propositions with features: " + features.size());
                result = IOManager.saveTextFeatures(FEATURES_FILEPATH, features);
            }
        } catch (Exception ex) {
            Logger.getLogger(FeatureExtractor.class.getName()).log(Level.SEVERE, null, ex);
        }

        return result;
    }

    /**
     * Create the linker manager object.
     *
     * @param lang
     * @param validLinkers
     * @param invalidLinkers
     * @return
     */
    private ArgumentLinkerManager createLinkerManager(String lang, HashSet<String> validLinkers, HashSet<String> invalidLinkers) {
        return IOManager.readLinkerTaxonomy(lang, validLinkers, invalidLinkers, VERBOSE);
    }

    /**
     *
     * @param rawData
     * @param lexicon
     * @return
     */
    private List<TextFeature> extractArgumentClassificationFeatures(List<Proposition> rawData, List<ArgumentLinker> lexicon) {
        return null;
    }

    /**
     *
     * @param rawData
     * @param lexicon
     * @return
     */
    private List<TextFeature> extractArgumentDetectionFeatures(List<Proposition> rawData, List<ArgumentLinker> lexicon) {
        List<TextFeature> features = new ArrayList<>();

        rawData.forEach((Proposition prop) -> {
            TextFeature tf = new TextFeature(this.argEngine, prop.getID(), prop.getText(), lexicon);

            tf.extraction();
            if (tf.isValid()) {
                features.add(tf);
            }
        });

        return features;
    }

}
