import React from 'react';
import { StatusBar } from 'expo-status-bar';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import Toast from 'react-native-toast-message';
import { HomeScreen } from './src/screens/HomeScreen';
import { SaveLinkScreen } from './src/screens/SaveLinkScreen';
import { LinkDetailScreen } from './src/screens/LinkDetailScreen';
import { Link } from './src/types/link';

export type RootStackParamList = {
  Home: undefined;
  SaveLink: { url?: string } | undefined;
  LinkDetail: { link: Link };
};

const Stack = createNativeStackNavigator<RootStackParamList>();

// Expo Go 테스트용 (ShareIntent 비활성화)
// Development Build에서는 ShareIntentProvider 사용
const AppNavigator = () => {
  return (
    <NavigationContainer>
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
    <>
      <AppNavigator />
      <Toast />
    </>
  );
}
