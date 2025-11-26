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
MODEL_NAME = "gemini-1.5-flash"

# Step 2b: System prompts for prompt enhancement (in multiple languages)
ENHANCEMENT_PROMPTS = {
    'en': """You are an expert prompt engineer. Your job is to take raw, incomplete user inputs 
and transform them into professional, well-structured prompts ready for AI assistants.

When given user input, you should:
1. Identify which framework field each input belongs to
2. Fill in missing fields intelligently based on context
3. Expand vague inputs into specific, actionable instructions
4. Maintain the user's original intent while improving clarity
5. Return ONLY the enhanced field values as JSON (no explanations)

Format: Return a JSON object with framework field names as keys and enhanced values.""",

    'ar': """أنت خبير متخصص في هندسة الأوامر. مهمتك تحويل المدخلات الخام والغير مكتملة من المستخدمين 
إلى أوامر احترافية منظمة وجاهزة لمساعدات الذكاء الاصطناعي.

عند إعطاؤك مدخلات المستخدم، يجب عليك:
1. تحديد أي حقل من حقول الإطار ينتمي إليه كل مدخل
2. ملء الحقول المفقودة بذكاء بناءً على السياق
3. توسيع المدخلات الغامضة إلى تعليمات محددة وقابلة للتنفيذ
4. الحفاظ على القصد الأصلي للمستخدم مع تحسين الوضوح
5. أرجع ONLY القيم المحسّنة كـ JSON (بدون شروحات)

الصيغة: أرجع كائن JSON به أسماء حقول الإطار كمفاتيح والقيم المحسّنة.""",

    'eg': """أنت خبير في فن كتابة الأوامر. الشغلة اللي بتعملها إنك تاخد المدخلات الخام من المستخدم 
وتحولها لأوامر احترافية جاهزة للذكاء الاصطناعي.

عند ما تتعطى مدخلات المستخدم، لازم:
1. تشوف كل مدخل ده بتاع حقل إيه من حقول الإطار
2. تملي الحقول الناقصة بذكاء من السياق
3. تاخد المدخلات الغامضة وتكتبها بشكل واضح ومحدد
4. تحافظ على قصد المستخدم وتحسن الكلام
5. أرجع قيم محسّنة بس كـ JSON (بدون شروح)

الصيغة: أرجع كائن JSON به أسماء الحقول والقيم المحسّنة."""
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
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(
            contents=[
                {'role': 'user', 'parts': [{'text': system_prompt}]},
                {'role': 'model', 'parts': [{'text': 'I understand. I will enhance prompts by filling in missing framework fields intelligfully.'}]},
                {'role': 'user', 'parts': [{'text': user_message}]}
            ]
        )
        
        # Step 7: Parse the response
        response_text = response.text
        
        # Step 8: Extract JSON from response
        # (Genai might include markdown or explanation, so we need to extract JSON)
        json_start = response_text.find('{')
        json_end = response_text.rfind('}') + 1
        
        # Step 9: If JSON found, try to parse it
        if json_start >= 0 and json_end > json_start:
            json_str = response_text[json_start:json_end]
            result = json.loads(json_str)
            return True, result
        else:
            # Step 10: If no JSON found, return failure
            return False, {}
            
    except Exception as e:
        # Step 11: Log error and return failure
        print(f"Error enhancing prompt with AI: {e}")
        return False, {}


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
        model = genai.GenerativeModel(MODEL_NAME)
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
