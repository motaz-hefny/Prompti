/**
 * AI Provider Types and Interfaces
 */

export type AIProvider = 'groq' | 'openrouter' | 'gemini' | 'huggingface' | 'cohere';

export interface AIProviderConfig {
  id: AIProvider;
  name: string;
  description: string;
  apiKeyLabel: string;
  apiKeyPlaceholder: string;
  signupUrl: string;
  docsUrl: string;
  freeRequests: string;
  speed: number; // 1-5 rating
  quality: number; // 1-5 rating
  defaultModel: string;
  models: Array<{
    id: string;
    name: string;
    description: string;
  }>;
}

export interface AISettings {
  provider: AIProvider;
  apiKey: string;
  model: string;
}

export const AI_PROVIDERS: Record<AIProvider, AIProviderConfig> = {
  groq: {
    id: 'groq',
    name: 'Groq',
    description: 'Fastest AI inference (10-100x faster). Best free tier.',
    apiKeyLabel: 'Groq API Key',
    apiKeyPlaceholder: 'gsk_...',
    signupUrl: 'https://console.groq.com/',
    docsUrl: 'https://console.groq.com/docs',
    freeRequests: '14,400/day',
    speed: 5,
    quality: 4,
    defaultModel: 'llama-3.3-70b-versatile',
    models: [
      {
        id: 'llama-3.3-70b-versatile',
        name: 'Llama 3.3 70B',
        description: 'Best balance of speed and quality'
      },
      {
        id: 'llama-3.1-70b-versatile',
        name: 'Llama 3.1 70B',
        description: 'High quality, versatile'
      },
      {
        id: 'mixtral-8x7b-32768',
        name: 'Mixtral 8x7B',
        description: 'Fast and efficient'
      },
      {
        id: 'gemma2-9b-it',
        name: 'Gemma 2 9B',
        description: 'Fastest, good quality'
      }
    ]
  },
  openrouter: {
    id: 'openrouter',
    name: 'OpenRouter',
    description: 'Access to 100+ models. Pay-as-you-go or free tier.',
    apiKeyLabel: 'OpenRouter API Key',
    apiKeyPlaceholder: 'sk-or-v1-...',
    signupUrl: 'https://openrouter.ai/',
    docsUrl: 'https://openrouter.ai/docs',
    freeRequests: 'Varies by model',
    speed: 4,
    quality: 5,
    defaultModel: 'meta-llama/llama-3.1-8b-instruct:free',
    models: [
      {
        id: 'meta-llama/llama-3.1-8b-instruct:free',
        name: 'Llama 3.1 8B (Free)',
        description: 'Free, good quality'
      },
      {
        id: 'google/gemini-flash-1.5',
        name: 'Gemini Flash 1.5',
        description: 'Fast and capable'
      },
      {
        id: 'mistralai/mistral-7b-instruct',
        name: 'Mistral 7B',
        description: 'High quality'
      },
      {
        id: 'anthropic/claude-3-haiku',
        name: 'Claude 3 Haiku',
        description: 'Fast, high quality (paid)'
      }
    ]
  },
  gemini: {
    id: 'gemini',
    name: 'Google Gemini',
    description: 'Google\'s AI models. Free tier available.',
    apiKeyLabel: 'Gemini API Key',
    apiKeyPlaceholder: 'AIza...',
    signupUrl: 'https://makersuite.google.com/app/apikey',
    docsUrl: 'https://ai.google.dev/docs',
    freeRequests: '1,500/day',
    speed: 3,
    quality: 4,
    defaultModel: 'gemini-1.5-flash',
    models: [
      {
        id: 'gemini-1.5-flash',
        name: 'Gemini 1.5 Flash',
        description: 'Fast and efficient'
      },
      {
        id: 'gemini-1.5-flash-8b',
        name: 'Gemini 1.5 Flash 8B',
        description: 'Lightweight and fast'
      },
      {
        id: 'gemini-pro',
        name: 'Gemini Pro',
        description: 'Legacy model'
      }
    ]
  },
  huggingface: {
    id: 'huggingface',
    name: 'Hugging Face',
    description: 'Free unlimited access to open source models.',
    apiKeyLabel: 'Hugging Face Token',
    apiKeyPlaceholder: 'hf_...',
    signupUrl: 'https://huggingface.co/settings/tokens',
    docsUrl: 'https://huggingface.co/docs/api-inference',
    freeRequests: 'Unlimited (rate limited)',
    speed: 3,
    quality: 4,
    defaultModel: 'mistralai/Mistral-7B-Instruct-v0.2',
    models: [
      {
        id: 'mistralai/Mistral-7B-Instruct-v0.2',
        name: 'Mistral 7B Instruct',
        description: 'High quality, versatile'
      },
      {
        id: 'meta-llama/Llama-2-7b-chat-hf',
        name: 'Llama 2 7B Chat',
        description: 'Good for conversations'
      },
      {
        id: 'microsoft/phi-2',
        name: 'Phi-2',
        description: 'Fast and efficient'
      }
    ]
  },
  cohere: {
    id: 'cohere',
    name: 'Cohere',
    description: 'High quality models. Generous free tier.',
    apiKeyLabel: 'Cohere API Key',
    apiKeyPlaceholder: 'co_...',
    signupUrl: 'https://dashboard.cohere.com/api-keys',
    docsUrl: 'https://docs.cohere.com/',
    freeRequests: '10,000/month',
    speed: 4,
    quality: 5,
    defaultModel: 'command-r',
    models: [
      {
        id: 'command-r',
        name: 'Command R',
        description: 'Best for instructions'
      },
      {
        id: 'command-light',
        name: 'Command Light',
        description: 'Faster, lighter'
      },
      {
        id: 'command-nightly',
        name: 'Command Nightly',
        description: 'Latest features'
      }
    ]
  }
};
