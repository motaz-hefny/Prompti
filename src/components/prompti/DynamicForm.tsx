import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip';
import { HelpCircle } from 'lucide-react';
import type { Language, Framework, FieldValues } from '@/types/prompti';
import { TRANSLATIONS, FRAMEWORK_DEFINITIONS, EXAMPLES } from '@/data/translations';

interface DynamicFormProps {
  language: Language;
  framework: Framework;
  fieldValues: FieldValues;
  onFieldChange: (key: string, value: string) => void;
  onInsertExample: () => void;
  onResetFields: () => void;
}

export function DynamicForm({
  language,
  framework,
  fieldValues,
  onFieldChange,
  onInsertExample,
  onResetFields
}: DynamicFormProps) {
  const t = TRANSLATIONS[language];
  const definition = FRAMEWORK_DEFINITIONS[language][framework];

  return (
    <Card>
      <CardHeader>
        <CardTitle>{definition.name}</CardTitle>
        <div className="flex gap-2 mt-2">
          <Button variant="outline" size="sm" onClick={onInsertExample}>
            {t.insertExampleButton}
          </Button>
          <Button variant="outline" size="sm" onClick={onResetFields}>
            {t.resetFieldsButton}
          </Button>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        <TooltipProvider>
          {definition.fields.map((field) => (
            <div key={field.key} className="space-y-2">
              <div className="flex items-center gap-2">
                <Label htmlFor={field.key}>
                  {field.label}
                  {field.required && <span className="text-destructive ml-1">*</span>}
                </Label>
                <Tooltip>
                  <TooltipTrigger asChild>
                    <HelpCircle className="w-4 h-4 text-muted-foreground cursor-help" />
                  </TooltipTrigger>
                  <TooltipContent>
                    <p className="max-w-xs">{field.help}</p>
                  </TooltipContent>
                </Tooltip>
              </div>
              {field.multiline ? (
                <Textarea
                  id={field.key}
                  value={fieldValues[field.key] || ''}
                  onChange={(e) => onFieldChange(field.key, e.target.value)}
                  rows={4}
                  className="resize-y"
                />
              ) : (
                <Input
                  id={field.key}
                  value={fieldValues[field.key] || ''}
                  onChange={(e) => onFieldChange(field.key, e.target.value)}
                />
              )}
            </div>
          ))}
        </TooltipProvider>
      </CardContent>
    </Card>
  );
}
