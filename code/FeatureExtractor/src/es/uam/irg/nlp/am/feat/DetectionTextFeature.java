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

import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.pipeline.CoreDocument;
import edu.stanford.nlp.trees.Tree;
import es.uam.irg.nlp.am.arguments.ArgumentEngine;
import es.uam.irg.nlp.am.arguments.ArgumentLinker;
import es.uam.irg.nlp.am.arguments.Phrase;
import es.uam.irg.utils.FeatureUtils;
import es.uam.irg.utils.StringUtils;
import java.util.ArrayList;
import java.util.List;

/**
 * Class containing the argumentative features extracted from a text for the
 * detection task.
 */
public class DetectionTextFeature extends TextFeature {

    // Class variables
    private List<String> adverbs;
    private int avgWordLength;
    private List<String> bigrams;
    private List<String> keyWords;
    private List<String> modalAuxs;
    private int numberPunctMarks;
    private int numberSubclauses;
    private int parseTreeDepth;
    private List<String> punctuation;
    private List<String> trigrams;
    private List<String> unigrams;
    private List<String> verbs;
    private List<String> wordCouples;

    /**
     *
     * @param id
     * @param text
     * @param argEngine
     * @param lexicon
     */
    public DetectionTextFeature(String id, String text, ArgumentEngine argEngine, List<ArgumentLinker> lexicon) {
        this.argEngine = argEngine;
        this.lexicon = lexicon;
        this.dateFormat = getDateFormat();
        this.id = id;
        this.text = text;
        this.unigrams = new ArrayList<>();
        this.bigrams = new ArrayList<>();
        this.trigrams = new ArrayList<>();
        this.adverbs = new ArrayList<>();
        this.verbs = new ArrayList<>();
        this.modalAuxs = new ArrayList<>();
        this.wordCouples = new ArrayList<>();
        this.punctuation = new ArrayList<>();
        this.keyWords = new ArrayList<>();
        this.textLength = text.length();
        this.avgWordLength = 0;
        this.numberPunctMarks = 0;
        this.parseTreeDepth = 0;
        this.numberSubclauses = 0;
        this.isValid = false;
    }

    /**
     *
     * @return
     */
    @Override
    public String toString() {
        String str = "{\"unigrams\": %s, \"bigrams\": %s, \"trigrams\": %s, \"adverbs\": %s, \"verbs\": %s, \"modal_aux\": %s,"
                + " \"word_couples\": %s, \"punctuation\": %s, \"key_words\": %s, \"text_length\": %d, \"avg_word_length\": %d,"
                + " \"number_punct_marks\": %d, \"parse_tree_depth\": %d, \"number_sub_clauses\": %d}";
        str = String.format(str, listToString(unigrams), listToString(bigrams), listToString(trigrams), listToString(adverbs),
                listToString(verbs), listToString(modalAuxs), listToString(wordCouples), listToString(punctuation),
                listToString(keyWords), textLength, avgWordLength, numberPunctMarks, parseTreeDepth, numberSubclauses);
        return str;
    }

    /**
     * Get phrase list.
     *
     * @return
     */
    private List<Phrase> getPhraseList() {
        Tree tree = this.argEngine.getConstituencyTree(this.text);
        List<Phrase> phraseList = this.argEngine.getPhraseList(tree);
        return phraseList;
    }

    /**
     *
     */
    @Override
    protected void extractFeatures() {
        CoreDocument nlpDoc = this.argEngine.createCoreNlpDocument(this.text);
        String currWord;
        String posTag;

        // 1. Split sentences into words
        for (CoreLabel token : nlpDoc.tokens()) {
            currWord = token.word();
            posTag = token.tag();

            // Adding words
            if ((posTag.equals("PUNCT") && !currWord.startsWith("etc")) || SPECIAL_PUNCT.indexOf(currWord.charAt(0)) >= 0) {
                String puntMark = StringUtils.cleanPuntuationMark(currWord);
                this.punctuation.add(puntMark);

            } else {
                // First filter
                if (StringUtils.isNumeric(currWord)) {
                    currWord = "$number$";
                } else if (StringUtils.isDateTime(currWord, this.dateFormat)) {
                    currWord = "$date$";
                } else if (StringUtils.isDateTime(currWord, "HH:mm")) {
                    currWord = "$time$";
                }

                // Second filter
                if (StringUtils.isValidToken(currWord)) {
                    this.unigrams.add(currWord);
                    this.avgWordLength += currWord.length();

                    // Adding POS tags
                    if (posTag.equals("VERB") && currWord.length() > 1) {
                        this.verbs.add(currWord);
                    } else if (posTag.equals("ADV")) {
                        this.adverbs.add(currWord);
                    } else if (posTag.equals("AUX")) {
                        this.modalAuxs.add(currWord);
                    }
                }
            }
        }

        // 2. If the sentence has valid words...
        if (this.unigrams.size() > 0) {
            this.avgWordLength /= this.unigrams.size();
            this.numberPunctMarks = this.punctuation.size();

            // 2.1 Group them into n-grams
            String bigram;
            String trigram;
            String wordN_1 = "";
            String wordN_2 = "";

            for (String word : this.unigrams) {
                bigram = (wordN_1.isEmpty() ? "$init$" : wordN_1) + "-" + word;
                this.bigrams.add(bigram);

                if (!wordN_1.isEmpty()) {
                    trigram = (wordN_2.isEmpty() ? "$init$" : wordN_2) + "-" + bigram;
                    this.trigrams.add(trigram);
                }

                wordN_2 = wordN_1;
                wordN_1 = word;
            }
            bigram = wordN_1 + "-$end$";
            trigram = wordN_2 + "-" + bigram;
            this.bigrams.add(bigram);
            this.trigrams.add(trigram);

            // 2.2. Create the parse tree
            List<Phrase> phraseList = getPhraseList();

            phraseList.forEach((Phrase frase) -> {
                if (frase.depth > this.parseTreeDepth) {
                    this.parseTreeDepth = frase.depth;
                }
            });
            this.numberSubclauses = phraseList.size();

            // 2.3. Group them into couple-of-words
            this.wordCouples = FeatureUtils.getWordCouples(this.unigrams);

            // 2.4. Get list of keywords
            this.keyWords = FeatureUtils.getUsedLinkerList(this.unigrams, this.lexicon);

            // 2.5. Save valid state
            this.isValid = true;
        }

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
