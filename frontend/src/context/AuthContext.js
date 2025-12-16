import React, { createContext, useContext, useState, useEffect } from 'react';
import { login as loginService, logout as logoutService, getUser, getToken, isAuthenticated as checkAuth, setAuthHeader } from '../services/authService';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = getToken();
    const username = getUser();
    
    if (token && username) {
      setUser(username);
      setAuthHeader(token);
    }
    
    setLoading(false);
  }, []);

  const login = async (username, password) => {
    const response = await loginService(username, password);
    setUser(username);
    setAuthHeader(response.access_token);
    return response;
  };

  const logout = () => {
    logoutService();
    setUser(null);
    setAuthHeader(null);
  };

  const isAuthenticated = () => {
    return checkAuth();
  };

  const value = {
    user,
    login,
    logout,
    isAuthenticated,
    loading
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};
