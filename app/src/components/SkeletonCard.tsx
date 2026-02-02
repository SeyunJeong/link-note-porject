import React, { useEffect, useRef } from 'react';
import { View, StyleSheet, Animated } from 'react-native';

export const SkeletonCard: React.FC = () => {
  const shimmerAnim = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    const shimmerLoop = Animated.loop(
      Animated.sequence([
        Animated.timing(shimmerAnim, {
          toValue: 1,
          duration: 1000,
          useNativeDriver: true,
        }),
        Animated.timing(shimmerAnim, {
          toValue: 0,
          duration: 1000,
          useNativeDriver: true,
        }),
      ])
    );
    shimmerLoop.start();

    return () => shimmerLoop.stop();
  }, [shimmerAnim]);

  const opacity = shimmerAnim.interpolate({
    inputRange: [0, 1],
    outputRange: [0.3, 0.7],
  });

  return (
    <View style={styles.card}>
      {/* Thumbnail placeholder */}
      <Animated.View style={[styles.thumbnail, { opacity }]} />

      <View style={styles.content}>
        {/* Title placeholder */}
        <Animated.View style={[styles.titleLine, { opacity }]} />
        <Animated.View style={[styles.titleLineShort, { opacity }]} />

        {/* Summary placeholder */}
        <Animated.View style={[styles.summaryLine, { opacity }]} />
        <Animated.View style={[styles.summaryLineShort, { opacity }]} />

        {/* Tags placeholder */}
        <View style={styles.tagsContainer}>
          <Animated.View style={[styles.tag, { opacity }]} />
          <Animated.View style={[styles.tag, { opacity }]} />
          <Animated.View style={[styles.tagShort, { opacity }]} />
        </View>

        {/* Date placeholder */}
        <Animated.View style={[styles.date, { opacity }]} />
      </View>
    </View>
  );
};

export const SkeletonList: React.FC<{ count?: number }> = ({ count = 3 }) => {
  return (
    <View style={styles.listContainer}>
      {Array.from({ length: count }).map((_, index) => (
        <SkeletonCard key={index} />
      ))}
    </View>
  );
};

const styles = StyleSheet.create({
  listContainer: {
    flex: 1,
    backgroundColor: '#f5f5f5',
    paddingVertical: 8,
  },
  card: {
    backgroundColor: '#fff',
    borderRadius: 12,
    marginHorizontal: 16,
    marginVertical: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
    overflow: 'hidden',
  },
  thumbnail: {
    width: '100%',
    height: 180,
    backgroundColor: '#e0e0e0',
  },
  content: {
    padding: 16,
  },
  titleLine: {
    width: '90%',
    height: 16,
    backgroundColor: '#e0e0e0',
    borderRadius: 4,
    marginBottom: 8,
  },
  titleLineShort: {
    width: '60%',
    height: 16,
    backgroundColor: '#e0e0e0',
    borderRadius: 4,
    marginBottom: 12,
  },
  summaryLine: {
    width: '100%',
    height: 14,
    backgroundColor: '#e0e0e0',
    borderRadius: 4,
    marginBottom: 6,
  },
  summaryLineShort: {
    width: '80%',
    height: 14,
    backgroundColor: '#e0e0e0',
    borderRadius: 4,
    marginBottom: 12,
  },
  tagsContainer: {
    flexDirection: 'row',
    marginBottom: 12,
  },
  tag: {
    width: 60,
    height: 24,
    backgroundColor: '#e0e0e0',
    borderRadius: 12,
    marginRight: 8,
  },
  tagShort: {
    width: 45,
    height: 24,
    backgroundColor: '#e0e0e0',
    borderRadius: 12,
    marginRight: 8,
  },
  date: {
    width: 80,
    height: 12,
    backgroundColor: '#e0e0e0',
    borderRadius: 4,
  },
});
