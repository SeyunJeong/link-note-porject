declare module 'expo-constants' {
  interface ExpoConfig {
    name?: string;
    slug?: string;
    version?: string;
    extra?: Record<string, unknown>;
  }

  interface Constants {
    expoConfig?: ExpoConfig | null;
    manifest?: unknown;
    systemFonts?: string[];
    deviceName?: string;
    isDevice?: boolean;
    platform?: {
      ios?: { buildNumber?: string };
      android?: { versionCode?: number };
    };
  }

  const Constants: Constants;
  export default Constants;
}
