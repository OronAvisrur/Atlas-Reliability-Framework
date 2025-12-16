import axios from 'axios';
import { register, login, logout, getToken, getUser, isAuthenticated, setAuthHeader } from '../authService';
import api from '../api';

jest.mock('axios');

describe('AuthService', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    localStorage.clear();
  });

  describe('register', () => {
    it('should register user successfully', async () => {
      const mockResponse = { id: 1, username: 'testuser', is_active: true };
      api.post = jest.fn().mockResolvedValue({ data: mockResponse });

      const result = await register('testuser', 'password123');

      expect(api.post).toHaveBeenCalledWith('/auth/register', {
        username: 'testuser',
        password: 'password123'
      });
      expect(result).toEqual(mockResponse);
    });

    it('should handle registration error', async () => {
      const error = new Error('Username already exists');
      api.post = jest.fn().mockRejectedValue(error);

      await expect(register('testuser', 'password123')).rejects.toThrow('Username already exists');
    });
  });

  describe('login', () => {
    it('should login user and store token', async () => {
      const mockResponse = { access_token: 'test-token', token_type: 'bearer' };
      api.post = jest.fn().mockResolvedValue({ data: mockResponse });

      const result = await login('testuser', 'password123');

      expect(api.post).toHaveBeenCalledWith('/auth/login', {
        username: 'testuser',
        password: 'password123'
      });
      expect(localStorage.getItem('atlas_token')).toBe('test-token');
      expect(localStorage.getItem('atlas_user')).toBe('testuser');
      expect(result).toEqual(mockResponse);
    });

    it('should handle login error', async () => {
      const error = new Error('Invalid credentials');
      api.post = jest.fn().mockRejectedValue(error);

      await expect(login('testuser', 'wrongpass')).rejects.toThrow('Invalid credentials');
    });
  });

  describe('logout', () => {
    it('should clear stored credentials', () => {
      localStorage.setItem('atlas_token', 'test-token');
      localStorage.setItem('atlas_user', 'testuser');

      logout();

      expect(localStorage.getItem('atlas_token')).toBeNull();
      expect(localStorage.getItem('atlas_user')).toBeNull();
    });
  });

  describe('getToken', () => {
    it('should return stored token', () => {
      localStorage.setItem('atlas_token', 'test-token');

      const token = getToken();

      expect(token).toBe('test-token');
    });

    it('should return null if no token', () => {
      const token = getToken();

      expect(token).toBeNull();
    });
  });

  describe('getUser', () => {
    it('should return stored username', () => {
      localStorage.setItem('atlas_user', 'testuser');

      const user = getUser();

      expect(user).toBe('testuser');
    });
  });

  describe('isAuthenticated', () => {
    it('should return true if token exists', () => {
      localStorage.setItem('atlas_token', 'test-token');

      const result = isAuthenticated();

      expect(result).toBe(true);
    });

    it('should return false if no token', () => {
      const result = isAuthenticated();

      expect(result).toBe(false);
    });
  });

  describe('setAuthHeader', () => {
    it('should set Authorization header when token provided', () => {
      setAuthHeader('test-token');

      expect(api.defaults.headers.common['Authorization']).toBe('Bearer test-token');
    });

    it('should remove Authorization header when token is null', () => {
      api.defaults.headers.common['Authorization'] = 'Bearer old-token';

      setAuthHeader(null);

      expect(api.defaults.headers.common['Authorization']).toBeUndefined();
    });
  });
});
