/**
 * AI Settings Component
 * Allows users to configure their AI provider, API key, and model
 */

import { useState, useEffect } from 'react';
import { Settings, ExternalLink, Info, Zap, Star } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { AI_PROVIDERS, type AIProvider, type AISettings as AISettingsType } from '@/types/aiProvider';

const STORAGE_KEY = 'prompti_ai_settings';

export function AISettings() {
  const [open, setOpen] = useState(false);
  const [settings, setSettings] = useState<AISettingsType>({
    provider: 'groq',
    apiKey: '',
    model: AI_PROVIDERS.groq.defaultModel
  });

  // Load settings from localStorage
  useEffect(() => {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        setSettings(parsed);
      } catch (e) {
        console.error('Failed to load AI settings:', e);
      }
    }
  }, []);

  // Save settings to localStorage
  const saveSettings = (newSettings: AISettingsType) => {
    setSettings(newSettings);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(newSettings));
  };

  const handleProviderChange = (provider: AIProvider) => {
    const newSettings: AISettingsType = {
      provider,
      apiKey: settings.apiKey, // Keep existing key
      model: AI_PROVIDERS[provider].defaultModel
    };
    saveSettings(newSettings);
  };

  const handleApiKeyChange = (apiKey: string) => {
    saveSettings({ ...settings, apiKey });
  };

  const handleModelChange = (model: string) => {
    saveSettings({ ...settings, model });
  };

  const currentProvider = AI_PROVIDERS[settings.provider];
  const hasApiKey = settings.apiKey && settings.apiKey.trim().length > 0;

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button variant="outline" size="sm" className="gap-2">
          <Settings className="h-4 w-4" />
          AI Settings
          {!hasApiKey && (
            <Badge variant="destructive" className="ml-1">
              Setup Required
            </Badge>
          )}
        </Button>
      </DialogTrigger>
      <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>AI Provider Settings</DialogTitle>
          <DialogDescription>
            Configure your AI provider to enable AI-powered prompt generation
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-6">
          {/* Provider Selection */}
          <div className="space-y-3">
            <Label>AI Provider</Label>
            <Select value={settings.provider} onValueChange={handleProviderChange}>
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {Object.values(AI_PROVIDERS).map((provider) => (
                  <SelectItem key={provider.id} value={provider.id}>
                    <div className="flex items-center gap-2">
                      <span>{provider.name}</span>
                      {provider.id === 'groq' && (
                        <Badge variant="secondary" className="text-xs">
                          Recommended
                        </Badge>
                      )}
                    </div>
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* Provider Info Card */}
          <Card>
            <CardHeader className="pb-3">
              <div className="flex items-start justify-between">
                <div>
                  <CardTitle className="text-lg">{currentProvider.name}</CardTitle>
                  <CardDescription className="mt-1">
                    {currentProvider.description}
                  </CardDescription>
                </div>
                <Button
                  variant="ghost"
                  size="sm"
                  asChild
                >
                  <a
                    href={currentProvider.signupUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="gap-1"
                  >
                    Get API Key
                    <ExternalLink className="h-3 w-3" />
                  </a>
                </Button>
              </div>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="grid grid-cols-3 gap-3 text-sm">
                <div className="flex items-center gap-2">
                  <Zap className="h-4 w-4 text-yellow-500" />
                  <div>
                    <div className="font-medium">Speed</div>
                    <div className="text-muted-foreground">
                      {'⭐'.repeat(currentProvider.speed)}
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <Star className="h-4 w-4 text-blue-500" />
                  <div>
                    <div className="font-medium">Quality</div>
                    <div className="text-muted-foreground">
                      {'⭐'.repeat(currentProvider.quality)}
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <Info className="h-4 w-4 text-green-500" />
                  <div>
                    <div className="font-medium">Free Tier</div>
                    <div className="text-muted-foreground">
                      {currentProvider.freeRequests}
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* API Key Input */}
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <Label htmlFor="api-key">{currentProvider.apiKeyLabel}</Label>
              <Button
                variant="link"
                size="sm"
                asChild
                className="h-auto p-0 text-xs"
              >
                <a
                  href={currentProvider.docsUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="gap-1"
                >
                  View Docs
                  <ExternalLink className="h-3 w-3" />
                </a>
              </Button>
            </div>
            <Input
              id="api-key"
              type="password"
              placeholder={currentProvider.apiKeyPlaceholder}
              value={settings.apiKey}
              onChange={(e) => handleApiKeyChange(e.target.value)}
            />
            <p className="text-xs text-muted-foreground">
              Your API key is stored locally and never sent to our servers.
            </p>
          </div>

          {/* Model Selection */}
          <div className="space-y-3">
            <Label>Model</Label>
            <Select value={settings.model} onValueChange={handleModelChange}>
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {currentProvider.models.map((model) => (
                  <SelectItem key={model.id} value={model.id}>
                    <div className="flex flex-col items-start">
                      <span>{model.name}</span>
                      <span className="text-xs text-muted-foreground">
                        {model.description}
                      </span>
                    </div>
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* Setup Instructions */}
          {!hasApiKey && (
            <Card className="border-yellow-500/50 bg-yellow-500/10">
              <CardHeader className="pb-3">
                <CardTitle className="text-sm flex items-center gap-2">
                  <Info className="h-4 w-4" />
                  Setup Required
                </CardTitle>
              </CardHeader>
              <CardContent className="text-sm space-y-2">
                <p>To use AI-powered prompt generation:</p>
                <ol className="list-decimal list-inside space-y-1 ml-2">
                  <li>
                    Click "Get API Key" to sign up for {currentProvider.name}
                  </li>
                  <li>Create an API key (free, no credit card required)</li>
                  <li>Paste your API key above</li>
                  <li>Click "Save Settings"</li>
                </ol>
              </CardContent>
            </Card>
          )}

          {/* Save Button */}
          <div className="flex justify-end gap-2">
            <Button variant="outline" onClick={() => setOpen(false)}>
              Cancel
            </Button>
            <Button onClick={() => setOpen(false)}>
              Save Settings
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}

/**
 * Hook to get current AI settings
 */
export function useAISettings(): AISettingsType {
  const [settings, setSettings] = useState<AISettingsType>({
    provider: 'groq',
    apiKey: '',
    model: AI_PROVIDERS.groq.defaultModel
  });

  useEffect(() => {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        setSettings(parsed);
      } catch (e) {
        console.error('Failed to load AI settings:', e);
      }
    }
  }, []);

  return settings;
}
