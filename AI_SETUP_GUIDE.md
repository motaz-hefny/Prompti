# AI Feature Setup Guide

This guide will help you enable the AI-powered prompt generation feature in Prompti.

## Quick Start

### 1. Get Your Google Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated API key

### 2. Configure Your Environment

1. In the project root directory, copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Open the `.env` file and add your API key:
   ```env
   VITE_GEMINI_API_KEY=your_actual_api_key_here
   ```

3. Save the file

### 3. Restart the Application

If the application is already running, restart it to load the new environment variables.

## How It Works

### Manual Assembly vs AI Generation

**Manual Assembly** (Generate Prompt button):
- Combines your input fields directly
- Follows the framework structure exactly
- Instant generation
- Works without API key

**AI-Enhanced** (✨ Generate with AI button):
- Sends your inputs to Google Gemini
- AI analyzes and optimizes your prompt
- Improves clarity and adds context
- Returns a professional, enhanced prompt
- Requires API key configuration

### Example Workflow

1. Fill in the framework fields with your information
2. Click "Generate Prompt" to see the manual assembly
3. Click "✨ Generate with AI" to get an AI-enhanced version
4. Compare both outputs
5. Choose the one that works best for your needs
6. Copy or download your preferred prompt

## Features

### AI Capabilities
- **Context Understanding**: AI understands the framework structure
- **Smart Enhancement**: Improves clarity without changing intent
- **Professional Language**: Uses appropriate tone and terminology
- **Structured Output**: Maintains framework organization

### Safety & Privacy
- Your inputs are sent to Google's Gemini API
- Google's safety filters are enabled
- No data is stored by Prompti
- Session data is stored locally in your browser

## Troubleshooting

### "API key is not configured"
- Make sure you created the `.env` file
- Verify the API key is correctly pasted
- Ensure the variable name is exactly `VITE_GEMINI_API_KEY`
- Restart the application after adding the key

### "Invalid API request"
- Check that you've filled in at least one field
- Ensure your inputs are not empty or just whitespace

### "API key is invalid or has insufficient permissions"
- Verify your API key at [Google AI Studio](https://makersuite.google.com/)
- Generate a new API key if needed
- Check that the API key has Gemini API access enabled

### "Rate limit exceeded"
- Google has rate limits on API usage
- Wait 30-60 seconds before trying again
- Consider upgrading your API quota if needed

### "Model not found" or "gemini-pro is not supported"
- **Fixed**: The app now uses `gemini-1.5-flash` model
- This is the current, supported model from Google
- If you see this error, ensure you have the latest version of the code
- The old `gemini-pro` model has been deprecated by Google

### Network Errors
- Check your internet connection
- Verify you can access Google services
- Check browser console for detailed error messages

## API Usage & Costs

### Free Tier
Google Gemini offers a generous free tier:
- 60 requests per minute
- 1,500 requests per day
- Suitable for personal use and testing

### Paid Tier
For higher usage:
- Visit [Google Cloud Console](https://console.cloud.google.com/)
- Enable billing for your project
- Higher rate limits and quotas available

## Security Best Practices

1. **Never commit your `.env` file to version control**
   - The `.env` file is already in `.gitignore`
   - Always use `.env.example` as a template

2. **Keep your API key private**
   - Don't share your API key publicly
   - Regenerate if accidentally exposed

3. **Use environment variables**
   - Never hardcode API keys in source code
   - Always use `import.meta.env.VITE_GEMINI_API_KEY`

## Additional Resources

- [Google Gemini API Documentation](https://ai.google.dev/docs)
- [Google AI Studio](https://makersuite.google.com/)
- [Gemini API Pricing](https://ai.google.dev/pricing)
- [API Quickstart Guide](https://ai.google.dev/tutorials/rest_quickstart)

## Support

If you encounter issues:
1. Check the browser console for error messages
2. Verify your API key configuration
3. Review the troubleshooting section above
4. Check Google's API status page

---

**Note**: The application works perfectly without an API key - you just won't have access to the AI enhancement feature. All other functionality (manual prompt assembly, export, multilingual support, etc.) works without any configuration.
