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
public class ArgumentFeature extends TextFeature {

    // Class variables
    private final ArgumentEngine argEngine;
    private final List<ArgumentLinker> lexicon;
    private final String dateFormat;

    // Structural features (5)
    private final int textLength;
    private final int textPosition;
    private int tokenCount;
    private int avgWordLength;
    private int punctMarksCount;

    // Lexical features (11)
    private List<String> bowUnigrams;
    private List<String> bowBigrams;
    private List<String> bowTrigrams;
    private List<String> posUnigrams;
    private List<String> posBigrams;
    private List<String> wordCouples;
    private List<String> entities;
    private List<String> adverbs;
    private List<String> verbs;
    private List<String> nouns;
    private List<String> modalAuxs;

    // Syntactic features (2)
    private int parseTreeDepth;
    private int subClausesCount;

    // Discourse markers (2)
    private List<String> punctuation;
    private List<String> keyWords;

    /**
     *
     * @param id
     * @param text
     * @param argEngine
     * @param lexicon
     */
    public ArgumentFeature(String id, String text, ArgumentEngine argEngine, List<ArgumentLinker> lexicon) {

        // Base variables
        this.id = id;
        this.text = text;
        this.argEngine = argEngine;
        this.lexicon = lexicon;
        this.dateFormat = getDateFormat();

        // Structural features
        this.textLength = text.length();
        this.textPosition = getSentencePosition();
        this.tokenCount = 0;
        this.avgWordLength = 0;
        this.punctMarksCount = 0;

        // Lexical features
        this.bowUnigrams = new ArrayList<>();
        this.bowBigrams = new ArrayList<>();
        this.bowTrigrams = new ArrayList<>();
        this.posUnigrams = new ArrayList<>();
        this.posBigrams = new ArrayList<>();
        this.wordCouples = new ArrayList<>();
        this.entities = new ArrayList<>();
        this.adverbs = new ArrayList<>();
        this.verbs = new ArrayList<>();
        this.nouns = new ArrayList<>();
        this.modalAuxs = new ArrayList<>();

        // Syntactic features
        this.parseTreeDepth = 0;
        this.subClausesCount = 0;

        // Discourse markers
        this.punctuation = new ArrayList<>();
        this.keyWords = new ArrayList<>();
    }

    /**
     * Runs feature extraction method.
     *
     * @return
     */
    @Override
    public boolean extraction() {
        if (this.textLength >= MIN_LENGTH) {
            // NLP-processing
            return extractFeatures();
        }
        return false;
    }

    /**
     *
     * @return
     */
    @Override
    public String toString() {
        String str = "{\"id\": \"%s\", \"bow_unigrams\": %s, \"bow_bigrams\": %s, \"bow_trigrams\": %s, \"pos_unigrams\": %s, \"pos_bigrams\": %s, \"word_couples\": %s,"
                + " \"entities\": %s, \"adverbs\": %s, \"verbs\": %s, \"nouns\": %s, \"modal_auxs\": %s, \"punctuation\": %s, \"key_words\": %s,"
                + " \"text_length\": %d, \"text_position\": %d, \"token_count\": %d, \"avg_word_length\": %d,"
                + " \"punct_marks_count\": %d, \"parse_tree_depth\": %d, \"sub_clauses_count\": %d}";
        str = String.format(str, id, listToString(bowUnigrams), listToString(bowBigrams), listToString(bowTrigrams), listToString(posUnigrams),
                listToString(posBigrams), listToString(wordCouples), listToString(entities), listToString(adverbs), listToString(verbs),
                listToString(nouns), listToString(modalAuxs), listToString(punctuation), listToString(keyWords),
                textLength, textPosition, tokenCount, avgWordLength, punctMarksCount, parseTreeDepth, subClausesCount);
        return str;
    }

    /**
     *
     */
    private boolean extractFeatures() {
        boolean isValid = false;

        // Get tokens
        CoreDocument nlpDoc = this.argEngine.createCoreNlpDocument(this.text);
        List<CoreLabel> tokens = nlpDoc.tokens();

        // Extract features
        if (tokens.size() > 0) {
            this.tokenCount = tokens.size();
            String currWord;
            String posTag;

            // 1. Split sentences into words
            for (CoreLabel token : tokens) {
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
                        this.bowUnigrams.add(currWord);
                        this.posUnigrams.add(posTag);
                        this.avgWordLength += currWord.length();

                        // Adding POS tags
                        if (posTag.equals("VERB") && currWord.length() > 1) {
                            this.verbs.add(currWord);
                        } else if (posTag.equals("ADV")) {
                            this.adverbs.add(currWord);
                        } else if (posTag.equals("AUX")) {
                            this.modalAuxs.add(currWord);
                        } else if (posTag.equals("NOUN")) {
                            this.nouns.add(currWord);
                        }
                    }
                }
            }

            // 2. If the sentence has valid words...
            if (this.bowUnigrams.size() > 0) {
                this.avgWordLength /= this.bowUnigrams.size();
                this.punctMarksCount = this.punctuation.size();

                // 2.1 Extract baseline lexical features
                String bigram;
                String trigram;
                String wordN_1 = "";
                String wordN_2 = "";

                for (String word : this.bowUnigrams) {
                    bigram = (wordN_1.isEmpty() ? "$init$" : wordN_1) + "-" + word;
                    this.bowBigrams.add(bigram);

                    if (!wordN_1.isEmpty()) {
                        trigram = (wordN_2.isEmpty() ? "$init$" : wordN_2) + "-" + bigram;
                        this.bowTrigrams.add(trigram);
                    }

                    wordN_2 = wordN_1;
                    wordN_1 = word;
                }
                bigram = wordN_1 + "-$end$";
                trigram = wordN_2 + "-" + bigram;
                this.bowBigrams.add(bigram);
                this.bowTrigrams.add(trigram);

                // 2.2. Extract POS bigrams
                wordN_1 = "";

                for (String word : this.posUnigrams) {
                    bigram = (wordN_1.isEmpty() ? "$init$" : wordN_1) + "-" + word;
                    this.posBigrams.add(bigram);
                    wordN_1 = word;
                }
                bigram = wordN_1 + "-$end$";
                this.posBigrams.add(bigram);

                // 2.3. Named entity recognition
                this.entities = this.argEngine.getNamedEntities(this.text);

                // 2.4. Create the parse tree
                List<Phrase> phraseList = getPhraseList();

                phraseList.forEach((Phrase frase) -> {
                    if (frase.depth > this.parseTreeDepth) {
                        this.parseTreeDepth = frase.depth;
                    }
                });
                this.subClausesCount = phraseList.size();

                // 2.5. Group them into couple-of-words
                this.wordCouples = FeatureUtils.getWordCouples(this.bowUnigrams);

                // 2.6. Get list of keywords
                this.keyWords = FeatureUtils.getUsedLinkerList(this.bowUnigrams, this.lexicon);

                // 2.7. Save valid state
                isValid = true;
            }
        }

        return isValid;
    }

    /**
     *
     * @return
     */
    private String getDateFormat() {
        String format = "";
        if (this.argEngine != null) {
            String lang = this.argEngine.getCurrentLanguage();
            format = (lang.equals("en") ? "MM/dd/yyyy" : "dd/MM/yyyy");
        }
        return format;
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

}
