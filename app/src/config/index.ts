import Constants from 'expo-constants';

interface AppConfig {
  apiBaseUrl: string;
}

const getConfig = (): AppConfig => {
  const extra = Constants.expoConfig?.extra as { apiBaseUrl?: string } | undefined;

  return {
    apiBaseUrl: extra?.apiBaseUrl || 'http://localhost:8000/api',
  };
};

export const config = getConfig();
