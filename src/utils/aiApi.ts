/**
 * Unified AI API - Supports multiple AI providers
 */

import axios from 'axios';
import type { AIProvider, AISettings } from '@/types/aiProvider';
import type { Framework, Language } from '@/types/prompti';
import { FRAMEWORK_DEFINITIONS } from '@/data/translations';

/**
 * Generate AI-enhanced prompt using the selected provider
 */
export async function generatePromptWithAI(
  framework: Framework,
  language: string,
  fieldValues: Record<string, string>,
  settings: AISettings
): Promise<string> {
  const { provider, apiKey, model } = settings;

  if (!apiKey || !apiKey.trim()) {
    throw new Error(`Please provide your ${provider.toUpperCase()} API key in the AI Settings.`);
  }

  // Build the prompt based on framework
  const lang = language as Language;
  const frameworkDef = FRAMEWORK_DEFINITIONS[lang][framework];
  const fieldDescriptions = Object.entries(fieldValues)
    .filter(([_, value]) => value && value.trim())
    .map(([key, value]) => `${key}: ${value}`)
    .join('\n');

  const systemPrompt = `You are an expert prompt engineer. Your task is to transform user inputs into a well-structured, professional prompt following the ${framework.toUpperCase()} framework.

Framework: ${framework.toUpperCase()}
Structure: ${frameworkDef.fields.map(f => f.key).join(', ')}

User's inputs:
${fieldDescriptions}

Generate an optimized prompt that an AI system can understand and respond to effectively. Return ONLY the final prompt text, without any explanations or meta-commentary.`;

  // Route to appropriate provider
  switch (provider) {
    case 'groq':
      return generateWithGroq(systemPrompt, apiKey, model);
    case 'openrouter':
      return generateWithOpenRouter(systemPrompt, apiKey, model);
    case 'gemini':
      return generateWithGemini(systemPrompt, apiKey, model);
    case 'huggingface':
      return generateWithHuggingFace(systemPrompt, apiKey, model);
    case 'cohere':
      return generateWithCohere(systemPrompt, apiKey, model);
    default:
      throw new Error(`Unsupported AI provider: ${provider}`);
  }
}

/**
 * Groq API Integration
 */
async function generateWithGroq(prompt: string, apiKey: string, model: string): Promise<string> {
  try {
    console.log(`🚀 Groq: Using model ${model}`);
    
    const response = await axios.post(
      'https://api.groq.com/openai/v1/chat/completions',
      {
        model,
        messages: [
          { role: 'user', content: prompt }
        ],
        temperature: 0.7,
        max_tokens: 2048
      },
      {
        headers: {
          'Authorization': `Bearer ${apiKey}`,
          'Content-Type': 'application/json'
        }
      }
    );

    const result = response.data.choices[0]?.message?.content;
    if (!result) {
      throw new Error('No response from Groq API');
    }

    console.log('✅ Groq: Success');
    return result.trim();
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const status = error.response?.status;
      const message = error.response?.data?.error?.message || error.message;
      
      if (status === 401) {
        throw new Error('Invalid Groq API key. Please check your API key.');
      }
      if (status === 429) {
        throw new Error('Groq rate limit exceeded. Please wait a moment and try again.');
      }
      throw new Error(`Groq API error: ${message}`);
    }
    throw error;
  }
}

/**
 * OpenRouter API Integration
 */
async function generateWithOpenRouter(prompt: string, apiKey: string, model: string): Promise<string> {
  try {
    console.log(`🚀 OpenRouter: Using model ${model}`);
    
    const response = await axios.post(
      'https://openrouter.ai/api/v1/chat/completions',
      {
        model,
        messages: [
          { role: 'user', content: prompt }
        ],
        temperature: 0.7,
        max_tokens: 2048
      },
      {
        headers: {
          'Authorization': `Bearer ${apiKey}`,
          'Content-Type': 'application/json',
          'HTTP-Referer': window.location.origin,
          'X-Title': 'Prompti'
        }
      }
    );

    const result = response.data.choices[0]?.message?.content;
    if (!result) {
      throw new Error('No response from OpenRouter API');
    }

    console.log('✅ OpenRouter: Success');
    return result.trim();
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const status = error.response?.status;
      const message = error.response?.data?.error?.message || error.message;
      
      if (status === 401) {
        throw new Error('Invalid OpenRouter API key. Please check your API key.');
      }
      if (status === 429) {
        throw new Error('OpenRouter rate limit exceeded. Please wait a moment and try again.');
      }
      throw new Error(`OpenRouter API error: ${message}`);
    }
    throw error;
  }
}

/**
 * Google Gemini API Integration
 */
async function generateWithGemini(prompt: string, apiKey: string, model: string): Promise<string> {
  try {
    console.log(`🚀 Gemini: Using model ${model}`);
    
    const response = await axios.post(
      `https://generativelanguage.googleapis.com/v1/models/${model}:generateContent?key=${apiKey}`,
      {
        contents: [{
          parts: [{
            text: prompt
          }]
        }],
        generationConfig: {
          temperature: 0.7,
          maxOutputTokens: 2048
        }
      },
      {
        headers: {
          'Content-Type': 'application/json'
        }
      }
    );

    const result = response.data.candidates?.[0]?.content?.parts?.[0]?.text;
    if (!result) {
      throw new Error('No response from Gemini API');
    }

    console.log('✅ Gemini: Success');
    return result.trim();
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const status = error.response?.status;
      const message = error.response?.data?.error?.message || error.message;
      
      if (status === 400 || status === 404) {
        throw new Error(`Gemini model "${model}" not available. Try a different model.`);
      }
      if (status === 429) {
        throw new Error('Gemini rate limit exceeded. Please wait a moment and try again.');
      }
      throw new Error(`Gemini API error: ${message}`);
    }
    throw error;
  }
}

/**
 * Hugging Face API Integration
 */
async function generateWithHuggingFace(prompt: string, apiKey: string, model: string): Promise<string> {
  try {
    console.log(`🚀 Hugging Face: Using model ${model}`);
    
    const response = await axios.post(
      `https://api-inference.huggingface.co/models/${model}`,
      {
        inputs: prompt,
        parameters: {
          max_new_tokens: 2048,
          temperature: 0.7,
          return_full_text: false
        }
      },
      {
        headers: {
          'Authorization': `Bearer ${apiKey}`,
          'Content-Type': 'application/json'
        }
      }
    );

    let result: string;
    if (Array.isArray(response.data)) {
      result = response.data[0]?.generated_text || response.data[0]?.text;
    } else {
      result = response.data.generated_text || response.data.text;
    }

    if (!result) {
      throw new Error('No response from Hugging Face API');
    }

    console.log('✅ Hugging Face: Success');
    return result.trim();
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const status = error.response?.status;
      const message = error.response?.data?.error || error.message;
      
      if (status === 401) {
        throw new Error('Invalid Hugging Face token. Please check your token.');
      }
      if (status === 503) {
        throw new Error('Model is loading. Please wait a moment and try again.');
      }
      throw new Error(`Hugging Face API error: ${message}`);
    }
    throw error;
  }
}

/**
 * Cohere API Integration
 */
async function generateWithCohere(prompt: string, apiKey: string, model: string): Promise<string> {
  try {
    console.log(`🚀 Cohere: Using model ${model}`);
    
    const response = await axios.post(
      'https://api.cohere.ai/v1/generate',
      {
        model,
        prompt,
        max_tokens: 2048,
        temperature: 0.7,
        stop_sequences: []
      },
      {
        headers: {
          'Authorization': `Bearer ${apiKey}`,
          'Content-Type': 'application/json'
        }
      }
    );

    const result = response.data.generations?.[0]?.text;
    if (!result) {
      throw new Error('No response from Cohere API');
    }

    console.log('✅ Cohere: Success');
    return result.trim();
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const status = error.response?.status;
      const message = error.response?.data?.message || error.message;
      
      if (status === 401) {
        throw new Error('Invalid Cohere API key. Please check your API key.');
      }
      if (status === 429) {
        throw new Error('Cohere rate limit exceeded. Please wait a moment and try again.');
      }
      throw new Error(`Cohere API error: ${message}`);
    }
    throw error;
  }
}
