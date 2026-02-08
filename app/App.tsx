import React, { useEffect, useRef } from 'react';
import { StatusBar } from 'expo-status-bar';
import { NavigationContainer, NavigationContainerRef } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import Toast from 'react-native-toast-message';
import { ShareIntentProvider, useShareIntent } from 'expo-share-intent';
import { HomeScreen } from './src/screens/HomeScreen';
import { SaveLinkScreen } from './src/screens/SaveLinkScreen';
import { LinkDetailScreen } from './src/screens/LinkDetailScreen';
import { Link } from './src/types/link';
import { linkApi } from './src/services/api';
import { showToast } from './src/utils/toast';

export type RootStackParamList = {
  Home: undefined;
  SaveLink: { url?: string } | undefined;
  LinkDetail: { link: Link };
};

const Stack = createNativeStackNavigator<RootStackParamList>();

const AppNavigator = () => {
  const { hasShareIntent, shareIntent, resetShareIntent } = useShareIntent();
  const navigationRef = useRef<NavigationContainerRef<RootStackParamList>>(null);

  useEffect(() => {
    if (hasShareIntent && shareIntent) {
      const sharedText = shareIntent.text || '';
      // URL 추출 (공유된 텍스트에서 URL 찾기)
      const urlMatch = sharedText.match(/https?:\/\/[^\s]+/);
      const url = urlMatch ? urlMatch[0] : sharedText.trim();

      if (url) {
        // 자동 저장 실행
        handleAutoSave(url);
      }
      resetShareIntent();
    }
  }, [hasShareIntent, shareIntent]);

  const handleAutoSave = async (url: string) => {
    showToast.info('저장 중...', url);
    try {
      const result = await linkApi.saveLink(url);
      showToast.success('저장 완료!', result.title);
    } catch (err: any) {
      const detail = err.response?.data?.detail || '';
      if (err.response?.status === 409) {
        showToast.info('이미 저장된 링크입니다.');
      } else {
        showToast.error('저장 실패', detail || '링크를 저장할 수 없습니다.');
      }
    }
  };

  return (
    <NavigationContainer ref={navigationRef}>
      <StatusBar style="auto" />
      <Stack.Navigator
        initialRouteName="Home"
        screenOptions={{
          headerStyle: {
            backgroundColor: '#fff',
          },
          headerTintColor: '#007AFF',
          headerTitleStyle: {
            fontWeight: '600',
          },
        }}
      >
        <Stack.Screen
          name="Home"
          component={HomeScreen}
          options={{
            title: '링크 노트',
          }}
        />
        <Stack.Screen
          name="SaveLink"
          component={SaveLinkScreen}
          options={{
            title: '링크 저장',
            presentation: 'modal',
          }}
        />
        <Stack.Screen
          name="LinkDetail"
          component={LinkDetailScreen}
          options={{
            title: '링크 상세',
          }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
};

export default function App() {
  return (
    <ShareIntentProvider>
      <AppNavigator />
      <Toast />
    </ShareIntentProvider>
  );
}
