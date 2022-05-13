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
package es.uam.irg.nlp.am.arguments;

/**
 * Class representing a statement or assertion that expresses a judgement or
 * opinion.
 */
public class Proposition {

    private final String id;
    private final String text;
    private final String type;

    /**
     * Class constructor.
     *
     * @param id
     * @param text
     * @param type
     */
    public Proposition(String id, String text, String type) {
        this.id = id;
        this.text = text;
        this.type = type;
    }

    public String getId() {
        return this.id;
    }

    public String getText() {
        return this.text;
    }

    public String getType() {
        return this.type;
    }

    @Override
    public String toString() {
        return String.format("%[s] %s -> %s",
                this.id, this.text, this.text, this.type);
    }

}
