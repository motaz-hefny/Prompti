import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip';
import { Copy, Download, Cloud, Sparkles, Loader2 } from 'lucide-react';
import { toast } from 'sonner';
import type { Language, Framework } from '@/types/prompti';
import { TRANSLATIONS } from '@/data/translations';
import { copyToClipboard, downloadAsText, validateFields, assemblePrompt } from '@/utils/promptUtils';
import { generatePromptWithAI } from '@/utils/aiApi';
import { useAISettings } from '@/components/AISettings';
import type { FieldValues } from '@/types/prompti';

interface PreviewPanelProps {
  language: Language;
  framework: Framework;
  fieldValues: FieldValues;
  allowBlanks: boolean;
  generatedPrompt: string;
  aiGeneratedPrompt: string;
  onGeneratePrompt: () => void;
  onAiGeneratePrompt: (prompt: string) => void;
}

export function PreviewPanel({
  language,
  framework,
  fieldValues,
  allowBlanks,
  generatedPrompt,
  aiGeneratedPrompt,
  onGeneratePrompt,
  onAiGeneratePrompt
}: PreviewPanelProps) {
  const t = TRANSLATIONS[language];
  const livePreview = assemblePrompt(language, framework, fieldValues);
  const [isGeneratingAI, setIsGeneratingAI] = useState(false);
  const aiSettings = useAISettings();

  const handleCopy = async (text: string) => {
    const success = await copyToClipboard(text);
    if (success) {
      toast.success(t.copySuccess);
    } else {
      toast.error(t.copyError);
    }
  };

  const handleDownload = (text: string, isAI = false) => {
    const filename = isAI 
      ? `prompti_ai_prompt_${framework}_${language}.txt`
      : `prompti_prompt_${framework}_${language}.txt`;
    const blob = new Blob([text], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const handleGenerate = () => {
    const isValid = validateFields(language, framework, fieldValues, allowBlanks);
    if (!isValid) {
      toast.error(t.validationError);
      return;
    }
    onGeneratePrompt();
  };

  const handleAiGenerate = async () => {
    // Check if API key is configured
    if (!aiSettings.apiKey || !aiSettings.apiKey.trim()) {
      toast.error('Please configure your AI provider in AI Settings first.');
      return;
    }

    setIsGeneratingAI(true);
    try {
      const aiPrompt = await generatePromptWithAI(framework, language, fieldValues, aiSettings);
      onAiGeneratePrompt(aiPrompt);
      toast.success(`AI prompt generated successfully using ${aiSettings.provider.toUpperCase()}!`);
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : t.aiGenerationError;
      toast.error(errorMessage);
    } finally {
      setIsGeneratingAI(false);
    }
  };

  return (
    <div className="space-y-4">
      <Card>
        <CardHeader>
          <CardTitle>{t.livePreviewTitle}</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="bg-muted p-4 rounded-md min-h-[200px] whitespace-pre-wrap font-mono text-sm">
            {livePreview || <span className="text-muted-foreground italic">Start typing to see preview...</span>}
          </div>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 gap-2">
        <Button onClick={handleGenerate} className="w-full" size="lg">
          {t.generatePromptButton}
        </Button>
        <Button 
          onClick={handleAiGenerate} 
          className="w-full" 
          size="lg"
          variant="outline"
          disabled={isGeneratingAI}
        >
          {isGeneratingAI ? (
            <>
              <Loader2 className="w-4 h-4 mr-2 animate-spin" />
              {t.generatingAI}
            </>
          ) : (
            <>
              <Sparkles className="w-4 h-4 mr-2" />
              {t.generateWithAIButton}
            </>
          )}
        </Button>
      </div>

      {generatedPrompt && (
        <Card>
          <CardHeader>
            <CardTitle>{t.generatedPromptTitle}</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="bg-muted p-4 rounded-md max-h-[300px] overflow-y-auto whitespace-pre-wrap font-mono text-sm">
              {generatedPrompt}
            </div>
            <div className="flex gap-2">
              <Button onClick={() => handleCopy(generatedPrompt)} variant="default" className="flex-1">
                <Copy className="w-4 h-4 mr-2" />
                {t.copyButton}
              </Button>
              <Button onClick={() => handleDownload(generatedPrompt, false)} variant="outline" className="flex-1">
                <Download className="w-4 h-4 mr-2" />
                {t.downloadButton}
              </Button>
              <TooltipProvider>
                <Tooltip>
                  <TooltipTrigger asChild>
                    <span className="flex-1">
                      <Button variant="outline" disabled className="w-full">
                        <Cloud className="w-4 h-4 mr-2" />
                        {t.saveToDriveButton}
                      </Button>
                    </span>
                  </TooltipTrigger>
                  <TooltipContent>
                    <p>{t.saveToDriveTooltip}</p>
                  </TooltipContent>
                </Tooltip>
              </TooltipProvider>
            </div>
          </CardContent>
        </Card>
      )}

      {aiGeneratedPrompt && (
        <Card className="border-primary">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-primary" />
              {t.aiGeneratedPromptTitle}
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="bg-muted p-4 rounded-md max-h-[300px] overflow-y-auto whitespace-pre-wrap font-mono text-sm">
              {aiGeneratedPrompt}
            </div>
            <div className="flex gap-2">
              <Button onClick={() => handleCopy(aiGeneratedPrompt)} variant="default" className="flex-1">
                <Copy className="w-4 h-4 mr-2" />
                {t.copyButton}
              </Button>
              <Button onClick={() => handleDownload(aiGeneratedPrompt, true)} variant="outline" className="flex-1">
                <Download className="w-4 h-4 mr-2" />
                {t.downloadButton}
              </Button>
              <TooltipProvider>
                <Tooltip>
                  <TooltipTrigger asChild>
                    <span className="flex-1">
                      <Button variant="outline" disabled className="w-full">
                        <Cloud className="w-4 h-4 mr-2" />
                        {t.saveToDriveButton}
                      </Button>
                    </span>
                  </TooltipTrigger>
                  <TooltipContent>
                    <p>{t.saveToDriveTooltip}</p>
                  </TooltipContent>
                </Tooltip>
              </TooltipProvider>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
