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

import es.uam.irg.io.IOManager;
import es.uam.irg.nlp.am.arguments.ArgumentEngine;
import es.uam.irg.nlp.am.arguments.ArgumentLinker;
import es.uam.irg.nlp.am.arguments.ArgumentLinkerManager;
import es.uam.irg.nlp.am.arguments.Proposition;
import es.uam.irg.nlp.am.feat.ArgumentFeature;
import es.uam.irg.nlp.am.feat.TextFeature;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * Extractor of argumentative features from textual content.
 */
public class FeatureExtractor {

    // Class constants
    private static final String FEATURES_FILEPATH = "../../data/features.json";
    private static final String PROPOSITIONS_FILEPATH = "../../data/propositions.csv";
    private static final boolean VERBOSE = true;

    // Class members
    private final ArgumentEngine argEngine;
    private final ArgumentLinkerManager lnkManager;

    /**
     * Class constructor.
     *
     * @param language
     * @param validLinkers
     * @param invalidLinkers
     */
    public FeatureExtractor(String language, HashSet<String> validLinkers, HashSet<String> invalidLinkers) {
        this.argEngine = new ArgumentEngine(language);
        this.lnkManager = createLinkerManager(language, validLinkers, invalidLinkers);
    }

    /**
     * Extracts the characteristics of the proposition file.
     *
     * @return
     */
    public boolean runProgram() {
        boolean result = false;

        // ML pipeline
        try {
            // 1. Get lexicon of linkers
            List<ArgumentLinker> lexicon = this.lnkManager.getLexicon(true);

            // 2. Get propositions data
            List<Proposition> rawData = getPropositionDataset();
            System.out.println(">> Total propositions: " + rawData.size());

            // 3. Extract features from propositions dataset
            List<TextFeature> features = extractArgumentFeatures(rawData, lexicon);

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
    private List<TextFeature> extractArgumentFeatures(List<Proposition> rawData, List<ArgumentLinker> lexicon) {
        List<TextFeature> features = new ArrayList<>();

        rawData.forEach((Proposition prop) -> {
            ArgumentFeature tf = new ArgumentFeature(prop.getId(), prop.getText(), this.argEngine, lexicon);
            tf.extraction();
            if (tf.isValid()) {
                features.add(tf);
            }
        });

        return features;
    }

    /**
     *
     * @return
     */
    private List<Proposition> getPropositionDataset() {
        List<Proposition> dataset = IOManager.readDatasetFromCsvFile(PROPOSITIONS_FILEPATH);
        return dataset;
    }

}
