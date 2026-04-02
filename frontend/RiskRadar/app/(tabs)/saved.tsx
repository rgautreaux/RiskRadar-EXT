import React, { useState, useCallback } from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  FlatList,
  TouchableOpacity,
  Platform,
  StatusBar,
  ActivityIndicator,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useRouter, useFocusEffect } from 'expo-router';
import { Colors } from '@/constants/theme';
import { useColorScheme } from '@/hooks/use-color-scheme';
import { useAuth } from '@/contexts/auth-context';
import { apiFetch } from '@/utils/api';

interface SavedDestination {
  id: number;
  city: string;
  state: string | null;
  zip_code: string | null;
  latitude: number;
  longitude: number;
  created_at: string;
}

export default function SavedScreen() {
  const router = useRouter();
  const scheme = useColorScheme() ?? 'light';
  const palette = Colors[scheme];
  const styles = getStyles(palette);
  const { isLoggedIn } = useAuth();

  const [destinations, setDestinations] = useState<SavedDestination[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchDestinations = useCallback(async () => {
    if (!isLoggedIn) { setLoading(false); return; }
    try {
      const data = await apiFetch<SavedDestination[]>('/users/destinations');
      setDestinations(data);
    } catch {
      // Not logged in or network error
    } finally {
      setLoading(false);
    }
  }, [isLoggedIn]);

  // Refresh every time the tab is focused
  useFocusEffect(
    useCallback(() => {
      setLoading(true);
      fetchDestinations();
    }, [fetchDestinations])
  );

  const handleDelete = async (id: number) => {
    try {
      await apiFetch(`/users/destinations/${id}`, { method: 'DELETE' });
      setDestinations((prev) => prev.filter((d) => d.id !== id));
    } catch {
      // ignore
    }
  };

  if (!isLoggedIn) {
    return (
      <SafeAreaView style={styles.safeArea}>
        <StatusBar barStyle={scheme === 'dark' ? 'light-content' : 'dark-content'} backgroundColor={palette.background} />
        <View style={styles.emptyContainer}>
          <Ionicons name="bookmark-outline" size={64} color={palette.textSecondary} />
          <Text style={styles.emptyTitle}>Save Your Destinations</Text>
          <Text style={styles.emptySubtitle}>Log in to save and quickly access your favorite travel destinations.</Text>
          <TouchableOpacity style={styles.loginButton} onPress={() => router.push('/auth/login')}>
            <Text style={styles.loginButtonText}>Log In</Text>
          </TouchableOpacity>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.safeArea}>
      <StatusBar barStyle={scheme === 'dark' ? 'light-content' : 'dark-content'} backgroundColor={palette.background} />

      <View style={styles.header}>
        <Text style={styles.headerTitle}>Saved Destinations</Text>
      </View>

      {loading ? (
        <ActivityIndicator size="large" color={palette.primary} style={{ paddingVertical: 40 }} />
      ) : destinations.length === 0 ? (
        <View style={styles.emptyContainer}>
          <Ionicons name="bookmark-outline" size={64} color={palette.textSecondary} />
          <Text style={styles.emptyTitle}>No Saved Destinations</Text>
          <Text style={styles.emptySubtitle}>Search for a city and tap the bookmark icon to save it here.</Text>
        </View>
      ) : (
        <FlatList
          data={destinations}
          keyExtractor={(item) => item.id.toString()}
          contentContainerStyle={styles.listContent}
          renderItem={({ item }) => (
            <TouchableOpacity
              style={styles.card}
              onPress={() =>
                router.push({
                  pathname: '/main/weather-report',
                  params: { query: item.zip_code ?? `${item.city}, ${item.state}` },
                })
              }
            >
              <View style={styles.cardLeft}>
                <Ionicons name="location" size={24} color={palette.primary} />
                <View style={styles.cardText}>
                  <Text style={styles.cardCity}>
                    {item.city}{item.state ? `, ${item.state}` : ''}
                  </Text>
                  {item.zip_code && (
                    <Text style={styles.cardZip}>{item.zip_code}</Text>
                  )}
                </View>
              </View>
              <TouchableOpacity
                style={styles.deleteButton}
                onPress={() => handleDelete(item.id)}
              >
                <Ionicons name="trash-outline" size={20} color={palette.danger} />
              </TouchableOpacity>
            </TouchableOpacity>
          )}
        />
      )}
    </SafeAreaView>
  );
}

function getStyles(palette: typeof Colors.light) {
  return StyleSheet.create({
    safeArea: {
      flex: 1,
      backgroundColor: palette.background,
    },
    header: {
      paddingHorizontal: 24,
      paddingTop: Platform.OS === 'android' ? 16 : 0,
      paddingBottom: 16,
      backgroundColor: palette.card,
      borderBottomWidth: 1,
      borderBottomColor: palette.border,
    },
    headerTitle: {
      fontSize: 24,
      fontWeight: '700',
      color: palette.text,
    },
    listContent: {
      padding: 24,
      paddingBottom: 40,
    },
    card: {
      flexDirection: 'row',
      alignItems: 'center',
      justifyContent: 'space-between',
      backgroundColor: palette.card,
      borderRadius: 16,
      padding: 16,
      marginBottom: 12,
      borderWidth: 1,
      borderColor: palette.border,
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 2 },
      shadowOpacity: 0.05,
      shadowRadius: 6,
      elevation: 2,
    },
    cardLeft: {
      flexDirection: 'row',
      alignItems: 'center',
      flex: 1,
    },
    cardText: {
      marginLeft: 12,
      flex: 1,
    },
    cardCity: {
      fontSize: 16,
      fontWeight: '600',
      color: palette.text,
    },
    cardZip: {
      fontSize: 13,
      color: palette.textSecondary,
      marginTop: 2,
    },
    deleteButton: {
      width: 40,
      height: 40,
      justifyContent: 'center',
      alignItems: 'center',
    },
    emptyContainer: {
      flex: 1,
      justifyContent: 'center',
      alignItems: 'center',
      padding: 40,
    },
    emptyTitle: {
      fontSize: 20,
      fontWeight: '700',
      color: palette.text,
      marginTop: 16,
      marginBottom: 8,
    },
    emptySubtitle: {
      fontSize: 14,
      color: palette.textSecondary,
      textAlign: 'center',
      lineHeight: 20,
    },
    loginButton: {
      marginTop: 24,
      backgroundColor: palette.primary,
      paddingHorizontal: 32,
      paddingVertical: 14,
      borderRadius: 16,
    },
    loginButtonText: {
      color: '#FFFFFF',
      fontSize: 16,
      fontWeight: '700',
    },
  });
}
