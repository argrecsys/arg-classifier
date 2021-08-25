/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package es.uam.irg.ml;

import es.uam.irg.decidemadrid.db.DMDBManager;
import es.uam.irg.decidemadrid.db.MongoDbManager;
import es.uam.irg.decidemadrid.entities.DMProposal;
import es.uam.irg.io.IOManager;
import es.uam.irg.nlp.am.arguments.ArgumentEngine;
import es.uam.irg.nlp.am.arguments.ArgumentLinkerManager;
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
 *
 * @author ansegura
 */
public class Dataset {
    
    private String filepath;
    private ArgumentLinkerManager lnkManager;
    private Map<String, Object> mdbSetup;
    private Map<String, Object> msqlSetup;
    private final ArgumentEngine argEngine;
    private boolean verbose;
    
    /**
     * Class constructor
     * 
     * @param argEngine
     * @param verbose 
     */
    public Dataset(ArgumentEngine argEngine, boolean verbose) {
        this.argEngine = argEngine;
        this.verbose = verbose;
        this.filepath  = Constants.DATASET_FILEPATH;
        this.mdbSetup = FunctionUtils.getDatabaseConfiguration(Constants.MONGO_DB);
        this.msqlSetup = FunctionUtils.getDatabaseConfiguration(Constants.MYSQL_DB);
        this.lnkManager = createLinkerManager(argEngine.getCurrentLanguage());
    }
    
    /**
     * 
     * @return 
     */
    public boolean createDataset() {
        List<Proposition> dataset = new ArrayList<>();
        
        // Temporary variables
        Map<Integer, DMProposal> proposals = getProposals();
        Map<Integer, List<Integer>> sentWithArgs = getSentencesWithArguments();
        int proposalID;
        int sentenceID;
        List<String> sentences;
        String label;
        
        // Analize argumentative proposals
        for (Map.Entry<Integer, DMProposal> entry : proposals.entrySet()) {
            proposalID = entry.getKey();
            sentences = argEngine.getSentences(entry.getValue().getSummary());
            
            for (int i=0; i < sentences.size(); i++) {
                sentenceID = i + 1;
                label = "0";
                
                if (sentWithArgs.containsKey(proposalID)) {
                    if (sentWithArgs.get(proposalID).contains(sentenceID)) {
                        label = "1";
                    }
                }
                dataset.add( new Proposition(proposalID, sentenceID, sentences.get(i), label));
            }
        }
        
        // Save dataset file to disk
        boolean result = IOManager.saveDatasetToCsvFile(this.filepath, dataset);
        return result;
    }
    
    /**
     * 
     * @return 
     */
    public List<Proposition> getDataset() {
        List<Proposition> dataset = IOManager.readDatasetToCsvFile(this.filepath);
        return dataset;
    }
    
    /**
     * Create the linker manager object.
     * 
     * @param lang
     * @param verbose
     * @return
     */
    private ArgumentLinkerManager createLinkerManager(String lang) {
        return IOManager.readLinkerTaxonomy(lang, this.verbose);
    }
    
    /**
     * 
     * @return 
     */
    private Map<Integer, DMProposal> getProposals() {
        Map<Integer, DMProposal> proposals = null;
        
        try {
            DMDBManager dbManager = new DMDBManager(this.msqlSetup);
            proposals = dbManager.selectProposals(Integer.MAX_VALUE, this.lnkManager.getLexicon(false));
            
            if (this.verbose) {
                System.out.println(">> Number of proposals: " + proposals.size());
            }
        }
        catch (Exception ex) {
            Logger.getLogger(Dataset.class.getName()).log(Level.SEVERE, null, ex);
        }
        
        return proposals;
    }
    
    /**
     *
     * @return 
     */
    private Map<Integer, List<Integer>> getSentencesWithArguments() {
        Map<Integer, List<Integer>> sentWithArgs = new HashMap<>();
        
        try {
            MongoDbManager dbManager = new MongoDbManager(this.mdbSetup);
            List<Document> sentences = dbManager.getDocumentArgumentIDs();
            
            for (Document doc : sentences) {
                String argumentID = doc.getString("argumentID");
                String[] tokens = argumentID.split("-");
                
                if (tokens.length == 2) {
                    int sentID = Integer.parseInt(tokens[0]);
                    int argID = Integer.parseInt(tokens[1]);
                            
                    if (!sentWithArgs.containsKey(sentID)) {
                        sentWithArgs.put(sentID, new ArrayList<>());
                    }
                    sentWithArgs.get(sentID).add(argID);
                }
            }
        }
        catch (NumberFormatException ex) {
            Logger.getLogger(ArgumentClassifier.class.getName()).log(Level.SEVERE, null, ex);
        }
        
        return sentWithArgs;
    }
    
}
