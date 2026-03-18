import { StyleSheet } from 'react-native';

import ParallaxScrollView from '@/components/parallax-scroll-view';
import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { useRiskData } from '@/hooks/useRiskData';

export default function HomeScreen() {
  const demoUserId = 1;
  const { loading, error, riskScore, prioritizedAlerts } = useRiskData(demoUserId);

  return (
    <ParallaxScrollView
      headerBackgroundColor={{ light: '#A1CEDC', dark: '#1D3D47' }}
      headerImage={<ThemedView />}>
      <ThemedView style={styles.titleContainer}>
        <ThemedText type="title">RiskRadar Stage 2</ThemedText>
      </ThemedView>
      <ThemedView style={styles.stepContainer}>
        <ThemedText type="subtitle">Personal Risk Snapshot</ThemedText>
        <ThemedText>Demo user ID: {demoUserId}</ThemedText>
        <ThemedText>
          Score: {riskScore ? `${riskScore.score} (${riskScore.level})` : 'Unavailable'}
        </ThemedText>
        {loading ? <ThemedText>Loading Stage 2 data...</ThemedText> : null}
        {error ? <ThemedText>{error}</ThemedText> : null}
      </ThemedView>

      <ThemedView style={styles.stepContainer}>
        <ThemedText type="subtitle">Top Prioritized Alerts</ThemedText>
        {prioritizedAlerts.length === 0 ? (
          <ThemedText>No prioritized alerts available yet.</ThemedText>
        ) : (
          prioritizedAlerts.slice(0, 5).map((alert) => (
            <ThemedView key={alert.id} style={styles.alertRow}>
              <ThemedText type="defaultSemiBold">{alert.title}</ThemedText>
              <ThemedText>
                {alert.urgency_label ?? 'low'} priority | score {alert.priority_score ?? 'n/a'}
              </ThemedText>
            </ThemedView>
          ))
        )}
      </ThemedView>
    </ParallaxScrollView>
  );
}

const styles = StyleSheet.create({
  titleContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  stepContainer: {
    gap: 8,
    marginBottom: 8,
  },
  alertRow: {
    paddingVertical: 6,
    borderBottomWidth: StyleSheet.hairlineWidth,
    borderBottomColor: '#9CA3AF',
  },
});
