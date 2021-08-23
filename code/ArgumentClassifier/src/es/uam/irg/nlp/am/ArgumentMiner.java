/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package es.uam.irg.nlp.am;

import es.uam.irg.decidemadrid.db.DMDBManager;
import es.uam.irg.decidemadrid.entities.DMProposal;
import es.uam.irg.utils.FunctionUtils;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author ansegura
 */
public class ArgumentMiner {
    
    // Class members
    private String language;
    private boolean verbose = true;
    private Map<Integer, DMProposal> proposals;
    private Map<String, Object> msqlSetup;
    
    /**
     * Class constructor.
     * 
     * @param language
     * @param verbose 
     */
    public ArgumentMiner(String language, boolean verbose) {
        this.language = language;
        this.verbose = verbose;
        this.msqlSetup = FunctionUtils.getDatabaseConfiguration(Constants.MYSQL_DB);
        this.proposals = getArgumentativeProposals(20);
    }
    
    /**
     * 
     * @return 
     */
    public boolean runProgram() {
        boolean result = false;
        
        
        
        return result;
    }
    
    /**
     * Wrapper function for (DMDBManager) selectNProposals method.
     * 
     * @param topN
     * @return 
     */
    private Map<Integer, DMProposal> getArgumentativeProposals(int topN) {
        Map<Integer, DMProposal> proposals = null;
        
        try {
            DMDBManager dbManager = null;
            if (msqlSetup != null && msqlSetup.size() == 4) {
                String dbServer = msqlSetup.get("db_server").toString();
                String dbName = msqlSetup.get("db_name").toString();
                String dbUserName = msqlSetup.get("db_user_name").toString();
                String dbUserPwd = msqlSetup.get("db_user_pw").toString();
                
                dbManager = new DMDBManager(dbServer, dbName, dbUserName, dbUserPwd);
            }
            else {
                dbManager = new DMDBManager();
            }
            
            proposals = dbManager.selectCustomProposals(topN);
            //proposals = dbManager.selectProposals(topN, this.lnkManager.getLexicon(false));
            
            if (this.verbose) {
                System.out.println(">> Number of proposals: " + proposals.size());
            }
        }
        catch (Exception ex) {
            Logger.getLogger(ArgumentMiner.class.getName()).log(Level.SEVERE, null, ex);
        }
        
        return proposals;
    }
}
