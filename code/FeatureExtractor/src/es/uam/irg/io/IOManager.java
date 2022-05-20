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

import es.uam.irg.nlp.am.arguments.ArgumentEngine;
import es.uam.irg.nlp.am.arguments.ArgumentLinker;
import es.uam.irg.nlp.am.arguments.ArgumentLinkerManager;
import es.uam.irg.nlp.am.arguments.Proposition;
import es.uam.irg.nlp.am.feat.TextFeature;
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
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.yaml.snakeyaml.Yaml;

/**
 * Support class containing static methods that allow reading and writing files
 * from a directory.
 */
public class IOManager {

    // Class constants
    private static final String LEXICON_FILEPATH = "Resources/data/argument_lexicon_{}.csv";
    private static final String STOPWORDS_FILEPATH = "../../data/stopwords/{}.txt";

    /**
     *
     * @param filepath
     * @return
     */
    public static List<Proposition> readDatasetFromCsvFile(String filepath) {
        List<Proposition> dataset = new ArrayList<>();
        int numLabels = 2;

        try {
            // Get the file
            File csvFile = new File(filepath);

            // Check if the specified file exists or not
            if (csvFile.exists()) {
                BufferedReader fileReader = new BufferedReader(new FileReader(csvFile));
                String row;
                String id;
                String text;
                String type;

                fileReader.readLine();
                while ((row = fileReader.readLine()) != null) {
                    String[] data = row.split(",");
                    int n = data.length;

                    if (n >= 4) {
                        id = data[0];
                        text = getTextField(data, numLabels);
                        type = data[n - numLabels];
                        dataset.add(new Proposition(id, text, type));
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
     * Loads the taxonomy and lexicon of argumentative linkers.
     *
     * @param lang
     * @param validLinkers
     * @param invalidLinkers
     * @param verbose
     * @return
     */
    public static ArgumentLinkerManager readLinkerTaxonomy(String lang, HashSet<String> validLinkers, HashSet<String> invalidLinkers, boolean verbose) {
        ArgumentLinkerManager linkers = new ArgumentLinkerManager();
        String lexiconFilepath = LEXICON_FILEPATH.replace("{}", lang);

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
                        if ((validLinkers.isEmpty() || validLinkers.contains(linker)) && (!invalidLinkers.contains(linker))) {
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
     * @param lang
     * @param verbose
     * @return
     */
    public static HashSet<String> readStopwordList(String lang, boolean verbose) {
        HashSet<String> stopwords = new HashSet<>();
        String language = (lang.equals(ArgumentEngine.LANG_EN) ? "english" : "spanish");
        String stopwordsFilepath = STOPWORDS_FILEPATH.replace("{}", language);

        try {
            // Get the file
            File txtFile = new File(stopwordsFilepath);

            // Check if the specified file exists or not
            if (txtFile.exists()) {
                BufferedReader reader = new BufferedReader(new FileReader(txtFile));
                String word;

                while ((word = reader.readLine()) != null) {
                    stopwords.add(word);
                }

                reader.close();
            }

        } catch (IOException ex) {
            Logger.getLogger(IOManager.class.getName()).log(Level.SEVERE, null, ex);
        }

        if (verbose) {
            System.out.println(">> Stopwords: " + stopwords.size());
        }

        return stopwords;
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
     * @param features
     * @return
     */
    public static boolean saveTextFeatures(String filepath, List<TextFeature> features) {
        boolean result = false;

        // Create JSON text
        StringBuilder sb = new StringBuilder();
        sb.append("{\n");
        for (TextFeature feature : features) {
            sb.append("  \"" + feature.getId() + "\": " + feature.toString() + ",\n");
        }
        String jsonText = sb.toString();
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
     * Gets the text of the proposition, even if it is divided into several
     * columns.
     *
     * @param data
     * @param numLabels
     * @return
     */
    private static String getTextField(String[] data, int numLabels) {
        String text = "";
        for (int i = 1; i < data.length - numLabels; i++) {
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
