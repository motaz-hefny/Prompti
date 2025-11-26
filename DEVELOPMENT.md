# DEVELOPMENT.md — Developer Guide for Prompti

**For future developers working on Prompti: this guide explains architecture, code conventions, and how to extend the application.**

---

## 📚 Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Code Conventions](#code-conventions)
3. [Module Breakdown](#module-breakdown)
4. [How to Extend](#how-to-extend)
5. [Testing Strategy](#testing-strategy)
6. [Common Tasks](#common-tasks)
7. [Troubleshooting](#troubleshooting)

---

## Architecture Overview

### Design Philosophy

Prompti follows these principles:

1. **Modularity**: Each module has one clear responsibility
2. **Statelessness**: Functions avoid side effects; state managed via `st.session_state`
3. **Explicitness**: Every line has a comment explaining its purpose
4. **Robustness**: Fallback logic handles missing data gracefully
5. **Accessibility**: All UI is keyboard-navigable, screen-reader friendly

### Data Flow

```
┌─────────────┐
│   User UI   │ (app.py - Streamlit components)
└──────┬──────┘
       │ onChange / onClick
       ↓
┌─────────────────────┐
│  Session State      │ (st.session_state)
│  - lang             │
│  - framework        │
│  - fields           │
│  - generated_prompt │
└──────┬──────────────┘
       │ reads/writes
       ↓
┌─────────────────────────────────────┐
│  Core Modules                       │
│  - i18n: translations & slang       │
│  - prompts: assembly & validation   │
│  - utils: helpers (RTL, clipboard)  │
│  - auth: user management (future)   │
└─────────────────────────────────────┘
       │ returns computed values
       ↓
┌─────────────────┐
│  Final Output   │ (code block, download, clipboard)
└─────────────────┘
```

### Execution Flow (Per Page Load)

1. **Streamlit runs from top to bottom** (reruns entire script on every interaction)
2. **Session state initializes** (app.py lines 30-45)
3. **Sidebar renders** (language, framework, sign-in, "Allow blanks")
4. **Main form renders** (dynamically based on selected framework)
5. **Live preview updates** (real-time, calls `assemble_prompt()` with `allow_blanks=True`)
6. **User clicks button** → triggers callback → session state updates → Streamlit reruns

---

## Code Conventions

### Comment Format

Every function and code block has comments structured as:

```python
# # Step X: Clear English description of what this code does
#
# Explanation of WHY (context, design decision, etc.)
```

### Example:

```python
# Step 1: Initialize language to English if not already set
if 'lang' not in st.session_state:
    st.session_state['lang'] = 'en'
```

### Naming Conventions

| Type | Convention | Example |
|------|-----------|---------|
| Functions | `snake_case` | `assemble_prompt()`, `get_rtl_css()` |
| Classes | `PascalCase` | `TranslationManager` (future) |
| Constants | `UPPER_CASE` | `FRAMEWORKS`, `EXAMPLES`, `TRANSLATIONS` |
| Variables | `snake_case` | `prompt_text`, `current_framework` |
| Private vars | `_leading_underscore` | `_internal_cache` |
| Session keys | `lowercase_with_underscores` | `st.session_state['generated_prompt']` |

### Translation Key Format

Translation keys follow the pattern:

```
[section]_[field_or_action]_[descriptor]

Examples:
'button_generate'          # Button label
'field_Instruction_label'  # Field label
'field_Instruction_help'   # Field help text
'copy_success'             # Success message
```

---

## Module Breakdown

### 1. **app.py** — Main Orchestrator

**Responsibility**: Render UI, handle user interactions, manage page layout

**Key sections**:
- Page configuration (`st.set_page_config()`)
- Session state initialization
- Sidebar rendering
- Two-column layout (form + preview)
- Event handlers (Generate, Insert Example, Reset)
- RTL CSS injection
- Smoke tests

**When to modify**:
- Adding UI elements
- Changing page layout
- Adding new buttons/controls
- Modifying form rendering logic

**Key dependencies**:
- `i18n.py` (for translations)
- `prompts.py` (for assembly logic)
- `utils.py` (for helpers)
- `auth.py` (for sign-in UI)

---

### 2. **i18n.py** — Internationalization

**Responsibility**: All translations, language-specific text, Egyptian slang variants

**Key sections**:
- `TRANSLATIONS` dict (3 languages × ~30+ keys each)
- `EG_SLANG_VARIANTS` dict (randomized Egyptian microcopy)
- `t(lang, key)` function with fallback logic
- `get_slang(lang, key)` function for randomization
- `init_translation_session_state()` initializer

**When to modify**:
- Adding/fixing translations
- Adding new Egyptian slang variants
- Adding a new language
- Fixing fallback logic

**Key design decisions**:
- Fallback chain: `TRANSLATIONS[lang] → TRANSLATIONS['ar'] (for eg) → TRANSLATIONS['en']`
- Slang randomization cached per page load for UX consistency
- All keys must exist in English as final fallback

---

### 3. **prompts.py** — Prompt Logic

**Responsibility**: Framework definitions, prompt assembly, examples, validation

**Key sections**:
- `FRAMEWORKS` dict (structure: fields, required fields)
- `EXAMPLES` dict (presets for each framework × language)
- `sanitize_input()` (prevents XSS)
- `assemble_prompt()` (core assembly logic)
- `get_example()` (fetches presets)

**When to modify**:
- Adding new frameworks
- Changing prompt assembly rules
- Adding framework examples
- Modifying validation logic
- Improving security/sanitization

**Key design decisions**:
- Frameworks stored as dict with metadata (makes UI generation easy)
- Assembly maintains exact field order per framework
- RCR-EOC Context label disambiguated to "Context (Work Environment):"
- Input sanitization removes `<script>`, `<iframe>`, escapes HTML

---

### 4. **utils.py** — Utility Helpers

**Responsibility**: CSS/JS helpers, filename generation, validation

**Key sections**:
- `get_rtl_css(lang)` (RTL styling)
- `get_clipboard_js(prompt_text, lang)` (copy-to-clipboard JS)
- `generate_filename(framework, lang)` (export filename)
- `validate_fields()` (field validation)

**When to modify**:
- Changing RTL styling
- Adding clipboard functionality
- Modifying export filename format
- Enhancing validation rules

**Key design decisions**:
- RTL CSS uses Streamlit class selectors (`.stButton`, `.stDownloadButton`)
- Code blocks stay LTR even in RTL mode for technical readability
- Clipboard JS uses modern `navigator.clipboard` with alert fallback
- Filename format: `prompti_prompt_<framework>_<lang>.txt`

---

### 5. **auth.py** — Authentication (Skeleton)

**Responsibility**: Sign-in UI, user session management, OAuth skeleton

**Key sections**:
- `render_mock_signin(lang)` (mock button + caption)
- `init_user_session()` (initializes session state)
- `authenticate_user_google()` (TODO: Google OAuth)
- `save_prompt_to_drive()` (TODO: Drive integration)

**When to modify**:
- Implementing Google OAuth2
- Adding user profile management
- Enabling "Save to Drive" feature
- Adding prompt history persistence

**Key design decisions**:
- All auth is currently mock (placeholder for future)
- OAuth integration should store credentials in Streamlit secrets (not code)
- User state stored in `st.session_state['user']`

---

## How to Extend

### Add a New Language

**Step 1: Add translations to `i18n.py`**

```python
TRANSLATIONS = {
    # ... existing languages ...
    'es': {  # Spanish example
        'title': 'Prompti — Generador de Prompts Estructurados',
        'sign_in': 'Iniciar sesión con Google',
        # ... copy all other keys from 'en' and translate ...
    }
}
```

**Step 2: Update sidebar in `app.py`**

```python
format_func=lambda x: {
    'en': 'English',
    'ar': 'العربية',
    'eg': 'مصرّي',
    'es': 'Español'  # Add this
}[x]
```

**Step 3 (optional): Add examples in `prompts.py`**

```python
EXAMPLES = {
    # ... existing examples ...
    'ICDF_es': {  # Spanish example for ICDF
        'Instruction': 'Resumir',
        'Context': 'Informe mensual para el director de marketing',
        # ...
    }
}
```

### Add a New Framework

**Step 1: Define framework in `prompts.py`**

```python
FRAMEWORKS = {
    # ... existing frameworks ...
    'SCAMPER': {
        'fields': ['Substitute', 'Combine', 'Adapt', 'Modify', 'Put', 'Eliminate', 'Reverse'],
        'required': ['Substitute'],
    }
}
```

**Step 2: Add translations in `i18n.py` (all 3 languages)**

```python
'en': {
    # ... existing ...
    'field_Substitute_label': 'Substitute',
    'field_Substitute_help': 'What could be substituted?',
    # ... for all fields in all languages ...
}
```

**Step 3: Add examples in `prompts.py`**

```python
EXAMPLES = {
    # ... existing ...
    'SCAMPER_en': {
        'Substitute': 'Replace paper with digital',
        # ...
    }
}
```

**Step 4: Sidebar auto-updates** (no changes needed in `app.py` — it reads from FRAMEWORKS dict)

### Implement Google OAuth2 Sign-In

**High-level steps**:

1. **Install dependencies**:
   ```bash
   pip install google-auth-oauthlib
   ```

2. **Get credentials**: Create OAuth app in Google Cloud Console, save credentials

3. **Store in Streamlit secrets** (`.streamlit/secrets.toml`):
   ```toml
   [oauth]
   client_id = "xxx.apps.googleusercontent.com"
   client_secret = "xxxxx"
   ```

4. **Implement in `auth.py`**:
   ```python
   def authenticate_user_google():
       from google_auth_oauthlib.flow import Flow
       # Initialize OAuth flow
       # Redirect to Google login
       # Handle callback
       # Store user in st.session_state['user']
   ```

5. **Update `app.py`** to call OAuth:
   ```python
   if st.button(t(lang, 'sign_in')):
       authenticate_user_google()
   ```

### Enable Clipboard Copy with JavaScript

The current implementation uses `pyperclip` (Python fallback). For better browser support:

1. **Use Streamlit components** in `app.py`:
   ```python
   from streamlit.components.v1 import html
   js_code = get_clipboard_js(prompt_text, lang)
   html(js_code, height=50)
   ```

2. **Handle postMessage callback**:
   ```python
   if st.session_state.get('clipboard_result') == 'success':
       st.success(t(lang, 'copy_success'))
   ```

---

## Testing Strategy

### Smoke Tests (Automatic)

Run on app startup (in `app.py`):
- ✓ TRANSLATIONS dict has all 3 languages
- ✓ 4 frameworks loaded
- ✓ EXAMPLES presets present

### Unit Tests (Future)

Example test for `assemble_prompt()`:

```python
from prompts import assemble_prompt

def test_assemble_prompt_icdf():
    fields = {
        'Instruction': 'Summarize',
        'Context': 'Report',
        'Data': 'Q3 figures',
        'Format': 'Bullet points'
    }
    success, result = assemble_prompt('ICDF', 'en', fields)
    assert success == True
    assert 'Instruction: Summarize' in result
    assert result.count('\n\n') == 3  # 3 section breaks for 4 fields
```

### Manual Testing Checklist

- [ ] Load app in English → check UI language
- [ ] Switch to Arabic → verify RTL styling applied
- [ ] Switch to Egyptian → verify slang variants render
- [ ] Select each framework → verify fields change
- [ ] Type in form → verify live preview updates
- [ ] Click "Insert Example" → fields populate
- [ ] Click "Generate Prompt" → prompt displays
- [ ] Click "Copy" → verify clipboard works
- [ ] Click "Download" → verify filename and content
- [ ] Click "Reset" → verify fields clear

---

## Common Tasks

### Debug Translation Issues

1. **Check if key exists**:
   ```python
   from i18n import t
   print(t('en', 'missing_key'))  # Returns 'missing_key' if not found
   ```

2. **Check fallback chain**:
   - For 'eg' language: checks 'eg' → 'ar' → 'en'
   - Returns key name if nothing found

3. **Add missing key**: Add to all 3 language dicts in TRANSLATIONS

### Add New Button

1. **Add translation key** in `i18n.py`:
   ```python
   'button_export': 'Export',
   ```

2. **Add to all 3 languages** (en, ar, eg)

3. **Render in `app.py`**:
   ```python
   if st.button(t(lang, 'button_export')):
       # Handle click
   ```

### Modify Prompt Assembly

1. **Update framework** in `prompts.py` (change fields, required, order)
2. **Update examples** in `prompts.py` (add/remove examples as needed)
3. **Update translations** in `i18n.py` (new field labels/help)
4. **Update README.md** with new framework details

### Deploy to Streamlit Cloud

1. **Push code to GitHub**
2. **Go to** https://share.streamlit.io/
3. **Click "New app"**
4. **Select repo and branch** (e.g., `main`)
5. **Select file** (`app.py`)
6. **Deploy!**

---

## Troubleshooting

### App won't start

**Problem**: `ModuleNotFoundError: No module named 'streamlit'`

**Solution**:
```bash
pip install -r requirements.txt
```

### Translation showing as "[key_name]"

**Problem**: Translation key not found

**Solution**:
1. Check spelling in TRANSLATIONS dict
2. Verify key exists in all 3 languages
3. Check fallback chain (see "Debug Translation Issues" above)

### RTL not working for Arabic

**Problem**: Text still left-to-right for Arabic/Egyptian

**Solution**:
1. Check `get_rtl_css()` is being called in `app.py`
2. Verify language code is 'ar' or 'eg' (not 'arabic')
3. Check browser cache (hard refresh)
4. Verify CSS is being injected: `st.markdown(rtl_css, unsafe_allow_html=True)`

### Clipboard copy fails

**Problem**: "Clipboard not available" error

**Solution**:
1. Check if `pyperclip` is installed: `pip list | grep pyperclip`
2. For browsers: use fallback (Download button)
3. Future: implement JavaScript clipboard API

### Session state not persisting

**Problem**: Form fields clear when clicking buttons

**Solution**:
1. Ensure fields stored in `st.session_state['fields'][framework]`
2. Check button key is unique (e.g., `key='btn_generate'`)
3. Verify framework not changing unexpectedly
4. Check session state initialization (lines 30-45 in app.py)

---

## Resources

- **Streamlit Docs**: https://docs.streamlit.io/
- **Python PEP 8**: https://pep8.org/
- **Google OAuth2**: https://developers.google.com/identity/protocols/oauth2
- **CHANGELOG.md**: Version history and detailed change log

---

## Questions?

For questions or clarifications about the code:
1. Check comments in the relevant file (every line is explained)
2. Review CHANGELOG.md for implementation details
3. Check README.md for usage guidance
4. Consult this DEVELOPMENT.md for architecture

---

**Last updated**: 2025-11-26
**Maintained by**: [Your team]
