const IS_DEV = process.env.APP_VARIANT === 'development';
const IS_PREVIEW = process.env.APP_VARIANT === 'preview';

const getAppName = () => {
  if (IS_DEV) return '링크 노트 (Dev)';
  if (IS_PREVIEW) return '링크 노트 (Preview)';
  return '링크 노트';
};

export default {
  expo: {
    name: getAppName(),
    slug: 'link-note',
    version: '1.0.0',
    orientation: 'portrait',
    icon: './assets/icon.png',
    userInterfaceStyle: 'automatic',
    newArchEnabled: false,
    splash: {
      image: './assets/splash-icon.png',
      resizeMode: 'contain',
      backgroundColor: '#ffffff',
    },
    ios: {
      supportsTablet: true,
      bundleIdentifier: 'com.linknote.app',
      infoPlist: {
        CFBundleURLTypes: [
          {
            CFBundleURLSchemes: ['linknote'],
          },
        ],
        NSAppTransportSecurity: {
          NSAllowsArbitraryLoads: true,
        },
      },
    },
    android: {
      adaptiveIcon: {
        foregroundImage: './assets/adaptive-icon.png',
        backgroundColor: '#ffffff',
      },
      // edgeToEdgeEnabled: true, // Expo Go에서 비활성화
      package: 'com.linknote.app',
      intentFilters: [
        {
          action: 'android.intent.action.SEND',
          category: ['android.intent.category.DEFAULT'],
          data: [
            {
              mimeType: 'text/plain',
            },
          ],
        },
      ],
    },
    web: {
      favicon: './assets/favicon.png',
    },
    scheme: 'linknote',
    extra: {
      apiBaseUrl: process.env.API_BASE_URL || 'http://localhost:8000/api',
      eas: {
        projectId: 'your-eas-project-id',
      },
    },
    // Expo Go 테스트 시 plugins 비활성화 (Development Build에서만 사용)
    // plugins: [
    //   [
    //     'expo-share-intent',
    //     {
    //       androidIntentFilters: ['text/*'],
    //       iosShareExtensionName: 'LinkNoteShare',
    //       iosActivationRules: {
    //         NSExtensionActivationSupportsText: true,
    //         NSExtensionActivationSupportsWebURLWithMaxCount: 1,
    //       },
    //     },
    //   ],
    // ],
  },
};
