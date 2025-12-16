import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import QueryPage from '../QueryPage';
import { AuthProvider } from '../../context/AuthContext';
import * as booksService from '../../services/booksService';
import * as authService from '../../services/authService';

jest.mock('../../services/booksService');
jest.mock('../../services/authService');

const mockNavigate = jest.fn();
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockNavigate,
}));

const renderWithProviders = (component) => {
  authService.getToken.mockReturnValue('test-token');
  authService.getUser.mockReturnValue('testuser');
  authService.isAuthenticated.mockReturnValue(true);

  return render(
    <BrowserRouter>
      <AuthProvider>{component}</AuthProvider>
    </BrowserRouter>
  );
};

describe('QueryPage', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('Rendering', () => {
    it('should render header with username and logout button', () => {
      renderWithProviders(<QueryPage />);

      expect(screen.getByText('ATLAS')).toBeInTheDocument();
      expect(screen.getByText('Welcome, testuser')).toBeInTheDocument();
      expect(screen.getByText('Logout')).toBeInTheDocument();
    });

    it('should render search form', () => {
      renderWithProviders(<QueryPage />);

      expect(screen.getByText('Search Books')).toBeInTheDocument();
      expect(screen.getByPlaceholderText(/describe the book/i)).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /search/i })).toBeInTheDocument();
    });
  });

  describe('Logout', () => {
    it('should logout and navigate to home', () => {
      authService.logout = jest.fn();
      renderWithProviders(<QueryPage />);

      const logoutButton = screen.getByText('Logout');
      fireEvent.click(logoutButton);

      expect(authService.logout).toHaveBeenCalled();
      expect(mockNavigate).toHaveBeenCalledWith('/');
    });
  });

  describe('Search Validation', () => {
    it('should show error for empty search', async () => {
      renderWithProviders(<QueryPage />);

      const searchButton = screen.getByRole('button', { name: /search/i });
      fireEvent.click(searchButton);

      await waitFor(() => {
        expect(screen.getByText('Please enter a book description')).toBeInTheDocument();
      });
    });
  });

  describe('Book Search', () => {
    it('should search books and display results', async () => {
      const mockResults = {
        total_items: 100,
        query_keywords: 'action superhero',
        items: [
          {
            title: 'Test Book',
            authors: ['Test Author'],
            description: 'Test description',
            categories: ['Fiction'],
            thumbnail: 'http://example.com/image.jpg'
          }
        ]
      };

      booksService.searchBooks.mockResolvedValue(mockResults);
      renderWithProviders(<QueryPage />);

      const searchInput = screen.getByPlaceholderText(/describe the book/i);
      const searchButton = screen.getByRole('button', { name: /search/i });

      fireEvent.change(searchInput, { target: { value: 'action superhero books' } });
      fireEvent.click(searchButton);

      await waitFor(() => {
        expect(screen.getByText('Search Results')).toBeInTheDocument();
        expect(screen.getByText(/found 100 books/i)).toBeInTheDocument();
        expect(screen.getByText('action superhero')).toBeInTheDocument();
        expect(screen.getByText('Test Book')).toBeInTheDocument();
        expect(screen.getByText('by Test Author')).toBeInTheDocument();
      });
    });

    it('should show error on search failure', async () => {
      booksService.searchBooks.mockRejectedValue({
        response: { data: { detail: 'Search failed' } }
      });

      renderWithProviders(<QueryPage />);

      const searchInput = screen.getByPlaceholderText(/describe the book/i);
      const searchButton = screen.getByRole('button', { name: /search/i });

      fireEvent.change(searchInput, { target: { value: 'test books' } });
      fireEvent.click(searchButton);

      await waitFor(() => {
        expect(screen.getByText('Search failed')).toBeInTheDocument();
      });
    });

    it('should show no results message when items empty', async () => {
      const mockResults = {
        total_items: 0,
        query_keywords: 'nonexistent',
        items: []
      };

      booksService.searchBooks.mockResolvedValue(mockResults);
      renderWithProviders(<QueryPage />);

      const searchInput = screen.getByPlaceholderText(/describe the book/i);
      const searchButton = screen.getByRole('button', { name: /search/i });

      fireEvent.change(searchInput, { target: { value: 'nonexistent books' } });
      fireEvent.click(searchButton);

      await waitFor(() => {
        expect(screen.getByText(/no books found/i)).toBeInTheDocument();
      });
    });
  });
});
