import axios from 'axios';
import type { Language, Framework, FieldValues } from '@/types/prompti';
import { FRAMEWORK_DEFINITIONS } from '@/data/translations';

const GEMINI_API_KEY = import.meta.env.VITE_GEMINI_API_KEY;

// List of FREE models only (no Pro models to avoid access issues)
// Ordered by likelihood of availability
const GEMINI_MODELS = [
  'gemini-1.5-flash',               // Most stable free model
  'gemini-1.5-flash-8b',            // Lightweight free model
  'gemini-1.5-flash-latest',        // Latest free flash
  'gemini-pro',                     // Legacy free model
  'gemini-1.0-pro-latest',          // Legacy with latest tag
  'gemini-1.0-pro'                  // Oldest legacy
];

// Try v1 API first, then v1beta
const API_VERSIONS = ['v1', 'v1beta'];

interface GeminiResponse {
  candidates: Array<{
    content: {
      parts: Array<{
        text: string;
      }>;
    };
  }>;
}

async function tryGenerateWithModel(
  modelName: string,
  apiVersion: string,
  systemPrompt: string
): Promise<string> {
  const url = `https://generativelanguage.googleapis.com/${apiVersion}/models/${modelName}:generateContent?key=${GEMINI_API_KEY}`;
  
  const response = await axios.post<GeminiResponse>(
    url,
    {
      contents: [
        {
          parts: [
            {
              text: systemPrompt
            }
          ]
        }
      ],
      generationConfig: {
        temperature: 0.7,
        topK: 40,
        topP: 0.95,
        maxOutputTokens: 2048,
      },
      safetySettings: [
        {
          category: 'HARM_CATEGORY_HARASSMENT',
          threshold: 'BLOCK_MEDIUM_AND_ABOVE'
        },
        {
          category: 'HARM_CATEGORY_HATE_SPEECH',
          threshold: 'BLOCK_MEDIUM_AND_ABOVE'
        },
        {
          category: 'HARM_CATEGORY_SEXUALLY_EXPLICIT',
          threshold: 'BLOCK_MEDIUM_AND_ABOVE'
        },
        {
          category: 'HARM_CATEGORY_DANGEROUS_CONTENT',
          threshold: 'BLOCK_MEDIUM_AND_ABOVE'
        }
      ]
    },
    {
      headers: {
        'Content-Type': 'application/json'
      }
    }
  );

  const generatedText = response.data.candidates?.[0]?.content?.parts?.[0]?.text;
  
  if (!generatedText) {
    throw new Error('No response generated from AI.');
  }

  return generatedText.trim();
}

export async function generatePromptWithAI(
  language: Language,
  framework: Framework,
  fieldValues: FieldValues
): Promise<string> {
  if (!GEMINI_API_KEY) {
    throw new Error('Gemini API key is not configured. Please add VITE_GEMINI_API_KEY to your .env file.');
  }

  const definition = FRAMEWORK_DEFINITIONS[language][framework];
  
  // Build the context for AI generation
  const fieldDescriptions = definition.fields
    .map((field) => {
      const value = fieldValues[field.key]?.trim() || '';
      if (!value) return null;
      return `${field.label}: ${value}`;
    })
    .filter(Boolean)
    .join('\n\n');

  if (!fieldDescriptions) {
    throw new Error('Please fill in at least one field before generating with AI.');
  }

  // Create the prompt for Gemini
  const systemPrompt = `You are an expert AI prompt engineer. Your task is to take the user's input fields and create an optimized, professional prompt that will work effectively with AI systems.

The user is using the ${framework} framework, which has these sections: ${definition.sections.join(', ')}.

Based on the user's inputs below, generate an enhanced, well-structured prompt that:
1. Maintains the core intent and information from the user's inputs
2. Improves clarity and specificity
3. Adds helpful context where appropriate
4. Structures the information in a way that will get better AI responses
5. Uses professional language and clear formatting
6. Follows the ${framework} framework structure

User's inputs:
${fieldDescriptions}

Generate an optimized prompt that an AI system can understand and respond to effectively. Return ONLY the final prompt text, without any explanations or meta-commentary.`;

  // Try models in order until one works
  let lastError: Error | null = null;
  let rateLimitCount = 0;
  
  for (const apiVersion of API_VERSIONS) {
    for (const model of GEMINI_MODELS) {
      try {
        console.log(`Trying model: ${model} with API version: ${apiVersion}`);
        const result = await tryGenerateWithModel(model, apiVersion, systemPrompt);
        console.log(`✅ Success with model: ${model} (${apiVersion})`);
        return result;
      } catch (error) {
        if (axios.isAxiosError(error)) {
          const status = error.response?.status;
          const errorMessage = error.response?.data?.error?.message || '';
          
          // If it's a "not found" error, try next model
          if (status === 404 || errorMessage.includes('not found') || errorMessage.includes('not supported')) {
            console.log(`❌ Model ${model} not available, trying next...`);
            lastError = new Error(`Model ${model} not available`);
            continue;
          }
          
          // Rate limit - count and continue to try other models
          if (status === 429) {
            console.log(`⚠️  Rate limited on ${model}, trying next model...`);
            rateLimitCount++;
            lastError = new Error('Rate limit exceeded');
            continue;
          }
          
          // For auth errors, throw immediately
          if (status === 403) {
            throw new Error('API key is invalid or has insufficient permissions. Please check your API key at https://makersuite.google.com/app/apikey');
          }
          
          // For bad request, try next model (might be model-specific)
          if (status === 400) {
            console.log(`⚠️  Bad request on ${model}, trying next model...`);
            lastError = new Error('Invalid API request');
            continue;
          }
          
          // Store error and continue
          console.log(`⚠️  Error on ${model}: ${errorMessage}`);
          lastError = error as Error;
        } else {
          lastError = error as Error;
        }
      }
    }
  }
  
  // If we get here, all models failed
  // Provide helpful error message based on what happened
  if (rateLimitCount === GEMINI_MODELS.length * API_VERSIONS.length) {
    throw new Error(
      'All models are currently rate limited. Please wait 60 seconds and try again. ' +
      'Google Gemini has a limit of 60 requests per minute on the free tier.'
    );
  }
  
  throw new Error(
    `Unable to generate AI prompt. All ${GEMINI_MODELS.length} models failed across ${API_VERSIONS.length} API versions. ` +
    `Last error: ${lastError?.message || 'Unknown error'}. ` +
    'Please check your API key and try again later.'
  );
}
