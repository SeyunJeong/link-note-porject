import React, { useEffect, useRef, useState } from 'react';
import { View, Text, ActivityIndicator, StyleSheet, TouchableOpacity, Alert } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { NavigationContainer, NavigationContainerRef } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import Toast from 'react-native-toast-message';
import { ShareIntentProvider, useShareIntent } from 'expo-share-intent';
import { AuthProvider, useAuth } from './src/contexts/AuthContext';
import { HomeScreen } from './src/screens/HomeScreen';
import { SaveLinkScreen } from './src/screens/SaveLinkScreen';
import { LinkDetailScreen } from './src/screens/LinkDetailScreen';
import { LoginScreen } from './src/screens/LoginScreen';
import { SignUpScreen } from './src/screens/SignUpScreen';
import { Link } from './src/types/link';
import { linkApi } from './src/services/api';
import { showToast } from './src/utils/toast';

export type RootStackParamList = {
  Home: undefined;
  SaveLink: { url?: string } | undefined;
  LinkDetail: { link: Link };
};

export type AuthStackParamList = {
  Login: undefined;
  SignUp: undefined;
};

const AppStack = createNativeStackNavigator<RootStackParamList>();
const AuthStack = createNativeStackNavigator<AuthStackParamList>();

// 미인증 상태에서 공유된 URL을 임시 저장
let pendingShareUrl: string | null = null;

const AppNavigator = () => {
  const { hasShareIntent, shareIntent, resetShareIntent } = useShareIntent();
  const { signOut } = useAuth();
  const navigationRef = useRef<NavigationContainerRef<RootStackParamList>>(null);

  // 로그인 후 대기열에 있는 URL 처리
  useEffect(() => {
    if (pendingShareUrl) {
      const url = pendingShareUrl;
      pendingShareUrl = null;
      handleAutoSave(url);
    }
  }, []);

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
    <AppStack.Navigator
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
      <AppStack.Screen
        name="Home"
        component={HomeScreen}
        options={{
          title: '링크 노트',
          headerRight: () => (
            <TouchableOpacity
              onPress={() => {
                Alert.alert('로그아웃', '정말 로그아웃하시겠습니까?', [
                  { text: '취소', style: 'cancel' },
                  { text: '로그아웃', style: 'destructive', onPress: () => signOut() },
                ]);
              }}
            >
              <Text style={{ color: '#FF3B30', fontSize: 15 }}>로그아웃</Text>
            </TouchableOpacity>
          ),
        }}
      />
      <AppStack.Screen
        name="SaveLink"
        component={SaveLinkScreen}
        options={{
          title: '링크 저장',
          presentation: 'modal',
        }}
      />
      <AppStack.Screen
        name="LinkDetail"
        component={LinkDetailScreen}
        options={{
          title: '링크 상세',
        }}
      />
    </AppStack.Navigator>
  );
};

const ShareIntentCatcher = () => {
  const { hasShareIntent, shareIntent, resetShareIntent } = useShareIntent();

  useEffect(() => {
    if (hasShareIntent && shareIntent) {
      const sharedText = shareIntent.text || '';
      const urlMatch = sharedText.match(/https?:\/\/[^\s]+/);
      const url = urlMatch ? urlMatch[0] : sharedText.trim();

      if (url) {
        pendingShareUrl = url;
        showToast.info('로그인 후 저장됩니다', url);
      }
      resetShareIntent();
    }
  }, [hasShareIntent, shareIntent]);

  return null;
};

const AuthNavigator = () => {
  return (
    <>
      <ShareIntentCatcher />
      <AuthStack.Navigator
        screenOptions={{ headerShown: false }}
      >
        <AuthStack.Screen name="Login" component={LoginScreen} />
        <AuthStack.Screen
          name="SignUp"
          component={SignUpScreen}
          options={{
            headerShown: true,
            title: '',
            headerBackTitle: '뒤로',
            headerTintColor: '#007AFF',
          }}
        />
      </AuthStack.Navigator>
    </>
  );
};

const RootNavigator = () => {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#007AFF" />
      </View>
    );
  }

  return (
    <NavigationContainer>
      <StatusBar style="auto" />
      {user ? <AppNavigator /> : <AuthNavigator />}
    </NavigationContainer>
  );
};

export default function App() {
  return (
    <AuthProvider>
      <ShareIntentProvider>
        <RootNavigator />
        <Toast />
      </ShareIntentProvider>
    </AuthProvider>
  );
}

const styles = StyleSheet.create({
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#fff',
  },
});
