/**
 * Mistral AI Training Configuration for PIANDT Chat Agent
 * This file contains the system prompt and knowledge base for training Mistral
 */

// System Prompt - This trains Mistral on how to respond
const MISTRAL_SYSTEM_PROMPT = `You are a knowledgeable assistant for the PIANDT (Proportional Information Architecture for Networked Digital Transactions) website. Your role is to help users understand the triadic information architecture and navigate the site effectively.

## Your Knowledge Base

PIANDT uses a triadic information architecture with three stages:
1. **In (Incoming Signals)**: Reception and initial processing of external signals
2. **Processing (Proc)**: Analysis, transformation, and synthesis of signals
3. **Out (Delivered Outputs)**: Formatted delivery of processed signals to stakeholders

## Key Principles

1. **Signal Proportionality**: S_In ∝ S_Proc ∝ S_Out - Every input signal generates a corresponding processing pathway and output mechanism
2. **Bidirectionality**: Information flows in both directions (organization ↔ external stakeholders)
3. **Automation**: The structured nature enables full automation of business transactions
4. **Triadic Mapping**: Every signal maintains explicit mapping across In, Proc, and Out stages

## Response Guidelines

- Be concise but informative
- Always reference specific pages when relevant
- Explain the triadic relationship when discussing any component
- Mention bidirectionality when relevant
- Highlight automation capabilities when appropriate
- Use the page descriptions and FAQs provided in context to give accurate answers
- If you don't know something, admit it rather than guessing

## Site Structure

The site has three main sections:
- **About PIANDT**: Mission, vision, governance, charitable purposes, trustees, our approach
- **Units**: Machine Intelligence Unit (MIU) with Vision, Products, and Services
- Each section has In, Processing, and Out variants

Always provide helpful, accurate information based on the context provided.`;

// Knowledge Base - Will be populated from pages.html
let KNOWLEDGE_BASE = [];

/**
 * Load knowledge base from pages.html
 * This extracts all page descriptions and FAQs for RAG
 */
async function loadKnowledgeBase() {
    try {
        const response = await fetch('site_agent/pages.html');
        const html = await response.text();
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        
        const rows = doc.querySelectorAll('tbody tr');
        KNOWLEDGE_BASE = [];
        
        rows.forEach((row, index) => {
            const cells = row.querySelectorAll('td');
            if (cells.length >= 7) {
                const url = cells[1]?.textContent?.trim() || '';
                const heading = cells[2]?.textContent?.trim() || '';
                const description = cells[3]?.textContent?.trim() || '';
                const faq = cells[5]?.textContent?.trim() || '';
                
                KNOWLEDGE_BASE.push({
                    id: index + 1,
                    url: url,
                    heading: heading,
                    description: description,
                    faq: faq
                });
            }
        });
        
        console.log(`✅ Loaded ${KNOWLEDGE_BASE.length} pages into knowledge base`);
        return KNOWLEDGE_BASE;
    } catch (error) {
        console.error('Error loading knowledge base:', error);
        return [];
    }
}

/**
 * Search knowledge base for relevant content (RAG)
 * Returns top N most relevant pages based on query
 */
function searchKnowledgeBase(query, topN = 3) {
    if (!KNOWLEDGE_BASE.length) return [];
    
    const queryLower = query.toLowerCase();
    const scored = KNOWLEDGE_BASE.map(page => {
        let score = 0;
        const heading = (page.heading || '').toLowerCase();
        const description = (page.description || '').toLowerCase();
        const faq = (page.faq || '').toLowerCase();
        
        // Score based on keyword matches
        const queryWords = queryLower.split(/\s+/);
        queryWords.forEach(word => {
            if (word.length < 3) return; // Skip short words
            
            if (heading.includes(word)) score += 10;
            if (description.includes(word)) score += 5;
            if (faq.includes(word)) score += 3;
        });
        
        // Boost score for exact phrase matches
        if (heading.includes(queryLower)) score += 20;
        if (description.includes(queryLower)) score += 15;
        
        return { ...page, score };
    });
    
    // Sort by score and return top N
    return scored
        .filter(p => p.score > 0)
        .sort((a, b) => b.score - a.score)
        .slice(0, topN);
}

/**
 * Build context for Mistral from knowledge base search
 */
function buildContext(query) {
    const relevantPages = searchKnowledgeBase(query, 3);
    
    if (relevantPages.length === 0) {
        return "No specific page information found. Use general PIANDT knowledge.";
    }
    
    let context = "Relevant page information:\n\n";
    relevantPages.forEach((page, idx) => {
        context += `Page ${idx + 1}: ${page.heading}\n`;
        context += `URL: ${page.url}\n`;
        context += `Description: ${page.description.substring(0, 500)}...\n`;
        if (page.faq) {
            context += `FAQ: ${page.faq.substring(0, 300)}...\n`;
        }
        context += "\n";
    });
    
    return context;
}

// Export for use in script.js
if (typeof window !== 'undefined') {
    window.MISTRAL_TRAINING = {
        SYSTEM_PROMPT: MISTRAL_SYSTEM_PROMPT,
        loadKnowledgeBase,
        searchKnowledgeBase,
        buildContext,
        KNOWLEDGE_BASE
    };
}

