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
import java.util.List;

/**
 * Class containing the argumentative features extracted from a text for the
 * classification task.
 */
public class ClassificationTextFeature extends TextFeature {

    public ClassificationTextFeature(String id, String text, ArgumentEngine argEngine, List<ArgumentLinker> lexicon) {
        this.argEngine = argEngine;
        this.lexicon = lexicon;
        this.dateFormat = getDateFormat();
        this.id = id;
        this.text = text;
    }

    @Override
    public String toString() {
        throw new UnsupportedOperationException("Not supported yet."); //To change body of generated methods, choose Tools | Templates.
    }

    @Override
    protected void extractFeatures() {
        throw new UnsupportedOperationException("Not supported yet."); //To change body of generated methods, choose Tools | Templates.
    }

    /**
     *
     * @return
     */
    @Override
    protected String getDateFormat() {
        String lang = this.argEngine.getCurrentLanguage();
        String format = (lang.equals("en") ? "MM/dd/yyyy" : "dd/MM/yyyy");
        return format;
    }

}
