import React, { createContext, useContext, useState, useEffect } from 'react';
import { UserProfile } from '../types';
import { api } from '../services/api';

interface AuthContextType {
  user: UserProfile | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email?: string, password?: string) => Promise<void>;
  signup: (name: string, email: string, password: string, careerGoal?: string) => Promise<void>;
  logout: () => void;
  updateUser: (updated: Partial<UserProfile>) => void;
  addPoints: (amount: number) => void;
  incrementStreak: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<UserProfile | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check local storage or auto-initialize with demo user
    const saved = localStorage.getItem('vizag_user');
    if (saved) {
      try {
        setUser(JSON.parse(saved));
      } catch {
        // Fall back to demo login
        loginDemo();
      }
    } else {
      loginDemo();
    }
    setIsLoading(false);
  }, []);

  const loginDemo = async () => {
    try {
      const data = await api.login();
      setUser(data.user);
      localStorage.setItem('vizag_user', JSON.stringify(data.user));
    } catch (e) {
      console.error(e);
    }
  };

  const login = async (email?: string, password?: string) => {
    const data = await api.login(email, password);
    setUser(data.user);
    localStorage.setItem('vizag_user', JSON.stringify(data.user));
    if (data.access_token) {
      localStorage.setItem('vizag_token', data.access_token);
    }
  };

  const signup = async (name: string, email: string, password: string, careerGoal = 'AI Engineer') => {
    const data = await api.signup(name, email, password, careerGoal);
    setUser(data.user);
    localStorage.setItem('vizag_user', JSON.stringify(data.user));
    if (data.access_token) {
      localStorage.setItem('vizag_token', data.access_token);
    }
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('vizag_user');
  };

  const updateUser = (updated: Partial<UserProfile>) => {
    setUser(prev => {
      if (!prev) return null;
      const next = { ...prev, ...updated };
      localStorage.setItem('vizag_user', JSON.stringify(next));
      return next;
    });
  };

  const addPoints = (amount: number) => {
    setUser(prev => {
      if (!prev) return null;
      const next = { ...prev, points: prev.points + amount };
      localStorage.setItem('vizag_user', JSON.stringify(next));
      return next;
    });
  };

  const incrementStreak = () => {
    setUser(prev => {
      if (!prev) return null;
      const next = { ...prev, streak: prev.streak + 1 };
      localStorage.setItem('vizag_user', JSON.stringify(next));
      return next;
    });
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: !!user,
        isLoading,
        login,
        signup,
        logout,
        updateUser,
        addPoints,
        incrementStreak
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within an AuthProvider');
  return context;
};
