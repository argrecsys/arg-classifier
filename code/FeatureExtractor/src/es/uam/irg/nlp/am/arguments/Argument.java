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

import es.uam.irg.utils.StringUtils;
import org.json.JSONObject;

/**
 * Argument class. The premise justifies, gives reasons for or supports the
 * conclusion (claim).
 */
public class Argument {

    // Private class members
    private final ArgumentId argumentId;
    private final String claim;
    private boolean isMajorClaim;
    private final ArgumentLinker linker;
    private final String premise;
    private final String sentenceText;

    /**
     * Regular constructor.
     *
     * @param argId
     * @param sentenceText
     * @param claim
     * @param premise
     * @param linker
     */
    public Argument(String argId, String sentenceText, String claim, String premise, ArgumentLinker linker) {
        this.argumentId = new ArgumentId(argId);
        this.sentenceText = sentenceText;
        this.claim = claim;
        this.premise = premise;
        this.linker = linker;

        completeArgument();
    }

    /**
     * Alternative constructor.
     *
     * @param json
     */
    public Argument(JSONObject json) {
        JSONObject lnk = json.getJSONObject("linker");

        this.argumentId = new ArgumentId(json.getString("argumentId"));
        this.sentenceText = json.getString("sentenceText");
        this.claim = json.getString("claim");
        this.premise = json.getString("premise");
        this.linker = new ArgumentLinker(lnk.getString("category"), lnk.getString("subCategory"), lnk.getString("relationType"), lnk.getString("linker"));

        completeArgument();
    }

    /**
     *
     * @param arg
     * @return
     */
    public boolean equals(Argument arg) {
        return (this.claim.equals(arg.claim) && this.premise.equals(arg.premise) && this.linker.equals(arg.linker));
    }

    /**
     *
     * @return
     */
    public String getClaim() {
        return this.claim;
    }

    /**
     *
     * @return
     */
    public String getId() {
        return this.argumentId.getArgumentId();
    }

    /**
     *
     * @return
     */
    public String getPremise() {
        return this.premise;
    }

    /**
     *
     * @return
     */
    public int getProposalId() {
        return this.argumentId.getProposalId();
    }

    /**
     *
     * @return
     */
    public String getText() {
        return this.sentenceText;
    }

    /**
     *
     * @return
     */
    public boolean isMajorClaim() {
        return this.isMajorClaim;
    }

    /**
     *
     * @return
     */
    @Override
    public String toString() {
        return String.format("[%s] - %s > %s [lnk: %s]",
                this.argumentId.getArgumentId(), this.claim, this.premise, this.linker.toString());
    }

    private void completeArgument() {
        this.isMajorClaim = (this.argumentId.getCommentId() == 0 && !StringUtils.isEmpty(claim) && StringUtils.isEmpty(premise));
    }

}
