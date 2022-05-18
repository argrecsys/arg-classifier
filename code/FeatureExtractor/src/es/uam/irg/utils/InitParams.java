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
package es.uam.irg.utils;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.json.JSONObject;

/**
 * Helper for loading application input parameters.
 */
public class InitParams {

    private final static String FILE_PATH = "Resources/config/params.json";

    public static Map<String, Object> readInitParams() {
        Map<String, Object> params = new HashMap<>();
        String jsonText = readJsonFile();

        if (!"".equals(jsonText)) {
            JSONObject json = new JSONObject(jsonText);

            if (!json.isEmpty()) {
                JSONObject data;

                // General parameters
                String lang = json.getString("language");
                params.put("language", lang);

                // Linkers parameters
                data = json.getJSONObject("linkers").getJSONObject(lang);
                Map<String, Object> linkers = new HashMap<>();
                linkers.put("invalidAspects", new HashSet(data.getJSONArray("invalidAspects").toList()));
                linkers.put("invalidLinkers", new HashSet(data.getJSONArray("invalidLinkers").toList()));
                linkers.put("validLinkers", new HashSet(data.getJSONArray("validLinkers").toList()));
                params.put("linkers", linkers);
            }
        }

        return params;
    }

    private static String readJsonFile() {
        StringBuilder jsonText = new StringBuilder();

        File jsonFile = new File(FILE_PATH);
        if (jsonFile.exists()) {
            try {
                BufferedReader reader = new BufferedReader(new FileReader(jsonFile));
                String row;
                while ((row = reader.readLine()) != null) {
                    jsonText.append(row + "\n");
                }
                reader.close();

            } catch (FileNotFoundException ex) {
                Logger.getLogger(InitParams.class.getName()).log(Level.SEVERE, null, ex);
            } catch (IOException ex) {
                Logger.getLogger(InitParams.class.getName()).log(Level.SEVERE, null, ex);
            }
        }

        return jsonText.toString();
    }

}
