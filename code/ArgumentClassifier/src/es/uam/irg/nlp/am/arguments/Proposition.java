/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package es.uam.irg.nlp.am.arguments;

/**
 * Class representing a statement or assertion that expresses a judgement or opinion
 * 
 * @author ansegura
 */
public class Proposition {
    
    private int proposalID;
    private int sentenceID;
    private String text;
    private String label;
    
    public Proposition(int proposalID, int sentenceID, String text, String label) {
        this.proposalID = proposalID;
        this.sentenceID = sentenceID;
        this.text = text;
        this.label = label;
    }
    
    @Override
    public String toString() {
        return String.format("%s-%s > %s [%s]", 
                this.proposalID, this.sentenceID, this.text, this.label);
    }
    
}
