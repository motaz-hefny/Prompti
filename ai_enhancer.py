# ==============================================================================
# ai_enhancer.py — AI-Powered Prompt Enhancement
# ==============================================================================
# Purpose: Use Google Gemini API to intelligently enhance user inputs
# Features:
#   - Fills missing framework fields intelligently
#   - Polishes rough inputs into professional prompts
#   - Understands user intent and expands it
#   - Completely free (Google Gemini free tier)
# ==============================================================================

import os
import json
import re
import traceback
from typing import Tuple

# Step 1: Try to import genai (Google Gemini SDK)
# If not installed, functions will return user input as-is
try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False

# ==============================================================================
# CONFIGURATION
# ==============================================================================

# Google Gemini model version to use
# Step 2a: Using gemini-1.5-flash (fastest, most free requests)
# Use a conservative, broadly-supported model by default.
# Many deployments accept 'models/text-bison-001' (see Google models docs).
# Default to Gemini 2.5 Flash as requested by the user (prefer Gemini 2.5 family).
MODEL_NAME = "models/gemini-2.5-flash"

# Candidate model names to try if the default MODEL_NAME is not available.
# Order: prefer Gemini 2.5 Flash, then other Gemini 2.5 and 3.x variants, then bison/chat fallbacks.
MODEL_CANDIDATES = [
    "models/gemini-2.5-flash",
    "models/gemini-2.5-pro",
    "models/gemini-3-pro",
    "models/gemini-2.0-flash",
    "models/text-bison-001",
    "text-bison@001",
    "models/chat-bison-001",
]

# Cached selected model after a successful probe
# For stability in deployment, prefer a known-good model by default.
# This forces the enhancer to use Gemini 2.5 Flash unless explicitly changed.
SELECTED_MODEL = "models/gemini-2.5-flash"

# Step 2b: System prompts for prompt enhancement (in multiple languages)
ENHANCEMENT_PROMPTS = {
    'en': (
        """
You are an expert prompt engineer. Your job is to take raw, incomplete user inputs
and transform them into professional, well-structured prompts ready for AI assistants.

When given user input, you should:
1. Identify which framework field each input belongs to
2. Fill in missing fields intelligently based on context
3. Expand vague inputs into specific, actionable instructions
4. Maintain the user's original intent while improving clarity

CRITICAL (follow exactly):
- Return a single valid JSON object and nothing else. Do not include any explanatory text, headings, or markdown.
- The JSON object must begin with '{' and end with '}' and contain only the framework field names as keys.
- If you cannot produce a value for a field, return an empty string for that key.

STRICT OUTPUT RULES (VERY IMPORTANT):
- Your response MUST be exactly one valid JSON object and nothing else — no commentary, no code fences, no leading or trailing characters.
- If you cannot produce a valid JSON object for any reason, respond exactly with an empty JSON object: {}
- Do not include ellipses, notes, or examples. Only the JSON object is allowed.

Format: Return a JSON object with framework field names as keys and enhanced values.
        """
    ),

    'ar': (
        """
أنت خبير متخصص في هندسة الأوامر. مهمتك تحويل المدخلات الخام والغير مكتملة من المستخدمين
إلى أوامر احترافية منظمة وجاهزة لمساعدات الذكاء الاصطناعي.

عند إعطاؤك مدخلات المستخدم، يجب عليك:
1. تحديد أي حقل من حقول الإطار ينتمي إليه كل مدخل
2. ملء الحقول المفقودة بذكاء بناءً على السياق
3. توسيع المدخلات الغامضة إلى تعليمات محددة وقابلة للتنفيذ
4. الحفاظ على القصد الأصلي للمستخدم مع تحسين الوضوح

مهم (التزم حرفياً):
- أعِد كائن JSON واحد فقط ولا تُدرج أي نص توضيحي أو عناوين أو تنسيقات Markdown.
- يجب أن يبدأ كائن JSON بـ '{' وينتهي بـ '}' ويحتوي فقط على أسماء حقول الإطار كمفاتيح.
- إن لم تستطع توليد قيمة لحقل ما، أعد سلسلة فارغة لذلك المفتاح.

قواعد صارمة للخروج (هامة جداً):
- يجب أن تكون استجابتك كائن JSON واحد صحيح وحسب — لا تعليقات ولا أقسام إضافية.
- إذا لم تستطع توليد JSON صالح لأي سبب، أعد الاستجابة بالضبط كائن JSON فارغ: {}
- لا تضف حروف زائدة أو تفسيرات أو أمثلة. فقط كائن JSON.

الصيغة: أرجع كائن JSON به أسماء حقول الإطار كمفاتيح والقيم المحسّنة.
        """
    ),

    'eg': (
        """
أنت خبير في فن كتابة الأوامر. الشغلة اللي بتعملها إنك تاخد المدخلات الخام من المستخدم
وتحولها لأوامر احترافية جاهزة للذكاء الاصطناعي.

عند ما تتعطى مدخلات المستخدم، لازم:
1. تشوف كل مدخل ده بتاع حقل إيه من حقول الإطار
2. تملي الحقول الناقصة بذكاء من السياق
3. تاخد المدخلات الغامضة وتكتبها بشكل واضح ومحدد
4. تحافظ على قصد المستخدم وتحسن الكلام

هام (مراعاة حرفية):
- رجّع كائن JSON واحد فقط ومفيش أي كلام تاني، ولا عناوين ولا Markdown.
- لازم يبدأ بـ '{' وينتهي بـ '}' ويحط بس أسماء الحقول كمفاتيح.
- لو مش قادر تدي قيمة لحقل سيبها "" (سلسلة فاضية).

قواعد خروج صارمة (مهمة جدًا):
- لازم الاستجابة تبقى كائن JSON واحد صحيح وبس — مفيش أي كلام تاني.
- لو مقدرتش تطلع JSON صالح لأي سبب، رجّع بالظبط كائن JSON فاضي: {}
- مفيش نقاط، ولا شروحات، ولا fences — بس كائن JSON.

الصيغة: أرجع كائن JSON به أسماء الحقول والقيم المحسّنة.
        """
    ),
}

# ==============================================================================
# INITIALIZATION
# ==============================================================================

def init_gemini_api(api_key: str = None) -> bool:
    """
    # init_gemini_api(api_key) — Initialize Google Gemini API
    #
    # Purpose: Set up Google Gemini authentication for prompt enhancement
    # 
    # Parameters:
    #   - api_key (str): Google Gemini API key
    #   - If None: looks for GOOGLE_GENAI_API_KEY environment variable
    #
    # Returns:
    #   - bool: True if API initialized successfully, False otherwise
    #
    # How to get API key:
    #   1. Go to: https://ai.google.dev/apikey
    #   2. Click "Get API Key" → "Create API Key in new project"
    #   3. Copy the key and set GOOGLE_GENAI_API_KEY environment variable
    #   4. Or pass directly: init_gemini_api("your_key_here")
    #
    # Notes:
    #   - Free tier: 60 requests per minute (very generous!)
    #   - No credit card required
    #   - API key should be kept secret
    """
    if not GENAI_AVAILABLE:
        return False
    
    # Step 1: Get API key from parameter, environment, or Streamlit secrets
    key = api_key or os.getenv('GOOGLE_GENAI_API_KEY')

    # If running inside Streamlit and user put the key into Streamlit Secrets,
    # prefer that value (useful for Streamlit Cloud deployments).
    if not key:
        try:
            # Import locally to avoid requiring Streamlit for non-UI contexts
            import streamlit as _st
            # Streamlit stores secrets as a dict-like object
            key = _st.secrets.get('GOOGLE_GENAI_API_KEY') or _st.secrets.get('google_genai_api_key')
        except Exception:
            # If Streamlit isn't available or no secret is present, continue
            key = key
    
    # Step 2: If no key provided, return False
    if not key:
        return False
    
    # Step 3: Configure Genai with API key
    try:
        genai.configure(api_key=key)
        return True
    except Exception as e:
        # Step 4: Log error and return False on failure
        print(f"Error initializing Gemini API: {e}")
        return False


def _probe_model(candidate: str) -> bool:
    """Try a minimal call to the model to confirm it supports generate_content.

    Returns True if the probe succeeds (no model-not-found or unsupported-method errors).
    This uses a very small prompt to minimize cost and side effects.
    """
    global SELECTED_MODEL
    if not GENAI_AVAILABLE:
        return False

    try:
        model = genai.GenerativeModel(candidate)
        # Minimal harmless prompt
        response = model.generate_content(contents=[{'role': 'user', 'parts': [{'text': 'Hello'}]}])
        # If we get text back, assume it worked
        if getattr(response, 'text', None):
            SELECTED_MODEL = candidate
            return True
        return False
    except Exception:
        return False


def get_working_model() -> str:
    """Return a working model name, probing candidates if needed.

    Caches the successful model in `SELECTED_MODEL`.
    """
    global SELECTED_MODEL
    if SELECTED_MODEL:
        return SELECTED_MODEL

    # Try default first
    candidates = [MODEL_NAME] + [c for c in MODEL_CANDIDATES if c != MODEL_NAME]
    for cand in candidates:
        if _probe_model(cand):
            return SELECTED_MODEL

    # If none worked, leave SELECTED_MODEL as None and return default for best-effort
    return MODEL_NAME


def list_available_models() -> dict:
    """Attempt multiple SDK calls to retrieve a list of available models.

    Returns a dict with either {'models': [...]} or {'error': '...'}.
    This tries several likely method names across genai SDK versions to be maximally compatible.
    """
    if not GENAI_AVAILABLE:
        return {'error': 'Generative AI SDK not installed'}

    try_methods = [
        lambda: genai.list_models(),
        lambda: genai.get_models(),
        # Some SDK variants expose models under genai.models.list()
        lambda: getattr(genai, 'models').list(),
    ]

    for fn in try_methods:
        try:
            raw = fn()
            models = []
            # Normalize different return types
            if isinstance(raw, dict):
                # e.g. {'models': [...]}
                for k in ('models', 'data'):
                    if k in raw and isinstance(raw[k], (list, tuple)):
                        for m in raw[k]:
                            try:
                                models.append(m.get('name') or m.get('id') or str(m))
                            except Exception:
                                models.append(str(m))
                        break
            elif isinstance(raw, (list, tuple)):
                for m in raw:
                    try:
                        models.append(m.get('name') or m.get('id') or str(m))
                    except Exception:
                        models.append(str(m))
            else:
                # Try to iterate attributes
                try:
                    for m in raw:
                        models.append(getattr(m, 'name', getattr(m, 'id', str(m))))
                except Exception:
                    models.append(str(raw))

            # Deduplicate and return first 50
            seen = []
            for x in models:
                if x not in seen:
                    seen.append(x)
            return {'models': seen[:50]}
        except Exception:
            continue

    return {'error': 'Could not list models with available SDK methods'}


def set_selected_model(name: str) -> None:
    """Force the enhancer to use the given model name for subsequent calls."""
    global SELECTED_MODEL
    SELECTED_MODEL = name


# ==============================================================================
# PROMPT ENHANCEMENT
# ==============================================================================

def enhance_prompt_with_ai(
    user_input: str,
    framework: str,
    lang: str = 'en'
) -> Tuple[bool, dict]:
    """
    # enhance_prompt_with_ai(user_input, framework, lang) — Enhance user input with AI
    #
    # Purpose: Use Gemini to intelligently fill in missing framework fields
    # based on user's rough input
    #
    # Parameters:
    #   - user_input (str): Raw user input (can be incomplete/vague)
    #   - framework (str): Target framework ('ICDF', 'RCR-EOC', 'MICRO', 'COSTAR')
    #   - lang (str): Language for enhancement ('en', 'ar', 'eg')
    #
    # Returns:
    #   - tuple: (success: bool, result: dict or None)
    #   - Success: (True, {field_name: enhanced_value, ...})
    #   - Failure: (False, {}) — returns original input unchanged
    #
    # Example:
    #   success, result = enhance_prompt_with_ai(
    #       user_input="Write about climate change",
    #       framework="ICDF",
    #       lang="en"
    #   )
    #   if success:
    #       print(result['Instruction'])  # Enhanced instruction
    #       print(result['Context'])       # AI-generated context
    #       print(result['Data'])          # AI-generated data
    #       print(result['Format'])        # AI-generated format
    #
    # Features:
    #   - Intelligently infers missing fields from user intent
    #   - Expands vague inputs into specific, actionable tasks
    #   - Maintains original language throughout
    #   - Falls back to user input if API fails
    #   - Rate limited by Gemini free tier (60 req/min)
    #
    # Notes:
    #   - Requires GOOGLE_GENAI_API_KEY environment variable
    #   - Free tier included (no payment required)
    #   - Fallback: returns empty dict if API unavailable
    """
    # Step 1: Check if Genai is available
    if not GENAI_AVAILABLE:
        return False, {}
    
    # Step 2: Get appropriate system prompt for language
    system_prompt = ENHANCEMENT_PROMPTS.get(lang, ENHANCEMENT_PROMPTS['en'])
    
    # Step 3: Build user message with framework context
    framework_fields = {
        'ICDF': ['Instruction', 'Context', 'Data', 'Format'],
        'RCR-EOC': ['Role', 'Context', 'Request', 'Examples', 'Output', 'Constraints'],
        'MICRO': ['Message', 'Intention', 'Context', 'Rhythm', 'Output'],
        'COSTAR': ['Context', 'Offer', 'Style', 'Target', 'Action', 'Result']
    }
    
    # Step 4: Get fields for this framework (default to ICDF if not found)
    fields = framework_fields.get(framework, framework_fields['ICDF'])
    
    # Step 5: Build the prompt for Genai
    user_message = f"""Framework: {framework}
Framework fields: {', '.join(fields)}
Raw user input: {user_input}

Please enhance this input by filling in all {framework} framework fields 
based on the user's intent. Return ONLY valid JSON with the framework fields."""
    
    # Step 6: Call Gemini API
    try:
        # Use a working model (probed/cached) to avoid model-not-found errors
        working_model = get_working_model()
        model = genai.GenerativeModel(working_model)
        response = model.generate_content(
            contents=[
                {'role': 'user', 'parts': [{'text': system_prompt}]},
                {'role': 'model', 'parts': [{'text': 'I understand. I will enhance prompts by filling in missing framework fields intelligfully.'}]},
                {'role': 'user', 'parts': [{'text': user_message}]}
            ]
        )
        
        # Step 7: Parse the response
        response_text = getattr(response, 'text', str(response))

        # Helper: try to load JSON safely from string
        def try_load(s: str):
            try:
                return json.loads(s)
            except Exception:
                return None

        # 1) Look for fenced JSON blocks ```json ... ``` or ``` ... ```
        m = re.search(r'```\s*json\s*(.*?)```', response_text, re.S | re.I)
        if not m:
            m = re.search(r'```(.*?)```', response_text, re.S)
        if m:
            candidate = m.group(1).strip()
            parsed = try_load(candidate)
            if parsed is not None:
                return True, parsed

        # 2) Try a naive first/last brace extraction, with cleaning of control chars
        # Remove problematic non-printable control characters except common whitespace (\n, \t, \r)
        cleaned = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f]', '', response_text)

        # Find all balanced JSON objects by scanning braces
        def find_json_objects(s: str):
            objs = []
            stack = 0
            start = None
            for i, ch in enumerate(s):
                if ch == '{':
                    if stack == 0:
                        start = i
                    stack += 1
                elif ch == '}' and stack > 0:
                    stack -= 1
                    if stack == 0 and start is not None:
                        objs.append(s[start:i+1])
                        start = None
            return objs

        candidates = find_json_objects(cleaned)
        for cand in candidates:
            parsed = try_load(cand)
            if parsed is not None:
                return True, parsed

        # 3) Last resort: try the simple first { .. last } slice on cleaned text
        jstart = cleaned.find('{')
        jend = cleaned.rfind('}')
        if jstart != -1 and jend != -1 and jend > jstart:
            maybe = cleaned[jstart:jend+1]
            parsed = try_load(maybe)
            if parsed is not None:
                return True, parsed

        # Nothing parsed — return failure with rich diagnostics for diagnosis
        diagnostic = {
            '_error': 'Failed to parse JSON from model response',
            '_raw_response': response_text[:2000],
            '_candidates_found': len(candidates) if 'candidates' in locals() else 0,
            '_cleaned_preview': cleaned[:1200] if 'cleaned' in locals() else None,
            '_response_repr': repr(response) if 'response' in locals() else None,
            '_response_type': type(response).__name__ if 'response' in locals() else None,
        }
        return False, diagnostic
            
    except Exception as e:
        # Step 11: Return failure with error details so UI can show useful diagnostics
        err = str(e)
        diagnostic = {
            '_error': f'Exception during AI call: {err}',
            '_traceback': traceback.format_exc(),
            '_response_repr': repr(response) if 'response' in locals() else None,
            '_response_type': type(response).__name__ if 'response' in locals() else None,
        }

        # If the error indicates the model is not found / unsupported, try to list available models
        try:
            # genai may provide a listing function; call it if available to help diagnose
            if 'genai' in globals() and hasattr(genai, 'list_models'):
                models = genai.list_models()
                # models may be a list of dict-like objects; extract ids/names
                model_ids = []
                for m in models:
                    try:
                        model_ids.append(m.get('name') or m.get('id') or str(m))
                    except Exception:
                        model_ids.append(str(m))
                diagnostic['_available_models'] = model_ids[:20]
            elif 'genai' in globals() and hasattr(genai, 'get_models'):
                models = genai.get_models()
                model_ids = [getattr(m, 'name', str(m)) for m in models]
                diagnostic['_available_models'] = model_ids[:20]
        except Exception:
            # Ignore any failures when attempting to list models — return original diagnostic
            pass

        return False, diagnostic


# ==============================================================================
# FIELD SUGGESTION
# ==============================================================================

def suggest_missing_fields(
    filled_fields: dict,
    framework: str,
    lang: str = 'en'
) -> dict:
    """
    # suggest_missing_fields(filled_fields, framework, lang) — Suggest values for empty fields
    #
    # Purpose: Use AI to suggest values for fields the user hasn't filled in
    #
    # Parameters:
    #   - filled_fields (dict): {field_name: user_value, ...}
    #   - framework (str): Target framework
    #   - lang (str): Language for suggestions
    #
    # Returns:
    #   - dict: {empty_field_name: suggested_value, ...}
    #
    # Example:
    #   suggestions = suggest_missing_fields(
    #       filled_fields={'Instruction': 'Write about AI'},
    #       framework='ICDF',
    #       lang='en'
    #   )
    #   # Returns: {'Context': 'For blog readers...', 'Data': '...', 'Format': '...'}
    """
    if not GENAI_AVAILABLE:
        return {}
    
    # Step 1: Build filled fields summary
    filled_summary = "\n".join([f"- {k}: {v}" for k, v in filled_fields.items() if v])
    
    # Step 2: Get system prompt
    system_prompt = ENHANCEMENT_PROMPTS.get(lang, ENHANCEMENT_PROMPTS['en'])
    
    # Step 3: Build request
    user_message = f"""Framework: {framework}
Filled fields:
{filled_summary}

Suggest values for the empty fields to complete this {framework} prompt. 
Return ONLY JSON with field names and suggested values."""
    
    # Step 4: Call API and return suggestions
    try:
        working_model = get_working_model()
        model = genai.GenerativeModel(working_model)
        response = model.generate_content(user_message)
        
        # Step 5: Parse JSON from response
        json_start = response.text.find('{')
        json_end = response.text.rfind('}') + 1
        if json_start >= 0 and json_end > json_start:
            return json.loads(response.text[json_start:json_end])
        return {}
    except Exception as e:
        print(f"Error suggesting fields: {e}")
        return {}
