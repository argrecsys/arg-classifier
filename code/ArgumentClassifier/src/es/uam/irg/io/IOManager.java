/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package es.uam.irg.io;

import es.uam.irg.nlp.am.arguments.Proposition;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.yaml.snakeyaml.Yaml;

/**
 *
 * @author ansegura
 */
public class IOManager {
    
    /**
     * 
     * @param filepath
     * @return 
     */
    public static Map<String, Object> readYamlFile(String filepath) {
        Map<String, Object> data = null;
        
        try {
            // Get the file
            File yamlFile = new File(filepath);

            // Check if the specified file exists or not
            if (yamlFile.exists()) {
                InputStream inputStream = new FileInputStream(yamlFile);
                Yaml yaml = new Yaml();
                data = (Map<String, Object>) yaml.load(inputStream);
            }
        
        } catch (FileNotFoundException ex) {
            Logger.getLogger(IOManager.class.getName()).log(Level.SEVERE, null, ex);
        }
        
        return data;
    }
    
    /**
     * 
     * @param filepath
     * @return 
     */
    public static List<Proposition> readDataset(String filepath) {
        List<Proposition> dataset = new ArrayList<>();
        
        try {
            // Get the file
            File csvFile = new File(filepath);

            // Check if the specified file exists or not
            if (csvFile.exists()) {
                BufferedReader reader = new BufferedReader( new FileReader(csvFile));
                String row;
                int proposalID;
                int sentenceID;
                String text;
                String label;

                reader.readLine();
                while ((row = reader.readLine()) != null) {
                    String[] data = row.split(",");

                    if (data.length == 4) {
                        proposalID = Integer.parseInt(data[0]);
                        sentenceID = Integer.parseInt(data[1]);
                        text = data[2];
                        label = data[3];
                        dataset.add( new Proposition(proposalID, sentenceID, text, label));
                    }
                }

                reader.close();
            }

        } catch (FileNotFoundException ex) {
            Logger.getLogger(IOManager.class.getName()).log(Level.SEVERE, null, ex);
        } catch (IOException ex) {
            Logger.getLogger(IOManager.class.getName()).log(Level.SEVERE, null, ex);
        }
        
        return dataset;
    }
    
}
