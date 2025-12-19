import { useEffect } from 'react';
import { toast } from 'sonner';
import { PromptiSidebar } from '@/components/prompti/PromptiSidebar';
import { DynamicForm } from '@/components/prompti/DynamicForm';
import { PreviewPanel } from '@/components/prompti/PreviewPanel';
import { usePromptiState } from '@/hooks/usePromptiState';
import { assemblePrompt, isRTL } from '@/utils/promptUtils';
import { TRANSLATIONS, EXAMPLES } from '@/data/translations';
import type { Language, Framework } from '@/types/prompti';

export default function Prompti() {
  const {
    state,
    setLanguage,
    setFramework,
    setAllowBlanks,
    setFieldValue,
    setAllFieldValues,
    resetFields,
    setGeneratedPrompt,
    setAiGeneratedPrompt
  } = usePromptiState();

  const { language, framework, allowBlanks, fieldValues, generatedPrompt, aiGeneratedPrompt } = state;
  const currentFieldValues = fieldValues[framework];
  const t = TRANSLATIONS[language];
  const rtl = isRTL(language);

  useEffect(() => {
    document.documentElement.dir = rtl ? 'rtl' : 'ltr';
    document.documentElement.lang = language;
  }, [language, rtl]);

  const handleInsertExample = () => {
    const examples = EXAMPLES[language][framework];
    setAllFieldValues(framework, examples);
    toast.success(t.exampleInserted);
  };

  const handleResetFields = () => {
    resetFields(framework);
    toast.success(t.fieldsReset);
  };

  const handleGeneratePrompt = () => {
    const prompt = assemblePrompt(language, framework, currentFieldValues);
    setGeneratedPrompt(prompt);
  };

  return (
    <div className={`min-h-screen bg-background ${rtl ? 'rtl' : 'ltr'}`}>
      <div className="container mx-auto p-4 xl:p-8">
        <div className="grid grid-cols-1 xl:grid-cols-12 gap-6">
          <div className="xl:col-span-3">
            <PromptiSidebar
              language={language}
              framework={framework}
              allowBlanks={allowBlanks}
              onLanguageChange={setLanguage}
              onFrameworkChange={setFramework}
              onAllowBlanksChange={setAllowBlanks}
            />
          </div>

          <div className="xl:col-span-5">
            <DynamicForm
              language={language}
              framework={framework}
              fieldValues={currentFieldValues}
              onFieldChange={(key, value) => setFieldValue(framework, key, value)}
              onInsertExample={handleInsertExample}
              onResetFields={handleResetFields}
            />
          </div>

          <div className="xl:col-span-4">
            <PreviewPanel
              language={language}
              framework={framework}
              fieldValues={currentFieldValues}
              allowBlanks={allowBlanks}
              generatedPrompt={generatedPrompt}
              aiGeneratedPrompt={aiGeneratedPrompt}
              onGeneratePrompt={handleGeneratePrompt}
              onAiGeneratePrompt={setAiGeneratedPrompt}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
