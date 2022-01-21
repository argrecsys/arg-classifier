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
 *
 * @author ansegura
 */
public class Phrase {

    // Class members
    public int depth;
    public String function;
    public String text;

    /**
     * Class constructor.
     *
     * @param text
     * @param function
     * @param depth
     */
    public Phrase(String text, String function, int depth) {
        this.text = text;
        this.function = function;
        this.depth = depth;
    }

    @Override
    public String toString() {
        return String.format("%s > %s [%s]", this.text, this.function, this.depth);
    }

}
