import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  SafeAreaView,
  ScrollView,
  Platform,
  StatusBar,
} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Ionicons } from '@expo/vector-icons';
import { useRouter, Redirect } from 'expo-router';
import { Colors } from '@/constants/theme';
import { useColorScheme } from '@/hooks/use-color-scheme';
import { useAuth } from '@/contexts/auth-context';
import { apiFetch } from '@/utils/api';
import { StateView } from '@/components/ui/state-view';

interface AlertStats {
  total: number;
  by_type: Record<string, number>;
  by_severity: Record<string, number>;
}

interface Summary {
  id: number;
  title: string;
  content: string;
  summary_type: string;
  region: string | null;
  generated_at: string;
}

interface AutocompleteResult {
  label: string;
  city: string;
  state: string;
}

const DEMO_SETTINGS_KEY = 'riskradar_demo_settings';

export default function HomeScreen() {
  const router = useRouter();
  const scheme = useColorScheme() ?? 'light';
  const palette = Colors[scheme];
  const styles = getStyles(palette);
  const { user, isLoggedIn, isGuest } = useAuth();
  const [searchQuery, setSearchQuery] = useState(user?.zip_code ?? '');
  const [suggestions, setSuggestions] = useState<AutocompleteResult[]>([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [stats, setStats] = useState<AlertStats | null>(null);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [loadingStats, setLoadingStats] = useState(true);
  const [loadingSummary, setLoadingSummary] = useState(true);
  const [errorStats, setErrorStats] = useState<string | null>(null);
  const [errorSummary, setErrorSummary] = useState<string | null>(null);
  const shouldRedirect = !isLoggedIn && !isGuest;
  const autocompleteTimeout = React.useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    if (user?.zip_code) setSearchQuery(user.zip_code);
  }, [user?.zip_code]);

  useEffect(() => {
    if (shouldRedirect || user?.zip_code) {
      return;
    }

    (async () => {
      try {
        const stored = await AsyncStorage.getItem(DEMO_SETTINGS_KEY);
        if (!stored) {
          return;
        }

        const parsed = JSON.parse(stored) as { zipCode?: string };
        if (parsed.zipCode) {
          setSearchQuery(parsed.zipCode);
        }
      } catch {
        // Keep the dashboard usable even if saved demo settings cannot be restored.
      }
    })();
  }, [user?.zip_code, shouldRedirect]);

  // Autocomplete for city names (debounced)
  const handleSearchChange = (text: string) => {
    setSearchQuery(text);

    // Clear previous timeout
    if (autocompleteTimeout.current) {
      clearTimeout(autocompleteTimeout.current);
    }

    // Only autocomplete for non-zip text with 2+ chars
    const isZip = /^\d+$/.test(text);
    if (!isZip && text.length >= 2) {
      autocompleteTimeout.current = setTimeout(async () => {
        try {
          const data = await apiFetch<AutocompleteResult[]>(
            `/location/autocomplete?q=${encodeURIComponent(text)}`
          );
          setSuggestions(data);
          setShowSuggestions(data.length > 0);
        } catch {
          setSuggestions([]);
          setShowSuggestions(false);
        }
      }, 300);
    } else {
      setSuggestions([]);
      setShowSuggestions(false);
    }
  };

  const selectSuggestion = (suggestion: AutocompleteResult) => {
    setSearchQuery(suggestion.label);
    setSuggestions([]);
    setShowSuggestions(false);
    router.push({ pathname: '/main/weather-report', params: { q: suggestion.label } });
  };

  useEffect(() => {
    if (shouldRedirect) return;

    (async () => {
      try {
        setErrorStats(null);
        const data = await apiFetch<AlertStats>('/alerts/stats');
        setStats(data);
      } catch {
        setErrorStats('Failed to load risk assessment data');
      }
      finally { setLoadingStats(false); }
    })();

    (async () => {
      try {
        setErrorSummary(null);
        const data = await apiFetch<Summary | null>('/summaries/latest');
        setSummary(data);
      } catch {
        setErrorSummary('Failed to load latest summary');
      }
      finally { setLoadingSummary(false); }
    })();
  }, [shouldRedirect]);

  // Redirect to welcome if not logged in and not a guest
  if (shouldRedirect) {
    return <Redirect href="/welcome" />;
  }

  const handleSearch = () => {
    const trimmed = searchQuery.trim();
    if (trimmed.length < 2) return;
    setShowSuggestions(false);
    // If it's a 5-digit zip, pass as zipCode for backward compat; otherwise pass as q
    const isZip = /^\d{5}$/.test(trimmed);
    router.push({
      pathname: '/main/weather-report',
      params: isZip ? { zipCode: trimmed } : { q: trimmed },
    });
  };

  const displayName = isLoggedIn ? (user?.display_name ?? 'User') : 'Guest';

  return (
    <SafeAreaView style={styles.safeArea}>
      <StatusBar barStyle={scheme === 'dark' ? 'light-content' : 'dark-content'} backgroundColor={palette.background} />

      {/* Header */}
      <View style={styles.header}>
        <View>
          <Text style={styles.greeting}>Welcome, {displayName}</Text>
          <Text style={styles.headerSubtitle}>Stay ahead of the weather</Text>
        </View>
        <View style={styles.headerActions}>
          <TouchableOpacity
            style={styles.settingsButton}
            onPress={() => router.push('/main/settings')}
          >
            <Ionicons name="settings-outline" size={24} color={palette.textSecondary} />
          </TouchableOpacity>
          <TouchableOpacity
            style={styles.profileButton}
            onPress={() => !isLoggedIn ? router.push('/auth/login') : router.push('/main/settings')}
          >
            <Ionicons name={!isLoggedIn ? 'log-in-outline' : 'person-circle-outline'} size={28} color={palette.primary} />
          </TouchableOpacity>
        </View>
      </View>

      <ScrollView contentContainerStyle={styles.scrollContent} showsVerticalScrollIndicator={false}>
        {/* Search Section */}
        <View style={styles.searchSection}>
          <Text style={styles.sectionTitle}>Check Location Risk</Text>
          <Text style={styles.sectionSubtitle}>
            {!isLoggedIn
              ? 'Enter a city, state, or zip code to see current weather and risk reports.'
              : 'Showing your home location. Search another city or zip code to check another area.'}
          </Text>

          <View style={styles.searchContainer}>
            <View style={styles.inputWrapper}>
              <Ionicons name="location-outline" size={20} color={palette.textSecondary} style={styles.inputIcon} />
              <TextInput
                style={styles.input}
                placeholder="City, State or Zip Code"
                placeholderTextColor={palette.textSecondary}
                keyboardType="default"
                autoCapitalize="words"
                autoCorrect={false}
                value={searchQuery}
                onChangeText={handleSearchChange}
                onSubmitEditing={handleSearch}
                returnKeyType="search"
                onFocus={() => {
                  if (suggestions.length > 0) setShowSuggestions(true);
                }}
              />
              {searchQuery.length > 0 && (
                <TouchableOpacity onPress={() => { setSearchQuery(''); setSuggestions([]); setShowSuggestions(false); }}>
                  <Ionicons name="close-circle" size={20} color={palette.textSecondary} />
                </TouchableOpacity>
              )}
            </View>
            <TouchableOpacity
              style={[styles.searchButton, searchQuery.trim().length < 2 && styles.searchButtonDisabled]}
              onPress={handleSearch}
              disabled={searchQuery.trim().length < 2}
            >
              <Ionicons name="search" size={20} color={palette.white} />
            </TouchableOpacity>
          </View>

          {/* Autocomplete Suggestions */}
          {showSuggestions && suggestions.length > 0 && (
            <View style={styles.suggestionsContainer}>
              {suggestions.map((item, idx) => (
                <TouchableOpacity
                  key={`${item.label}-${idx}`}
                  style={[
                    styles.suggestionItem,
                    idx < suggestions.length - 1 && { borderBottomWidth: 1, borderBottomColor: palette.border },
                  ]}
                  onPress={() => selectSuggestion(item)}
                >
                  <Ionicons name="location" size={16} color={palette.primary} style={{ marginRight: 10 }} />
                  <Text style={styles.suggestionText}>{item.label}</Text>
                </TouchableOpacity>
              ))}
            </View>
          )}
        </View>

        {/* Latest Summary Card */}
        <TouchableOpacity
          style={styles.card}
          onPress={() => {
            const trimmed = searchQuery.trim();
            const isZip = /^\d{5}$/.test(trimmed);
            router.push({
              pathname: '/main/weather-report',
              params: isZip ? { zipCode: trimmed } : { q: trimmed || 'Unknown Location' },
            });
          }}
        >
          <View style={styles.cardHeader}>
            <View style={styles.cardIconBox}>
              <Ionicons name="partly-sunny" size={24} color="#F59E0B" />
            </View>
            <Text style={styles.cardTitle}>Latest Summary</Text>
          </View>

          <StateView
            state={loadingSummary ? 'loading' : errorSummary ? 'error' : summary ? 'success' : 'empty'}
            loadingText="Loading summary..."
            emptyText={searchQuery.trim().length >= 2 ? `No summary available for ${searchQuery}` : 'Enter a city or zip code to see summaries'}
            emptyIcon="document-outline"
            errorText={errorSummary || 'Failed to load summary'}
            onRetry={() => {
              setLoadingSummary(true);
              setErrorSummary(null);
              (async () => {
                try {
                  const data = await apiFetch<Summary | null>('/summaries/latest');
                  setSummary(data);
                } catch {
                  setErrorSummary('Failed to load latest summary');
                } finally {
                  setLoadingSummary(false);
                }
              })();
            }}
          >
            <View style={styles.summaryBox}>
              <Text style={styles.summaryTitle}>{summary?.title}</Text>
              <Text style={styles.summaryText} numberOfLines={3}>{summary?.content}</Text>
              <Text style={styles.summaryMeta}>
                Generated {summary ? new Date(summary.generated_at).toLocaleDateString() : ''}
              </Text>
            </View>
          </StateView>
        </TouchableOpacity>

        {/* Risk Assessment Card */}
        <View style={styles.card}>
          <View style={styles.cardHeader}>
            <View style={[styles.cardIconBox, { backgroundColor: '#FEE2E2' }]}>
              <Ionicons name="warning-outline" size={24} color={palette.danger} />
            </View>
            <Text style={styles.cardTitle}>Risk Assessment</Text>
          </View>

          <StateView
            state={loadingStats ? 'loading' : errorStats ? 'error' : stats ? 'success' : 'empty'}
            loadingText="Loading risk data..."
            emptyText="No risk data available"
            emptyIcon="stats-chart-outline"
            errorText={errorStats || 'Failed to load risk data'}
            onRetry={() => {
              setLoadingStats(true);
              setErrorStats(null);
              (async () => {
                try {
                  const data = await apiFetch<AlertStats>('/alerts/stats');
                  setStats(data);
                } catch {
                  setErrorStats('Failed to load risk assessment data');
                } finally {
                  setLoadingStats(false);
                }
              })();
            }}
          >
            <View style={styles.statsContainer}>
              <View style={styles.statRow}>
                <Text style={styles.statLabel}>Total Active Alerts</Text>
                <Text style={styles.statValue}>{stats?.total}</Text>
              </View>
              {stats && Object.entries(stats.by_severity).map(([severity, count]) => (
                <View key={severity} style={styles.statRow}>
                  <Text style={styles.statLabel}>{severity}</Text>
                  <Text style={styles.statValue}>{count}</Text>
                </View>
              ))}
            </View>
          </StateView>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

function getStyles(palette: typeof Colors.light | typeof Colors.dark) {
  return StyleSheet.create({
    safeArea: {
      flex: 1,
      backgroundColor: palette.background,
    },
    header: {
      flexDirection: 'row',
      justifyContent: 'space-between',
      alignItems: 'center',
      paddingHorizontal: 24,
      paddingTop: Platform.OS === 'android' ? 16 : 0,
      paddingBottom: 16,
      backgroundColor: palette.card,
      borderBottomWidth: 1,
      borderBottomColor: palette.border,
    },
    greeting: {
      fontSize: 24,
      fontWeight: '700',
      color: palette.text,
    },
    headerSubtitle: {
      fontSize: 14,
      color: palette.textSecondary,
      marginTop: 2,
    },
    headerActions: {
      flexDirection: 'row',
      alignItems: 'center',
    },
    settingsButton: {
      width: 44,
      height: 44,
      justifyContent: 'center',
      alignItems: 'center',
      marginRight: 8,
    },
    profileButton: {
      width: 44,
      height: 44,
      borderRadius: 22,
      backgroundColor: palette.secondary,
      justifyContent: 'center',
      alignItems: 'center',
    },
    scrollContent: {
      padding: 24,
      paddingBottom: 40,
    },
    searchSection: {
      marginBottom: 32,
    },
    sectionTitle: {
      fontSize: 20,
      fontWeight: '700',
      color: palette.text,
      marginBottom: 8,
    },
    sectionSubtitle: {
      fontSize: 14,
      color: palette.textSecondary,
      marginBottom: 16,
      lineHeight: 20,
    },
    searchContainer: {
      flexDirection: 'row',
      alignItems: 'center',
    },
    inputWrapper: {
      flex: 1,
      flexDirection: 'row',
      alignItems: 'center',
      backgroundColor: palette.card,
      borderWidth: 1,
      borderColor: palette.border,
      borderRadius: 16,
      height: 56,
      paddingHorizontal: 16,
      marginRight: 12,
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 1 },
      shadowOpacity: 0.05,
      shadowRadius: 2,
      elevation: 2,
    },
    inputIcon: {
      marginRight: 12,
    },
    input: {
      flex: 1,
      fontSize: 16,
      color: palette.text,
      height: '100%',
    },
    searchButton: {
      width: 56,
      height: 56,
      backgroundColor: palette.primary,
      borderRadius: 16,
      justifyContent: 'center',
      alignItems: 'center',
      shadowColor: palette.primary,
      shadowOffset: { width: 0, height: 4 },
      shadowOpacity: 0.3,
      shadowRadius: 4.65,
      elevation: 8,
    },
    searchButtonDisabled: {
      backgroundColor: palette.textSecondary,
      shadowOpacity: 0,
      elevation: 0,
    },
    suggestionsContainer: {
      marginTop: 8,
      backgroundColor: palette.card,
      borderRadius: 12,
      borderWidth: 1,
      borderColor: palette.border,
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 2 },
      shadowOpacity: 0.1,
      shadowRadius: 4,
      elevation: 4,
      overflow: 'hidden',
    },
    suggestionItem: {
      flexDirection: 'row',
      alignItems: 'center',
      paddingVertical: 12,
      paddingHorizontal: 16,
    },
    suggestionText: {
      fontSize: 15,
      color: palette.text,
    },
    card: {
      backgroundColor: palette.card,
      borderRadius: 24,
      padding: 20,
      marginBottom: 20,
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 4 },
      shadowOpacity: 0.05,
      shadowRadius: 12,
      elevation: 4,
      borderWidth: 1,
      borderColor: palette.border,
    },
    cardHeader: {
      flexDirection: 'row',
      alignItems: 'center',
      marginBottom: 16,
    },
    cardIconBox: {
      width: 48,
      height: 48,
      borderRadius: 16,
      backgroundColor: '#FEF3C7',
      justifyContent: 'center',
      alignItems: 'center',
      marginRight: 12,
    },
    cardTitle: {
      fontSize: 18,
      fontWeight: '700',
      color: palette.text,
    },
    summaryBox: {
      backgroundColor: palette.surfaceMuted,
      borderRadius: 16,
      padding: 16,
    },
    summaryTitle: {
      fontSize: 16,
      fontWeight: '600',
      color: palette.text,
      marginBottom: 8,
    },
    summaryText: {
      fontSize: 14,
      lineHeight: 20,
      color: palette.textSecondary,
    },
    summaryMeta: {
      fontSize: 12,
      color: palette.textSecondary,
      marginTop: 8,
    },
    statsContainer: {
      backgroundColor: palette.surfaceMuted,
      borderRadius: 16,
      padding: 16,
    },
    statRow: {
      flexDirection: 'row',
      justifyContent: 'space-between',
      paddingVertical: 8,
      borderBottomWidth: 1,
      borderBottomColor: palette.border,
    },
    statLabel: {
      fontSize: 14,
      color: palette.textSecondary,
      textTransform: 'capitalize',
    },
    statValue: {
      fontSize: 14,
      fontWeight: '700',
      color: palette.text,
    },
  });
}
