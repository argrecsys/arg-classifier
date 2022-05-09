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
package es.uam.irg.nlp.am.arguments;

/**
 *
 * @author Usuario
 */
public class ArgumentId {

    private final String argumentId;
    private final int commentId;
    private final int proposalId;
    private final int sequenceNumber;

    public ArgumentId(String argId) {
        this.argumentId = argId;

        String[] tokens = argId.split("-");
        if (tokens.length == 3) {
            this.proposalId = Integer.parseInt(tokens[0]);
            this.commentId = Integer.parseInt(tokens[1]);
            this.sequenceNumber = Integer.parseInt(tokens[2]);
        } else {
            this.proposalId = -1;
            this.commentId = -1;
            this.sequenceNumber = -1;
        }
    }

    public String getArgumentId() {
        return this.argumentId;
    }

    public int getCommentId() {
        return this.commentId;
    }

    public int getProposalId() {
        return this.proposalId;
    }

    public int getSequenceNumber() {
        return this.sequenceNumber;
    }

}
