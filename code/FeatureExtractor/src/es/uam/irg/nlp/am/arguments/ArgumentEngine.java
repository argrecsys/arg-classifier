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
import edu.stanford.nlp.util.CoreMap;
import es.uam.irg.io.IOManager;
import java.io.*;
import java.util.*;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * Class of the argument extractor engine.
 */
public class ArgumentEngine {

    public static final String LANG_EN = "en";
    public static final String LANG_ES = "es";
    private static final HashSet<String> ENTITY_TYPE = new HashSet(
            Arrays.asList("PERSON", "LOCATION", "ORGANIZATION", "MISC", "CITY", "STATE_OR_PROVINCE", "COUNTRY", "TITLE"));
    private static final String SPANISH_PROPERTIES = "Resources/config/StanfordCoreNLP-spanish.properties";

    // Class members
    private final String language;
    private StanfordCoreNLP pipeline;
    private final HashSet<String> stopwords;

    /**
     * Class constructor.
     *
     * @param lang
     */
    public ArgumentEngine(String lang) {
        this.language = lang;
        this.stopwords = getStopwordList(language);
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
     * @param text
     * @return
     */
    public Tree getConstituencyTree(String text) {
        Annotation annotation = new Annotation(text);
        pipeline.annotate(annotation);
        CoreMap sentence = annotation.get(CoreAnnotations.SentencesAnnotation.class).get(0);
        Tree tree = sentence.get(TreeCoreAnnotations.TreeAnnotation.class);
        return tree;
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
     * @param text
     * @return
     */
    public List<String> getNamedEntities(String text) {
        List<String> entities = new ArrayList<>();
        CoreDocument document = pipeline.processToCoreDocument(text);

        for (CoreEntityMention em : document.entityMentions()) {
            if (ENTITY_TYPE.contains(em.entityType())) {
                if (!this.stopwords.contains(em.text().toLowerCase()) || em.entityType().equals("ORGANIZATION") || (em.entityType().equals("MISC") && em.text().length() > 2)) {
                    entities.add(em.text());
                }
            }
        }

        return entities;
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
     * Creates the Stanford CoreNLP pipeline according to the specified
     * language.
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

    /**
     * Gets the set of stopwords in a specific language.
     *
     * @param language
     * @return
     */
    private HashSet<String> getStopwordList(String lang) {
        return IOManager.readStopwordList(lang, true);
    }

}
