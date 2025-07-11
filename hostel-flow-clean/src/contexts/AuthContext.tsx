
import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { authAPI, getAuthToken, setAuthToken, removeAuthToken } from '@/services/api';

interface User {
  is_superuser: any;
  id: string;
  email: string;
  username: string;
  room_number: string;
  is_staff?: boolean;
  is_admin?: boolean;
  is_serviceprovider?: boolean;
}

interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  register: (userData: { email: string; password: string; username: string; room_number: string }) => Promise<void>;
  logout: () => void;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const token = getAuthToken();
    if (token) {
      loadUser();
    } else {
      setIsLoading(false);
    }
  }, []);

  const loadUser = async () => {
    try {
      const userData = await authAPI.getProfile();
      console.log(userData);
      setUser(userData);
    } catch (error) {
      console.error('Failed to load user:', error);
      removeAuthToken();
    } finally {
      setIsLoading(false);
    }
  };

  const login = async (email: string, password: string) => {
    const response = await authAPI.login({ email, password });
    setAuthToken(response.access_token);
    await loadUser();
  };

  const register = async (userData: { email: string; password: string; name: string; room_number: string }) => {
    const response = await authAPI.register(userData);
    setAuthToken(response.access_token);
    await loadUser();
  };

  const logout = () => {
    removeAuthToken();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, register, logout, isLoading }}>
      {children}
    </AuthContext.Provider>
  );
};
