# Mistral AI Chat Agent Setup

## Overview
The chat agent has been integrated with Mistral AI to provide intelligent, context-aware responses about the PIANDT website.

## Setup Instructions

### 1. Get Your Mistral API Key
1. Visit https://console.mistral.ai/
2. Sign up or log in to your account
3. Navigate to API Keys section
4. Create a new API key
5. Copy your API key

### 2. Configure the API Key

**Option A: Browser Console (Recommended for Testing)**
1. Open your browser's developer console (F12 or Cmd+Option+I)
2. Run the following command:
```javascript
localStorage.setItem('mistral_api_key', 'your-api-key-here');
```
3. Refresh the page

**Option B: Direct Code Edit**
1. Open `script.js`
2. Find the line: `const MISTRAL_API_KEY = localStorage.getItem('mistral_api_key') || '';`
3. Replace with: `const MISTRAL_API_KEY = 'your-api-key-here';`

### 3. Model Selection
The default model is `mistral-small`. You can change it in `script.js`:
- `mistral-tiny` - Fastest, least capable
- `mistral-small` - Balanced (default)
- `mistral-medium` - More capable
- `mistral-large-latest` - Most capable

## Features

### Intelligent Responses
- Context-aware answers about website structure
- Natural language understanding
- Conversation history maintained across messages
- Automatic fallback to rule-based system if API unavailable

### Knowledge Base
The agent has access to:
- Website structure (In, Processing, Out stages)
- Machine Intelligence Unit (MIU) information
- Product and service categories
- Page paths and descriptions

### Conversation Context
- Maintains last 10 messages for context
- Understands follow-up questions
- Provides relevant links automatically

## Usage

1. Click the chat agent button (bottom right)
2. Type your question
3. The agent will respond using Mistral AI
4. If API key is not set, it falls back to rule-based responses

## Troubleshooting

### API Key Not Working
- Verify the key is correct in browser console: `localStorage.getItem('mistral_api_key')`
- Check browser console for error messages
- Ensure you have API credits/quota available

### Network Errors
- Check your internet connection
- Verify Mistral API is accessible
- Check browser console for CORS or network errors

### Fallback Mode
If Mistral API is unavailable, the system automatically uses a rule-based fallback that still provides helpful responses about the website structure.

## Security Note
⚠️ **Important**: For production, do NOT hardcode API keys in client-side code. Use a backend proxy to handle API calls securely.




