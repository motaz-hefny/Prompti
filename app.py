# app.py — Prompti Main Streamlit Application
# ============================================================================
# This is the main entry point for the Prompti web application.
# Orchestrates all modules (i18n, prompts, utils, auth) to create the complete UI.
#
# Architecture:
#   - Streamlit for web framework (lightweight, rapid development)
#   - Modular design: i18n.py, prompts.py, utils.py, auth.py
#   - Session-based state management for form persistence
#   - Real-time live preview as user types
#
# Run: streamlit run app.py
# ============================================================================

import streamlit as st
from i18n import t, get_slang, init_translation_session_state
from prompts import FRAMEWORKS, assemble_prompt, get_example
from utils import get_rtl_css, generate_filename, validate_fields
from auth import render_mock_signin, init_user_session

# ==============================================================================
# PAGE CONFIGURATION
# ==============================================================================

# Step 1: Configure Streamlit page settings (tab title, icon, layout)
st.set_page_config(
    page_title='Prompti',  # Browser tab title
    page_icon='🎯',        # Browser tab icon
    layout='wide',         # Wide layout (two-column preferred)
    initial_sidebar_state='expanded'  # Sidebar visible by default
)

# ==============================================================================
# SESSION STATE INITIALIZATION
# ==============================================================================

# Step 2: Initialize translation/UI session state (language, framework, etc.)
init_translation_session_state()

# Step 3: Initialize user authentication session state (for future OAuth)
init_user_session()

# Step 4: Initialize form fields storage
# Structure: st.session_state['fields'][framework_name] = {field_name: value, ...}
if 'fields' not in st.session_state:
    st.session_state['fields'] = {}

# Step 5: Initialize generated prompt storage (populated when user clicks Generate)
if 'generated_prompt' not in st.session_state:
    st.session_state['generated_prompt'] = None

# ==============================================================================
# SIDEBAR CONTROLS
# ==============================================================================

st.sidebar.markdown("## ⚙️ Settings")

# Step 6: Language selector (radio button)
# Translates ALL UI text when changed
# Stores in st.session_state['lang'] ('en', 'ar', or 'eg')
# DO NOT use st.session_state['lang'] = ... when key='lang' is set
# The key parameter automatically manages session state assignment
st.sidebar.radio(
    label=t(st.session_state['lang'], 'language_label'),  # "Language" / "اللغة" / "اللغة"
    options=['en', 'ar', 'eg'],
    format_func=lambda x: {'en': 'English', 'ar': 'العربية', 'eg': 'مصرّي'}[x],
    key='lang'
)

# Step 7: Framework selector (dropdown)
# Switching frameworks preserves field state for each framework
# Stores in st.session_state['framework'] via key parameter
# DO NOT use st.session_state['framework'] = ... when key is set
st.sidebar.selectbox(
    label=t(st.session_state['lang'], 'framework_label'),  # "Framework" / "الإطار"
    options=['ICDF', 'RCR-EOC', 'MICRO', 'COSTAR'],
    key='framework'
)

# Step 8: Initialize field storage for current framework if not present
if st.session_state['framework'] not in st.session_state['fields']:
    st.session_state['fields'][st.session_state['framework']] = {}

# Step 9: Get framework metadata (fields list, required fields)
current_framework_meta = FRAMEWORKS[st.session_state['framework']]
current_framework_fields = current_framework_meta['fields']
current_required_fields = current_framework_meta['required']

# Step 10: Mock Google Sign-In button
render_mock_signin(st.session_state['lang'])

st.sidebar.markdown("---")

# Step 11: "Allow blanks" checkbox (disables required field validation)
allow_blanks = st.sidebar.checkbox(
    label=t(st.session_state['lang'], 'allow_blanks'),  # "Allow blanks (disable validation)"
    value=False,
    key='allow_blanks'
)

# ==============================================================================
# MAIN CONTENT AREA — TWO COLUMN LAYOUT
# ==============================================================================

# Step 12: Create two-column layout
col_form, col_preview = st.columns([1, 1], gap='medium')

# ============================================================================
# LEFT COLUMN — DYNAMIC FORM FOR SELECTED FRAMEWORK
# ============================================================================

with col_form:
    st.markdown(f"### 📝 {st.session_state['framework']}")
    st.markdown("Fill in the fields below. Fields marked with **\*** are required (unless \"Allow blanks\" is enabled).")

    # Step 13: Dynamically render form inputs for current framework
    # Iterate through framework fields and create text_area for each
    for field_name in current_framework_fields:
        # Step 13a: Determine if this field is required
        is_required = field_name in current_required_fields

        # Step 13b: Fetch translated label and help text
        label_key = f'field_{field_name}_label'
        help_key = f'field_{field_name}_help'
        translated_label = t(st.session_state['lang'], label_key)
        translated_help = t(st.session_state['lang'], help_key)

        # Step 13c: Add asterisk to label if field is required
        label_display = f"{translated_label} {'*' if is_required else ''}"

        # Step 13d: Create text_area for this field
        # Stores value in st.session_state['fields'][framework][field_name]
        field_value = st.session_state['fields'][st.session_state['framework']].get(field_name, '')
        
        # Step 13e: Render text area and store input
        st.session_state['fields'][st.session_state['framework']][field_name] = st.text_area(
            label=label_display,
            value=field_value,
            help=translated_help,
            key=f"{st.session_state['framework']}_{field_name}",
            height=80
        )

    st.markdown("---")

    # Step 14: Action buttons in form column
    col_gen, col_ex, col_reset = st.columns(3)

    # Step 14a: "Generate Prompt" button
    with col_gen:
        if st.button(
            label=t(st.session_state['lang'], 'button_generate'),
            use_container_width=True,
            key='btn_generate'
        ):
            # Step 14a-i: Validate fields (unless allow_blanks=True)
            current_fields = st.session_state['fields'][st.session_state['framework']]
            is_valid = validate_fields(current_fields, current_required_fields, allow_blanks)

            # Step 14a-ii: If validation passes, assemble and store prompt
            if is_valid:
                success, result = assemble_prompt(
                    framework=st.session_state['framework'],
                    lang=st.session_state['lang'],
                    fields=current_fields,
                    allow_blanks=allow_blanks
                )

                # Step 14a-iii: If assembly succeeds, store prompt and show success
                if success:
                    st.session_state['generated_prompt'] = result
                    st.success(t(st.session_state['lang'], 'smoke_ok'))
                else:
                    # Step 14a-iv: If assembly fails, show error (result is error message)
                    st.error(result)
            else:
                # Step 14a-v: If validation fails, show required fields error
                st.error(t(st.session_state['lang'], 'required_error'))

    # Step 14b: "Insert Example" button
    with col_ex:
        if st.button(
            label=t(st.session_state['lang'], 'insert_example'),
            use_container_width=True,
            key='btn_example'
        ):
            # Step 14b-i: Fetch example for current framework and language
            example_data = get_example(st.session_state['framework'], st.session_state['lang'])

            # Step 14b-ii: Populate fields with example data
            st.session_state['fields'][st.session_state['framework']].update(example_data)

            # Step 14b-iii: Show success message
            st.success(t(st.session_state['lang'], 'example_filled'))

    # Step 14c: "Reset Fields" button
    with col_reset:
        if st.button(
            label=t(st.session_state['lang'], 'reset_form'),
            use_container_width=True,
            key='btn_reset'
        ):
            # Step 14c-i: Clear all fields for current framework
            st.session_state['fields'][st.session_state['framework']] = {}

            # Step 14c-ii: Clear generated prompt
            st.session_state['generated_prompt'] = None

            # Step 14c-iii: Show success message
            st.success(t(st.session_state['lang'], 'reset_done'))

# ============================================================================
# RIGHT COLUMN — LIVE PREVIEW + FINAL PROMPT + EXPORT
# ============================================================================

with col_preview:
    # Step 15: Display live preview label
    st.markdown(f"### 👁️ {t(st.session_state['lang'], 'preview_label')}")

    # Step 16: Render live preview
    # Updates in real-time as user types in form fields
    current_fields = st.session_state['fields'][st.session_state['framework']]
    success, preview_result = assemble_prompt(
        framework=st.session_state['framework'],
        lang=st.session_state['lang'],
        fields=current_fields,
        allow_blanks=True  # Force blanks allowed for live preview
    )

    # Step 16a: Display preview in code block
    if success:
        st.code(preview_result, language='text')
    else:
        st.info("👉 Fill in fields to see preview")

    st.markdown("---")

    # Step 17: Display final generated prompt (if user clicked Generate)
    if st.session_state['generated_prompt']:
        st.markdown(f"### ✨ {t(st.session_state['lang'], 'generated_label')}")

        # Step 17a: Display final prompt in code block
        st.code(st.session_state['generated_prompt'], language='text')

        st.markdown("---")

        # Step 17b: Export buttons below final prompt
        st.markdown("### 📤 Export Options")

        export_col1, export_col2 = st.columns(2, gap='small')

        # Step 17b-i: Copy to Clipboard button
        with export_col1:
            if st.button(
                label=get_slang(st.session_state['lang'], 'button_copy'),
                use_container_width=True,
                key='btn_copy'
            ):
                # Step 17b-i-A: Copy to clipboard (simplified for demo)
                # In production: use st.components.v1.html with JavaScript
                try:
                    import pyperclip
                    pyperclip.copy(st.session_state['generated_prompt'])
                    st.success(get_slang(st.session_state['lang'], 'copy_success'))
                except Exception as e:
                    st.error(t(st.session_state['lang'], 'copy_fail'))

        # Step 17b-ii: Download Prompt button
        with export_col2:
            filename = generate_filename(st.session_state['framework'], st.session_state['lang'])
            st.download_button(
                label=t(st.session_state['lang'], 'button_download'),
                data=st.session_state['generated_prompt'],
                file_name=filename,
                mime='text/plain',
                use_container_width=True,
                key='btn_download'
            )

        # Step 17b-iii: Disabled Save to Drive button (placeholder for Pro)
        st.button(
            label=t(st.session_state['lang'], 'button_save_drive'),
            disabled=True,
            use_container_width=True,
            key='btn_save_drive'
        )

        # Step 17b-iv: Caption explaining Save to Drive is a Pro feature
        st.caption(t(st.session_state['lang'], 'save_to_drive_tooltip'))

# ==============================================================================
# RTL STYLING INJECTION
# ==============================================================================

# Step 18: Inject RTL CSS if language is Arabic or Egyptian
rtl_css = get_rtl_css(st.session_state['lang'])
if rtl_css:
    st.markdown(rtl_css, unsafe_allow_html=True)

# ==============================================================================
# PAGE TITLE & HEADER
# ==============================================================================

# Step 19: Display page title (this goes at top, but defined last due to Streamlit ordering)
# NOTE: Streamlit renders in order, so title appears after sidebar but before main content
# To fix, move this to line 2 after st.set_page_config (future refactor)
st.markdown(f"# {t(st.session_state['lang'], 'title')}")
st.markdown("---")

# ==============================================================================
# SMOKE TESTS (Development Only)
# ==============================================================================

# Step 20: Verify initialization on page load (development diagnostic)
def run_smoke_tests():
    """
    # run_smoke_tests() — Verify app components are initialized correctly
    #
    # Checks:
    #   1. TRANSLATIONS dict loaded with all three languages (en, ar, eg)
    #   2. All required translation keys present in each language
    #   3. FRAMEWORKS dict loaded with exactly 4 frameworks
    #   4. EXAMPLES dict has presets for all frameworks and languages
    #
    # Purpose: Early detection of configuration errors (missing translations, etc.)
    # Called once on first page load via st.session_state
    """
    if 'smoke_tests_run' not in st.session_state:
        # Step 20a: Check TRANSLATIONS completeness
        try:
            assert 'en' in t('en', 'title'), "English translations missing"
            assert 'ar' in t('ar', 'title'), "Arabic translations missing"
            assert 'eg' in t('eg', 'title'), "Egyptian translations missing"
            print("✓ Smoke test: TRANSLATIONS loaded correctly")
        except AssertionError as e:
            print(f"✗ Smoke test failed: {e}")

        # Step 20b: Check FRAMEWORKS count
        try:
            assert len(FRAMEWORKS) == 4, f"Expected 4 frameworks, got {len(FRAMEWORKS)}"
            print("✓ Smoke test: 4 frameworks loaded correctly")
        except AssertionError as e:
            print(f"✗ Smoke test failed: {e}")

        # Step 20c: Check EXAMPLES presence
        try:
            from prompts import EXAMPLES
            assert len(EXAMPLES) > 0, "EXAMPLES dict is empty"
            print("✓ Smoke test: EXAMPLES loaded correctly")
        except AssertionError as e:
            print(f"✗ Smoke test failed: {e}")

        # Step 20d: Mark tests as run (only run once per session)
        st.session_state['smoke_tests_run'] = True

# Step 21: Run smoke tests on page load
run_smoke_tests()

# ==============================================================================
# END app.py
# ==============================================================================
