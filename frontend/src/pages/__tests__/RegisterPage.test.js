import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import RegisterPage from '../RegisterPage';
import * as authService from '../../services/authService';

jest.mock('../../services/authService');

const mockNavigate = jest.fn();
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockNavigate,
}));

const renderWithRouter = (component) => {
  return render(<BrowserRouter>{component}</BrowserRouter>);
};

describe('RegisterPage', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    jest.useFakeTimers();
  });

  afterEach(() => {
    jest.runOnlyPendingTimers();
    jest.useRealTimers();
  });

  describe('Rendering', () => {
    it('should render register form', () => {
      renderWithRouter(<RegisterPage />);

      expect(screen.getByText('Register')).toBeInTheDocument();
      expect(screen.getByLabelText('Username')).toBeInTheDocument();
      expect(screen.getByLabelText(/^Password$/)).toBeInTheDocument();
      expect(screen.getByLabelText('Confirm Password')).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /register/i })).toBeInTheDocument();
    });

    it('should render login link', () => {
      renderWithRouter(<RegisterPage />);

      expect(screen.getByText(/already have an account/i)).toBeInTheDocument();
      expect(screen.getByText('Login here')).toBeInTheDocument();
    });
  });

  describe('Form Validation', () => {
    it('should show error for empty fields', async () => {
      renderWithRouter(<RegisterPage />);

      const registerButton = screen.getByRole('button', { name: /register/i });
      fireEvent.click(registerButton);

      await waitFor(() => {
        expect(screen.getByText('Please fill in all fields')).toBeInTheDocument();
      });
    });

    it('should show error for short username', async () => {
      renderWithRouter(<RegisterPage />);

      fireEvent.change(screen.getByLabelText('Username'), { target: { value: 'ab' } });
      fireEvent.change(screen.getByLabelText(/^Password$/), { target: { value: 'password123' } });
      fireEvent.change(screen.getByLabelText('Confirm Password'), { target: { value: 'password123' } });
      fireEvent.click(screen.getByRole('button', { name: /register/i }));

      await waitFor(() => {
        expect(screen.getByText('Username must be at least 3 characters')).toBeInTheDocument();
      });
    });

    it('should show error for short password', async () => {
      renderWithRouter(<RegisterPage />);

      fireEvent.change(screen.getByLabelText('Username'), { target: { value: 'testuser' } });
      fireEvent.change(screen.getByLabelText(/^Password$/), { target: { value: '12345' } });
      fireEvent.change(screen.getByLabelText('Confirm Password'), { target: { value: '12345' } });
      fireEvent.click(screen.getByRole('button', { name: /register/i }));

      await waitFor(() => {
        expect(screen.getByText('Password must be at least 6 characters')).toBeInTheDocument();
      });
    });

    it('should show error for password mismatch', async () => {
      renderWithRouter(<RegisterPage />);

      fireEvent.change(screen.getByLabelText('Username'), { target: { value: 'testuser' } });
      fireEvent.change(screen.getByLabelText(/^Password$/), { target: { value: 'password123' } });
      fireEvent.change(screen.getByLabelText('Confirm Password'), { target: { value: 'password456' } });
      fireEvent.click(screen.getByRole('button', { name: /register/i }));

      await waitFor(() => {
        expect(screen.getByText('Passwords do not match')).toBeInTheDocument();
      });
    });
  });

  describe('Registration Submission', () => {
    it('should call register and navigate on success', async () => {
      authService.register.mockResolvedValue({ id: 1, username: 'testuser' });

      renderWithRouter(<RegisterPage />);

      fireEvent.change(screen.getByLabelText('Username'), { target: { value: 'testuser' } });
      fireEvent.change(screen.getByLabelText(/^Password$/), { target: { value: 'password123' } });
      fireEvent.change(screen.getByLabelText('Confirm Password'), { target: { value: 'password123' } });
      fireEvent.click(screen.getByRole('button', { name: /register/i }));

      await waitFor(() => {
        expect(screen.getByText(/registration successful/i)).toBeInTheDocument();
      });

      jest.advanceTimersByTime(2000);

      await waitFor(() => {
        expect(mockNavigate).toHaveBeenCalledWith('/login');
      });
    });

    it('should show error on registration failure', async () => {
      authService.register.mockRejectedValue({
        response: { data: { detail: 'Username already exists' } }
      });

      renderWithRouter(<RegisterPage />);

      fireEvent.change(screen.getByLabelText('Username'), { target: { value: 'testuser' } });
      fireEvent.change(screen.getByLabelText(/^Password$/), { target: { value: 'password123' } });
      fireEvent.change(screen.getByLabelText('Confirm Password'), { target: { value: 'password123' } });
      fireEvent.click(screen.getByRole('button', { name: /register/i }));

      await waitFor(() => {
        expect(screen.getByText('Username already exists')).toBeInTheDocument();
      });
    });
  });
});
