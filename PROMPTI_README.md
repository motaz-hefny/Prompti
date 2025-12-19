# Prompti - Structured Prompt Generator

A lightweight web-based tool designed to help users create precise, professional prompts for AI systems. Prompti converts loosely-formed goals into structured prompts using four proven frameworks, with optional AI-powered enhancement via Google Gemini.

## Features

### 🎯 Four Proven Frameworks
- **ICDF**: Instruction, Context, Data, Format
- **RCR-EOC**: Role, Context, Request, Examples, Output, Constraints
- **MICRO**: Message, Intention, Context, Rhythm, Output
- **COSTAR**: Context, Offer, Style, Target, Action, Result

### ✨ AI-Powered Enhancement
- **Google Gemini Integration**: Generate AI-enhanced prompts based on your inputs
- **Smart Optimization**: AI analyzes your fields and creates optimized, professional prompts
- **Dual Output**: Compare manual assembly vs AI-generated prompts side-by-side
- **Intelligent Context**: AI understands the framework structure and enhances accordingly

### 🌍 Multilingual Support
- **English**: Default language with comprehensive UI
- **Modern Standard Arabic (العربية)**: Formal Arabic with full RTL support
- **Egyptian Arabic (مصرّي)**: Colloquial Egyptian with playful microcopy

### ✨ Key Capabilities
- **Dynamic Form Interface**: Framework-specific input fields with contextual help tooltips
- **Live Preview**: Real-time preview updates as you type
- **Field Validation**: Required field validation with "Allow blanks" option
- **Session Persistence**: Field values persist per framework across sessions
- **Example Insertion**: One-click population with language-specific examples
- **Export Options**:
  - Copy to clipboard with success feedback
  - Download as .txt file with proper naming convention
  - Save to Drive (placeholder for Pro subscription)

### 🎨 Design
- Clean, professional interface with Google blue accent (#4285F4)
- Card-based layout with clear visual hierarchy
- Responsive design optimized for desktop and mobile
- Full RTL (Right-to-Left) support for Arabic languages
- Dark mode support

## Setup

### Environment Configuration

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Get your Google Gemini API key:
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Copy the key

3. Add your API key to `.env`:
```env
VITE_GEMINI_API_KEY=your_actual_api_key_here
```

### Running the Application

The application will work without an API key, but the AI generation feature will be disabled. To enable AI-powered prompt generation, you must configure the Gemini API key as described above.

## Usage

### Getting Started
1. **Select Language**: Choose from English, Modern Standard Arabic, or Egyptian Arabic
2. **Choose Framework**: Select the prompt framework that best fits your needs
3. **Fill in Fields**: Complete the framework-specific fields (marked with * for required)
4. **Preview**: Watch the live preview update as you type
5. **Generate**: 
   - Click "Generate Prompt" for manual assembly
   - Click "✨ Generate with AI" for AI-enhanced version
6. **Export**: Copy to clipboard or download as a text file

### AI Generation vs Manual Assembly

**Manual Assembly** (Generate Prompt):
- Directly combines your input fields
- Follows framework structure exactly
- Instant generation
- No API key required

**AI-Enhanced** (Generate with AI):
- Analyzes your inputs and creates an optimized prompt
- Improves clarity and specificity
- Adds helpful context where appropriate
- Uses professional language
- Requires Google Gemini API key
- Takes a few seconds to generate

### Framework Selection Guide

**ICDF** - Best for:
- Clear, straightforward tasks
- Data analysis requests
- Format-specific outputs

**RCR-EOC** - Best for:
- Complex professional tasks
- Role-based scenarios
- Constrained outputs

**MICRO** - Best for:
- Communication-focused tasks
- Tone-specific requests
- Intention-driven prompts

**COSTAR** - Best for:
- Marketing and content creation
- Audience-targeted outputs
- Result-oriented tasks

### Tips for Better Prompts
1. Be specific in your instructions
2. Provide relevant context
3. Include examples when possible
4. Specify desired output format
5. Use the "Insert Example" button to see framework patterns
6. Try both manual and AI generation to compare results

## Technical Details

### Technology Stack
- **Frontend**: React 18 with TypeScript
- **UI Components**: shadcn/ui with Radix UI primitives
- **Styling**: Tailwind CSS with custom design system
- **State Management**: React hooks with session storage
- **Routing**: React Router v7
- **Notifications**: Sonner for toast messages
- **AI Integration**: Google Gemini API via Axios

### Project Structure
```
src/
├── components/
│   ├── prompti/
│   │   ├── PromptiSidebar.tsx    # Language & framework selection
│   │   ├── DynamicForm.tsx       # Framework-specific input form
│   │   └── PreviewPanel.tsx      # Live preview & export controls
│   └── ui/                        # shadcn/ui components
├── data/
│   └── translations.ts            # All translations and examples
├── hooks/
│   └── usePromptiState.ts        # Session state management
├── pages/
│   └── Prompti.tsx               # Main application page
├── types/
│   └── prompti.ts                # TypeScript type definitions
└── utils/
    ├── promptUtils.ts            # Prompt assembly & export utilities
    └── geminiApi.ts              # Google Gemini API integration
```

### Key Features Implementation

**AI Generation**
- Uses Google Gemini Pro model
- Sends framework context and user inputs
- Configurable temperature and safety settings
- Error handling for API failures
- Loading states during generation

**Session Persistence**
- Uses browser sessionStorage to persist field values
- Separate state for each framework
- Survives page refreshes within the same session
- Stores both manual and AI-generated prompts

**RTL Support**
- Automatic detection based on language selection
- CSS direction changes applied to document root
- Proper text alignment and layout adjustments

**Validation**
- Required field checking before prompt generation
- "Allow blanks" option to bypass validation
- User-friendly error messages via toast notifications

**Export Functionality**
- Clipboard API for copy functionality
- Blob-based file download with proper naming
- Separate filenames for AI vs manual prompts
- Disabled "Save to Drive" with tooltip for Pro feature

## API Configuration

### Google Gemini API

The application uses the Gemini Pro model with the following configuration:

- **Model**: `gemini-pro`
- **Temperature**: 0.7 (balanced creativity)
- **Top K**: 40
- **Top P**: 0.95
- **Max Output Tokens**: 2048
- **Safety Settings**: Medium and above blocking for all categories

### Error Handling

The application handles various API errors gracefully:
- Missing API key: Clear error message with setup instructions
- Invalid API key: Authentication error message
- Rate limiting: Retry suggestion
- Network errors: Generic error with retry option

## Browser Compatibility
- Modern browsers with ES6+ support
- Chrome, Firefox, Safari, Edge (latest versions)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Accessibility
- All inputs have visible labels
- Help tooltips for all fields
- Keyboard navigation support
- High contrast color scheme
- Screen reader friendly
- Loading states for async operations

## Future Enhancements
- Google OAuth authentication
- Save to Google Drive integration
- Custom framework creation
- Prompt history and versioning
- Collaboration features
- Additional language locales
- Alternative AI models (Claude, GPT-4, etc.)
- Prompt templates library
- A/B testing for prompts

## Troubleshooting

### AI Generation Not Working

1. **Check API Key**: Ensure `VITE_GEMINI_API_KEY` is set in your `.env` file
2. **Verify API Key**: Test your key at [Google AI Studio](https://makersuite.google.com/)
3. **Check Console**: Look for error messages in browser developer console
4. **Rate Limits**: If you see 429 errors, wait a moment before trying again

### Common Issues

- **"API key is not configured"**: Add your Gemini API key to `.env` file
- **"Invalid API request"**: Check that your inputs are not empty
- **"Rate limit exceeded"**: Wait 30-60 seconds before trying again
- **Network errors**: Check your internet connection

## License
Copyright 2025 Prompti

---

Built with ❤️ using React, TypeScript, shadcn/ui, and Google Gemini AI
