import React from 'react';
import { View, ViewProps, ViewStyle } from 'react-native';

import { Colors, Shadows, Spacing } from '@/constants/theme';
import { useColorScheme } from '@/hooks/use-color-scheme';

export interface ThemedViewProps extends ViewProps {
  surface?: 'background' | 'card' | 'surfaceMuted';
  padding?: 'xs' | 'sm' | 'md' | 'lg' | 'xl';
  elevated?: boolean;
}

export function ThemedView({
  style,
  surface = 'background',
  elevated = false,
  padding,
  ...rest
}: ThemedViewProps) {
  const scheme = useColorScheme() ?? 'light';
  const palette = Colors[scheme];

  // Resolve background color based on surface semantic
  let backgroundColor: string;
  switch (surface) {
    case 'card':
      backgroundColor = palette.card;
      break;
    case 'surfaceMuted':
      backgroundColor = palette.surfaceMuted;
      break;
    case 'background':
    default:
      backgroundColor = palette.background;
      break;
  }

  // Build style array
  const viewStyle: ViewProps['style'] = [
    { backgroundColor },
    padding && getPaddingStyle(padding),
    elevated && Shadows.card,
    style,
  ];

  return (
    <View
      style={viewStyle}
      {...rest}
    />
  );
}

/**
 * Resolve padding values from preset keys.
 */
function getPaddingStyle(
  padding: 'xs' | 'sm' | 'md' | 'lg' | 'xl'
): ViewStyle {
  const paddingMap = {
    xs: Spacing.xs,
    sm: Spacing.sm,
    md: Spacing.md,
    lg: Spacing.lg,
    xl: Spacing.xl,
  };

  return {
    padding: paddingMap[padding],
  };
}
