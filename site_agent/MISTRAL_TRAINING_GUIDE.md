# Mistral AI Training Guide for PIANDT Chat Agent

## Overview

This guide explains how to train Mistral AI to respond effectively to site users using the PIANDT website's content.

## Architecture

The training system uses **RAG (Retrieval Augmented Generation)** which combines:
1. **System Prompt**: Core instructions for Mistral
2. **Knowledge Base**: All page descriptions and FAQs from `pages.html`
3. **Context Retrieval**: Relevant pages selected based on user queries
4. **Conversation History**: Last 8-10 messages for context

## How It Works

### 1. Knowledge Base Loading
- On initialization, `mistral_training_config.js` loads all pages from `pages.html`
- Extracts: URL, heading, description, and FAQ for each page
- Creates a searchable knowledge base

### 2. Query Processing
When a user asks a question:
1. **Search**: The system searches the knowledge base for relevant pages
2. **Score**: Pages are scored based on keyword matches
3. **Select**: Top 3 most relevant pages are selected
4. **Context**: Selected pages are formatted into context for Mistral

### 3. Mistral API Call
- System prompt + context + conversation history are sent to Mistral
- Mistral generates a response based on the provided context
- Response is formatted and displayed to the user

## Training Components

### System Prompt (`MISTRAL_SYSTEM_PROMPT`)
Located in `mistral_training_config.js`, this prompt:
- Defines Mistral's role as a PIANDT assistant
- Explains the triadic architecture (In, Proc, Out)
- Provides key principles (proportionality, bidirectionality, automation)
- Sets response guidelines (concise, accurate, reference pages)

### Knowledge Base
- Automatically loaded from `pages.html`
- Contains all 52 pages with descriptions and FAQs
- Updated automatically when `pages.html` is regenerated

### RAG (Retrieval Augmented Generation)
- `searchKnowledgeBase()`: Finds relevant pages
- `buildContext()`: Formats context for Mistral
- Ensures responses are grounded in actual site content

## Setup Instructions

### 1. Include Training Config
Add to your HTML pages (before `script.js`):
```html
<script src="site_agent/mistral_training_config.js"></script>
<script src="script.js"></script>
```

### 2. Get Mistral API Key
1. Visit https://console.mistral.ai/
2. Sign up/login
3. Create an API key
4. Set it in chat: `/setkey your-api-key`

### 3. Test the Integration
1. Open chat agent
2. Type: `/setkey your-api-key`
3. Ask: "What is the triadic information architecture?"
4. Mistral should respond using site content

## Customization

### Adjust System Prompt
Edit `MISTRAL_SYSTEM_PROMPT` in `mistral_training_config.js` to:
- Change response style
- Add domain-specific knowledge
- Modify guidelines

### Change Model
In `script.js`, find:
```javascript
model: 'mistral-small', // Change to 'mistral-medium' or 'mistral-large-latest'
```

### Adjust Context Size
In `script.js`:
```javascript
...conversationHistory.slice(-8), // Change -8 to adjust context window
```

### Modify RAG Parameters
In `mistral_training_config.js`:
```javascript
function searchKnowledgeBase(query, topN = 3) { // Change topN
```

## Best Practices

### 1. Keep Knowledge Base Updated
- Regenerate `pages.html` when content changes
- Knowledge base auto-updates on next load

### 2. Monitor Responses
- Check browser console for errors
- Review Mistral responses for accuracy
- Adjust system prompt if needed

### 3. Optimize Context
- Too much context = slower, more expensive
- Too little context = less accurate
- Balance: 3-5 relevant pages usually optimal

### 4. Test Different Models
- `mistral-tiny`: Fast, basic responses
- `mistral-small`: Balanced (recommended)
- `mistral-medium`: Better quality, slower
- `mistral-large-latest`: Best quality, slowest

## Advanced: Fine-Tuning

For even better results, you can:

### 1. Create Training Dataset
Extract Q&A pairs from your FAQs:
```javascript
// Example training data format
const trainingData = [
    {
        input: "What is the triadic architecture?",
        output: "The triadic information architecture has three stages..."
    },
    // ... more examples
];
```

### 2. Fine-Tune Mistral Model
- Use Mistral's fine-tuning API
- Train on your specific Q&A pairs
- Deploy fine-tuned model

### 3. Add Domain-Specific Terms
Update system prompt with:
- Technical terminology
- Acronyms and abbreviations
- Industry-specific concepts

## Troubleshooting

### Knowledge Base Not Loading
- Check browser console for errors
- Verify `pages.html` path is correct
- Ensure CORS allows fetching

### Poor Response Quality
- Increase context (more pages)
- Improve system prompt clarity
- Try a larger model (mistral-medium)

### API Errors
- Verify API key is correct
- Check API quota/credits
- Review network tab for errors

## Security Notes

⚠️ **Important**: 
- Never expose API keys in client-side code for production
- Use a backend proxy to handle API calls
- Implement rate limiting
- Monitor API usage

## Example Training Flow

1. **User asks**: "What is MIU?"
2. **System searches**: Finds pages with "MIU" in heading/description
3. **Context built**: Includes MIU vision, products, services pages
4. **Mistral receives**: System prompt + MIU context + conversation history
5. **Mistral responds**: "MIU (Machine Intelligence Unit) is part of the Units section..."
6. **Response displayed**: Formatted with links to relevant pages

## Next Steps

1. ✅ Set up Mistral API key
2. ✅ Test basic queries
3. ✅ Monitor response quality
4. ✅ Adjust system prompt as needed
5. ✅ Consider fine-tuning for production

For questions or issues, check the browser console for detailed error messages.

