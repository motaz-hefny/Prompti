# Prompti — Ultimate Windsurf-ready specification (single text artifact, Markdown-formatted)

This document is an expanded, more concrete, and human-readable brief you can paste into Windsurf (or hand to a developer). It adds:
- A clear human-readable description of what the app does and who it serves
- A single-file MVP option and an advanced multi-file architecture option
- Full TRANSLATIONS including English, Modern Standard Arabic (MSA), and Egyptian colloquial (eg) with heavy slang variants
- A built-in randomized-eg slang strategy (so messages vary)
- Exact implementation rules, UI behaviors, acceptance tests, examples, README, deploy notes, and developer guidance
Use this text exactly as a deterministic spec. Request Windsurf to output either Option A (single-file app.py + requirements.txt) or Option B (multi-file repo). The produced app must pass acceptance tests below.

---

1 — Human-friendly description (what Prompti does, who it helps, and why)
Prompti is a lightweight web tool for creating precise, professional prompts for AI systems. It helps users convert loosely-formed goals into structured prompts using four proven frameworks (ICDF, RCR-EOC, MICRO, COSTAR). Prompti targets:
- Product managers, marketers, analysts, and AI users who need repeatable, audit-ready prompts
- Non-native English speakers who want translated UI and native Arabic (MSA) plus playful Egyptian dialect
- Rapid prototyping and sharing of prompts via copy/download for immediate use in LLMs or agent systems

What the app does (plain language):
- Presents four structured prompt templates; users fill fields that capture intent, context, examples, constraints, and output format
- Shows a live preview of the assembled prompt as the user types
- Produces a final, standardized prompt string with clear labeled sections ready to paste into an AI tool
- Lets the user copy the prompt to the clipboard or download it as a .txt file
- Supports English, Modern Standard Arabic (formal) and Egyptian Arabic (playful), including randomized slang variants so Egyptian microcopy feels lively and not repetitive
- Provides a mock "Sign In with Google" button for future integration; Save-to-Drive is a disabled placeholder for Pro features

Why this matters:
- Produces consistent, repeatable prompts that make AI output reliable and auditable
- Multilingual UI expands adoption; Egyptian slang builds personality and delight for local audiences
- Minimal friction; works on free hosting for an immediate MVP

---

2 — Delivery options (pick one in Windsurf)
- Option A (MVP): Single-file app.py + requirements.txt. Fastest path to run and deploy on Streamlit Community Cloud or Hugging Face Spaces.
- Option B (Advanced): Multi-file repo:
  - app.py (UI)
  - i18n.py (TRANSLATIONS + helpers)
  - prompts.py (assemble_prompt, EXAMPLES, unit-testable)
  - utils.py (clipboard helper, RTL_CSS, sanitizer)
  - auth.py (mock + future OAuth skeleton)
  - requirements.txt
  - README.md

Recommendation: start Option A, then refactor to Option B once initial tests pass.

---

3 — High-level UI & UX (exact behavior to implement)
Sidebar:
- Language selector (radio): English / العربية / مصرّي  (internal codes: 'en','ar','eg')
- Framework selector (selectbox): ICDF / RCR-EOC / MICRO / COSTAR
- Mock Sign In with Google button (translated)
- Allow blanks checkbox (translated)
- Persist selection via st.session_state['lang'] and ['framework']

Main area (responsive):
- Two columns:
  - Left: dynamic form for selected framework, with help text/tooltips (use help= parameter).
  - Right: Live preview at top, final generated prompt (st.code) and export buttons below.
- Live Preview updates immediately as the user types.
- Generate final prompt button validates required fields (unless Allow blanks) and writes the final string to session_state['generated_prompt'] and displays it in st.code.

Export controls (below final prompt):
- Copy to Clipboard: JS via st.components.v1.html using navigator.clipboard.writeText(prompt). Post a message back to Streamlit and show st.success or st.error with translated message.
- Download Prompt: st.download_button producing prompti_prompt_<framework>_<lang>.txt (text/plain).
- Save to Drive: st.button(..., disabled=True) with st.caption showing save_to_drive_tooltip (translated).

RTL:
- When 'ar' or 'eg' selected inject CSS:
  body { direction: rtl; text-align: right; }
- Ensure code block and buttons align right; flip button visual order for RTL.

Session persistence:
- Store field values per-framework: st.session_state['fields'][framework] = {...}
- Switching frameworks saves/restores field state.

Examples:
- Provide one-click "Insert example" that populates fields from EXAMPLES for the chosen framework/language and shows a small success message.

Accessibility:
- All inputs have visible labels and help= tooltips
- Buttons are keyboard-focusable; color contrast is readable

---

4 — TRANSLATIONS (en / ar / eg) + heavy Egyptian slang randomization strategy
Include this TRANSLATIONS block verbatim. Additionally include an EG_SLANG_VARIANTS structure for randomized microcopy. Implement helper function t(lang,key) that:
- If key found in TRANSLATIONS[lang] return it
- Else if lang == 'eg' and key in TRANSLATIONS['ar'] return TRANSLATIONS['ar'][key]
- Else return TRANSLATIONS['en'].get(key,key)

Add get_slang(lang,key) helper for 'eg' that randomly picks a variant from EG_SLANG_VARIANTS[key] when available.

TRANSLATIONS = {
  'en': {
    'title': 'Prompti — Structured Prompt Generator',
    'sign_in': 'Sign In with Google',
    'language_label': 'Language',
    'framework_label': 'Framework',
    'frameworks': {'ICDF':'ICDF','RCR-EOC':'RCR-EOC','MICRO':'MICRO','COSTAR':'COSTAR'},
    'allow_blanks': 'Allow blanks (disable required validation)',
    'field_Instruction_label':'Instruction',
    'field_Instruction_help':"The action. Define the primary task (e.g., 'Summarize', 'Analyze', 'Draft').",
    'field_Context_label':'Context',
    'field_Context_help':"The Situation/Purpose. Explain why the task is being done and who the audience is.",
    'field_Data_label':'Data',
    'field_Data_help':"The Input. Provide the raw data or detailed information the AI needs to process.",
    'field_Format_label':'Format',
    'field_Format_help':"The Output Style. Specify the desired structure and tone.",
    'field_Role_label':'Role',
    'field_Role_help':"The Persona. Assign the AI a clear professional identity.",
    'field_Request_label':'Request',
    'field_Request_help':"The Specific Job. State the precise deliverable.",
    'field_Examples_label':'Examples',
    'field_Examples_help':"Few-shot example input and desired output to set expectations.",
    'field_Output_label':'Output',
    'field_Output_help':"The Structure. Define the exact structure of the response.",
    'field_Constraints_label':'Constraints',
    'field_Constraints_help':"The Limitations. Set boundaries the AI must follow.",
    'field_Message_label':'Message',
    'field_Message_help':"The Core Idea. What is the single, central theme or takeaway you want to convey?",
    'field_Intention_label':'Intention',
    'field_Intention_help':"The Goal. What action or feeling should the audience have after consuming the content?",
    'field_Rhythm_label':'Rhythm',
    'field_Rhythm_help':"Tone and Pace. Define the style, mood, and speed.",
    'field_Offer_label':'Offer',
    'field_Offer_help':"The Value Proposition. The deal, discount, or benefit.",
    'field_Style_label':'Style',
    'field_Style_help':"The Voice. The brand personality.",
    'field_Target_label':'Target',
    'field_Target_help':"The Audience Profile. Define the ideal customer.",
    'field_Action_label':'Action',
    'field_Action_help':"Call to Action (CTA). What must the user click or do?",
    'field_Result_label':'Result',
    'field_Result_help':"The Business Goal. What outcome do we want from this marketing piece?",
    'button_generate':'Generate Prompt',
    'button_preview':'Preview',
    'button_copy':'Copy to Clipboard',
    'button_download':'Download Prompt',
    'button_save_drive':'Save to Drive (Placeholder)',
    'save_to_drive_tooltip':'Feature requires Pro subscription.',
    'mock_signin_info':'This is a mock sign-in UI.',
    'copy_success':'Prompt copied to clipboard.',
    'copy_fail':'Clipboard not available. Use Download button.',
    'preview_label':'Live preview (updates as you type)',
    'generated_label':'Final generated prompt',
    'insert_example':'Insert example',
    'reset_form':'Reset fields',
    'example_filled':'Example fields inserted.',
    'required_error':'Please fill required fields or enable "Allow blanks".',
    'smoke_ok':'Smoke checks passed.'
  },
  'ar': {
    'title':'برومبتي — منشئ عبارات مهيكلة',
    'sign_in':'تسجيل الدخول عبر جوجل',
    'language_label':'اللغة',
    'framework_label':'الإطار',
    'frameworks':{'ICDF':'ICDF','RCR-EOC':'RCR-EOC','MICRO':'MICRO','COSTAR':'COSTAR'},
    'allow_blanks':'السماح بالفراغات (تعطيل تحقق الحقول المطلوبة)',
    'field_Instruction_label':'التعليمات',
    'field_Instruction_help':'الإجراء. عرّف المهمة الأساسية (مثل: لخص، حلل، اكتب).',
    'field_Context_label':'السياق',
    'field_Context_help':'الوضع/الهدف. اشرح سبب تنفيذ المهمة ومن هو الجمهور.',
    'field_Data_label':'البيانات',
    'field_Data_help':'المدخلات. قدّم البيانات أو المعلومات التي يحتاجها الذكاء الاصطناعي لمعالجتها.',
    'field_Format_label':'التنسيق',
    'field_Format_help':'نمط الإخراج. حدد البنية والنبرة المطلوبة.',
    'field_Role_label':'الدور',
    'field_Role_help':'الشخصية. عيّن هوية مهنية للذكاء الاصطناعي.',
    'field_Request_label':'الطلب',
    'field_Request_help':'المهمة المحددة. ضع المخرجات المطلوبة بدقة.',
    'field_Examples_label':'أمثلة',
    'field_Examples_help':'مثال مدخل ومثال المخرجات المرغوبة لضبط التوقّعات.',
    'field_Output_label':'الإخراج',
    'field_Output_help':'البنية. حدّد البنية الدقيقة للاستجابة.',
    'field_Constraints_label':'القيود',
    'field_Constraints_help':'الحدود. ضع القواعد التي يجب أن يتبعها الذكاء الاصطناعي.',
    'field_Message_label':'الرسالة',
    'field_Message_help':'الفكرة الأساسية. الفكرة أو الاستنتاج الذي تريد نقله.',
    'field_Intention_label':'النية',
    'field_Intention_help':'الهدف. ما الإجراء أو الشعور المطلوب لدى الجمهور؟',
    'field_Rhythm_label':'الإيقاع',
    'field_Rhythm_help':'النغمة والسرعة. حدد الأسلوب والمزاج والوتيرة.',
    'field_Offer_label':'العرض',
    'field_Offer_help':'القيمة المقدمة. الخصم أو الفائدة.',
    'field_Style_label':'النغمة',
    'field_Style_help':'صوت العلامة التجارية.',
    'field_Target_label':'الالهدف',
    'field_Target_help':'ملف الجمهور المستهدف.',
    'field_Action_label':'الإجراء',
    'field_Action_help':'نداء لاتخاذ إجراء. ما الذي يجب أن يفعله المستخدم؟',
    'field_Result_label':'النتيجة',
    'field_Result_help':'هدف العمل. النتيجة المرغوبة.',
    'button_generate':'إنشاء العبارة',
    'button_preview':'معاينة',
    'button_copy':'نسخ إلى الحافظة',
    'button_download':'تنزيل العبارة',
    'button_save_drive':'حفظ إلى Drive (نموذجي)',
    'save_to_drive_tooltip':'الميزة تتطلب اشتراك Pro.',
    'mock_signin_info':'هذه واجهة تسجيل دخول تجريبية.',
    'copy_success':'تم نسخ العبارة إلى الحافظة.',
    'copy_fail':'الميزة غير متاحة. استخدم زر التنزيل.',
    'preview_label':'معاينة مباشرة (تتحدّث أثناء الكتابة)',
    'generated_label':'العبارة النهائية المولّدة',
    'insert_example':'إدراج مثال',
    'reset_form':'إعادة تعيين الحقول',
    'example_filled':'تم إدخال المثال في الحقول.',
    'required_error':'يرجى تعبئة الحقول المطلوبة أو تفعيل "السماح بالفراغات".',
    'smoke_ok':'اختبارات التدخين ناجحة.'
  },
  'eg': {
    # Heavy colloquial Egyptian (for labels mostly safe; microcopy playful)
    'title':'برومبتي — مولّد برومبت',
    'sign_in':'دخول بجوجل',
    'language_label':'اللغة',
    'framework_label':'الإطار',
    'frameworks':{'ICDF':'ICDF','RCR-EOC':'RCR-EOC','MICRO':'MICRO','COSTAR':'COSTAR'},
    'allow_blanks':'خلي الحقول فاضية لو تحب',
    'field_Instruction_label':'التعليمات',
    'field_Instruction_help':'اعمل إيه بالظبط. اكتب المهمة الأساسية (مثال: لخّص، حلّل، اكتب).',
    'field_Context_label':'السياق',
    'field_Context_help':'ليه بنعمل ده ومين اللي هيقراه؟',
    'field_Data_label':'البيانات',
    'field_Data_help':'المدخلات. حط البيانات أو النص اللي عايز النظام يشتغل عليه.',
    'field_Format_label':'التنسيق',
    'field_Format_help':'شكل الخرج. نقاط ولا فقرة؟ نغمة رسمية ولا خفيفة؟',
    'field_Role_label':'الدور',
    'field_Role_help':'هيتصرف كأنه مين؟ (مثال: مدير مشروع كبير).',
    'field_Request_label':'الطلب',
    'field_Request_help':'المطلوب بالظبط. اكتب المهمة بوضوح.',
    'field_Examples_label':'أمثلة',
    'field_Examples_help':'هات مثال للمدخل والمُخرَج المرغوب علشان النظام يفهم.',
    'field_Output_label':'الإخراج',
    'field_Output_help':'شكل الرد اللي عايزه.',
    'field_Constraints_label':'القيود',
    'field_Constraints_help':'حط حدود أو حاجات ممنوعة.',
    'field_Message_label':'الرسالة',
    'field_Message_help':'الفكرة اللي عايز توصلها.',
    'field_Intention_label':'النية',
    'field_Intention_help':'عايز الناس تعمل إيه أو تحس بإيه بعد ما يقروها؟',
    'field_Rhythm_label':'الإيقاع',
    'field_Rhythm_help':'نبرة وسرعة الكلام. عايزها حماسية ولا هادية؟',
    'field_Offer_label':'العرض',
    'field_Offer_help':'العرض أو الخصم أو الميزة اللي عندك.',
    'field_Style_label':'الطابع',
    'field_Style_help':'شخصية الماركة: بسيطة، أنيقة، ولا مرحة؟',
    'field_Target_label':'الزباين',
    'field_Target_help':'مين الجمهور المستهدف؟',
    'field_Action_label':'الإجراء',
    'field_Action_help':'عايزهم يعملوا إيه؟ اضغطوا، اشتركوا، ولا اتصلوا؟',
    'field_Result_label':'النتيجة',
    'field_Result_help':'النتيجة اللي بتدور عليها.',
    'button_generate':'اطلع البرومبت',
    'button_preview':'شوف المعاينة',
    'button_copy':'انسخها',
    'button_download':'نزّلها',
    'button_save_drive':'احفظ على Drive (نموذجي)',
    'save_to_drive_tooltip':'الخاصية للمشتركين Pro، انت مش منّهم لسه :)',
    'mock_signin_info':'دي تجربة تسجيل دخول، مش دخول حقيقي.',
    'copy_success':'اتنسخت! جاهز تلزقها.',
    'copy_fail':'مفيش صلاحية للحافظة. جرّب تنزيل الملف.',
    'preview_label':'المعاينة الحيّة (بتتحدّث وانت بتكتب)',
    'generated_label':'البرومبت النهائي',
    'insert_example':'حط مثال جاهز',
    'reset_form':'افرّغ الحقول',
    'example_filled':'اتعبّيت الحقول بالمثال.',
    'required_error':'كمّل الحقول المطلوبة ولا فعل "خلي الحقول فاضية".',
    'smoke_ok':'الشيكات نجحت.'
  }
}

# EG slang variants (for randomized microcopy)
EG_SLANG_VARIANTS = {
  'copy_success': [
    'اتنسخت! جاهز تلزقها.',
    'اتنسخت يا معلم، دوس علطول.',
    'تمام — اتنسخت. خشّ وِلصّق.',
    'يقلبت الحكاية: اتنسخت خلاص.'
  ],
  'button_copy': [
    'انسخها',
    'انسخها ياباشا',
    'انسخها دلوقتي',
    'هاتها انسخ'
  ],
  'insert_example': [
    'حط مثال جاهز',
    'حطلي مثال كده',
    'جيّب مثال واملى الحقول',
    'ارمِلي مثال'
  ],
  'mock_signin_info': [
    'دي تجربة تسجيل دخول، مش دخول حقيقي.',
    'دي فِكّرية بس علشان نجرب، مش تسجيل حقيقي.',
    'أخدنا سيرة جوجل بس للعرض، مش تسجيل فعلي.'
  ]
}

Implementation note:
- When lang == 'eg' and key in EG_SLANG_VARIANTS, render random.choice(EG_SLANG_VARIANTS[key]) each time the UI renders the message/button. Persist randomness per-session or per-action (recommended: new random variant each page load or each button render; do not change mid-input to avoid UX confusion).

---

5 — EXAMPLES (presets)
Include the following EXAMPLES dict exactly (English, MSA, and Egyptian seeds). Windsurf may expand.

EXAMPLES = {
  'ICDF_en': {
    'Instruction':'Summarize',
    'Context':'Monthly report for the marketing director',
    'Data':'Q3 sales figures: Revenue $120,000; Units sold 8,200; Top region: EMEA.',
    'Format':'Bullet points; Formal tone; Max 200 words; Include concluding recommendation.'
  },
  'RCR-EOC_en': {
    'Role':'Senior Project Manager',
    'Context':'Fast-paced agile development team',
    'Request':'Review weekly performance report and identify recurring issues',
    'Examples':'(Input) Sprint burndown shows frequent scope creep; (Output) One-paragraph analysis and 3 prioritized recommendations.',
    'Output':'Three-column table: Problem; Proposed Solution; Recommendation',
    'Constraints':'Keep responses under three sentences'
  },
  'MICRO_en': {
    'Message':'AI is a tool for smarter studying',
    'Intention':'Motivate students to try the product',
    'Context':'University students under academic pressure',
    'Rhythm':'Motivational, high energy, informal, quick',
    'Output':'5-minute YouTube script segmented Intro/Body/CTA'
  },
  'COSTAR_en': {
    'Context':'We are launching a new smart product line.',
    'Offer':'25% off all cleaning products for 72 hours.',
    'Style':'Simple, elegant, warm, like a personal recommendation from a friend.',
    'Target':'Women aged 25-45 who dislike strenuous cleaning.',
    'Action':'Click the link before the offer expires.',
    'Result':'Maximize sales during the 3-day window'
  },
  'ICDF_ar': {
    'Instruction':'لخص',
    'Context':'تقرير شهري لمدير التسويق',
    'Data':'أرقام المبيعات للربع الثالث: الإيرادات 120,000$؛ الوحدات المباعة 8,200؛ المنطقة الأعلى: EMEA.',
    'Format':'نقاط؛ نبرة رسمية؛ حد أقصى 200 كلمة؛ تضمين توصية ختامية.'
  },
  'ICDF_eg': {
    'Instruction':'لخّص اللي حصل',
    'Context':'تقرير شهري لمدير التسويق',
    'Data':'أرقام مبيعات الربع التالت: الإيراد 120,000$؛ الوحدات 8,200؛ أحسن منطقة: EMEA.',
    'Format':'نقاط؛ نغمة رسمية؛ مش أكتر من 200 كلمة؛ وحط توصية ختامية.'
  }
}

---

6 — Prompt assembly rules (exact, machine-checkable)
- Sections for each framework must be in this order and labeled with translated labels:
  - ICDF: Instruction, Context, Data, Format
  - RCR-EOC: Role, Context (Work Environment), Request, Examples, Output, Constraints
  - MICRO: Message, Intention, Context, Rhythm, Output
  - COSTAR: Context, Offer, Style, Target, Action, Result
- For RCR-EOC use label "Context (Work Environment):" to disambiguate in the final prompt.
- Each labeled section must be followed by its value (or nothing if blank) and there must be exactly two newline characters between sections.
- Trim whitespace on values; preserve internal newlines in provided text.
- Final assembled prompt: single string, no trailing whitespace or trailing newline.

---

7 — Acceptance tests (automatable checks)
Automate or manually verify:
- When loading EXAMPLES['ICDF_en'], assemble_prompt must return exactly:

Instruction: Summarize

Context: Monthly report for the marketing director

Data: Q3 sales figures: Revenue $120,000; Units sold 8,200; Top region: EMEA.

Format: Bullet points; Formal tone; Max 200 words; Include concluding recommendation.

- Assemble RCR-EOC_en and MICRO_en to match expected outputs in EXAMPLES.
- Language toggle changes UI strings entirely; 'ar' and 'eg' apply RTL and translated labels.
- 'eg' microcopy uses randomized variants from EG_SLANG_VARIANTS for keys that are randomized (e.g., copy_success).
- Copy to clipboard writes exact assembled prompt; fallback shows translated copy_fail.
- Download saves a .txt file with correct content and filename pattern prompti_prompt_<framework>_<lang>.txt.
- Save to Drive is disabled and shows tooltip caption.
- Insert example populates fields for current framework and language.
- Reset fields clears only current framework's stored items.

---

8 — README.md (paste into repo)
# Prompti — Structured Prompt Generator

Quick start:
1. Python 3.9+ recommended.
2. pip install -r requirements.txt
3. streamlit run app.py

Features:
- Multilingual UI: English, Modern Standard Arabic, Egyptian colloquial (randomized slang variants)
- Four prompt frameworks: ICDF, RCR-EOC, MICRO, COSTAR
- Live preview, Generate, Copy, Download, disabled Save-to-Drive placeholder
- TRANSLATIONS centralized for easy extension

Deployment:
- Streamlit Community Cloud and Hugging Face Spaces recommended for free deployment.

Extending:
- Add locales to TRANSLATIONS; add slang variants to EG_SLANG_VARIANTS for randomized Egyptian tone.

---

9 — Implementation tips and code hints (for Windsurf)
- t(lang,key) helper uses fallback: TRANSLATIONS[lang].get(key) → TRANSLATIONS['ar'].get(key) (for 'eg') → TRANSLATIONS['en'].get(key)
- get_slang(lang,key): if lang=='eg' and key in EG_SLANG_VARIANTS: return random.choice(EG_SLANG_VARIANTS[key]) else return t(lang,key)
- Persist random picks per session if desired: store chosen variant in session_state on first render for consistency within session (recommended).
- Clipboard JS snippet (use st.components.v1.html): include postMessage to Streamlit; on postMessage show success/error with t(lang,'copy_success') or t(lang,'copy_fail').
- For disabled Save-to-Drive tooltip: Streamlit lacks per-widget hover-tooltips; include st.caption(t(lang,'save_to_drive_tooltip')) next to the disabled button.
- Use st.code for monospaced prompt output. For RTL code blocks, wrap in a container with style direction: rtl if lang in ('ar','eg').

---

10 — Developer checklist (pre-delivery)
- [ ] app runs with pip install -r requirements.txt and streamlit run app.py
- [ ] Languages 'en','ar','eg' present and t() fallback works
- [ ] Randomized Egyptian microcopy implemented and persisted per session if intended
- [ ] Acceptance tests pass for EXAMPLES
- [ ] Copy + Download export flows work and show translated user feedback
- [ ] Save-to-Drive disabled with visible tooltip/caption
- [ ] Smoke checks print to console at start: TRANSLATIONS keys found; frameworks count == 4; EXAMPLES present

---

11 — Final notes about the Egyptian slang choice
- You requested heavy, native, playful Egyptian slang. This doc contains an 'eg' locale with heavy colloquial microcopy and EG_SLANG_VARIANTS for randomized variants of key microcopy strings (copy success, copy button label, insert example and other microcopy).
- UX recommendation: keep critical help/tooltips largely clear (MSA or lightly colloquial) to avoid misunderstanding while allowing playful slang for buttons and notifications.
- Randomization: choose per-page-load random variants or persistent-per-session pick. Per-action re-randomization can be fun but may confuse users if text changes mid-task.

---

END — Paste this entire text into Windsurf or give it to your developer. Ask for Option A (single-file) to deliver a runnable MVP quickly, then use Option B (multi-file) to refactor for maintainability. This artifact is intentionally exhaustive; implementation must follow the assembly rules and acceptance tests exactly.
