import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  ActivityIndicator,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import { useNavigation, useRoute, RouteProp } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { linkApi } from '../services/api';
import { RootStackParamList } from '../../App';
import { showToast } from '../utils/toast';

type SaveLinkScreenNavigationProp = NativeStackNavigationProp<RootStackParamList, 'SaveLink'>;
type SaveLinkScreenRouteProp = RouteProp<RootStackParamList, 'SaveLink'>;

export const SaveLinkScreen: React.FC = () => {
  const navigation = useNavigation<SaveLinkScreenNavigationProp>();
  const route = useRoute<SaveLinkScreenRouteProp>();
  const [url, setUrl] = useState(route.params?.url || '');

  // params로 전달된 URL이 변경되면 업데이트
  useEffect(() => {
    if (route.params?.url) {
      setUrl(route.params.url);
    }
  }, [route.params?.url]);
  const [loading, setLoading] = useState(false);
  const [savedLink, setSavedLink] = useState<{
    title: string;
    summary: string;
  } | null>(null);

  const handleSave = async () => {
    if (!url.trim()) {
      showToast.error('URL을 입력해주세요.');
      return;
    }

    setLoading(true);
    setSavedLink(null);

    try {
      const result = await linkApi.saveLink(url.trim());
      setSavedLink({
        title: result.title,
        summary: result.summary,
      });
      showToast.success('저장 완료!', result.title);
      // 1.5초 후 홈 화면으로 자동 이동
      setTimeout(() => {
        navigation.goBack();
      }, 1500);
    } catch (err: any) {
      const message =
        err.response?.data?.detail || '링크를 저장할 수 없습니다.';
      showToast.error('링크 저장 실패', message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      <View style={styles.content}>
        <Text style={styles.title}>링크 저장하기</Text>
        <Text style={styles.subtitle}>유튜브 링크를 입력해주세요</Text>

        <TextInput
          style={styles.input}
          placeholder="https://youtube.com/watch?v=..."
          placeholderTextColor="#999"
          value={url}
          onChangeText={setUrl}
          autoCapitalize="none"
          autoCorrect={false}
          keyboardType="url"
          editable={!loading}
        />

        <TouchableOpacity
          style={[styles.button, loading && styles.buttonDisabled]}
          onPress={handleSave}
          disabled={loading}
        >
          {loading ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <Text style={styles.buttonText}>저장 및 요약</Text>
          )}
        </TouchableOpacity>

        {savedLink && (
          <View style={styles.resultContainer}>
            <Text style={styles.resultTitle}>저장 완료!</Text>
            <Text style={styles.resultLinkTitle}>{savedLink.title}</Text>
            <Text style={styles.resultSummary}>{savedLink.summary}</Text>
          </View>
        )}
      </View>
    </KeyboardAvoidingView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  content: {
    flex: 1,
    padding: 20,
    justifyContent: 'center',
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#1a1a1a',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: '#666',
    marginBottom: 24,
  },
  input: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    fontSize: 16,
    borderWidth: 1,
    borderColor: '#e0e0e0',
    marginBottom: 16,
  },
  button: {
    backgroundColor: '#007AFF',
    borderRadius: 12,
    padding: 16,
    alignItems: 'center',
  },
  buttonDisabled: {
    backgroundColor: '#999',
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  resultContainer: {
    marginTop: 24,
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    borderWidth: 1,
    borderColor: '#e0e0e0',
  },
  resultTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#34c759',
    marginBottom: 12,
  },
  resultLinkTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#1a1a1a',
    marginBottom: 8,
  },
  resultSummary: {
    fontSize: 14,
    color: '#666',
    lineHeight: 20,
  },
});
