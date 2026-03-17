// @ts-nocheck

import { useEffect, useMemo, useState } from 'react';

import {
  fetchPrioritizedAlerts,
  fetchRiskScore,
  type PrioritizedAlert,
  type RiskScoreResponse,
} from '@/services/riskService';

export type RiskDataState = {
  loading: boolean;
  error: string | null;
  riskScore: RiskScoreResponse | null;
  prioritizedAlerts: PrioritizedAlert[];
};

export function useRiskData(userId: number): RiskDataState {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [riskScore, setRiskScore] = useState<RiskScoreResponse | null>(null);
  const [prioritizedAlerts, setPrioritizedAlerts] = useState<PrioritizedAlert[]>([]);

  useEffect(() => {
    let active = true;

    async function load(): Promise<void> {
      setLoading(true);
      setError(null);

      try {
        const [score, alerts] = await Promise.all([
          fetchRiskScore(userId),
          fetchPrioritizedAlerts(userId),
        ]);

        if (!active) {
          return;
        }

        setRiskScore(score);
        setPrioritizedAlerts(alerts);
      } catch {
        if (!active) {
          return;
        }
        setError('Risk data is unavailable right now.');
      } finally {
        if (active) {
          setLoading(false);
        }
      }
    }

    load();

    return () => {
      active = false;
    };
  }, [userId]);

  return useMemo(
    () => ({
      loading,
      error,
      riskScore,
      prioritizedAlerts,
    }),
    [loading, error, riskScore, prioritizedAlerts],
  );
}
