# i18n.py — Internationalization & Translation Management
# ============================================================================
# This module centralizes all UI translations for Prompti across three locales:
# - 'en': English
# - 'ar': Modern Standard Arabic (MSA, formal)
# - 'eg': Egyptian Arabic colloquial (informal, playful slang)
#
# Features:
# - Comprehensive TRANSLATIONS dictionary for all UI strings
# - EG_SLANG_VARIANTS for randomized Egyptian microcopy
# - t(lang, key) helper with intelligent fallback logic
# - get_slang(lang, key) for randomized dialect selection with session persistence
#
# Future extensions: Add locales by creating new entries in TRANSLATIONS
# ============================================================================

import random
import streamlit as st

# ==============================================================================
# TRANSLATIONS DICTIONARY
# ==============================================================================
# Main translation dictionary organized by language code.
# Each entry is a dict of key-value pairs for UI strings.
# Structure: TRANSLATIONS[lang_code][key] = translated_string

TRANSLATIONS = {
    # ========================================================================
    # English (en) — Formal, professional
    # ========================================================================
    'en': {
        # ==== Page & General ====
        'title': 'Prompti — Structured Prompt Generator',
        'sign_in': 'Sign In with Google',

        # ==== Sidebar Labels ====
        'language_label': 'Language',
        'framework_label': 'Framework',

        # ==== Framework Names (appear in selectbox) ====
        'framework_icdf': 'ICDF',
        'framework_rcr': 'RCR-EOC',
        'framework_micro': 'MICRO',
        'framework_costar': 'COSTAR',

        # ==== Sidebar Options ====
        'allow_blanks': 'Allow blanks (disable required validation)',

        # ==== ICDF Framework Fields ====
        'field_Instruction_label': 'Instruction',
        'field_Instruction_help': "The action. Define the primary task (e.g., 'Summarize', 'Analyze', 'Draft').",
        'field_Context_label': 'Context',
        'field_Context_help': "The Situation/Purpose. Explain why the task is being done and who the audience is.",
        'field_Data_label': 'Data',
        'field_Data_help': "The Input. Provide the raw data or detailed information the AI needs to process.",
        'field_Format_label': 'Format',
        'field_Format_help': "The Output Style. Specify the desired structure and tone.",

        # ==== RCR-EOC Framework Fields ====
        'field_Role_label': 'Role',
        'field_Role_help': "The Persona. Assign the AI a clear professional identity.",
        'field_Request_label': 'Request',
        'field_Request_help': "The Specific Job. State the precise deliverable.",
        'field_Examples_label': 'Examples',
        'field_Examples_help': "Few-shot example input and desired output to set expectations.",
        'field_Output_label': 'Output',
        'field_Output_help': "The Structure. Define the exact structure of the response.",
        'field_Constraints_label': 'Constraints',
        'field_Constraints_help': "The Limitations. Set boundaries the AI must follow.",

        # ==== MICRO Framework Fields ====
        'field_Message_label': 'Message',
        'field_Message_help': "The Core Idea. What is the single, central theme or takeaway you want to convey?",
        'field_Intention_label': 'Intention',
        'field_Intention_help': "The Goal. What action or feeling should the audience have after consuming the content?",
        'field_Rhythm_label': 'Rhythm',
        'field_Rhythm_help': "Tone and Pace. Define the style, mood, and speed.",

        # ==== COSTAR Framework Fields ====
        'field_Offer_label': 'Offer',
        'field_Offer_help': "The Value Proposition. The deal, discount, or benefit.",
        'field_Style_label': 'Style',
        'field_Style_help': "The Voice. The brand personality.",
        'field_Target_label': 'Target',
        'field_Target_help': "The Audience Profile. Define the ideal customer.",
        'field_Action_label': 'Action',
        'field_Action_help': "Call to Action (CTA). What must the user click or do?",
        'field_Result_label': 'Result',
        'field_Result_help': "The Business Goal. What outcome do we want from this marketing piece?",

        # ==== Buttons ====
        'button_generate': 'Generate Prompt',
        'button_preview': 'Preview',
        'button_copy': 'Copy to Clipboard',
        'button_download': 'Download Prompt',
        'button_save_drive': 'Save to Drive (Placeholder)',
        'insert_example': 'Insert Example',
        'reset_form': 'Reset Fields',

        # ==== Tooltips & Messages ====
        'save_to_drive_tooltip': 'Feature requires Pro subscription.',
        'mock_signin_info': 'This is a mock sign-in UI.',
        'copy_success': 'Prompt copied to clipboard.',
        'copy_fail': 'Clipboard not available. Use Download button.',
        'preview_label': 'Live preview (updates as you type)',
        'generated_label': 'Final generated prompt',
        'example_filled': 'Example fields inserted.',
        'reset_done': 'Fields cleared.',
        'required_error': 'Please fill required fields or enable "Allow blanks".',
        'smoke_ok': 'Smoke checks passed.',
    },

    # ========================================================================
    # Modern Standard Arabic (ar) — Formal, professional
    # ========================================================================
    'ar': {
        # ==== Page & General ====
        'title': 'برومبتي — منشئ عبارات مهيكلة',
        'sign_in': 'تسجيل الدخول عبر جوجل',

        # ==== Sidebar Labels ====
        'language_label': 'اللغة',
        'framework_label': 'الإطار',

        # ==== Framework Names ====
        'framework_icdf': 'ICDF',
        'framework_rcr': 'RCR-EOC',
        'framework_micro': 'MICRO',
        'framework_costar': 'COSTAR',

        # ==== Sidebar Options ====
        'allow_blanks': 'السماح بالفراغات (تعطيل تحقق الحقول المطلوبة)',

        # ==== ICDF Framework Fields ====
        'field_Instruction_label': 'التعليمات',
        'field_Instruction_help': 'الإجراء. عرّف المهمة الأساسية (مثل: لخص، حلل، اكتب).',
        'field_Context_label': 'السياق',
        'field_Context_help': 'الوضع/الهدف. اشرح سبب تنفيذ المهمة ومن هو الجمهور.',
        'field_Data_label': 'البيانات',
        'field_Data_help': 'المدخلات. قدّم البيانات أو المعلومات التي يحتاجها الذكاء الاصطناعي لمعالجتها.',
        'field_Format_label': 'التنسيق',
        'field_Format_help': 'نمط الإخراج. حدد البنية والنبرة المطلوبة.',

        # ==== RCR-EOC Framework Fields ====
        'field_Role_label': 'الدور',
        'field_Role_help': 'الشخصية. عيّن هوية مهنية للذكاء الاصطناعي.',
        'field_Request_label': 'الطلب',
        'field_Request_help': 'المهمة المحددة. ضع المخرجات المطلوبة بدقة.',
        'field_Examples_label': 'أمثلة',
        'field_Examples_help': 'مثال مدخل ومثال المخرجات المرغوبة لضبط التوقّعات.',
        'field_Output_label': 'الإخراج',
        'field_Output_help': 'البنية. حدّد البنية الدقيقة للاستجابة.',
        'field_Constraints_label': 'القيود',
        'field_Constraints_help': 'الحدود. ضع القواعد التي يجب أن يتبعها الذكاء الاصطناعي.',

        # ==== MICRO Framework Fields ====
        'field_Message_label': 'الرسالة',
        'field_Message_help': 'الفكرة الأساسية. الفكرة أو الاستنتاج الذي تريد نقله.',
        'field_Intention_label': 'النية',
        'field_Intention_help': 'الهدف. ما الإجراء أو الشعور المطلوب لدى الجمهور؟',
        'field_Rhythm_label': 'الإيقاع',
        'field_Rhythm_help': 'النغمة والسرعة. حدد الأسلوب والمزاج والوتيرة.',

        # ==== COSTAR Framework Fields ====
        'field_Offer_label': 'العرض',
        'field_Offer_help': 'القيمة المقدمة. الخصم أو الفائدة.',
        'field_Style_label': 'النغمة',
        'field_Style_help': 'صوت العلامة التجارية.',
        'field_Target_label': 'الالهدف',
        'field_Target_help': 'ملف الجمهور المستهدف.',
        'field_Action_label': 'الإجراء',
        'field_Action_help': 'نداء لاتخاذ إجراء. ما الذي يجب أن يفعله المستخدم؟',
        'field_Result_label': 'النتيجة',
        'field_Result_help': 'هدف العمل. النتيجة المرغوبة.',

        # ==== Buttons ====
        'button_generate': 'إنشاء العبارة',
        'button_preview': 'معاينة',
        'button_copy': 'نسخ إلى الحافظة',
        'button_download': 'تنزيل العبارة',
        'button_save_drive': 'حفظ إلى Drive (نموذجي)',
        'insert_example': 'إدراج مثال',
        'reset_form': 'إعادة تعيين الحقول',

        # ==== Tooltips & Messages ====
        'save_to_drive_tooltip': 'الميزة تتطلب اشتراك Pro.',
        'mock_signin_info': 'هذه واجهة تسجيل دخول تجريبية.',
        'copy_success': 'تم نسخ العبارة إلى الحافظة.',
        'copy_fail': 'الميزة غير متاحة. استخدم زر التنزيل.',
        'preview_label': 'معاينة مباشرة (تتحدّث أثناء الكتابة)',
        'generated_label': 'العبارة النهائية المولّدة',
        'example_filled': 'تم إدخال المثال في الحقول.',
        'reset_done': 'تم تنظيف الحقول.',
        'required_error': 'يرجى تعبئة الحقول المطلوبة أو تفعيل "السماح بالفراغات".',
        'smoke_ok': 'اختبارات التدخين ناجحة.',
    },

    # ========================================================================
    # Egyptian Arabic (eg) — Colloquial, playful, informal
    # ========================================================================
    'eg': {
        # ==== Page & General ====
        'title': 'برومبتي — مولّد برومبت',
        'sign_in': 'دخول بجوجل',

        # ==== Sidebar Labels ====
        'language_label': 'اللغة',
        'framework_label': 'الإطار',

        # ==== Framework Names ====
        'framework_icdf': 'ICDF',
        'framework_rcr': 'RCR-EOC',
        'framework_micro': 'MICRO',
        'framework_costar': 'COSTAR',

        # ==== Sidebar Options ====
        'allow_blanks': 'خلي الحقول فاضية لو تحب',

        # ==== ICDF Framework Fields ====
        'field_Instruction_label': 'التعليمات',
        'field_Instruction_help': 'اعمل إيه بالظبط. اكتب المهمة الأساسية (مثال: لخّص، حلّل، اكتب).',
        'field_Context_label': 'السياق',
        'field_Context_help': 'ليه بنعمل ده ومين اللي هيقراه؟',
        'field_Data_label': 'البيانات',
        'field_Data_help': 'المدخلات. حط البيانات أو النص اللي عايز النظام يشتغل عليه.',
        'field_Format_label': 'التنسيق',
        'field_Format_help': 'شكل الخرج. نقاط ولا فقرة؟ نغمة رسمية ولا خفيفة؟',

        # ==== RCR-EOC Framework Fields ====
        'field_Role_label': 'الدور',
        'field_Role_help': 'هيتصرف كأنه مين؟ (مثال: مدير مشروع كبير).',
        'field_Request_label': 'الطلب',
        'field_Request_help': 'المطلوب بالظبط. اكتب المهمة بوضوح.',
        'field_Examples_label': 'أمثلة',
        'field_Examples_help': 'هات مثال للمدخل والمُخرَج المرغوب علشان النظام يفهم.',
        'field_Output_label': 'الإخراج',
        'field_Output_help': 'شكل الرد اللي عايزه.',
        'field_Constraints_label': 'القيود',
        'field_Constraints_help': 'حط حدود أو حاجات ممنوعة.',

        # ==== MICRO Framework Fields ====
        'field_Message_label': 'الرسالة',
        'field_Message_help': 'الفكرة اللي عايز توصلها.',
        'field_Intention_label': 'النية',
        'field_Intention_help': 'عايز الناس تعمل إيه أو تحس بإيه بعد ما يقروها؟',
        'field_Rhythm_label': 'الإيقاع',
        'field_Rhythm_help': 'نبرة وسرعة الكلام. عايزها حماسية ولا هادية؟',

        # ==== COSTAR Framework Fields ====
        'field_Offer_label': 'العرض',
        'field_Offer_help': 'العرض أو الخصم أو الميزة اللي عندك.',
        'field_Style_label': 'الطابع',
        'field_Style_help': 'شخصية الماركة: بسيطة، أنيقة، ولا مرحة؟',
        'field_Target_label': 'الزباين',
        'field_Target_help': 'مين الجمهور المستهدف؟',
        'field_Action_label': 'الإجراء',
        'field_Action_help': 'عايزهم يعملوا إيه؟ اضغطوا، اشتركوا، ولا اتصلوا؟',
        'field_Result_label': 'النتيجة',
        'field_Result_help': 'النتيجة اللي بتدور عليها.',

        # ==== Buttons ====
        'button_generate': 'اطلع البرومبت',
        'button_preview': 'شوف المعاينة',
        'button_copy': 'انسخها',
        'button_download': 'نزّلها',
        'button_save_drive': 'احفظ على Drive (نموذجي)',
        'insert_example': 'حط مثال جاهز',
        'reset_form': 'افرّغ الحقول',

        # ==== Tooltips & Messages ====
        'save_to_drive_tooltip': 'الخاصية للمشتركين Pro، انت مش منّهم لسه :)',
        'mock_signin_info': 'دي تجربة تسجيل دخول، مش دخول حقيقي.',
        'copy_success': 'اتنسخت! جاهز تلزقها.',  # Will be overridden by EG_SLANG_VARIANTS
        'copy_fail': 'مفيش صلاحية للحافظة. جرّب تنزيل الملف.',
        'preview_label': 'المعاينة الحيّة (بتتحدّث وانت بتكتب)',
        'generated_label': 'البرومبت النهائي',
        'example_filled': 'اتعبّيت الحقول بالمثال.',
        'reset_done': 'اتفرّغت الحقول.',
        'required_error': 'كمّل الحقول المطلوبة ولا فعل "خلي الحقول فاضية".',
        'smoke_ok': 'الشيكات نجحت.',
    }
}

# ==============================================================================
# EG_SLANG_VARIANTS DICTIONARY
# ==============================================================================
# Randomized variants for Egyptian colloquial microcopy to add personality & delight.
# Structure: EG_SLANG_VARIANTS[key] = [variant1, variant2, variant3, ...]
# 
# How it works:
# - When rendering a UI element with key in this dict, pick random.choice(variants)
# - Persist the chosen variant in st.session_state per page load for UX consistency
# - Users see consistent slang within a session, but variety on page refresh

EG_SLANG_VARIANTS = {
    # ========================================================================
    # Copy Success Message — Randomized on copy action or page load
    # ========================================================================
    'copy_success': [
        'اتنسخت! جاهز تلزقها.',
        'اتنسخت يا معلم، دوس علطول.',
        'تمام — اتنسخت. خشّ وِلصّق.',
        'يقلبت الحكاية: اتنسخت خلاص.',
    ],

    # ========================================================================
    # Copy Button Label — Randomized per session
    # ========================================================================
    'button_copy': [
        'انسخها',
        'انسخها ياباشا',
        'انسخها دلوقتي',
        'هاتها انسخ',
    ],

    # ========================================================================
    # Insert Example Button Label — Randomized per session
    # ========================================================================
    'insert_example': [
        'حط مثال جاهز',
        'حطلي مثال كده',
        'جيّب مثال واملى الحقول',
        'ارمِلي مثال',
    ],

    # ========================================================================
    # Mock Sign-In Info — Randomized per session
    # ========================================================================
    'mock_signin_info': [
        'دي تجربة تسجيل دخول، مش دخول حقيقي.',
        'دي فِكّرية بس علشان نجرب، مش تسجيل حقيقي.',
        'أخدنا سيرة جوجل بس للعرض، مش تسجيل فعلي.',
    ],
}

# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def t(lang, key):
    """
    # t(lang, key) — Translate UI string with intelligent fallback
    #
    # Purpose: Fetch translated string for given language & key with graceful degradation
    # 
    # Parameters:
    #   - lang (str): Language code ('en', 'ar', 'eg')
    #   - key (str): Translation key (e.g., 'title', 'button_copy')
    #
    # Returns:
    #   - str: Translated string, or key name if not found (as fallback)
    #
    # Fallback logic:
    #   1. Try: TRANSLATIONS[lang][key]
    #   2. If lang == 'eg' and not found, try: TRANSLATIONS['ar'][key] (MSA fallback)
    #   3. If still not found, try: TRANSLATIONS['en'][key] (English fallback)
    #   4. If still not found, return the key itself (graceful degradation)
    #
    # Example:
    #   t('en', 'title') → 'Prompti — Structured Prompt Generator'
    #   t('eg', 'title') → 'برومبتي — مولّد برومبت'
    #   t('eg', 'nonexistent_key') → 'nonexistent_key' (fallback)
    """
    # Step 1: Try primary language lookup
    if lang in TRANSLATIONS and key in TRANSLATIONS[lang]:
        return TRANSLATIONS[lang][key]

    # Step 2: For Egyptian, fallback to MSA (Modern Standard Arabic)
    if lang == 'eg' and key in TRANSLATIONS['ar']:
        return TRANSLATIONS['ar'][key]

    # Step 3: Fallback to English as final resort
    if key in TRANSLATIONS['en']:
        return TRANSLATIONS['en'][key]

    # Step 4: Return key itself if nothing found (graceful degradation)
    return key


def get_slang(lang, key):
    """
    # get_slang(lang, key) — Fetch randomized Egyptian slang variant
    #
    # Purpose: Return a randomized variant of Egyptian colloquial microcopy
    # for buttons, messages, and UI labels to add personality & delight.
    #
    # Parameters:
    #   - lang (str): Language code ('en', 'ar', 'eg')
    #   - key (str): Slang variant key (e.g., 'copy_success', 'button_copy')
    #
    # Returns:
    #   - str: Translated string (Egyptian variant if available, else fallback to t())
    #
    # Behavior:
    #   - If lang == 'eg' and key exists in EG_SLANG_VARIANTS:
    #     * Pick one variant randomly: random.choice(EG_SLANG_VARIANTS[key])
    #     * Persist variant in st.session_state to avoid UI jitter within session
    #     * Returns chosen variant
    #   - Otherwise: fallback to regular t(lang, key) translation
    #
    # Session Persistence:
    #   - First time a key is rendered: random.choice() selects variant
    #   - Variant stored in st.session_state['slang_cache'][key]
    #   - Subsequent renders use cached variant (consistent UX within session)
    #   - New page load = new random pick (variety across sessions)
    #
    # Example:
    #   get_slang('eg', 'copy_success') → 'اتنسخت! جاهز تلزقها.' (random variant)
    #   get_slang('en', 'copy_success') → 'Prompt copied to clipboard.' (no slang for English)
    """
    # Step 1: Initialize slang cache in session state if not present
    if 'slang_cache' not in st.session_state:
        st.session_state['slang_cache'] = {}

    # Step 2: Check if this is an Egyptian request and key has slang variants
    if lang == 'eg' and key in EG_SLANG_VARIANTS:
        # Step 3: Check if we've already cached this variant in the session
        if key not in st.session_state['slang_cache']:
            # Step 4a: First time seeing this key — pick random variant and cache it
            chosen_variant = random.choice(EG_SLANG_VARIANTS[key])
            st.session_state['slang_cache'][key] = chosen_variant
        # Step 4b: Return cached variant (ensures consistency within session)
        return st.session_state['slang_cache'][key]

    # Step 5: Non-Egyptian or key doesn't have slang variants — use standard translation
    return t(lang, key)


def init_translation_session_state():
    """
    # init_translation_session_state() — Initialize session state for translations
    #
    # Purpose: Ensure all translation-related session state is properly initialized
    # on app start or reset. This prevents KeyError when accessing lang, framework, etc.
    #
    # Returns:
    #   - None (modifies st.session_state in place)
    #
    # Initializations:
    #   - st.session_state['lang']: Current UI language code ('en', 'ar', 'eg')
    #   - st.session_state['slang_cache']: Cache for randomized Egyptian variants
    #   - st.session_state['framework']: Current selected framework
    #
    # Called by: app.py during page initialization
    """
    # Step 1: Initialize language to English if not already set
    if 'lang' not in st.session_state:
        st.session_state['lang'] = 'en'

    # Step 2: Initialize slang variant cache for Egyptian randomization
    if 'slang_cache' not in st.session_state:
        st.session_state['slang_cache'] = {}

    # Step 3: Initialize framework selector to ICDF (first framework)
    if 'framework' not in st.session_state:
        st.session_state['framework'] = 'ICDF'

# ==============================================================================
# END i18n.py
# ==============================================================================
