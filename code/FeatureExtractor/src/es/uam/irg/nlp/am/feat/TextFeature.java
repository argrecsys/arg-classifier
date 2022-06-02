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

import es.uam.irg.utils.FunctionUtils;
import java.util.List;

/**
 * Abstract text feature class.
 */
public abstract class TextFeature {

    // Class contants
    public static final int MIN_LENGTH = 3;
    public static final String SPECIAL_PUNCT = "¡!¿?'%:";

    // Text variables
    protected String id;
    protected String text;

    public abstract boolean extraction();

    /**
     *
     * @return
     */
    public String getId() {
        return this.id;
    }

    /**
     *
     * @return
     */
    public String getText() {
        return this.text;
    }

    // Abstract methods
    @Override
    public abstract String toString();

    /**
     *
     * @return
     */
    protected int getSentencePosition() {
        int sentPosition = 0;
        if (!this.id.isEmpty()) {
            String[] tokens = this.id.split("-");
            sentPosition = Integer.parseInt(tokens[2]);
        }
        return sentPosition;
    }

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
