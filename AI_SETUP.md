# AI SETUP GUIDE - Get Google Gemini API Key & Test

## ⚡ Quick Setup (6 minutes)

### Step 1: Get Free Google Gemini API Key (2 min)

1. **Visit**: https://ai.google.dev/apikey
2. **Click**: "Get API Key" button
3. **Select**: "Create API Key in new project"
4. **Copy**: Your new API key (long string like `AIzaS...`)
5. **Keep it safe**: Don't share this key publicly

---

### Step 2: Set Environment Variable (1 min)

**Option A - For This Session Only:**
```bash
export GOOGLE_GENAI_API_KEY="paste_your_key_here"
```

Then restart Streamlit:
```bash
cd "/home/motaz/WebProjects/Prompti - Structured Prompt Generator"
streamlit run app.py
```

**Option B - Permanently (Linux/Mac):**
```bash
echo 'export GOOGLE_GENAI_API_KEY="paste_your_key_here"' >> ~/.bashrc
source ~/.bashrc
```

**Option C - Permanently (Windows):**
```powershell
[Environment]::SetEnvironmentVariable("GOOGLE_GENAI_API_KEY", "paste_your_key_here", "User")
# Then restart PowerShell
```

---

### Step 3: Install Google Gemini Package (2 min)

```bash
pip install google-generativeai
```

---

### Step 4: Test It! (1 min)

1. Open your Streamlit app
2. Fill in the **Instruction** field with something simple:
   ```
   Write a blog post about AI
   ```
3. Click the **"✨ AI"** button (4th button in the action row)
4. Watch it enhance your prompt! 🎉

---

## ✅ What You Should See

### Before clicking AI:
```
Instruction: Write a blog post about AI
Context: [empty]
Data: [empty]
Format: [empty]
```

### After clicking AI:
```
Instruction: Write a compelling blog post exploring the 
            latest developments in artificial intelligence

Context: For tech enthusiasts and business professionals 
        interested in AI trends and applications

Data: Include recent breakthroughs in large language models, 
     AI ethics, and practical business use cases

Format: 3-4 engaging paragraphs, 600-800 words, 
       conversational yet informative tone
```

---

## 🆘 Troubleshooting

### Button shows warning "API key not configured"
**Solution**: 
1. Check you set the environment variable correctly
2. Restart Streamlit: `Ctrl+C` then `streamlit run app.py`
3. Verify key set: In terminal, type `echo $GOOGLE_GENAI_API_KEY` (should show your key)

### Error: "google.generativeai could not be imported"
**Solution**:
```bash
pip install google-generativeai
```

### AI button shows "Using your input as-is"
**Possible causes**:
1. API key not valid (check at https://ai.google.dev/apikey)
2. Rate limit reached (60 per minute is generous, but possible)
3. API error (temporary - try again in 30 seconds)

### App looks slow when clicking AI
**Normal!** It's calling Google's API. Usually takes 3-10 seconds. Watch the spinner! ⏳

---

## 🎯 Now What?

### You can:

1. **Use AI to enhance prompts** ✨
   - Click "✨ AI" button to improve any prompt
   - AI fills missing fields automatically
   - Works in 3 languages!

2. **Edit fields manually** ✏️
   - After AI enhancement, edit any field you want
   - Create exactly what you need

3. **Generate final prompt** 📝
   - Click "Generate Prompt" to create final prompt
   - Copy to clipboard (fixed!) or download

4. **Share with ChatGPT/Claude** 🚀
   - Your prompt is now professional and complete
   - Use it in any AI chatbot!

---

## 💡 Pro Tips

### Tip 1: Start with rough ideas
```
DON'T worry about perfect wording
AI will polish it for you
Just give it something to work with
```

### Tip 2: AI enhances based on framework
```
Different frameworks = different enhancement
ICDF → focuses on data + structure
RCR-EOC → focuses on role + examples
MICRO → focuses on tone + rhythm
COSTAR → focuses on offer + target
```

### Tip 3: Multi-language support
```
English → Professional, formal language
العربية → Modern Standard Arabic
مصرّي → Egyptian colloquial, fun tone
```

### Tip 4: You can always edit
```
AI suggestion not perfect?
Edit any field!
AI is a helper, not the final word
```

---

## 📊 Pricing Reminder

| Plan | Cost | Requests/min | Best for |
|------|------|-------------|---------|
| Google Gemini Free | **FREE** ✓ | 60 | You! |
| OpenAI $0.50/M tokens | Paid | Unlimited | Production |
| Claude API $3/M tokens | Paid | Higher | Enterprise |

**You chose the best option: FREE with Google Gemini!** 🎉

---

## 🚀 Ready?

Your API key is your 30-second ticket to AI-powered prompts!

Get it now: https://ai.google.dev/apikey

Then come back and test the "✨ AI" button! 👇
