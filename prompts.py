# prompts.py — Prompt Assembly & Framework Logic
# ============================================================================
# This module centralizes all prompt framework definitions, assembly logic,
# and example presets. It handles:
# - FRAMEWORKS: Definitions of ICDF, RCR-EOC, MICRO, COSTAR
# - EXAMPLES: Sample preset data for each framework and language
# - assemble_prompt(): Core logic to build structured prompts
# - sanitize_input(): Prevent injection attacks
# - get_example(): Fetch presets by framework and language
#
# All framework field orders and required fields are defined here,
# making them easy to modify or extend in the future.
# ============================================================================

# ==============================================================================
# FRAMEWORK DEFINITIONS
# ==============================================================================
# Each framework defines:
#   - 'fields': Ordered list of field names for this framework
#   - 'required': List of field names that must be filled (unless allow_blanks=True)
#   - 'labels_key': Mapping to translation keys (e.g., 'field_Instruction_label')
#
# Purpose: Centralize framework logic so UI can dynamically generate forms
# and assemble_prompt() can validate and construct prompts in correct order.

FRAMEWORKS = {
    # ========================================================================
    # ICDF — Instruction, Context, Data, Format
    # ========================================================================
    # Use case: Task-based prompting (summarization, analysis, drafting)
    # Best for: Instruction-driven work with clear input/output structure
    #
    'ICDF': {
        # fields: ordered list of field names for this framework
        'fields': ['Instruction', 'Context', 'Data', 'Format'],
        # required: which fields must be filled (unless allow_blanks=True)
        'required': ['Instruction', 'Format'],
        # labels_key: mapping from field name to TRANSLATIONS key
        # (used by UI to fetch label and help text)
    },

    # ========================================================================
    # RCR-EOC — Role, Context, Request, Examples, Output, Constraints
    # ========================================================================
    # Use case: Role-based + few-shot prompting (AI personas, agent behavior)
    # Best for: Complex tasks requiring context, examples, and specific output format
    #
    'RCR-EOC': {
        # fields: ordered list of field names for this framework
        'fields': ['Role', 'Context', 'Request', 'Examples', 'Output', 'Constraints'],
        # required: which fields must be filled (unless allow_blanks=True)
        'required': ['Role', 'Request'],
        # Note: Context label in final prompt is "Context (Work Environment):" to disambiguate
    },

    # ========================================================================
    # MICRO — Message, Intention, Context, Rhythm, Output
    # ========================================================================
    # Use case: Content/messaging prompting (copywriting, social media, video)
    # Best for: Creative messaging, tone/voice definition, narrative structure
    #
    'MICRO': {
        # fields: ordered list of field names for this framework
        'fields': ['Message', 'Intention', 'Context', 'Rhythm', 'Output'],
        # required: which fields must be filled (unless allow_blanks=True)
        'required': ['Message', 'Intention'],
    },

    # ========================================================================
    # COSTAR — Context, Offer, Style, Target, Action, Result
    # ========================================================================
    # Use case: Marketing/copywriting prompting (sales pages, campaigns, CTAs)
    # Best for: Customer-facing content, offers, and conversion optimization
    #
    'COSTAR': {
        # fields: ordered list of field names for this framework
        'fields': ['Context', 'Offer', 'Style', 'Target', 'Action', 'Result'],
        # required: which fields must be filled (unless allow_blanks=True)
        'required': ['Offer', 'Action'],
    },
}

# ==============================================================================
# EXAMPLES — Preset Data for Each Framework/Language
# ==============================================================================
# Provides presets for users to quickly populate fields and see framework usage.
# Structure: EXAMPLES[framework_lang_code] = {field: value, field: value, ...}
#
# Naming: {FRAMEWORK}_{LANG_CODE}
#   - FRAMEWORK: ICDF, RCR-EOC, MICRO, COSTAR (underscore instead of hyphen)
#   - LANG_CODE: en (English), ar (MSA Arabic), eg (Egyptian Arabic)
#
# Purpose:
#   - Users click "Insert Example" → fields populate with preset data
#   - Shows best practices for each framework and language
#   - Helps non-experts understand how to fill the form
#

EXAMPLES = {
    # ========================================================================
    # ICDF Examples
    # ========================================================================

    # ICDF_en: English example for task-based summarization
    'ICDF_en': {
        'Instruction': 'Summarize',
        'Context': 'Monthly report for the marketing director',
        'Data': 'Q3 sales figures: Revenue $120,000; Units sold 8,200; Top region: EMEA.',
        'Format': 'Bullet points; Formal tone; Max 200 words; Include concluding recommendation.',
    },

    # ICDF_ar: Modern Standard Arabic example
    'ICDF_ar': {
        'Instruction': 'لخص',
        'Context': 'تقرير شهري لمدير التسويق',
        'Data': 'أرقام المبيعات للربع الثالث: الإيرادات 120,000$؛ الوحدات المباعة 8,200؛ المنطقة الأعلى: EMEA.',
        'Format': 'نقاط؛ نبرة رسمية؛ حد أقصى 200 كلمة؛ تضمين توصية ختامية.',
    },

    # ICDF_eg: Egyptian Arabic example (informal, colloquial)
    'ICDF_eg': {
        'Instruction': 'لخّص اللي حصل',
        'Context': 'تقرير شهري لمدير التسويق',
        'Data': 'أرقام مبيعات الربع التالت: الإيراد 120,000$؛ الوحدات 8,200؛ أحسن منطقة: EMEA.',
        'Format': 'نقاط؛ نغمة رسمية؛ مش أكتر من 200 كلمة؛ وحط توصية ختامية.',
    },

    # ========================================================================
    # RCR-EOC Examples
    # ========================================================================

    # RCR-EOC_en: English example for role-based task with examples
    'RCR-EOC_en': {
        'Role': 'Senior Project Manager',
        'Context': 'Fast-paced agile development team',
        'Request': 'Review weekly performance report and identify recurring issues',
        'Examples': '(Input) Sprint burndown shows frequent scope creep; (Output) One-paragraph analysis and 3 prioritized recommendations.',
        'Output': 'Three-column table: Problem; Proposed Solution; Recommendation',
        'Constraints': 'Keep responses under three sentences',
    },

    # RCR-EOC_ar: Modern Standard Arabic example
    'RCR-EOC_ar': {
        'Role': 'مدير مشروع أول',
        'Context': 'فريق تطوير سريع التطور',
        'Request': 'راجع تقرير الأداء الأسبوعي وحدد المشاكل المتكررة',
        'Examples': '(المدخل) مخطط الحروق يُظهر زحف نطاق متكرر؛ (المخرج) تحليل فقرة واحدة و 3 توصيات مرتبة حسب الأولوية.',
        'Output': 'جدول ثلاثي الأعمدة: المشكلة؛ الحل المقترح؛ التوصية',
        'Constraints': 'اجعل الاستجابات أقل من ثلاث جمل',
    },

    # RCR-EOC_eg: Egyptian Arabic example
    'RCR-EOC_eg': {
        'Role': 'مدير مشروع شاطر',
        'Context': 'فريق تطوير سريع شوية',
        'Request': 'شوف تقرير الأسبوع وقول لي فيه إيه مشاكل بتتكرر',
        'Examples': '(المدخل) البرن داون بيقول إن الفريق دايماً بيضيف حاجات زيادة؛ (المخرج) فقرة واحدة وتلات حلول بالترتيب.',
        'Output': 'جدول فيه تلاث أعمدة: المشكلة؛ الحل؛ التوصية',
        'Constraints': 'مش أكتر من تلات جمل',
    },

    # ========================================================================
    # MICRO Examples
    # ========================================================================

    # MICRO_en: English example for messaging/content creation
    'MICRO_en': {
        'Message': 'AI is a tool for smarter studying',
        'Intention': 'Motivate students to try the product',
        'Context': 'University students under academic pressure',
        'Rhythm': 'Motivational, high energy, informal, quick',
        'Output': '5-minute YouTube script segmented Intro/Body/CTA',
    },

    # MICRO_ar: Modern Standard Arabic example
    'MICRO_ar': {
        'Message': 'الذكاء الاصطناعي أداة للدراسة الذكية',
        'Intention': 'تحفيز الطلاب لتجربة المنتج',
        'Context': 'طلاب الجامعة تحت الضغط الأكاديمي',
        'Rhythm': 'تحفيزي، طاقة عالية، غير رسمي، سريع',
        'Output': 'سيناريو يوتيوب لمدة 5 دقائق: المقدمة/المتن/نداء الإجراء',
    },

    # MICRO_eg: Egyptian Arabic example
    'MICRO_eg': {
        'Message': 'الذكاء الاصطناعي أداة للمذاكرة الذكية',
        'Intention': 'نشجع الطلاب يجربوا التطبيق',
        'Context': 'طلاب جامعة فيهم ضغط دراسي كتير',
        'Rhythm': 'حماسي، طاقة عالية، بسيط، سريع',
        'Output': 'سيناريو يوتيوب 5 دقائق: مقدمة + الموضوع + نداء',
    },

    # ========================================================================
    # COSTAR Examples
    # ========================================================================

    # COSTAR_en: English example for marketing/copywriting
    'COSTAR_en': {
        'Context': 'We are launching a new smart product line.',
        'Offer': '25% off all cleaning products for 72 hours.',
        'Style': 'Simple, elegant, warm, like a personal recommendation from a friend.',
        'Target': 'Women aged 25-45 who dislike strenuous cleaning.',
        'Action': 'Click the link before the offer expires.',
        'Result': 'Maximize sales during the 3-day window',
    },

    # COSTAR_ar: Modern Standard Arabic example
    'COSTAR_ar': {
        'Context': 'نطلق خط منتجات ذكي جديد.',
        'Offer': 'خصم 25% على جميع منتجات التنظيف لمدة 72 ساعة.',
        'Style': 'بسيط، أنيق، دافئ، مثل توصية شخصية من صديق.',
        'Target': 'النساء اللواتي تتراوح أعمارهن بين 25-45 سنة ولا يحبذن التنظيف الشاق.',
        'Action': 'انقر على الرابط قبل انتهاء العرض.',
        'Result': 'تعظيم المبيعات خلال النافذة المدتها 3 أيام',
    },

    # COSTAR_eg: Egyptian Arabic example
    'COSTAR_eg': {
        'Context': 'بنطلق خط منتجات ذكي جديد.',
        'Offer': '25% خصم على كل منتجات التنظيف لمدة 72 ساعة بس.',
        'Style': 'بسيط، شيك، دافي، زي ما يقول لك صاحبك توصية.',
        'Target': 'البنات اللي عندهم بين 25 لـ 45 سنة وما يحبوا الكنس والتنظيف.',
        'Action': 'اضغط على الرابط وخد الخصم قبل ما ينتهي.',
        'Result': 'نزود المبيعات في التلات أيام دي',
    },
}

# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def sanitize_input(text):
    """
    # sanitize_input(text) — Prevent injection attacks in prompt text
    #
    # Purpose: Clean user input to prevent malicious code injection while
    # preserving legitimate content and formatting (newlines, etc.)
    #
    # Parameters:
    #   - text (str): User input text to sanitize
    #
    # Returns:
    #   - str: Sanitized text with harmful sequences removed
    #
    # Sanitization rules (applied in order):
    #   1. Remove <script> tags and contents (XSS prevention)
    #   2. Remove <iframe> tags and contents (frame injection prevention)
    #   3. Escape angle brackets < > to prevent HTML injection
    #   4. Preserve newlines for formatting (internal line breaks allowed)
    #
    # Safety notes:
    #   - This is NOT complete HTML escaping (that's done at render time)
    #   - Designed for text prompt content, not HTML contexts
    #   - Future: Consider using html.escape() for full safety
    #
    # Example:
    #   sanitize_input('<script>alert("xss")</script>hello')
    #   → 'hello'
    #
    #   sanitize_input('Line 1\nLine 2') → 'Line 1\nLine 2' (preserved)
    """
    # Step 1: Check if input is a string; if not, return empty string
    if not isinstance(text, str):
        return ''

    # Step 2: Remove <script> tags and all content between them
    import re
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)

    # Step 3: Remove <iframe> tags and all content between them
    text = re.sub(r'<iframe[^>]*>.*?</iframe>', '', text, flags=re.IGNORECASE | re.DOTALL)

    # Step 4: Replace lone angle brackets (but preserve legitimate content)
    # Only escape if they don't look like part of a word (defensive)
    text = text.replace('&', '&amp;')  # Escape ampersands first
    text = text.replace('<', '&lt;')   # Escape < to &lt;
    text = text.replace('>', '&gt;')   # Escape > to &gt;

    # Step 5: Return sanitized text (newlines preserved for multiline content)
    return text.strip()


def assemble_prompt(framework, lang, fields, allow_blanks=False):
    """
    # assemble_prompt(framework, lang, fields, allow_blanks) — Assemble final prompt
    #
    # Purpose: Validate field values and construct final prompt string in framework-
    # specific order with proper formatting (labeled sections, newlines, etc.)
    #
    # Parameters:
    #   - framework (str): Framework name ('ICDF', 'RCR-EOC', 'MICRO', 'COSTAR')
    #   - lang (str): Language code ('en', 'ar', 'eg')
    #   - fields (dict): Field name → user input value (from form)
    #   - allow_blanks (bool): If True, skip required field validation
    #
    # Returns:
    #   - tuple: (success: bool, prompt_or_error: str)
    #   - Success: (True, final_prompt_string)
    #   - Failure: (False, error_message_in_requested_language)
    #
    # Validation:
    #   - If allow_blanks=False, checks that all required fields have non-empty values
    #   - Returns error message (translated) if validation fails
    #   - Error messages use TRANSLATIONS[lang] via fallback lookup
    #
    # Assembly rules (from spec):
    #   1. Iterate through framework fields in defined order
    #   2. For each field: emit label (translated) + ": " + value
    #   3. Special case RCR-EOC 'Context' → label as "Context (Work Environment):"
    #   4. Separate sections with exactly two newlines ("\n\n")
    #   5. Sanitize all user input via sanitize_input()
    #   6. Trim whitespace on values; preserve internal newlines
    #   7. Return single string with NO trailing whitespace or newline
    #
    # Example output (ICDF_en):
    #   "Instruction: Summarize\n\nContext: ...\n\nData: ...\n\nFormat: ..."
    #
    # Error handling:
    #   - Returns (False, error_message) if framework not found
    #   - Returns (False, error_message) if required fields missing and allow_blanks=False
    #   - Returns (True, prompt_string) on success
    #
    # Translation of labels:
    #   - Imports from i18n module: t(lang, f'field_{fieldname}_label')
    #   - Falls back gracefully to English if lang-specific label missing
    """
    # Step 1: Import translation function (avoid circular import in module initialization)
    from i18n import t

    # Step 2: Validate that framework exists in FRAMEWORKS dict
    if framework not in FRAMEWORKS:
        return (False, f"Framework '{framework}' not found.")

    # Step 3: Get framework metadata (fields list, required fields list)
    framework_meta = FRAMEWORKS[framework]
    framework_fields = framework_meta['fields']
    required_fields = framework_meta['required']

    # Step 4: Validate required fields ONLY if allow_blanks=False
    if not allow_blanks:
        # Step 4a: Check each required field for empty/missing value
        for field_name in required_fields:
            # Step 4b: Get value from fields dict; if missing or empty, fail validation
            field_value = fields.get(field_name, '').strip()
            if not field_value:
                # Step 4c: Return error message (translated)
                error_msg = t(lang, 'required_error')
                return (False, error_msg)

    # Step 5: Assemble prompt by iterating through fields in framework-defined order
    prompt_sections = []

    # Step 5a: Iterate through each field in framework order
    for field_name in framework_fields:
        # Step 5b: Get user input for this field; default to empty string if missing
        field_value = fields.get(field_name, '').strip()

        # Step 5c: Sanitize input to prevent injection attacks
        sanitized_value = sanitize_input(field_value)

        # Step 5d: Fetch translated label for this field
        # Examples: 'field_Instruction_label', 'field_Role_label', etc.
        label_key = f'field_{field_name}_label'
        translated_label = t(lang, label_key)

        # Step 5e: Special case for RCR-EOC Context field (disambiguate)
        if framework == 'RCR-EOC' and field_name == 'Context':
            # Step 5e-i: Override label to "Context (Work Environment):" for clarity
            translated_label = translated_label + ' (Work Environment)'

        # Step 5f: Construct section: "Label: Value"
        section = f"{translated_label}: {sanitized_value}"

        # Step 5g: Add section to list
        prompt_sections.append(section)

    # Step 6: Join all sections with exactly two newlines between them
    # This creates the final multi-section prompt string
    final_prompt = '\n\n'.join(prompt_sections)

    # Step 7: Strip trailing whitespace (no trailing newline)
    final_prompt = final_prompt.rstrip()

    # Step 8: Return success tuple with final prompt
    return (True, final_prompt)


def get_example(framework, lang):
    """
    # get_example(framework, lang) — Fetch example preset for framework/language
    #
    # Purpose: Retrieve a pre-filled example (preset) for a given framework and
    # language. Users click "Insert Example" to populate form fields with this data.
    #
    # Parameters:
    #   - framework (str): Framework name ('ICDF', 'RCR-EOC', 'MICRO', 'COSTAR')
    #   - lang (str): Language code ('en', 'ar', 'eg')
    #
    # Returns:
    #   - dict: Example data {field_name: example_value, ...}
    #   - Empty dict {} if framework/language combo not found
    #
    # Key name format:
    #   - Constructed as: f"{framework}_{lang}"
    #   - Replace hyphens in framework name with underscores
    #   - Examples: 'ICDF_en', 'RCR_EOC_en', 'MICRO_ar', 'COSTAR_eg'
    #
    # Example:
    #   get_example('ICDF', 'en') → {'Instruction': 'Summarize', 'Context': '...', ...}
    #   get_example('FAKE_FRAMEWORK', 'en') → {} (not found)
    #
    # Usage in UI:
    #   - User clicks "Insert Example" button in sidebar
    #   - Calls this function with current framework and language
    #   - Returns fields dict that populates form input fields
    #   - User sees example and can modify it for their use case
    """
    # Step 1: Construct example key from framework name and language code
    # Replace hyphens with underscores (e.g., RCR-EOC → RCR_EOC)
    example_key = f"{framework.replace('-', '_')}_{lang}"

    # Step 2: Look up example in EXAMPLES dict; return empty dict if not found
    return EXAMPLES.get(example_key, {})

# ==============================================================================
# END prompts.py
# ==============================================================================
