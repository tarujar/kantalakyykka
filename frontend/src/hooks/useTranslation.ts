import { translations } from '../translations/fi';

export function useTranslation() {
  const t = (key: string, params?: Record<string, string | number>) => {
    const keys = key.split('.');
    let value: any = translations;
    
    for (const k of keys) {
      value = value[k];
      if (!value) return key;
    }

    if (params) {
      return Object.entries(params).reduce(
        (str, [key, val]) => str.replace(`{{${key}}}`, val.toString()),
        value
      );
    }

    return value;
  };

  return { t };
} 