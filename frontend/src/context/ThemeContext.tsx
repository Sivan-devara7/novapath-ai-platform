import React, { createContext, useContext, useEffect, useState } from 'react';

export type ThemeId = 'cyber-aurora' | 'cosmic-nebula' | 'nordic-frost' | 'sunset-horizon' | 'midnight-nova';

export interface ThemeMeta {
  id: ThemeId;
  name: string;
  mode: 'dark' | 'light';
  tagline: string;
  primaryColor: string;
  secondaryColor: string;
  gradient: string;
  badge: string;
}

export const THEMES: ThemeMeta[] = [
  {
    id: 'cyber-aurora',
    name: 'Cyber Aurora',
    mode: 'dark',
    tagline: 'Neon Emerald & Electric Cyan',
    primaryColor: '#10b981',
    secondaryColor: '#06b6d4',
    gradient: 'linear-gradient(135deg, #06b6d4 0%, #10b981 50%, #3b82f6 100%)',
    badge: 'DEFAULT',
  },
  {
    id: 'cosmic-nebula',
    name: 'Cosmic Nebula',
    mode: 'dark',
    tagline: 'Royal Violet & Neon Magenta',
    primaryColor: '#a855f7',
    secondaryColor: '#ec4899',
    gradient: 'linear-gradient(135deg, #a855f7 0%, #ec4899 50%, #f43f5e 100%)',
    badge: 'DARK',
  },
  {
    id: 'nordic-frost',
    name: 'Nordic Frost',
    mode: 'light',
    tagline: 'Arctic Pearl & Ocean Sapphire',
    primaryColor: '#0284c7',
    secondaryColor: '#0d9488',
    gradient: 'linear-gradient(135deg, #0284c7 0%, #2563eb 50%, #4f46e5 100%)',
    badge: 'LIGHT',
  },
  {
    id: 'sunset-horizon',
    name: 'Sunset Horizon',
    mode: 'light',
    tagline: 'Warm Sand, Coral & Amber Gold',
    primaryColor: '#f43f5e',
    secondaryColor: '#f59e0b',
    gradient: 'linear-gradient(135deg, #f43f5e 0%, #f59e0b 50%, #fbbf24 100%)',
    badge: 'LIGHT',
  },
  {
    id: 'midnight-nova',
    name: 'Midnight Nova',
    mode: 'dark',
    tagline: 'Deep Space & Sky Blue',
    primaryColor: '#38bdf8',
    secondaryColor: '#818cf8',
    gradient: 'linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%)',
    badge: 'CLASSIC',
  },
];

interface ThemeContextType {
  theme: ThemeId;
  themeMeta: ThemeMeta;
  setTheme: (theme: ThemeId) => void;
  availableThemes: ThemeMeta[];
  isDark: boolean;
  toggleQuickMode: () => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

const STORAGE_KEY = 'novapath_theme';
const DEFAULT_THEME: ThemeId = 'cyber-aurora';

export const ThemeProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [theme, setThemeState] = useState<ThemeId>(() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY) as ThemeId;
      if (saved && THEMES.some(t => t.id === saved)) {
        return saved;
      }
    } catch {
      // Ignore localStorage read errors
    }
    return DEFAULT_THEME;
  });

  const currentMeta = THEMES.find(t => t.id === theme) || THEMES[0];
  const isDark = currentMeta.mode === 'dark';

  const setTheme = (newTheme: ThemeId) => {
    setThemeState(newTheme);
    try {
      localStorage.setItem(STORAGE_KEY, newTheme);
    } catch {
      // Ignore localStorage write errors
    }
  };

  const toggleQuickMode = () => {
    // If dark, switch to the primary light theme (nordic-frost)
    // If light, switch to the default dark theme (cyber-aurora)
    if (isDark) {
      setTheme('nordic-frost');
    } else {
      setTheme('cyber-aurora');
    }
  };

  useEffect(() => {
    const root = document.documentElement;
    root.setAttribute('data-theme', theme);
    if (isDark) {
      root.classList.add('dark');
      root.classList.remove('light');
    } else {
      root.classList.add('light');
      root.classList.remove('dark');
    }
  }, [theme, isDark]);

  return (
    <ThemeContext.Provider
      value={{
        theme,
        themeMeta: currentMeta,
        setTheme,
        availableThemes: THEMES,
        isDark,
        toggleQuickMode,
      }}
    >
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = (): ThemeContextType => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};
