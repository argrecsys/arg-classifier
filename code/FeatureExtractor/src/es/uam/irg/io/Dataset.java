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

import es.uam.irg.decidemadrid.db.DMDBManager;
import es.uam.irg.decidemadrid.db.MongoDbManager;
import es.uam.irg.decidemadrid.entities.DMComment;
import es.uam.irg.decidemadrid.entities.DMProposal;
import es.uam.irg.nlp.am.FeatureExtractor;
import es.uam.irg.nlp.am.arguments.ArgumentEngine;
import es.uam.irg.nlp.am.arguments.ArgumentLinker;
import es.uam.irg.nlp.am.arguments.Proposition;
import es.uam.irg.utils.FunctionUtils;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.bson.Document;

/**
 * Creates and returns the main dataset of the ML pipeline.
 */
public class Dataset {

    // Class constants
    private static final String DATASET_FILEPATH = "../../data/source/propositions.csv";

    // Class members
    private ArgumentEngine argEngine;
    private List<ArgumentLinker> lexicon;
    private Map<String, Object> mdbSetup;
    private Map<String, Object> msqlSetup;

    /**
     * Class constructor
     *
     * @param argEngine
     */
    public Dataset(ArgumentEngine argEngine) {
        this.argEngine = argEngine;
        this.mdbSetup = FunctionUtils.getDatabaseConfiguration(FunctionUtils.MONGO_DB);
        this.msqlSetup = FunctionUtils.getDatabaseConfiguration(FunctionUtils.MYSQL_DB);
    }

    /**
     *
     * @param customProposalIds
     * @return @throws Exception
     */
    public List<Proposition> createDataset(Integer[] customProposalIds) throws Exception {
        List<Proposition> dataset = new ArrayList<>();

        // Temporary variables
        Map<Integer, DMProposal> proposals = null;
        Map<Integer, DMComment> proposalComments = null;
        
        try {
            DMDBManager dbManager = new DMDBManager(this.msqlSetup);

            proposals = dbManager.selectProposals2(customProposalIds);
            System.out.println(">> Number of proposals: " + proposals.size());

            proposalComments = dbManager.selectComments();
            System.out.println(">> Number of comments: " + proposalComments.size());

        } catch (Exception ex) {
            Logger.getLogger(Dataset.class.getName()).log(Level.SEVERE, null, ex);
        }

        Map<Integer, Map<Integer, ArgumentLinker>> sentWithArgs = getSentencesWithArguments();
        int proposalID;
        int sentenceID;
        List<String> sentences;
        ArgumentLinker linker;

        // Analize argumentative proposals
        for (Map.Entry<Integer, DMProposal> entry : proposals.entrySet()) {
            proposalID = entry.getKey();
            sentences = argEngine.getSentences(entry.getValue().getSummary());

            for (int i = 0; i < sentences.size(); i++) {
                sentenceID = i + 1;
                linker = new ArgumentLinker("-", "-", "-", "-");

                if (sentWithArgs.containsKey(proposalID)) {
                    if (sentWithArgs.get(proposalID).containsKey(sentenceID)) {
                        linker = sentWithArgs.get(proposalID).get(sentenceID);
                    }
                }
                dataset.add(new Proposition(proposalID, sentenceID, sentences.get(i), linker));
            }
        }

        // Save dataset file to disk
        if (!IOManager.saveDatasetToCsvFile(DATASET_FILEPATH, dataset)) {
            throw new Exception("Exception - the file could not be created.");
        }

        return dataset;
    }

    /**
     *
     * @return
     */
    public List<Proposition> getDataset() {
        List<Proposition> dataset = IOManager.readDatasetToCsvFile(DATASET_FILEPATH);
        return dataset;
    }

    /**
     *
     * @return
     */
    private Map<Integer, Map<Integer, ArgumentLinker>> getSentencesWithArguments() {
        Map<Integer, Map<Integer, ArgumentLinker>> sentWithArgs = new HashMap<>();

        try {
            MongoDbManager dbManager = new MongoDbManager(this.mdbSetup);
            List<Document> sentences = dbManager.getDocumentsWithArguments(false);
            System.out.println(">> Total sentences with arguments: " + sentences.size());

            // Temp variables
            String[] tokens;
            int nTokens;
            ArgumentLinker linker;

            for (Document doc : sentences) {
                tokens = doc.getString("argumentID").split("-");
                nTokens = tokens.length;
                linker = new ArgumentLinker(doc.get("linker", Document.class));

                if (nTokens > 2) {
                    int docID = Integer.parseInt(tokens[nTokens - 3]);
                    int sentID = Integer.parseInt(tokens[nTokens - 2]);

                    if (!sentWithArgs.containsKey(docID)) {
                        sentWithArgs.put(docID, new HashMap<>());
                    }
                    if (!sentWithArgs.get(docID).containsKey(sentID)) {
                        sentWithArgs.get(docID).put(sentID, linker);
                    }
                } else {
                    System.out.println("-- ERROR!");
                }
            }
        } catch (NumberFormatException ex) {
            Logger.getLogger(FeatureExtractor.class.getName()).log(Level.SEVERE, null, ex);
        }

        return sentWithArgs;
    }

}
