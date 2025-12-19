import type { Language, Framework, FieldValues } from '@/types/prompti';
import { FRAMEWORK_DEFINITIONS } from '@/data/translations';

export function assemblePrompt(
  language: Language,
  framework: Framework,
  fieldValues: FieldValues
): string {
  const definition = FRAMEWORK_DEFINITIONS[language][framework];
  const sections: string[] = [];

  definition.fields.forEach((field, index) => {
    const value = fieldValues[field.key]?.trim() || '';
    if (value) {
      const sectionLabel = definition.sections[index];
      sections.push(`${sectionLabel}:\n${value}`);
    }
  });

  return sections.join('\n\n');
}

export function validateFields(
  language: Language,
  framework: Framework,
  fieldValues: FieldValues,
  allowBlanks: boolean
): boolean {
  if (allowBlanks) return true;

  const definition = FRAMEWORK_DEFINITIONS[language][framework];
  return definition.fields.every(field => {
    if (!field.required) return true;
    const value = fieldValues[field.key]?.trim();
    return value && value.length > 0;
  });
}

export async function copyToClipboard(text: string): Promise<boolean> {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch (error) {
    console.error('Failed to copy to clipboard:', error);
    return false;
  }
}

export function downloadAsText(
  text: string,
  framework: Framework,
  language: Language
): void {
  const filename = `prompti_prompt_${framework}_${language}.txt`;
  const blob = new Blob([text], { type: 'text/plain' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

export function isRTL(language: Language): boolean {
  return language === 'ar' || language === 'eg';
}
