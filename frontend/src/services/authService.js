import api from './api';

const TOKEN_KEY = 'atlas_token';
const USER_KEY = 'atlas_user';

export const register = async (username, password) => {
  const response = await api.post('/api/auth/register', {
    username,
    password
  });
  return response.data;
};

export const login = async (username, password) => {
  const response = await api.post('/api/auth/login', {
    username,
    password
  });
  
  const { access_token } = response.data;
  localStorage.setItem(TOKEN_KEY, access_token);
  localStorage.setItem(USER_KEY, username);
  
  return response.data;
};

export const logout = () => {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
};

export const getToken = () => {
  return localStorage.getItem(TOKEN_KEY);
};

export const getUser = () => {
  return localStorage.getItem(USER_KEY);
};

export const isAuthenticated = () => {
  return !!getToken();
};

export const setAuthHeader = (token) => {
  if (token) {
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  } else {
    delete api.defaults.headers.common['Authorization'];
  }
};
