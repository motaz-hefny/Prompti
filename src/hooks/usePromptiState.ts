import { useState, useEffect } from 'react';
import type { Language, Framework, FieldValues, SessionState } from '@/types/prompti';

const STORAGE_KEY = 'prompti_session';

const DEFAULT_STATE: SessionState = {
  language: 'en',
  framework: 'ICDF',
  allowBlanks: false,
  fieldValues: {
    'ICDF': {},
    'RCR-EOC': {},
    'MICRO': {},
    'COSTAR': {}
  },
  generatedPrompt: '',
  aiGeneratedPrompt: '',
  slangVariant: 0
};

export function usePromptiState() {
  const [state, setState] = useState<SessionState>(() => {
    try {
      const stored = sessionStorage.getItem(STORAGE_KEY);
      if (stored) {
        return { ...DEFAULT_STATE, ...JSON.parse(stored) };
      }
    } catch (error) {
      console.error('Failed to load session state:', error);
    }
    return DEFAULT_STATE;
  });

  useEffect(() => {
    try {
      sessionStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    } catch (error) {
      console.error('Failed to save session state:', error);
    }
  }, [state]);

  const setLanguage = (language: Language) => {
    setState(prev => ({ ...prev, language }));
  };

  const setFramework = (framework: Framework) => {
    setState(prev => ({ ...prev, framework }));
  };

  const setAllowBlanks = (allowBlanks: boolean) => {
    setState(prev => ({ ...prev, allowBlanks }));
  };

  const setFieldValue = (framework: Framework, key: string, value: string) => {
    setState(prev => ({
      ...prev,
      fieldValues: {
        ...prev.fieldValues,
        [framework]: {
          ...prev.fieldValues[framework],
          [key]: value
        }
      }
    }));
  };

  const setAllFieldValues = (framework: Framework, values: FieldValues) => {
    setState(prev => ({
      ...prev,
      fieldValues: {
        ...prev.fieldValues,
        [framework]: values
      }
    }));
  };

  const resetFields = (framework: Framework) => {
    setState(prev => ({
      ...prev,
      fieldValues: {
        ...prev.fieldValues,
        [framework]: {}
      }
    }));
  };

  const setGeneratedPrompt = (prompt: string) => {
    setState(prev => ({ ...prev, generatedPrompt: prompt }));
  };

  const setAiGeneratedPrompt = (prompt: string) => {
    setState(prev => ({ ...prev, aiGeneratedPrompt: prompt }));
  };

  return {
    state,
    setLanguage,
    setFramework,
    setAllowBlanks,
    setFieldValue,
    setAllFieldValues,
    resetFields,
    setGeneratedPrompt,
    setAiGeneratedPrompt
  };
}
