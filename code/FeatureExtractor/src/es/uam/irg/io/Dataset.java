/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package es.uam.irg.io;

import es.uam.irg.decidemadrid.db.DMDBManager;
import es.uam.irg.decidemadrid.db.MongoDbManager;
import es.uam.irg.decidemadrid.entities.DMProposal;
import es.uam.irg.nlp.am.Constants;
import es.uam.irg.nlp.am.FeatureExtractor;
import es.uam.irg.nlp.am.arguments.ArgumentEngine;
import es.uam.irg.nlp.am.arguments.ArgumentLinker;
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
    private ArgumentEngine argEngine;
    
    /**
     * Class constructor
     * 
     * @param argEngine
     */
    public Dataset(ArgumentEngine argEngine) {
        this.argEngine = argEngine;
        this.filepath  = Constants.DATASET_FILEPATH;
        this.mdbSetup = FunctionUtils.getDatabaseConfiguration(Constants.MONGO_DB);
        this.msqlSetup = FunctionUtils.getDatabaseConfiguration(Constants.MYSQL_DB);
        this.lnkManager = createLinkerManager(argEngine.getCurrentLanguage());
    }
    
    /**
     * 
     * @return
     * @throws Exception 
     */
    public List<Proposition> createDataset() throws Exception {
        List<Proposition> dataset = new ArrayList<>();
        
        // Temporary variables
        Map<Integer, DMProposal> proposals = getProposals();
        Map<Integer, Map<Integer, ArgumentLinker>> sentWithArgs = getSentencesWithArguments();
        int proposalID;
        int sentenceID;
        List<String> sentences;
        ArgumentLinker linker;
        
        // Analize argumentative proposals
        for (Map.Entry<Integer, DMProposal> entry : proposals.entrySet()) {
            proposalID = entry.getKey();
            sentences = argEngine.getSentences(entry.getValue().getSummary());
            
            for (int i=0; i < sentences.size(); i++) {
                sentenceID = i + 1;
                linker = new ArgumentLinker("-", "-", "-", "-");
                
                if (sentWithArgs.containsKey(proposalID)) {
                    if (sentWithArgs.get(proposalID).containsKey(sentenceID)) {
                        linker = sentWithArgs.get(proposalID).get(sentenceID);
                    }
                }
                dataset.add( new Proposition(proposalID, sentenceID, sentences.get(i), linker));
            }
        }
        
        // Save dataset file to disk
        if (!IOManager.saveDatasetToCsvFile(this.filepath, dataset)) {
            throw new Exception("Exception - the file could not be created.");
        }
        
        return dataset;
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
        return IOManager.readLinkerTaxonomy(lang, true);
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
            System.out.println(">> Number of proposals: " + proposals.size());
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
    private Map<Integer, Map<Integer, ArgumentLinker>> getSentencesWithArguments() {
        Map<Integer, Map<Integer, ArgumentLinker>> sentWithArgs = new HashMap<>();
        
        try {
            MongoDbManager dbManager = new MongoDbManager(this.mdbSetup);
            List<Document> sentences = dbManager.getDocumentsWithArguments();
            String[] tokens;
            ArgumentLinker linker;
            
            for (Document doc : sentences) {
                tokens = doc.getString("argumentID").split("-");
                linker = new ArgumentLinker(doc.get("linker", Document.class));

                if (tokens.length == 2) {
                    int sentID = Integer.parseInt(tokens[0]);
                    int argID = Integer.parseInt(tokens[1]);
                            
                    if (!sentWithArgs.containsKey(sentID)) {
                        sentWithArgs.put(sentID, new HashMap<>());
                    }
                    sentWithArgs.get(sentID).put(argID, linker);
                }
            }
        }
        catch (NumberFormatException ex) {
            Logger.getLogger(FeatureExtractor.class.getName()).log(Level.SEVERE, null, ex);
        }
        
        return sentWithArgs;
    }
    
}
