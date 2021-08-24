/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package es.uam.irg.decidemadrid.db;

import com.mongodb.BasicDBObject;
import com.mongodb.MongoClient;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import org.bson.Document;

/**
 *
 * @author ansegura
 */
public class MongoDbManager {
    
    // Public constants
    public static final String DB_NAME = "decide_madrid_2019_09";
    public static final int DB_PORT = 27017; 
    public static final String DB_SERVER = "localhost";
    
    // Private connector object
    private MongoDatabase db;
    private MongoClient mongoClient;
    
    /**
     * Manager constructor.
     */
    public MongoDbManager() {
        this(DB_SERVER , DB_PORT, DB_NAME);
    }
    
    /**
     * 
     * @param client
     * @param port
     * @param database 
     */
    public MongoDbManager(String client, int port, String database) {
        try {
            this.mongoClient = new MongoClient(client , port);
            this.db = mongoClient.getDatabase(database);
        }
        catch (Exception ex) {
            this.mongoClient = null;
            this.db = null;
        }
    }
    
    /**
     * 
     * @param setup
     */
    public MongoDbManager(Map<String, Object> setup) {
        try {
            if (setup != null && setup.size() == 3) {
                String client = setup.get("db_server").toString();
                int port = Integer.parseInt(setup.get("db_port").toString());
                String database = setup.get("db_name").toString();
                
                this.mongoClient = new MongoClient(client , port);
                this.db = mongoClient.getDatabase(database);
            }
            else {
                this.mongoClient = new MongoClient(DB_SERVER , DB_PORT);
                this.db = mongoClient.getDatabase(DB_NAME);
            }
        }
        catch (Exception ex) {
            this.mongoClient = null;
            this.db = null;
        }
    }
    
    /**
     * 
     * @return 
     */
    public List<Document> getDocumentArgumentIDs() {
        List<Document> docs = new ArrayList<>();
        
        try {
            String collName = "annotations";
            MongoCollection<Document> collection = db.getCollection(collName);
            BasicDBObject fields = new BasicDBObject("argumentID", 1);
            
            for (Document doc : collection.find().projection(fields)) {
                docs.add(doc);
            }
        }
        catch (Exception ex) {
            System.err.println("MongoDB error: " + ex.getMessage());
        }
        
        return docs;
    }
    
}
