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
    private ArgumentLinker linker;
    
    // Class members
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
