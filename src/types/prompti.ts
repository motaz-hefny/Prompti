export type Language = 'en' | 'ar' | 'eg';

export type Framework = 'ICDF' | 'RCR-EOC' | 'MICRO' | 'COSTAR';

export interface FrameworkField {
  key: string;
  label: string;
  help: string;
  required: boolean;
  multiline?: boolean;
}

export interface FrameworkDefinition {
  name: string;
  fields: FrameworkField[];
  sections: string[];
}

export interface FieldValues {
  [key: string]: string;
}

export interface SessionState {
  language: Language;
  framework: Framework;
  allowBlanks: boolean;
  fieldValues: {
    [key in Framework]: FieldValues;
  };
  generatedPrompt: string;
  aiGeneratedPrompt: string;
  slangVariant: number;
}

export interface Translations {
  appTitle: string;
  appSubtitle: string;
  signInWithGoogle: string;
  languageLabel: string;
  frameworkLabel: string;
  allowBlanksLabel: string;
  insertExampleButton: string;
  resetFieldsButton: string;
  generatePromptButton: string;
  generateWithAIButton: string;
  livePreviewTitle: string;
  generatedPromptTitle: string;
  aiGeneratedPromptTitle: string;
  generatingAI: string;
  copyButton: string;
  downloadButton: string;
  saveToDriveButton: string;
  saveToDriveTooltip: string;
  copySuccess: string;
  copyError: string;
  exampleInserted: string;
  fieldsReset: string;
  validationError: string;
  aiGenerationError: string;
  frameworks: {
    [key in Framework]: string;
  };
  languages: {
    en: string;
    ar: string;
    eg: string;
  };
}
