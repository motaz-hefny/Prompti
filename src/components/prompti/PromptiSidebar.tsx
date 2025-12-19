import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Checkbox } from '@/components/ui/checkbox';
import { AISettings } from '@/components/AISettings';
import type { Language, Framework } from '@/types/prompti';
import { TRANSLATIONS } from '@/data/translations';

interface PromptiSidebarProps {
  language: Language;
  framework: Framework;
  allowBlanks: boolean;
  onLanguageChange: (language: Language) => void;
  onFrameworkChange: (framework: Framework) => void;
  onAllowBlanksChange: (checked: boolean) => void;
}

export function PromptiSidebar({
  language,
  framework,
  allowBlanks,
  onLanguageChange,
  onFrameworkChange,
  onAllowBlanksChange
}: PromptiSidebarProps) {
  const t = TRANSLATIONS[language];

  return (
    <Card className="h-fit">
      <CardHeader>
        <CardTitle className="text-2xl font-bold">{t.appTitle}</CardTitle>
        <p className="text-sm text-muted-foreground">{t.appSubtitle}</p>
      </CardHeader>
      <CardContent className="space-y-6">
        <Button
          variant="outline"
          className="w-full"
          disabled
        >
          <svg className="w-5 h-5 mr-2" viewBox="0 0 24 24">
            <path
              fill="currentColor"
              d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
            />
            <path
              fill="currentColor"
              d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
            />
            <path
              fill="currentColor"
              d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
            />
            <path
              fill="currentColor"
              d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
            />
          </svg>
          {t.signInWithGoogle}
        </Button>

        <div className="w-full">
          <AISettings />
        </div>

        <div className="space-y-3">
          <Label className="text-base font-semibold">{t.languageLabel}</Label>
          <RadioGroup value={language} onValueChange={(value) => onLanguageChange(value as Language)}>
            <div className="flex items-center space-x-2">
              <RadioGroupItem value="en" id="lang-en" />
              <Label htmlFor="lang-en" className="cursor-pointer">{t.languages.en}</Label>
            </div>
            <div className="flex items-center space-x-2">
              <RadioGroupItem value="ar" id="lang-ar" />
              <Label htmlFor="lang-ar" className="cursor-pointer">{t.languages.ar}</Label>
            </div>
            <div className="flex items-center space-x-2">
              <RadioGroupItem value="eg" id="lang-eg" />
              <Label htmlFor="lang-eg" className="cursor-pointer">{t.languages.eg}</Label>
            </div>
          </RadioGroup>
        </div>

        <div className="space-y-3">
          <Label htmlFor="framework-select" className="text-base font-semibold">{t.frameworkLabel}</Label>
          <Select value={framework} onValueChange={(value) => onFrameworkChange(value as Framework)}>
            <SelectTrigger id="framework-select">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="ICDF">{t.frameworks.ICDF}</SelectItem>
              <SelectItem value="RCR-EOC">{t.frameworks['RCR-EOC']}</SelectItem>
              <SelectItem value="MICRO">{t.frameworks.MICRO}</SelectItem>
              <SelectItem value="COSTAR">{t.frameworks.COSTAR}</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div className="flex items-center space-x-2">
          <Checkbox
            id="allow-blanks"
            checked={allowBlanks}
            onCheckedChange={onAllowBlanksChange}
          />
          <Label htmlFor="allow-blanks" className="cursor-pointer">{t.allowBlanksLabel}</Label>
        </div>
      </CardContent>
    </Card>
  );
}
