import Constants from 'expo-constants';

interface AppConfig {
  apiBaseUrl: string;
  supabaseUrl: string;
  supabaseAnonKey: string;
}

const getConfig = (): AppConfig => {
  const extra = Constants.expoConfig?.extra as {
    apiBaseUrl?: string;
    supabaseUrl?: string;
    supabaseAnonKey?: string;
  } | undefined;

  return {
    apiBaseUrl: extra?.apiBaseUrl || 'http://localhost:8000/api',
    supabaseUrl: extra?.supabaseUrl || '',
    supabaseAnonKey: extra?.supabaseAnonKey || '',
  };
};

export const config = getConfig();
