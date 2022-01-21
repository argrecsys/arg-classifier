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

import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.pipeline.*;
import edu.stanford.nlp.trees.Tree;
import edu.stanford.nlp.trees.TreeCoreAnnotations;
import java.io.*;
import java.util.*;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author ansegura
 */
public class ArgumentEngine {

    public static final String LANG_EN = "en";
    public static final String LANG_ES = "es";
    private static final String SPANISH_PROPERTIES = "Resources/config/StanfordCoreNLP-spanish.properties";

    // Class members
    private final String language;
    private StanfordCoreNLP pipeline;

    /**
     * Class constructor.
     *
     * @param lang
     */
    public ArgumentEngine(String lang) {
        this.language = lang;
        createPipeline();
    }

    /**
     *
     * @param text
     * @return
     */
    public CoreDocument createCoreNlpDocument(String text) {
        CoreDocument document = pipeline.processToCoreDocument(text);
        return document;
    }

    /**
     *
     * @return
     */
    public String getCurrentLanguage() {
        return this.language;
    }

    /**
     *
     * @param tree
     * @return
     */
    public List<Phrase> getPhraseList(Tree tree) {
        List<Phrase> syntagmaList = new ArrayList<>();
        if (tree != null) {
            getPhraseList(tree, 0, syntagmaList);
        }
        return syntagmaList;
    }

    /**
     * Divides a paragraph into sentences.
     *
     * @param text a string representing the text of a document (a paragraph).
     * @return
     */
    public List<String> getSentences(String text) {
        List<String> sentences = new ArrayList<>();

        CoreDocument nlpDoc = createCoreNlpDocument(text);
        nlpDoc.sentences().forEach(sent -> {
            sentences.add(sent.text());
        });

        return sentences;
    }

    /**
     *
     * @param text
     * @return
     */
    public Tree getTree(String text) {
        Annotation annotation = new Annotation(text);
        pipeline.annotate(annotation);
        Tree tree = annotation.get(CoreAnnotations.SentencesAnnotation.class).get(0).get(TreeCoreAnnotations.TreeAnnotation.class);
        return tree;
    }

    /**
     * Configures CoreNLP properties according to the specified language.
     */
    private void createPipeline() {
        Properties props = new Properties();

        try {
            if (language.equals(LANG_EN)) {
                props.setProperty("annotators", "tokenize, ssplit, pos, lemma, ner, parse, dcoref, sentiment");
            } else if (language.equals(LANG_ES)) {
                props.load(new FileInputStream(SPANISH_PROPERTIES));
            }
            this.pipeline = new StanfordCoreNLP(props);

        } catch (FileNotFoundException ex) {
            Logger.getLogger(ArgumentEngine.class.getName()).log(Level.SEVERE, null, ex);
        } catch (IOException ex) {
            Logger.getLogger(ArgumentEngine.class.getName()).log(Level.SEVERE, null, ex);
        }

    }

    /**
     *
     * @param tree
     * @param depth
     * @param syntagmaList
     * @return
     */
    private String getPhraseList(Tree tree, int depth, List<Phrase> syntagmaList) {
        String text = "";

        if (tree.numChildren() == 0) {
            text = tree.value() + " ";
        } else {
            for (Tree node : tree.children()) {
                text += getPhraseList(node, depth + 1, syntagmaList);
            }
            if (text.split(" ").length > 1) {
                syntagmaList.add(new Phrase(text.trim(), tree.value(), depth));
            }
        }

        return text;
    }

}
