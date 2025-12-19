# Prompti Web Application Requirements Document

## 1. Application Overview

### 1.1 Application Name
Prompti — Structured Prompt Generator with Multi-AI Enhancement

### 1.2 Application Description
Prompti is a lightweight web-based tool designed to help users create precise, professional prompts for AI systems. It converts loosely-formed goals into structured prompts using four proven frameworks (ICDF, RCR-EOC, MICRO, COSTAR). The application targets product managers, marketers, analysts, AI users, and non-native English speakers who need repeatable, audit-ready prompts. Now enhanced with multi-AI provider support including Google Gemini, Groq, Open Router, and other alternatives for flexible prompt generation.

### 1.3 Target Users
- Product managers, marketers, and analysts requiring repeatable prompts
- AI users needing audit-ready structured prompts
- Non-native English speakers wanting multilingual UI support
- Users seeking rapid prototyping and sharing of AI prompts
- Users wanting AI-enhanced prompt variations with multiple model options

---

## 2. Core Features

### 2.1 Authentication
- Mock'Sign In with Google' button (UI placeholder only, non-functional in current version)
- Note: Full Google OAuth integration requires additional setup and is planned for future Pro version
- Current version operates without authentication requirement

### 2.2 Prompt Framework Selection
Four structured prompt templates:
- **ICDF**: Instruction, Context, Data, Format
- **RCR-EOC**: Role, Context (Work Environment), Request, Examples, Output, Constraints
- **MICRO**: Message, Intention, Context, Rhythm, Output\n- **COSTAR**: Context, Offer, Style, Target, Action, Result

### 2.3 Dynamic Form Interface
- Framework-specific input fields with help tooltips
- Field validation (required fields unless 'Allow blanks' is enabled)
- Session persistence for field values per framework
- One-click example insertion for each framework
- Reset fields functionality

### 2.4 Live Preview
- Real-time preview updates as user types
- Display assembled prompt structure
- Show formatted output with proper section labels
\n### 2.5 Prompt Generation
- Generate final structured prompt based on user input
- Validate required fields before generation
- Display final prompt in monospaced code format

### 2.6 AI Model Selector
- **Dropdown Menu**: Select AI provider from available options
- **Supported Providers**:
  - Google Gemini (gemini-pro)
  - Groq (mixtral-8x7b-32768, llama2-70b-4096)
  - Open Router (multiple models via unified API)
  - Other alternatives (extensible architecture)
- **Model Display**: Show selected model name and provider
- **Fallback Logic**: Auto-switch to next available provider if current fails
- **Status Indicator**: Visual feedback for provider availability

### 2.7 AI-Enhanced Prompt Generation
- **AI Generate Button**: Triggers selected AI provider API to generate inspired prompt
- **Input Processing**: Sends all user-filled fields to chosen AI model
- **AI Output**: Generates a new prompt inspired by user input, creatively enhanced
- **Display**: Shows AI-generated prompt in separate section below manual prompt
- **Feedback**: Loading indicator during API call, error handling with provider-specific messages
- **Retry Mechanism**: Automatic fallback to alternative providers if primary fails

### 2.8 Export Options
- **Copy to Clipboard**: JavaScript-based clipboard copy with success/error feedback (works for both manual and AI-generated prompts)
- **Download Prompt**: Save as .txt file with naming pattern'prompti_prompt_<framework>_<lang>_<type>_<provider>.txt'
- **Save to Drive**: Disabled placeholder button with tooltip indicating Pro subscription requirement

### 2.9 Multilingual Support
Three language options:
- **English (en)**: Default language
- **Modern Standard Arabic (ar)**: Formal Arabic with RTL support
- **Egyptian Arabic (eg)**: Colloquial Egyptian with randomized slang variants for playful microcopy

### 2.10 RTL (Right-to-Left) Support\n- Automatic RTL layout for Arabic languages
- Right-aligned text and UI elements
- Flipped button visual order for RTL languages

---\n
## 3. User Interface Design

### 3.1 Layout Structure

**Sidebar:**
- Language selector (radio buttons): English / العربية / مصرّي
- Framework selector (dropdown): ICDF / RCR-EOC / MICRO / COSTAR
- **AI Model Selector (dropdown)**: Gemini / Groq / Open Router / Others
- Mock'Sign In with Google' button (non-functional placeholder)
-'Allow blanks' checkbox\n
**Main Area (Two-column layout):**
- **Left Column**: Dynamic form with framework-specific fields and help tooltips
- **Right Column**: \n  - Live preview section (top)\n  - Manual generated prompt display (code block)
  - AI model selector and status indicator
  - AI-generated prompt display (code block with distinct styling and provider label)
  - Export controls (Copy, Download, Save to Drive buttons for both manual and AI prompts)
  - 'Generate with AI' button positioned between manual and AI prompt sections

### 3.2 Design Style
- **Color Scheme**: Clean professional palette with primary blue accent (#4285F4), neutral grays, high-contrast text, distinct accent colors per AI provider (Gemini: purple #9C27B0, Groq: orange #FF6B35, Open Router: teal #00BCD4)
- **Typography**: Sans-serif font family (system default or Roboto), monospaced font (Courier or Monaco) for code blocks
- **Layout**: Card-based design with clear visual hierarchy, generous whitespace, responsive grid system
- **Interactive Elements**: Rounded buttons with subtle shadows, smooth hover transitions, clear focus states, AI provider badges with gradient effects
- **Visual Feedback**: Success messages in green, error messages in red, loading spinner with provider logo during AI generation, disabled states with reduced opacity and explanatory tooltips

---

## 4. Technical Requirements

### 4.1 Technology Stack
- **Framework**: Streamlit (Python-based web framework)
- **Language**: Python 3.9+
- **AI Integration**: Multi-provider support (Google Gemini, Groq, Open Router)\n- **Dependencies**: Listed in requirements.txt (including google-generativeai, groq, openai libraries)
\n### 4.2 API Configuration
- **Google Gemini API Key**: AIzaSyDZBbO8P4MEZ5lUhade1G8JJVJL_GKdDKE
- **Groq API Key**: User-provided or configured in environment\n- **Open Router API Key**: User-provided or configured in environment\n- **Configuration Method**: Set as environment variables or configure in Streamlit secrets.toml file:\n  - GEMINI_API_KEY\n  - GROQ_API_KEY
  - OPENROUTER_API_KEY
- **API Models**:
  - Gemini: gemini-pro, gemini-1.5-pro\n  - Groq: mixtral-8x7b-32768, llama2-70b-4096, llama3-70b-8192
  - Open Router: gpt-4, claude-3-opus, and other supported models

### 4.3 Implementation Options
- **Option A (MVP)**: Single-file app.py + requirements.txt
- **Option B (Advanced)**: Multi-file architecture:\n  - app.py (UI)\n  - i18n.py (translations and helpers)
  - prompts.py (prompt assembly logic)
  - ai_generator.py (multi-provider AI integration with fallback logic)
  - providers/ (separate modules for each AI provider)
  - utils.py (clipboard helper, RTL CSS, sanitizer)
  - auth.py (mock + future OAuth skeleton)
  - requirements.txt\n  - README.md

### 4.4 Data Persistence
- Session state management for field values per framework
- Framework switching saves and restores field state
- Random slang variant persistence per session for Egyptian locale
- Store both manual and AI-generated prompts in session state
- Persist selected AI provider preference

### 4.5 Prompt Assembly Rules
- Sections must follow framework-specific order with translated labels
- Two newline characters between sections
- Trim whitespace on values, preserve internal newlines
- No trailing whitespace or newline in final output
\n### 4.6 AI Generation Rules
- Send all user-filled fields to selected AI provider with instruction to generate inspired variation
- API prompt template:'Based on the following structured prompt elements, generate a creative and enhanced prompt that is inspired by but not identical to the input: [user fields]'
- **Fallback Logic**: If primary provider fails, automatically try next available provider in order: Gemini → Groq → Open Router → Others
- Handle API rate limits and errors gracefully with provider-specific error messages
- Timeout set to 10 seconds per provider with fallback to next\n- Display which provider successfully generated the prompt

---

## 5. Functional Specifications

### 5.1 Language Toggle
- Changes all UI strings to selected language
- Applies RTL layout for Arabic languages
- Loads language-specific examples\n- Persists selection in session state

### 5.2 Framework Selection
- Displays framework-specific input fields
- Loads saved field values for selected framework
- Updates live preview based on framework structure
\n### 5.3 AI Model Selection
- Dropdown displays available AI providers
- Shows provider status (available/unavailable) with visual indicators
- Persists selection in session state
- Updates AI generation button label with selected provider name
- Displays provider-specific configuration requirements if API key missing

### 5.4 Field Input and Validation
- Required field validation (unless 'Allow blanks' enabled)
- Help tooltips for each field explaining purpose
- Real-time live preview updates
\n### 5.5 Example Insertion
- One-click population of fields with predefined examples
- Language-specific examples (English, MSA, Egyptian)
- Success message confirmation
\n### 5.6 Prompt Generation
- Validates required fields\n- Assembles prompt according to framework rules
- Displays final prompt in code block\n- Stores in session state for export
\n### 5.7 AI Prompt Generation
- User selects AI provider from dropdown
- User clicks 'Generate with AI' button
- System validates that manual prompt has been generated
- Displays loading indicator with provider logo
- Sends user input fields to selected AI provider API
- If provider fails, automatically tries next available provider
- Receives AI-generated prompt variation
- Displays AI prompt in separate code block with provider badge
- Stores AI prompt and provider info in session state
- Shows success message with provider name or error feedback with retry options

### 5.8 Export Functionality
- **Copy**: Uses JavaScript clipboard API with fallback message (separate buttons for manual and AI prompts)
- **Download**: Generates .txt file with proper naming convention including provider name
- **Save to Drive**: Disabled with tooltip explaining Pro requirement
\n---

## 6. Acceptance Criteria

### 6.1 Functional Tests
- Loading EXAMPLES produces exact expected prompt output
- Language toggle changes all UI strings correctly
- RTL layout applies properly for Arabic languages
- Egyptian locale uses randomized slang variants
- Copy to clipboard writes exact assembled prompt (both manual and AI)
- Download saves correct .txt file with proper filename including provider\n- Save to Drive button is disabled with visible tooltip
- Insert example populates fields correctly
- Reset fields clears current framework data only
- AI model selector displays all available providers
- AI generation works with each configured provider
- Fallback logic switches to next provider on failure
- Provider status indicators update correctly
- Loading indicator shows current provider during generation
- Error messages specify which provider failed and why
- Both manual and AI prompts can be exported independently
- Provider badge displays correctly on AI-generated prompts

### 6.2 Accessibility Requirements
- All inputs have visible labels
- Help tooltips available for all fields
- Buttons are keyboard-focusable
- Color contrast meets readability standards
- AI generation status announced for screen readers
- Provider selection accessible via keyboard navigation
\n---

## 7. Deployment\n
### 7.1 Google Sign-In Status
- **Current Implementation**: Mock button (UI placeholder only)
- **Functionality**: Non-functional in current version
- **Future Implementation**: Requires Google OAuth 2.0 setup including:
  - Google Cloud Console project creation
  - OAuth 2.0 credentials configuration
  - Authorized redirect URIs setup
  - Streamlit-google-auth library integration
- **Recommendation**: Deploy current version without authentication, add OAuth in future update

### 7.2 Publishing Options
\n**Option 1: Streamlit Community Cloud (Recommended)**
- Free hosting for public apps
- Steps:
  1. Push code to GitHub repository
  2. Visit share.streamlit.io
  3. Connect GitHub account
  4. Select repository and branch
  5. Add API keys to Secrets section (Settings > Secrets):\n     - GEMINI_API_KEY
     - GROQ_API_KEY
     - OPENROUTER_API_KEY\n  6. Deploy
- Public URL format: https://[username]-[repo-name]-[branch]-[app-file].streamlit.app
\n**Option 2: Hugging Face Spaces**
- Free hosting with GPU options
- Steps:
  1. Create account at huggingface.co
  2. Create new Space, select Streamlit SDK
  3. Upload app.py and requirements.txt
  4. Add API keys in Settings > Repository secrets
  5. Space auto-deploys\n- Public URL format: https://huggingface.co/spaces/[username]/[space-name]

**Option 3: Self-Hosting**
- Deploy on personal server or cloud VM (AWS, Google Cloud, Azure)
- Requires domain setup and SSL certificate
- Use process manager (PM2, systemd) for production

### 7.3 Installation Steps
1. Python 3.9+ required
2. Install dependencies: pip install -r requirements.txt
3. Configure API keys:\n   - Method A: Set environment variables:\n     ```\n     export GEMINI_API_KEY='AIzaSyDZBbO8P4MEZ5lUhade1G8JJVJL_GKdDKE'
     export GROQ_API_KEY='your_groq_api_key'
     export OPENROUTER_API_KEY='your_openrouter_api_key'
     ```
   - Method B: Create .streamlit/secrets.toml file with content:
     ```
     GEMINI_API_KEY = 'AIzaSyDZBbO8P4MEZ5lUhade1G8JJVJL_GKdDKE'
     GROQ_API_KEY = 'your_groq_api_key'
     OPENROUTER_API_KEY = 'your_openrouter_api_key'
     ```
4. Run application: streamlit run app.py\n5. Access at http://localhost:8501
\n### 7.4 Environment Variables
- **GEMINI_API_KEY**: AIzaSyDZBbO8P4MEZ5lUhade1G8JJVJL_GKdDKE (required for Gemini provider)
- **GROQ_API_KEY**: User-provided (required for Groq provider)
- **OPENROUTER_API_KEY**: User-provided (required for Open Router provider)
\n### 7.5 Security Notes
- Never commit API keys to public repositories
- Use Streamlit secrets or environment variables for production
- Consider API key rotation for long-term deployments
- Monitor API usage across all providers to avoid unexpected charges
- Implement rate limiting per provider to prevent abuse

---

## 8. Future Enhancements

### 8.1 Pro Features (Placeholder)
- Google OAuth authentication (full implementation)
- Save to Google Drive integration
- Advanced prompt templates\n- Collaboration features
- Custom AI model fine-tuning
- API usage analytics dashboard

### 8.2 Extensibility
- Additional language locales\n- More prompt frameworks
- Custom framework creation
- Prompt history and versioning
- AI prompt refinement iterations
- Additional AI providers (Anthropic Claude, Cohere, etc.)
- Model performance comparison features

---

## 9. Reference Files

1. Technical Specification Document: Prompti — Ultimate Windsurf-ready specification (provided in user upload)
   - Contains complete TRANSLATIONS dictionary (en/ar/eg)
   - EG_SLANG_VARIANTS for randomized Egyptian microcopy
   - EXAMPLES presets for all frameworks and languages
   - Detailed implementation rules and acceptance tests
   - Developer checklist and deployment notes