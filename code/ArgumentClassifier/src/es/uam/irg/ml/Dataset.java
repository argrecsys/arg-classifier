/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package es.uam.irg.ml;

import es.uam.irg.clf.ArgumentClassifier;
import es.uam.irg.clf.Constants;
import es.uam.irg.decidemadrid.db.MongoDbManager;
import es.uam.irg.io.IOManager;
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
    private Map<String, Object> mdbSetup;
    private Map<String, Object> msqlSetup;
    private boolean verbose;
    
    /**
     * Class constructor
     * 
     * @param verbose 
     */
    public Dataset(boolean verbose) {
        this.verbose = verbose;
        this.filepath  = Constants.DATASET_FILEPATH;
        this.mdbSetup = FunctionUtils.getDatabaseConfiguration(Constants.MONGO_DB);
        this.msqlSetup = FunctionUtils.getDatabaseConfiguration(Constants.MYSQL_DB);
    }
    
    /**
     * 
     * @return 
     */
    public boolean createDataset() {
        boolean result = false;
        
        Map<Integer, List<Integer>> sentWithArgs = getSentencesWithArguments();
        if (this.verbose) {
            System.out.println(sentWithArgs);
        }
        
        return result;
    }
    
    /**
     * 
     * @return 
     */
    public List<Proposition> getDataset() {
        List<Proposition> dataset = IOManager.readDataset(this.filepath);
        return dataset;
    }
    
    /**
     * 
     * @return 
     */
    private Map<Integer, List<Integer>> getSentencesWithArguments() {
        Map<Integer, List<Integer>> sentWithArgs = new HashMap<>();
        
        try {
            MongoDbManager dbManager = new MongoDbManager(mdbSetup);
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
