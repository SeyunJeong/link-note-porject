import React from 'react';
import { View, Text, ScrollView, TouchableOpacity, StyleSheet } from 'react-native';
import { PLATFORM_CONFIG, CATEGORIES } from '../utils/platform';

interface FilterChipsProps {
  selectedMediaType: string | null;
  selectedCategory: string | null;
  onMediaTypeChange: (value: string | null) => void;
  onCategoryChange: (value: string | null) => void;
}

export const FilterChips: React.FC<FilterChipsProps> = ({
  selectedMediaType,
  selectedCategory,
  onMediaTypeChange,
  onCategoryChange,
}) => {
  const mediaTypes = Object.entries(PLATFORM_CONFIG);

  return (
    <View style={styles.container}>
      {/* 매체별 필터 */}
      <ScrollView
        horizontal
        showsHorizontalScrollIndicator={false}
        contentContainerStyle={styles.chipRow}
      >
        <TouchableOpacity
          style={[styles.chip, !selectedMediaType && styles.chipActive]}
          onPress={() => onMediaTypeChange(null)}
        >
          <Text style={[styles.chipText, !selectedMediaType && styles.chipTextActive]}>
            전체
          </Text>
        </TouchableOpacity>
        {mediaTypes.map(([key, config]) => (
          <TouchableOpacity
            key={key}
            style={[
              styles.chip,
              selectedMediaType === key && { backgroundColor: config.color },
            ]}
            onPress={() => onMediaTypeChange(selectedMediaType === key ? null : key)}
          >
            <Text
              style={[
                styles.chipText,
                selectedMediaType === key && styles.chipTextActive,
              ]}
            >
              {config.label}
            </Text>
          </TouchableOpacity>
        ))}
      </ScrollView>

      {/* 주제별 필터 */}
      <ScrollView
        horizontal
        showsHorizontalScrollIndicator={false}
        contentContainerStyle={styles.chipRow}
      >
        <TouchableOpacity
          style={[styles.chip, !selectedCategory && styles.chipActive]}
          onPress={() => onCategoryChange(null)}
        >
          <Text style={[styles.chipText, !selectedCategory && styles.chipTextActive]}>
            전체
          </Text>
        </TouchableOpacity>
        {CATEGORIES.map((cat) => (
          <TouchableOpacity
            key={cat}
            style={[styles.chip, selectedCategory === cat && styles.chipActive]}
            onPress={() => onCategoryChange(selectedCategory === cat ? null : cat)}
          >
            <Text
              style={[
                styles.chipText,
                selectedCategory === cat && styles.chipTextActive,
              ]}
            >
              {cat}
            </Text>
          </TouchableOpacity>
        ))}
      </ScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#f5f5f5',
    paddingTop: 8,
    gap: 6,
  },
  chipRow: {
    paddingHorizontal: 16,
    gap: 8,
    paddingBottom: 4,
  },
  chip: {
    paddingHorizontal: 14,
    paddingVertical: 7,
    borderRadius: 16,
    backgroundColor: '#fff',
    borderWidth: 1,
    borderColor: '#ddd',
  },
  chipActive: {
    backgroundColor: '#007AFF',
    borderColor: '#007AFF',
  },
  chipText: {
    fontSize: 13,
    color: '#555',
    fontWeight: '500',
  },
  chipTextActive: {
    color: '#fff',
    fontWeight: '600',
  },
});
