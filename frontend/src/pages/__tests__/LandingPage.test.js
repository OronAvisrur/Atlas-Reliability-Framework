import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import LandingPage from '../LandingPage';
import * as api from '../../services/api';

jest.mock('../../services/api');

const renderWithRouter = (component) => {
  return render(<BrowserRouter>{component}</BrowserRouter>);
};

describe('LandingPage', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('Initial Render', () => {
    it('should render header with logo and auth buttons', () => {
      api.fetchMetrics.mockResolvedValue('');

      renderWithRouter(<LandingPage />);

      expect(screen.getByText('ATLAS')).toBeInTheDocument();
      expect(screen.getByText('RELIABILITY FRAMEWORK')).toBeInTheDocument();
      expect(screen.getByText('Login')).toBeInTheDocument();
      expect(screen.getByText('Register')).toBeInTheDocument();
    });

    it('should render hero section', () => {
      api.fetchMetrics.mockResolvedValue('');

      renderWithRouter(<LandingPage />);

      expect(screen.getByText('High Availability Book Search Service')).toBeInTheDocument();
      expect(screen.getByText('FastAPI + PostgreSQL + Ollama LLM + Kubernetes')).toBeInTheDocument();
    });

    it('should show loading state initially', () => {
      api.fetchMetrics.mockResolvedValue('');

      renderWithRouter(<LandingPage />);

      expect(screen.getByText('Loading metrics...')).toBeInTheDocument();
    });
  });

  describe('Metrics Loading', () => {
    it('should display metrics after successful fetch', async () => {
      const mockMetrics = 'http_requests_total 100\nactive_requests 5';
      api.fetchMetrics.mockResolvedValue(mockMetrics);

      renderWithRouter(<LandingPage />);

      await waitFor(() => {
        expect(screen.getByText('Total Requests')).toBeInTheDocument();
        expect(screen.getByText('Active Requests')).toBeInTheDocument();
      });
    });

    it('should display error message on fetch failure', async () => {
      api.fetchMetrics.mockRejectedValue(new Error('Network error'));

      renderWithRouter(<LandingPage />);

      await waitFor(() => {
        expect(screen.getByText('Failed to load metrics')).toBeInTheDocument();
      });
    });
  });

  describe('Features Section', () => {
    it('should render all feature cards', () => {
      api.fetchMetrics.mockResolvedValue('');

      renderWithRouter(<LandingPage />);

      expect(screen.getByText('🔐 Secure Authentication')).toBeInTheDocument();
      expect(screen.getByText('📚 Smart Book Search')).toBeInTheDocument();
      expect(screen.getByText('⚡ High Availability')).toBeInTheDocument();
      expect(screen.getByText('📊 Prometheus Monitoring')).toBeInTheDocument();
    });
  });
});
