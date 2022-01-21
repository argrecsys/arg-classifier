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
package es.uam.irg.decidemadrid.db;

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
    public static final String DB_COLLECTION = "annotations";

    // Private connector object
    private MongoDatabase db;
    private MongoClient mongoClient;
    private String collName;

    /**
     * Manager constructor.
     */
    public MongoDbManager() {
        this(DB_SERVER, DB_PORT, DB_NAME, DB_COLLECTION);
    }

    /**
     *
     * @param client
     * @param port
     * @param database
     * @param collection
     */
    public MongoDbManager(String client, int port, String database, String collection) {
        try {
            this.mongoClient = new MongoClient(client, port);
            this.db = mongoClient.getDatabase(database);
            this.collName = collection;
        } catch (Exception ex) {
            this.mongoClient = null;
            this.db = null;
            this.collName = null;
        }
    }

    /**
     *
     * @param setup
     */
    public MongoDbManager(Map<String, Object> setup) {
        try {
            if (setup != null && setup.size() == 4) {
                String client = setup.get("db_server").toString();
                int port = Integer.parseInt(setup.get("db_port").toString());
                String database = setup.get("db_name").toString();
                String collection = setup.get("db_collection").toString();

                this.mongoClient = new MongoClient(client, port);
                this.db = mongoClient.getDatabase(database);
                this.collName = collection;
            } else {
                this.mongoClient = null;
                this.db = null;
                this.collName = null;
            }
        } catch (Exception ex) {
            this.mongoClient = null;
            this.db = null;
            this.collName = null;
        }
    }

    /**
     *
     * @param allDocuments
     * @return
     */
    public List<Document> getDocumentsWithArguments(boolean allDocuments) {
        List<Document> docs = new ArrayList<>();

        try {
            MongoCollection<Document> collection = db.getCollection(collName);

            for (Document doc : collection.find()) {
                if (allDocuments || doc.getInteger("commentID") == -1) {
                    docs.add(doc);
                }
            }
        } catch (Exception ex) {
            System.err.println("MongoDB error: " + ex.getMessage());
        }

        return docs;
    }

}
