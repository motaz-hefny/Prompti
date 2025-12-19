import type { Language, Translations, FrameworkDefinition, Framework } from '@/types/prompti';

export const TRANSLATIONS: Record<Language, Translations> = {
  en: {
    appTitle: 'Prompti',
    appSubtitle: 'Structured Prompt Generator',
    signInWithGoogle: 'Sign In with Google',
    languageLabel: 'Language',
    frameworkLabel: 'Framework',
    allowBlanksLabel: 'Allow blanks',
    insertExampleButton: 'Insert Example',
    resetFieldsButton: 'Reset Fields',
    generatePromptButton: 'Generate Prompt',
    generateWithAIButton: '✨ Generate with AI',
    livePreviewTitle: 'Live Preview',
    generatedPromptTitle: 'Generated Prompt',
    aiGeneratedPromptTitle: 'AI-Enhanced Prompt',
    generatingAI: 'Generating with AI...',
    copyButton: 'Copy to Clipboard',
    downloadButton: 'Download as .txt',
    saveToDriveButton: 'Save to Drive',
    saveToDriveTooltip: 'Pro subscription required',
    copySuccess: 'Copied to clipboard!',
    copyError: 'Failed to copy',
    exampleInserted: 'Example inserted successfully',
    fieldsReset: 'Fields reset',
    validationError: 'Please fill in all required fields',
    aiGenerationError: 'AI generation failed',
    frameworks: {
      'ICDF': 'ICDF',
      'RCR-EOC': 'RCR-EOC',
      'MICRO': 'MICRO',
      'COSTAR': 'COSTAR'
    },
    languages: {
      en: 'English',
      ar: 'العربية',
      eg: 'مصرّي'
    }
  },
  ar: {
    appTitle: 'برومبتي',
    appSubtitle: 'مولّد الأوامر المنظّمة',
    signInWithGoogle: 'تسجيل الدخول بحساب جوجل',
    languageLabel: 'اللغة',
    frameworkLabel: 'الإطار',
    allowBlanksLabel: 'السماح بالحقول الفارغة',
    insertExampleButton: 'إدراج مثال',
    resetFieldsButton: 'إعادة تعيين الحقول',
    generatePromptButton: 'توليد الأمر',
    generateWithAIButton: '✨ توليد بالذكاء الاصطناعي',
    livePreviewTitle: 'معاينة مباشرة',
    generatedPromptTitle: 'الأمر المولّد',
    aiGeneratedPromptTitle: 'الأمر المحسّن بالذكاء الاصطناعي',
    generatingAI: 'جاري التوليد بالذكاء الاصطناعي...',
    copyButton: 'نسخ إلى الحافظة',
    downloadButton: 'تنزيل كملف نصي',
    saveToDriveButton: 'حفظ في Drive',
    saveToDriveTooltip: 'يتطلب اشتراك Pro',
    copySuccess: 'تم النسخ إلى الحافظة!',
    copyError: 'فشل النسخ',
    exampleInserted: 'تم إدراج المثال بنجاح',
    fieldsReset: 'تم إعادة تعيين الحقول',
    validationError: 'يرجى ملء جميع الحقول المطلوبة',
    aiGenerationError: 'فشل التوليد بالذكاء الاصطناعي',
    frameworks: {
      'ICDF': 'ICDF',
      'RCR-EOC': 'RCR-EOC',
      'MICRO': 'MICRO',
      'COSTAR': 'COSTAR'
    },
    languages: {
      en: 'English',
      ar: 'العربية',
      eg: 'مصرّي'
    }
  },
  eg: {
    appTitle: 'برومبتي',
    appSubtitle: 'مولّد الأوامر المنظّمة',
    signInWithGoogle: 'ادخل بحساب جوجل',
    languageLabel: 'اللغة',
    frameworkLabel: 'الإطار',
    allowBlanksLabel: 'اسمح بالحقول الفاضية',
    insertExampleButton: 'حط مثال',
    resetFieldsButton: 'امسح الحقول',
    generatePromptButton: 'اعمل الأمر',
    generateWithAIButton: '✨ اعمله بالAI',
    livePreviewTitle: 'معاينة مباشرة',
    generatedPromptTitle: 'الأمر المولّد',
    aiGeneratedPromptTitle: 'الأمر المحسّن بالAI',
    generatingAI: 'بيتعمل بالAI...',
    copyButton: 'انسخ',
    downloadButton: 'نزّل كملف',
    saveToDriveButton: 'احفظ في Drive',
    saveToDriveTooltip: 'محتاج اشتراك Pro',
    copySuccess: 'اتنسخ!',
    copyError: 'مانسخش',
    exampleInserted: 'المثال اتحط',
    fieldsReset: 'الحقول اتمسحت',
    validationError: 'املا الحقول المطلوبة',
    aiGenerationError: 'الAI مانفعش',
    frameworks: {
      'ICDF': 'ICDF',
      'RCR-EOC': 'RCR-EOC',
      'MICRO': 'MICRO',
      'COSTAR': 'COSTAR'
    },
    languages: {
      en: 'English',
      ar: 'العربية',
      eg: 'مصرّي'
    }
  }
};

export const FRAMEWORK_DEFINITIONS: Record<Language, Record<Framework, FrameworkDefinition>> = {
  en: {
    ICDF: {
      name: 'ICDF',
      sections: ['Instruction', 'Context', 'Data', 'Format'],
      fields: [
        {
          key: 'instruction',
          label: 'Instruction',
          help: 'What do you want the AI to do?',
          required: true,
          multiline: true
        },
        {
          key: 'context',
          label: 'Context',
          help: 'Background information or situation',
          required: true,
          multiline: true
        },
        {
          key: 'data',
          label: 'Data',
          help: 'Specific data or examples to work with',
          required: false,
          multiline: true
        },
        {
          key: 'format',
          label: 'Format',
          help: 'How should the output be structured?',
          required: true,
          multiline: true
        }
      ]
    },
    'RCR-EOC': {
      name: 'RCR-EOC',
      sections: ['Role', 'Context', 'Request', 'Examples', 'Output', 'Constraints'],
      fields: [
        {
          key: 'role',
          label: 'Role',
          help: 'What role should the AI assume?',
          required: true,
          multiline: false
        },
        {
          key: 'context',
          label: 'Context',
          help: 'Work environment or situation',
          required: true,
          multiline: true
        },
        {
          key: 'request',
          label: 'Request',
          help: 'What specifically do you need?',
          required: true,
          multiline: true
        },
        {
          key: 'examples',
          label: 'Examples',
          help: 'Sample inputs or outputs',
          required: false,
          multiline: true
        },
        {
          key: 'output',
          label: 'Output',
          help: 'Desired output format',
          required: true,
          multiline: true
        },
        {
          key: 'constraints',
          label: 'Constraints',
          help: 'Limitations or requirements',
          required: false,
          multiline: true
        }
      ]
    },
    MICRO: {
      name: 'MICRO',
      sections: ['Message', 'Intention', 'Context', 'Rhythm', 'Output'],
      fields: [
        {
          key: 'message',
          label: 'Message',
          help: 'Core message or goal',
          required: true,
          multiline: true
        },
        {
          key: 'intention',
          label: 'Intention',
          help: 'What is the purpose?',
          required: true,
          multiline: true
        },
        {
          key: 'context',
          label: 'Context',
          help: 'Situational background',
          required: true,
          multiline: true
        },
        {
          key: 'rhythm',
          label: 'Rhythm',
          help: 'Tone, style, or pacing',
          required: false,
          multiline: true
        },
        {
          key: 'output',
          label: 'Output',
          help: 'Expected output format',
          required: true,
          multiline: true
        }
      ]
    },
    COSTAR: {
      name: 'COSTAR',
      sections: ['Context', 'Offer', 'Style', 'Target', 'Action', 'Result'],
      fields: [
        {
          key: 'context',
          label: 'Context',
          help: 'Background situation',
          required: true,
          multiline: true
        },
        {
          key: 'offer',
          label: 'Offer',
          help: 'What are you providing?',
          required: true,
          multiline: true
        },
        {
          key: 'style',
          label: 'Style',
          help: 'Communication style or tone',
          required: false,
          multiline: true
        },
        {
          key: 'target',
          label: 'Target',
          help: 'Who is the audience?',
          required: true,
          multiline: true
        },
        {
          key: 'action',
          label: 'Action',
          help: 'What action should be taken?',
          required: true,
          multiline: true
        },
        {
          key: 'result',
          label: 'Result',
          help: 'Expected outcome',
          required: true,
          multiline: true
        }
      ]
    }
  },
  ar: {
    ICDF: {
      name: 'ICDF',
      sections: ['التعليمات', 'السياق', 'البيانات', 'التنسيق'],
      fields: [
        {
          key: 'instruction',
          label: 'التعليمات',
          help: 'ماذا تريد من الذكاء الاصطناعي أن يفعل؟',
          required: true,
          multiline: true
        },
        {
          key: 'context',
          label: 'السياق',
          help: 'معلومات خلفية أو الموقف',
          required: true,
          multiline: true
        },
        {
          key: 'data',
          label: 'البيانات',
          help: 'بيانات محددة أو أمثلة للعمل معها',
          required: false,
          multiline: true
        },
        {
          key: 'format',
          label: 'التنسيق',
          help: 'كيف يجب أن يكون هيكل الإخراج؟',
          required: true,
          multiline: true
        }
      ]
    },
    'RCR-EOC': {
      name: 'RCR-EOC',
      sections: ['الدور', 'السياق', 'الطلب', 'الأمثلة', 'الإخراج', 'القيود'],
      fields: [
        {
          key: 'role',
          label: 'الدور',
          help: 'ما الدور الذي يجب أن يتولاه الذكاء الاصطناعي؟',
          required: true,
          multiline: false
        },
        {
          key: 'context',
          label: 'السياق',
          help: 'بيئة العمل أو الموقف',
          required: true,
          multiline: true
        },
        {
          key: 'request',
          label: 'الطلب',
          help: 'ما الذي تحتاجه بالتحديد؟',
          required: true,
          multiline: true
        },
        {
          key: 'examples',
          label: 'الأمثلة',
          help: 'عينات من المدخلات أو المخرجات',
          required: false,
          multiline: true
        },
        {
          key: 'output',
          label: 'الإخراج',
          help: 'تنسيق الإخراج المطلوب',
          required: true,
          multiline: true
        },
        {
          key: 'constraints',
          label: 'القيود',
          help: 'القيود أو المتطلبات',
          required: false,
          multiline: true
        }
      ]
    },
    MICRO: {
      name: 'MICRO',
      sections: ['الرسالة', 'النية', 'السياق', 'الإيقاع', 'الإخراج'],
      fields: [
        {
          key: 'message',
          label: 'الرسالة',
          help: 'الرسالة الأساسية أو الهدف',
          required: true,
          multiline: true
        },
        {
          key: 'intention',
          label: 'النية',
          help: 'ما هو الغرض؟',
          required: true,
          multiline: true
        },
        {
          key: 'context',
          label: 'السياق',
          help: 'الخلفية الظرفية',
          required: true,
          multiline: true
        },
        {
          key: 'rhythm',
          label: 'الإيقاع',
          help: 'النبرة أو الأسلوب أو الوتيرة',
          required: false,
          multiline: true
        },
        {
          key: 'output',
          label: 'الإخراج',
          help: 'تنسيق الإخراج المتوقع',
          required: true,
          multiline: true
        }
      ]
    },
    COSTAR: {
      name: 'COSTAR',
      sections: ['السياق', 'العرض', 'الأسلوب', 'الهدف', 'الإجراء', 'النتيجة'],
      fields: [
        {
          key: 'context',
          label: 'السياق',
          help: 'الموقف الخلفي',
          required: true,
          multiline: true
        },
        {
          key: 'offer',
          label: 'العرض',
          help: 'ماذا تقدم؟',
          required: true,
          multiline: true
        },
        {
          key: 'style',
          label: 'الأسلوب',
          help: 'أسلوب التواصل أو النبرة',
          required: false,
          multiline: true
        },
        {
          key: 'target',
          label: 'الهدف',
          help: 'من هو الجمهور؟',
          required: true,
          multiline: true
        },
        {
          key: 'action',
          label: 'الإجراء',
          help: 'ما الإجراء الذي يجب اتخاذه؟',
          required: true,
          multiline: true
        },
        {
          key: 'result',
          label: 'النتيجة',
          help: 'النتيجة المتوقعة',
          required: true,
          multiline: true
        }
      ]
    }
  },
  eg: {
    ICDF: {
      name: 'ICDF',
      sections: ['التعليمات', 'السياق', 'البيانات', 'التنسيق'],
      fields: [
        {
          key: 'instruction',
          label: 'التعليمات',
          help: 'عايز الAI يعمل إيه؟',
          required: true,
          multiline: true
        },
        {
          key: 'context',
          label: 'السياق',
          help: 'معلومات خلفية أو الموقف',
          required: true,
          multiline: true
        },
        {
          key: 'data',
          label: 'البيانات',
          help: 'بيانات معينة أو أمثلة',
          required: false,
          multiline: true
        },
        {
          key: 'format',
          label: 'التنسيق',
          help: 'عايز الناتج يطلع إزاي؟',
          required: true,
          multiline: true
        }
      ]
    },
    'RCR-EOC': {
      name: 'RCR-EOC',
      sections: ['الدور', 'السياق', 'الطلب', 'الأمثلة', 'الإخراج', 'القيود'],
      fields: [
        {
          key: 'role',
          label: 'الدور',
          help: 'الAI يشتغل كإيه؟',
          required: true,
          multiline: false
        },
        {
          key: 'context',
          label: 'السياق',
          help: 'بيئة الشغل أو الموقف',
          required: true,
          multiline: true
        },
        {
          key: 'request',
          label: 'الطلب',
          help: 'محتاج إيه بالظبط؟',
          required: true,
          multiline: true
        },
        {
          key: 'examples',
          label: 'الأمثلة',
          help: 'عينات من المدخلات أو المخرجات',
          required: false,
          multiline: true
        },
        {
          key: 'output',
          label: 'الإخراج',
          help: 'تنسيق الناتج المطلوب',
          required: true,
          multiline: true
        },
        {
          key: 'constraints',
          label: 'القيود',
          help: 'القيود أو المتطلبات',
          required: false,
          multiline: true
        }
      ]
    },
    MICRO: {
      name: 'MICRO',
      sections: ['الرسالة', 'النية', 'السياق', 'الإيقاع', 'الإخراج'],
      fields: [
        {
          key: 'message',
          label: 'الرسالة',
          help: 'الرسالة الأساسية أو الهدف',
          required: true,
          multiline: true
        },
        {
          key: 'intention',
          label: 'النية',
          help: 'الغرض إيه؟',
          required: true,
          multiline: true
        },
        {
          key: 'context',
          label: 'السياق',
          help: 'الخلفية الظرفية',
          required: true,
          multiline: true
        },
        {
          key: 'rhythm',
          label: 'الإيقاع',
          help: 'النبرة أو الأسلوب',
          required: false,
          multiline: true
        },
        {
          key: 'output',
          label: 'الإخراج',
          help: 'تنسيق الناتج المتوقع',
          required: true,
          multiline: true
        }
      ]
    },
    COSTAR: {
      name: 'COSTAR',
      sections: ['السياق', 'العرض', 'الأسلوب', 'الهدف', 'الإجراء', 'النتيجة'],
      fields: [
        {
          key: 'context',
          label: 'السياق',
          help: 'الموقف الخلفي',
          required: true,
          multiline: true
        },
        {
          key: 'offer',
          label: 'العرض',
          help: 'بتقدم إيه؟',
          required: true,
          multiline: true
        },
        {
          key: 'style',
          label: 'الأسلوب',
          help: 'أسلوب التواصل أو النبرة',
          required: false,
          multiline: true
        },
        {
          key: 'target',
          label: 'الهدف',
          help: 'الجمهور مين؟',
          required: true,
          multiline: true
        },
        {
          key: 'action',
          label: 'الإجراء',
          help: 'الإجراء المطلوب إيه؟',
          required: true,
          multiline: true
        },
        {
          key: 'result',
          label: 'النتيجة',
          help: 'النتيجة المتوقعة',
          required: true,
          multiline: true
        }
      ]
    }
  }
};

export const EXAMPLES: Record<Language, Record<Framework, Record<string, string>>> = {
  en: {
    ICDF: {
      instruction: 'Analyze the sentiment of customer reviews',
      context: 'E-commerce platform with thousands of product reviews',
      data: 'Sample reviews: "Great product!", "Terrible quality", "Average experience"',
      format: 'JSON output with sentiment score (1-5) and category (positive/negative/neutral)'
    },
    'RCR-EOC': {
      role: 'Senior Marketing Analyst',
      context: 'Launching a new product in competitive market',
      request: 'Create a comprehensive market analysis report',
      examples: 'Include competitor analysis, target demographics, pricing strategy',
      output: 'Executive summary with actionable recommendations',
      constraints: 'Maximum 2 pages, focus on data-driven insights'
    },
    MICRO: {
      message: 'Improve customer retention',
      intention: 'Identify key factors affecting customer loyalty',
      context: 'SaaS company with 10,000 active users',
      rhythm: 'Professional, data-driven, actionable',
      output: 'Prioritized list of retention strategies with expected impact'
    },
    COSTAR: {
      context: 'Small business owner struggling with social media presence',
      offer: 'Social media content calendar for next month',
      style: 'Casual, engaging, brand-aligned',
      target: 'Small business owners aged 30-50',
      action: 'Create 30-day content plan with post ideas and timing',
      result: 'Increased engagement and follower growth'
    }
  },
  ar: {
    ICDF: {
      instruction: 'تحليل مشاعر مراجعات العملاء',
      context: 'منصة تجارة إلكترونية تحتوي على آلاف المراجعات',
      data: 'عينات من المراجعات: "منتج رائع!"، "جودة سيئة"، "تجربة متوسطة"',
      format: 'إخراج JSON مع درجة المشاعر (1-5) والفئة (إيجابي/سلبي/محايد)'
    },
    'RCR-EOC': {
      role: 'محلل تسويق أول',
      context: 'إطلاق منتج جديد في سوق تنافسي',
      request: 'إنشاء تقرير شامل لتحليل السوق',
      examples: 'تضمين تحليل المنافسين، الفئات المستهدفة، استراتيجية التسعير',
      output: 'ملخص تنفيذي مع توصيات قابلة للتنفيذ',
      constraints: 'حد أقصى صفحتان، التركيز على الرؤى المستندة إلى البيانات'
    },
    MICRO: {
      message: 'تحسين الاحتفاظ بالعملاء',
      intention: 'تحديد العوامل الرئيسية المؤثرة على ولاء العملاء',
      context: 'شركة SaaS مع 10,000 مستخدم نشط',
      rhythm: 'احترافي، مستند إلى البيانات، قابل للتنفيذ',
      output: 'قائمة مرتبة حسب الأولوية لاستراتيجيات الاحتفاظ مع التأثير المتوقع'
    },
    COSTAR: {
      context: 'صاحب عمل صغير يعاني من التواجد على وسائل التواصل الاجتماعي',
      offer: 'تقويم محتوى وسائل التواصل الاجتماعي للشهر القادم',
      style: 'غير رسمي، جذاب، متوافق مع العلامة التجارية',
      target: 'أصحاب الأعمال الصغيرة الذين تتراوح أعمارهم بين 30-50',
      action: 'إنشاء خطة محتوى لمدة 30 يومًا مع أفكار المنشورات والتوقيت',
      result: 'زيادة التفاعل ونمو المتابعين'
    }
  },
  eg: {
    ICDF: {
      instruction: 'حلل مشاعر مراجعات الزباين',
      context: 'منصة تجارة إلكترونية فيها آلاف المراجعات',
      data: 'عينات من المراجعات: "منتج تحفة!"، "جودة وحشة"، "تجربة عادية"',
      format: 'ناتج JSON مع درجة المشاعر (1-5) والفئة (إيجابي/سلبي/محايد)'
    },
    'RCR-EOC': {
      role: 'محلل تسويق كبير',
      context: 'بنطلق منتج جديد في سوق فيه منافسة',
      request: 'اعمل تقرير شامل لتحليل السوق',
      examples: 'حط تحليل المنافسين، الفئات المستهدفة، استراتيجية الأسعار',
      output: 'ملخص تنفيذي مع توصيات قابلة للتنفيذ',
      constraints: 'حد أقصى صفحتين، ركز على الرؤى المستندة للبيانات'
    },
    MICRO: {
      message: 'حسّن الاحتفاظ بالزباين',
      intention: 'حدد العوامل الرئيسية اللي بتأثر على ولاء الزباين',
      context: 'شركة SaaS فيها 10,000 مستخدم نشط',
      rhythm: 'احترافي، مستند للبيانات، قابل للتنفيذ',
      output: 'قائمة مرتبة لاستراتيجيات الاحتفاظ مع التأثير المتوقع'
    },
    COSTAR: {
      context: 'صاحب بزنس صغير بيعاني من التواجد على السوشيال ميديا',
      offer: 'تقويم محتوى السوشيال ميديا للشهر الجاي',
      style: 'كاجوال، جذاب، متوافق مع البراند',
      target: 'أصحاب البزنس الصغير من سن 30-50',
      action: 'اعمل خطة محتوى لمدة 30 يوم مع أفكار البوستات والتوقيت',
      result: 'زيادة التفاعل ونمو الفولوورز'
    }
  }
};
