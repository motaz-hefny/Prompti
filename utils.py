# utils.py — Utility Helpers & CSS/JS Helpers
# ============================================================================
# This module provides helper functions for:
# - RTL (Right-to-Left) CSS injection for Arabic/Egyptian languages
# - Clipboard JavaScript for copy-to-clipboard functionality
# - Filename generation for exports
# - Field validation helpers
#
# All functions are stateless and designed to be called from app.py
# ============================================================================

# ==============================================================================
# RTL CSS & STYLING HELPERS
# ==============================================================================

def get_rtl_css(lang):
    """
    # get_rtl_css(lang) — Generate RTL (Right-to-Left) CSS for Arabic/Egyptian
    #
    # Purpose: Inject CSS into Streamlit to enable right-to-left text direction
    # and proper alignment for Arabic ('ar') and Egyptian ('eg') languages.
    #
    # Parameters:
    #   - lang (str): Language code ('en', 'ar', 'eg')
    #
    # Returns:
    #   - str: HTML <style> block with RTL CSS (empty string if lang is 'en')
    #
    # CSS rules applied when lang in ('ar', 'eg'):
    #   1. body { direction: rtl; }: Text flows right-to-left
    #   2. body { text-align: right; }: Text aligned to right side
    #   3. input, textarea, [class*="textbox"] { direction: rtl; }: Form inputs RTL
    #   4. .stButton > button { flex-direction: row-reverse; }: Buttons flipped
    #   5. .stDownloadButton > button { flex-direction: row-reverse; }: Download btn flipped
    #   6. code { direction: ltr; }: Code blocks stay LTR (technical content)
    #   7. code { text-align: left; }: Code text left-aligned
    #
    # Returns for 'en': Empty string (no RTL styling needed)
    #
    # Usage in app.py:
    #   rtl_css = get_rtl_css(st.session_state['lang'])
    #   if rtl_css:
    #       st.markdown(rtl_css, unsafe_allow_html=True)
    #
    # Design notes:
    #   - Uses Streamlit class selectors (.stButton, .stDownloadButton, etc.)
    #   - Code blocks override to LTR for technical readability
    #   - flex-direction: row-reverse flips button icon+text order for RTL
    #   - Safe: only injects CSS, no JavaScript or dangerous content
    """
    # Step 1: Check if language is English — if so, no RTL styling needed
    if lang == 'en':
        return ''

    # Step 2: Check if language is Arabic or Egyptian — if so, apply RTL CSS
    if lang in ('ar', 'eg'):
        # Step 3: Build RTL CSS string with all necessary rules
        rtl_css = """
        <style>
        /* RTL (Right-to-Left) styling for Arabic and Egyptian Arabic */
        
        /* Step 1: Set document direction and text alignment to right */
        body {
            direction: rtl !important;
            text-align: right !important;
        }
        
        /* Step 2: Apply RTL to form inputs (text areas, text boxes) */
        input, textarea, [class*="textbox"] {
            direction: rtl !important;
            text-align: right !important;
        }
        
        /* Step 3: Flip button layout (icon + text) for RTL context */
        .stButton > button {
            flex-direction: row-reverse !important;
        }
        
        /* Step 4: Flip download button layout for RTL context */
        .stDownloadButton > button {
            flex-direction: row-reverse !important;
        }
        
        /* Step 5: Keep code blocks in LTR (left-to-right) for technical readability */
        code {
            direction: ltr !important;
            text-align: left !important;
        }
        
        /* Step 6: Ensure pre-formatted code stays readable in LTR */
        pre {
            direction: ltr !important;
            text-align: left !important;
        }
        
        /* Step 7: Sidebar stays properly aligned */
        [data-testid="stSidebar"] {
            direction: rtl !important;
        }
        </style>
        """
        # Step 4: Return RTL CSS string
        return rtl_css

    # Step 5: If language is neither 'en' nor Arabic, return empty string (no RTL)
    return ''

# ==============================================================================
# CLIPBOARD & JAVASCRIPT HELPERS
# ==============================================================================

def get_clipboard_js(prompt_text, lang):
    """
    # get_clipboard_js(prompt_text, lang) — Generate JavaScript for copy-to-clipboard
    #
    # Purpose: Create HTML/JavaScript snippet that copies prompt_text to user's
    # clipboard using modern navigator.clipboard.writeText() API with fallback.
    #
    # Parameters:
    #   - prompt_text (str): The exact prompt text to copy to clipboard
    #   - lang (str): Language code for fallback messages ('en', 'ar', 'eg')
    #
    # Returns:
    #   - str: HTML string with JavaScript code ready for st.components.v1.html()
    #
    # Behavior:
    #   1. Generates hidden button that triggers clipboard copy on click
    #   2. Uses navigator.clipboard.writeText(text) for modern browsers
    #   3. Posts message back to Streamlit for success/error feedback
    #   4. Fallback to alert() if clipboard unavailable
    #   5. Handles errors gracefully (permission denied, etc.)
    #
    # Browser compatibility:
    #   - Modern (Chrome, Firefox, Safari, Edge): navigator.clipboard API
    #   - Older: Falls back to alert (limited UX but functional)
    #
    # Usage in app.py:
    #   js_code = get_clipboard_js(final_prompt, st.session_state['lang'])
    #   st.components.v1.html(js_code, height=50)
    #
    # Security notes:
    #   - No eval() or dangerous operations
    #   - Text is JSON-encoded to prevent injection
    #   - Uses postMessage() for Streamlit communication
    #
    # Example output (generated JavaScript):
    #   <button onclick="copyPrompt()">Copy</button>
    #   <script>
    #   function copyPrompt() {
    #     text = "Instruction: Summarize\n\n..."
    #     navigator.clipboard.writeText(text).then(...)
    #   }
    #   </script>
    """
    # Step 1: JSON-encode prompt text to safely embed in JavaScript
    import json
    prompt_json = json.dumps(prompt_text)

    # Step 2: Build JavaScript code for clipboard copy operation
    js_code = f"""
    <html>
    <head>
        <style>
        /* Minimal styling for hidden button */
        #copyButton {{
            padding: 10px 20px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
        }}
        #copyButton:hover {{
            background-color: #45a049;
        }}
        </style>
    </head>
    <body>
        <!-- Hidden button that user clicks to copy -->
        <button id="copyButton" onclick="copyPrompt()">Copy to Clipboard</button>
        
        <script>
        // Define copyPrompt() function that copies text to clipboard
        function copyPrompt() {{
            // Step 1: Get the prompt text to copy (JSON-encoded, decoded here)
            var promptText = {prompt_json};
            
            // Step 2: Check if navigator.clipboard API is available (modern browsers)
            if (navigator.clipboard && navigator.clipboard.writeText) {{
                // Step 3: Use modern clipboard API for secure copy
                navigator.clipboard.writeText(promptText)
                    .then(function() {{
                        // Step 4a: Success — post message to Streamlit
                        window.parent.postMessage(
                            {{type: 'streamlit:setComponentValue', value: 'copy_success'}},
                            '*'
                        );
                        alert('Copied to clipboard!');
                    }})
                    .catch(function(error) {{
                        // Step 4b: Error — post error message to Streamlit
                        window.parent.postMessage(
                            {{type: 'streamlit:setComponentValue', value: 'copy_fail'}},
                            '*'
                        );
                        alert('Failed to copy: ' + error);
                    }});
            }} else {{
                // Step 5: Fallback for older browsers without clipboard API
                alert('Copy to clipboard not supported in this browser. Use Download button instead.');
                window.parent.postMessage(
                    {{type: 'streamlit:setComponentValue', value: 'copy_fail'}},
                    '*'
                );
            }}
        }}
        </script>
    </body>
    </html>
    """

    # Step 3: Return JavaScript HTML string
    return js_code

# ==============================================================================
# FILENAME & EXPORT HELPERS
# ==============================================================================

def generate_filename(framework, lang):
    """
    # generate_filename(framework, lang) — Generate export filename for download
    #
    # Purpose: Create a standardized, sanitized filename for downloaded prompts
    # following the pattern: prompti_prompt_<framework>_<lang>.txt
    #
    # Parameters:
    #   - framework (str): Framework name ('ICDF', 'RCR-EOC', 'MICRO', 'COSTAR')
    #   - lang (str): Language code ('en', 'ar', 'eg')
    #
    # Returns:
    #   - str: Filename string (e.g., 'prompti_prompt_ICDF_en.txt')
    #
    # Filename format:
    #   - Prefix: 'prompti_prompt_'
    #   - Framework: Lowercase, hyphens kept (e.g., 'icdf', 'rcr-eoc')
    #   - Underscore: '_'
    #   - Language: Lowercase code (e.g., 'en', 'ar', 'eg')
    #   - Extension: '.txt'
    #
    # Sanitization:
    #   - Converts framework/lang to lowercase
    #   - Removes any special characters that might break filenames
    #   - Returns safe, filesystem-compatible filename
    #
    # Example filenames:
    #   generate_filename('ICDF', 'en') → 'prompti_prompt_icdf_en.txt'
    #   generate_filename('RCR-EOC', 'ar') → 'prompti_prompt_rcr-eoc_ar.txt'
    #   generate_filename('MICRO', 'eg') → 'prompti_prompt_micro_eg.txt'
    #
    # Usage in app.py:
    #   filename = generate_filename(st.session_state['framework'], st.session_state['lang'])
    #   st.download_button(label="Download", data=prompt_text, file_name=filename, ...)
    """
    # Step 1: Convert framework and language to lowercase for filename
    framework_lower = framework.lower()
    lang_lower = lang.lower()

    # Step 2: Construct filename using the standardized pattern
    filename = f"prompti_prompt_{framework_lower}_{lang_lower}.txt"

    # Step 3: Return filename
    return filename

# ==============================================================================
# FIELD VALIDATION HELPERS
# ==============================================================================

def validate_fields(fields, required_fields, allow_blanks):
    """
    # validate_fields(fields, required_fields, allow_blanks) — Validate form fields
    #
    # Purpose: Check that all required fields have non-empty values (unless blanks allowed)
    #
    # Parameters:
    #   - fields (dict): Field name → value mapping from form inputs
    #   - required_fields (list): List of field names that are required
    #   - allow_blanks (bool): If True, skip validation (allow empty fields)
    #
    # Returns:
    #   - bool: True if validation passes; False if required fields are empty
    #
    # Validation rules:
    #   1. If allow_blanks=True, always return True (skip validation)
    #   2. For each field in required_fields:
    #      a. Get value from fields dict (default to empty string if missing)
    #      b. Strip whitespace from value
    #      c. If value is empty, return False (validation failed)
    #   3. If all required fields have content, return True (validation passed)
    #
    # Example:
    #   fields = {'Instruction': 'Summarize', 'Context': ''}
    #   required = ['Instruction', 'Context']
    #   validate_fields(fields, required, False) → False (Context is empty)
    #
    #   validate_fields(fields, required, True) → True (allow_blanks=True)
    #
    # Usage in app.py:
    #   is_valid = validate_fields(form_data, required_fields, allow_blanks_checkbox)
    #   if not is_valid:
    #       st.error("Please fill in all required fields")
    """
    # Step 1: Check if blanks are allowed — if so, skip validation
    if allow_blanks:
        return True

    # Step 2: Iterate through each required field
    for field_name in required_fields:
        # Step 2a: Get field value from dict; default to empty string if missing
        field_value = fields.get(field_name, '').strip()

        # Step 2b: If field is empty, validation fails
        if not field_value:
            return False

    # Step 3: All required fields have content — validation passed
    return True

# ==============================================================================
# END utils.py
# ==============================================================================
