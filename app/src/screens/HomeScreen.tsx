import React, { useState, useCallback } from 'react';
import {
  View,
  FlatList,
  StyleSheet,
  Text,
  RefreshControl,
  TouchableOpacity,
} from 'react-native';
import { useNavigation, useFocusEffect } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { LinkCard } from '../components/LinkCard';
import { SkeletonList } from '../components/SkeletonCard';
import { linkApi } from '../services/api';
import { Link } from '../types/link';
import { RootStackParamList } from '../../App';

type HomeScreenNavigationProp = NativeStackNavigationProp<RootStackParamList, 'Home'>;

export const HomeScreen: React.FC = () => {
  const navigation = useNavigation<HomeScreenNavigationProp>();
  const [links, setLinks] = useState<Link[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchLinks = useCallback(async () => {
    try {
      setError(null);
      const response = await linkApi.getLinks();
      setLinks(response.links);
    } catch (err) {
      setError('링크를 불러올 수 없습니다.');
      console.error('Failed to fetch links:', err);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, []);

  // 화면이 포커스될 때마다 목록 새로고침
  useFocusEffect(
    useCallback(() => {
      fetchLinks();
    }, [fetchLinks])
  );

  const handleRefresh = () => {
    setRefreshing(true);
    fetchLinks();
  };

  if (loading) {
    return <SkeletonList count={3} />;
  }

  if (error) {
    return (
      <View style={styles.centerContainer}>
        <Text style={styles.errorText}>{error}</Text>
      </View>
    );
  }

  if (links.length === 0) {
    return (
      <View style={styles.centerContainer}>
        <Text style={styles.emptyText}>저장된 링크가 없습니다.</Text>
        <Text style={styles.emptySubText}>
          + 버튼을 눌러 링크를 저장해보세요.
        </Text>
        <TouchableOpacity style={styles.fab} onPress={() => navigation.navigate('SaveLink')}>
          <Text style={styles.fabText}>+</Text>
        </TouchableOpacity>
      </View>
    );
  }

  const handleAddLink = () => {
    navigation.navigate('SaveLink');
  };

  return (
    <View style={styles.container}>
      <FlatList
        data={links}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (
          <LinkCard
            link={item}
            onPress={() => navigation.navigate('LinkDetail', { link: item })}
          />
        )}
        contentContainerStyle={styles.listContent}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={handleRefresh} />
        }
      />
      <TouchableOpacity style={styles.fab} onPress={handleAddLink}>
        <Text style={styles.fabText}>+</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  centerContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f5f5f5',
    padding: 20,
  },
  listContent: {
    paddingVertical: 8,
  },
  errorText: {
    fontSize: 16,
    color: '#ff3b30',
    textAlign: 'center',
  },
  emptyText: {
    fontSize: 18,
    color: '#1a1a1a',
    fontWeight: '600',
    marginBottom: 8,
  },
  emptySubText: {
    fontSize: 14,
    color: '#666',
    textAlign: 'center',
  },
  fab: {
    position: 'absolute',
    right: 20,
    bottom: 30,
    width: 56,
    height: 56,
    borderRadius: 28,
    backgroundColor: '#007AFF',
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 4,
    elevation: 8,
  },
  fabText: {
    fontSize: 28,
    color: '#fff',
    fontWeight: '300',
    marginTop: -2,
  },
});
