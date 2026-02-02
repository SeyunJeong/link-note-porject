import React, { useState } from 'react';
import {
  View,
  Text,
  Image,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Linking,
  Share,
  Alert,
  ActivityIndicator,
} from 'react-native';
import { useRoute, useNavigation, RouteProp } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { RootStackParamList } from '../../App';
import { linkApi } from '../services/api';
import { showToast } from '../utils/toast';

type LinkDetailScreenRouteProp = RouteProp<RootStackParamList, 'LinkDetail'>;
type LinkDetailScreenNavigationProp = NativeStackNavigationProp<RootStackParamList, 'LinkDetail'>;

export const LinkDetailScreen: React.FC = () => {
  const route = useRoute<LinkDetailScreenRouteProp>();
  const navigation = useNavigation<LinkDetailScreenNavigationProp>();
  const { link } = route.params;
  const [deleting, setDeleting] = useState(false);

  const handleOpenLink = () => {
    Linking.openURL(link.url);
  };

  const handleShare = async () => {
    try {
      await Share.share({
        message: `${link.title}\n${link.url}`,
        url: link.url,
      });
    } catch (error) {
      console.error('Share error:', error);
    }
  };

  const handleDelete = () => {
    Alert.alert(
      '링크 삭제',
      '이 링크를 삭제하시겠습니까?\n삭제된 링크는 복구할 수 없습니다.',
      [
        { text: '취소', style: 'cancel' },
        {
          text: '삭제',
          style: 'destructive',
          onPress: async () => {
            setDeleting(true);
            try {
              await linkApi.deleteLink(link.id);
              showToast.success('삭제 완료', '링크가 삭제되었습니다.');
              navigation.goBack();
            } catch (error: any) {
              const message = error.response?.data?.detail || '삭제에 실패했습니다.';
              showToast.error('삭제 실패', message);
              setDeleting(false);
            }
          },
        },
      ]
    );
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('ko-KR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <ScrollView style={styles.container}>
      {link.thumbnail && (
        <Image source={{ uri: link.thumbnail }} style={styles.thumbnail} />
      )}

      <View style={styles.content}>
        <Text style={styles.title}>{link.title}</Text>

        {link.category && (
          <View style={styles.categoryContainer}>
            <Text style={styles.categoryText}>{link.category}</Text>
          </View>
        )}

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>요약</Text>
          <Text style={styles.summary}>{link.summary}</Text>
        </View>

        {link.tags.length > 0 && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>태그</Text>
            <View style={styles.tagsContainer}>
              {link.tags.map((tag, index) => (
                <View key={index} style={styles.tag}>
                  <Text style={styles.tagText}>{tag}</Text>
                </View>
              ))}
            </View>
          </View>
        )}

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>저장일</Text>
          <Text style={styles.date}>{formatDate(link.created_at)}</Text>
        </View>

        <View style={styles.buttonContainer}>
          <TouchableOpacity style={styles.primaryButton} onPress={handleOpenLink}>
            <Text style={styles.primaryButtonText}>YouTube에서 보기</Text>
          </TouchableOpacity>

          <TouchableOpacity style={styles.secondaryButton} onPress={handleShare}>
            <Text style={styles.secondaryButtonText}>공유하기</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={styles.deleteButton}
            onPress={handleDelete}
            disabled={deleting}
          >
            {deleting ? (
              <ActivityIndicator color="#ff3b30" size="small" />
            ) : (
              <Text style={styles.deleteButtonText}>삭제하기</Text>
            )}
          </TouchableOpacity>
        </View>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  thumbnail: {
    width: '100%',
    height: 220,
    resizeMode: 'cover',
  },
  content: {
    padding: 20,
  },
  title: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#1a1a1a',
    marginBottom: 12,
    lineHeight: 30,
  },
  categoryContainer: {
    alignSelf: 'flex-start',
    backgroundColor: '#007AFF',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 16,
    marginBottom: 20,
  },
  categoryText: {
    fontSize: 13,
    color: '#fff',
    fontWeight: '600',
  },
  section: {
    marginBottom: 24,
  },
  sectionTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#666',
    marginBottom: 8,
    textTransform: 'uppercase',
    letterSpacing: 0.5,
  },
  summary: {
    fontSize: 16,
    color: '#333',
    lineHeight: 24,
  },
  tagsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  tag: {
    backgroundColor: '#e8e8e8',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 16,
    marginRight: 8,
    marginBottom: 8,
  },
  tagText: {
    fontSize: 14,
    color: '#555',
  },
  date: {
    fontSize: 15,
    color: '#666',
  },
  buttonContainer: {
    marginTop: 12,
    gap: 12,
  },
  primaryButton: {
    backgroundColor: '#FF0000',
    borderRadius: 12,
    padding: 16,
    alignItems: 'center',
  },
  primaryButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  secondaryButton: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#ddd',
  },
  secondaryButtonText: {
    color: '#333',
    fontSize: 16,
    fontWeight: '600',
  },
  deleteButton: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#ff3b30',
    marginTop: 8,
  },
  deleteButtonText: {
    color: '#ff3b30',
    fontSize: 16,
    fontWeight: '600',
  },
});
