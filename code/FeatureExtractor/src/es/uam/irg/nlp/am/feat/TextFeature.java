/**
 * Copyright 2022
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
package es.uam.irg.nlp.am.feat;

import es.uam.irg.nlp.am.arguments.ArgumentEngine;
import es.uam.irg.nlp.am.arguments.ArgumentLinker;
import es.uam.irg.utils.FunctionUtils;
import java.util.List;

/**
 * Abstract text feature class.
 */
public abstract class TextFeature {

    // Class contants
    public static final int MIN_LENGTH = 3;
    public static final String SPECIAL_PUNCT = "¡!¿?'%:";

    // Class variables
    protected ArgumentEngine argEngine;
    protected String dateFormat;
    protected String id;
    protected boolean isValid;
    protected List<ArgumentLinker> lexicon;
    protected String text;
    protected int textLength;

    /**
     * Runs feature extraction method.
     */
    public void extraction() {

        // NLP-processing
        if (this.textLength >= MIN_LENGTH) {
            extractFeatures();
        }
    }

    /**
     *
     * @return
     */
    public String getID() {
        return this.id;
    }

    /**
     *
     * @return
     */
    public boolean isValid() {
        return this.isValid;
    }

    // Abstract methods
    @Override
    public abstract String toString();

    protected abstract void extractFeatures();

    protected abstract String getDateFormat();

    /**
     *
     * @param list
     * @return
     */
    protected String listToString(List<String> list) {
        String separator = "\"";
        String result = FunctionUtils.listToString(list, separator);
        if (result.equals("\"\"")) {
            result = "";
        }
        return "[" + result + "]";
    }

}
