/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package es.uam.irg.io;

import es.uam.irg.nlp.am.Constants;
import es.uam.irg.nlp.am.TextFeature;
import es.uam.irg.nlp.am.arguments.ArgumentLinker;
import es.uam.irg.nlp.am.arguments.ArgumentLinkerManager;
import es.uam.irg.nlp.am.arguments.Proposition;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStreamWriter;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
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

    private static final HashSet<String> INVALID_LINKERS = new HashSet(Arrays.asList("e", "ni", "o", "y"));
    private static final HashSet<String> VALID_LINKERS = new HashSet();

    /**
     *
     * @param filepath
     * @return
     */
    public static List<Proposition> readDatasetToCsvFile(String filepath) {
        List<Proposition> dataset = new ArrayList<>();

        try {
            // Get the file
            File csvFile = new File(filepath);

            // Check if the specified file exists or not
            if (csvFile.exists()) {
                BufferedReader fileReader = new BufferedReader(new FileReader(csvFile));
                String row;
                int proposalID;
                int sentenceID;
                String text;
                String linker;
                String category;
                String subCategory;

                fileReader.readLine();
                while ((row = fileReader.readLine()) != null) {
                    String[] data = row.split(",");
                    int n = data.length;

                    if (n >= 6) {
                        proposalID = Integer.parseInt(data[0]);
                        sentenceID = Integer.parseInt(data[1]);
                        text = getTextField(data);
                        linker = data[n - 3];
                        category = data[n - 2];
                        subCategory = data[n - 1];
                        dataset.add(new Proposition(proposalID, sentenceID, text, new ArgumentLinker(category, subCategory, "", linker)));
                    }
                }

                fileReader.close();
            }

        } catch (FileNotFoundException ex) {
            Logger.getLogger(IOManager.class.getName()).log(Level.SEVERE, null, ex);
        } catch (IOException ex) {
            Logger.getLogger(IOManager.class.getName()).log(Level.SEVERE, null, ex);
        }

        return dataset;
    }

    /**
     *
     * @param lang
     * @param verbose
     * @return
     */
    public static ArgumentLinkerManager readLinkerTaxonomy(String lang, boolean verbose) {
        ArgumentLinkerManager linkers = new ArgumentLinkerManager();
        String lexiconFilepath = Constants.LEXICON_FILEPATH.replace("{}", lang);

        try {
            // Get the file
            File csvFile = new File(lexiconFilepath);

            // Check if the specified file exists or not
            if (csvFile.exists()) {
                BufferedReader reader = new BufferedReader(new FileReader(csvFile));
                String row;
                String category;
                String subCategory;
                String relationType;
                String linker;

                reader.readLine();
                while ((row = reader.readLine()) != null) {
                    String[] data = row.split(",");

                    if (data.length == 6) {
                        category = data[2];
                        subCategory = data[3];
                        relationType = data[4];
                        linker = data[5];

                        // If the linker is a valid one and also not invalid... then add it
                        if ((VALID_LINKERS.isEmpty() || VALID_LINKERS.contains(linker)) && (!INVALID_LINKERS.contains(linker))) {
                            linkers.addLinker(category, subCategory, relationType, linker);
                        }
                    }
                }

                reader.close();
            }

        } catch (IOException ex) {
            Logger.getLogger(IOManager.class.getName()).log(Level.SEVERE, null, ex);
        }

        if (verbose) {
            System.out.println(">> Taxonomy:");
            Map<String, Map<String, List<ArgumentLinker>>> taxonomy = linkers.getTaxonomy();
            taxonomy.entrySet().forEach(entry -> {
                System.out.println(entry.getKey());
                for (Map.Entry<String, List<ArgumentLinker>> subentry : entry.getValue().entrySet()) {
                    System.out.println("  " + subentry.getKey());
                    List<ArgumentLinker> items = subentry.getValue();

                    for (int i = 0; i < items.size(); i++) {
                        System.out.println("    " + items.get(i).linker);
                    }
                }
            });

            List<ArgumentLinker> lexicon = linkers.getLexicon(true);
            System.out.println(">> Lexicon: " + lexicon.size());
            for (int i = 0; i < lexicon.size(); i++) {
                System.out.format("Linker -> %s \n", lexicon.get(i).toString());
            }
        }

        return linkers;
    }

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
     * @param dataset
     * @return
     */
    public static boolean saveDatasetToCsvFile(String filepath, List<Proposition> dataset) {
        boolean result = false;

        try {
            FileOutputStream file = new FileOutputStream(filepath);
            OutputStreamWriter fileWriter = new OutputStreamWriter(file, StandardCharsets.UTF_8);

            fileWriter.write("proposal_id,sentence_id,text,linker_value,category,sub_category\n");
            for (Proposition prop : dataset) {
                ArgumentLinker linker = prop.getLinker();
                String line = String.format("%s,%s,\"%s\",%s,%s,%s\n",
                        prop.getProposalID(), prop.getSentenceID(), prop.getText(), linker.linker, linker.category, linker.subCategory);
                fileWriter.write(line);
            }

            fileWriter.close();
            result = true;

        } catch (FileNotFoundException ex) {
            Logger.getLogger(IOManager.class.getName()).log(Level.SEVERE, null, ex);
        } catch (IOException ex) {
            Logger.getLogger(IOManager.class.getName()).log(Level.SEVERE, null, ex);
        }

        return result;
    }

    /**
     *
     * @param filepath
     * @param features
     * @return
     */
    public static boolean saveTextFeatures(String filepath, List<TextFeature> features) {
        boolean result = false;

        // Create JSON text
        String jsonText = "{\n";
        for (TextFeature feature : features) {
            jsonText += "  \"" + feature.getID() + "\": " + feature.toString() + ",\n";
        }
        jsonText = jsonText.substring(0, jsonText.length() - 2) + "\n}";

        try {
            // Save JSON text
            OutputStreamWriter fileWriter = new OutputStreamWriter(new FileOutputStream(filepath), StandardCharsets.UTF_8);
            fileWriter.write(jsonText);
            fileWriter.close();

            result = true;

        } catch (FileNotFoundException ex) {
            Logger.getLogger(IOManager.class.getName()).log(Level.SEVERE, null, ex);
        } catch (IOException ex) {
            Logger.getLogger(IOManager.class.getName()).log(Level.SEVERE, null, ex);
        }

        return result;
    }

    /**
     *
     * @param data
     * @return
     */
    private static String getTextField(String[] data) {
        String text = "";
        for (int i = 2; i < data.length - 3; i++) {
            text += (!"".equals(text) ? "," : "") + data[i];
        }
        if (text.charAt(0) == '"') {
            text = text.substring(1, text.length());
        }
        if (text.charAt(text.length() - 1) == '"') {
            text = text.substring(0, text.length() - 1);
        }
        return text;
    }

}
