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
 * Class representing a statement or assertion that expresses a judgement or opinion.
 *
 * @author ansegura
 */
public class Proposition {

    // Class members
    private ArgumentLinker linker;
    private int proposalID;
    private int sentenceID;
    private String text;

    /**
     * Class constructor.
     *
     * @param proposalID
     * @param sentenceID
     * @param text
     * @param linker
     */
    public Proposition(int proposalID, int sentenceID, String text, ArgumentLinker linker) {
        this.proposalID = proposalID;
        this.sentenceID = sentenceID;
        this.text = text;
        this.linker = linker;
    }

    public String getID() {
        return String.format("%d-%d", this.proposalID, this.sentenceID);
    }

    public ArgumentLinker getLinker() {
        return this.linker;
    }

    public int getProposalID() {
        return this.proposalID;
    }

    public int getSentenceID() {
        return this.sentenceID;
    }

    public String getText() {
        return this.text;
    }

    @Override
    public String toString() {
        return String.format("%s-%s > %s [%s]",
                this.proposalID, this.sentenceID, this.text, this.linker);
    }

}
