# README.md — Prompti Project Documentation

## 🎯 Prompti — Structured Prompt Generator

A lightweight, multilingual web app for creating precise, professional prompts for AI systems. Built with Streamlit, supporting English, Modern Standard Arabic (MSA), and Egyptian colloquial dialect.

---

## ✨ Features

### Core Functionality
- **4 Prompt Frameworks**: ICDF, RCR-EOC, MICRO, COSTAR
  - Each framework is optimized for different use cases (instruction-based, role-based, messaging, marketing)
  - Dynamically generated forms based on selected framework
- **Live Preview**: Real-time prompt assembly as you type
- **Generate & Export**: 
  - One-click prompt generation with validation
  - Copy to clipboard (with fallback for unsupported browsers)
  - Download as .txt file with auto-generated filename
  - Disabled "Save to Drive" placeholder (Pro feature, future)

### Multilingual Support
- **English** ('en'): Professional, formal tone
- **Modern Standard Arabic** ('ar'): Formal, professional Arabic
- **Egyptian Colloquial** ('eg'): Playful, informal with randomized slang variants
  - Microcopy variations for buttons, success messages, etc.
  - Session-based persistence ensures consistent UX within a session

### User Experience
- Responsive two-column layout (form on left, live preview + exports on right)
- RTL (Right-to-Left) support for Arabic/Egyptian languages
- Accessible form inputs with help tooltips and required field indicators
- Framework switching preserves field state (no data loss)
- "Insert Example" for quick framework learning
- "Reset Fields" to start over

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)

### Installation

1. **Clone or download the project**:
   ```bash
   cd /path/to/Prompti
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**:
   ```bash
   streamlit run app.py
   ```

4. **Open in browser**:
   - Streamlit will automatically open `http://localhost:8501`
   - If not, manually navigate to that URL

---

## 📁 Project Structure

```
Prompti/
├── app.py                    # Main Streamlit application (UI orchestration)
├── i18n.py                   # Internationalization (translations, slang variants)
├── prompts.py                # Prompt assembly logic (frameworks, examples, validation)
├── utils.py                  # Utility helpers (RTL CSS, clipboard JS, filename generation)
├── auth.py                   # Authentication skeleton (mock sign-in, future OAuth)
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── CHANGELOG.md              # Detailed version history and changes
└── 00-Goal.md                # Original project specification
```

### Module Responsibilities

| Module | Purpose |
|--------|---------|
| `app.py` | Main Streamlit app; orchestrates UI, handles form submission, renders two-column layout |
| `i18n.py` | All translations (English, MSA, Egyptian); slang randomization; fallback logic |
| `prompts.py` | Framework definitions, example presets, prompt assembly, input sanitization |
| `utils.py` | RTL CSS, clipboard JavaScript, filename generation, field validation |
| `auth.py` | Mock sign-in UI, user session management (future OAuth integration) |

---

## 🔧 Configuration

### Environment Variables
Currently, no environment variables are required. Future versions will support:
- `GOOGLE_CLIENT_ID`: For Google OAuth2 sign-in
- `GOOGLE_CLIENT_SECRET`: For Google OAuth2 sign-in

### Streamlit Secrets (.streamlit/secrets.toml)
For deployed apps, store sensitive info in Streamlit secrets:
```toml
[oauth]
google_client_id = "your-client-id"
google_client_secret = "your-client-secret"
```

---

## 📖 Usage

### Basic Workflow

1. **Select Language** (sidebar)
   - Choose: English / العربية / مصرّي
   - All UI text updates immediately

2. **Select Framework** (sidebar)
   - Choose: ICDF / RCR-EOC / MICRO / COSTAR
   - Form fields update based on framework

3. **Fill Fields** (left column)
   - Input text for each field
   - Required fields marked with `*`
   - Toggle "Allow blanks" to skip validation

4. **Review Live Preview** (right column, top)
   - Automatically updates as you type
   - Shows formatted prompt structure

5. **Generate Final Prompt** (left column)
   - Click "Generate Prompt" button
   - Validates required fields (unless "Allow blanks" enabled)
   - Shows success or error message

6. **Export** (right column, bottom)
   - **Copy**: Copies to clipboard (fallback: use Download)
   - **Download**: Saves as `prompti_prompt_<framework>_<lang>.txt`
   - **Save to Drive**: Disabled (placeholder for Pro tier)

### Framework Quick Reference

| Framework | Best For | Key Fields |
|-----------|----------|-----------|
| **ICDF** | Task execution | Instruction, Context, Data, Format |
| **RCR-EOC** | Role-based agents | Role, Context, Request, Examples, Output, Constraints |
| **MICRO** | Creative messaging | Message, Intention, Context, Rhythm, Output |
| **COSTAR** | Marketing copy | Context, Offer, Style, Target, Action, Result |

---

## 🌍 Deployment

### Streamlit Community Cloud (Recommended for MVP)

1. **Push code to GitHub**
2. **Go to** [share.streamlit.io](https://share.streamlit.io)
3. **Click "New app"** and select your GitHub repo
4. **Select branch & file**: `main` / `app.py`
5. **Deploy!** (instant, automatic redeploys on push)

### Hugging Face Spaces

1. **Create new Space** on [huggingface.co](https://huggingface.co)
2. **Select "Docker"** and push your repo
3. **Follow HF deployment docs**

### Self-Hosted (Linux/macOS/Windows)

1. **Install Python 3.9+**
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Run**: `streamlit run app.py`
4. **Use reverse proxy** (nginx, Caddy) for HTTPS

---

## 🔐 Security Notes

### Input Sanitization
- All user input is sanitized via `sanitize_input()` in `prompts.py`
- Removes `<script>`, `<iframe>`, and HTML injection attempts
- Preserves legitimate newlines for formatting

### Clipboard Access
- Uses modern `navigator.clipboard` API (secure)
- Fallback to alert() for older browsers
- No data leaves the browser (client-side only)

### Authentication (Future)
- Will use OAuth2 with Google
- Credentials stored in Streamlit secrets, never in code
- Future: PKCE flow for additional security

---

## 🧪 Testing

### Smoke Tests
The app runs automatic smoke tests on startup:
- ✓ TRANSLATIONS dict loaded (all 3 languages)
- ✓ 4 frameworks loaded
- ✓ EXAMPLES presets present

Check browser console or terminal for output.

### Manual Testing Checklist

- [ ] Load app, verify UI renders
- [ ] Switch language → all strings update
- [ ] Switch framework → form fields update
- [ ] Type in field → live preview updates
- [ ] Click "Insert Example" → fields populate
- [ ] Click "Generate Prompt" → prompt displays
- [ ] Click "Copy" → clipboard works (or shows fallback)
- [ ] Click "Download" → file saves with correct name
- [ ] RTL CSS applied for Arabic/Egyptian → text right-aligned
- [ ] "Save to Drive" disabled with tooltip visible

---

## 🚧 Roadmap (Future Features)

### Phase 2 — Post-MVP
- [ ] Prompt history (store last 5 per session)
- [ ] Framework guidance tooltips/videos
- [ ] Prompt quality feedback (1-5 star rating)
- [ ] User accounts + OAuth2 with Google
- [ ] Save prompts to Google Drive (Pro)

### Phase 3 — Mobile & Advanced
- [ ] Android app (WebView or native)
- [ ] Offline mode (PWA)
- [ ] Template marketplace (user-created frameworks)
- [ ] Batch prompt generation (CSV import)
- [ ] API for programmatic access

---

## 🛠️ Development Notes

### Adding a New Language

1. **Add to `TRANSLATIONS` dict** in `i18n.py`:
   ```python
   'fr': {
       'title': 'Prompti — Générateur de Prompts Structurés',
       'sign_in': 'Se connecter avec Google',
       # ... all other keys
   }
   ```

2. **Add to language selector** in `app.py`:
   ```python
   format_func=lambda x: {'en': 'English', 'ar': 'العربية', 'eg': 'مصرّي', 'fr': 'Français'}[x]
   ```

3. **Add examples** (optional) in `prompts.py`:
   ```python
   'ICDF_fr': {
       'Instruction': 'Résumer',
       # ...
   }
   ```

### Adding a New Framework

1. **Add to `FRAMEWORKS` dict** in `prompts.py`:
   ```python
   'SOAR': {
       'fields': ['Situation', 'Objective', 'Action', 'Result'],
       'required': ['Situation', 'Objective'],
   }
   ```

2. **Add field labels/help** to `TRANSLATIONS` in `i18n.py`:
   ```python
   'field_Situation_label': 'Situation',
   'field_Situation_help': '...',
   # ... for all fields
   ```

3. **Add examples** in `prompts.py`:
   ```python
   'SOAR_en': {
       'Situation': '...',
       # ...
   }
   ```

4. **Update sidebar selectbox** in `app.py` (auto-updates from FRAMEWORKS)

### Code Annotations
Every line of code includes a hash-comment explaining its purpose. When modifying:
1. Update the comment to reflect changes
2. Maintain consistent indentation
3. Update CHANGELOG.md with date/version
4. Test changes before committing

---

## 📝 Change Log

See `CHANGELOG.md` for detailed version history, including:
- Feature additions
- Bug fixes
- Code refactoring
- Timestamp for each change
- Notes for future developers

---

## 📞 Support & Contribution

### Reporting Issues
1. Document the issue (steps to reproduce, expected vs. actual behavior)
2. Include browser/OS/Python version
3. Check existing issues first

### Contributing
1. Fork the repo
2. Create a feature branch
3. Add tests and documentation
4. Submit a pull request

### Code Style
- PEP 8 compliant
- Clear variable names
- Comprehensive comments
- Type hints (future enhancement)

---

## 📄 License

[Specify your license here — e.g., MIT, Apache 2.0, etc.]

---

## 🎉 Thank You!

Prompti was designed to make AI prompt creation faster, more consistent, and more enjoyable for non-native English speakers. Enjoy!

---

**Questions or suggestions?** Feel free to reach out or open an issue on GitHub.

Last updated: 2025-11-26
