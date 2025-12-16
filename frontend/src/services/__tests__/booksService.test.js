import { searchBooks } from '../booksService';
import api from '../api';
import { getToken } from '../authService';

jest.mock('../api');
jest.mock('../authService');

describe('BooksService', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('searchBooks', () => {
    it('should search books with authorization header', async () => {
      const mockToken = 'test-token';
      const mockDescription = 'action superhero books';
      const mockResponse = {
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

      getToken.mockReturnValue(mockToken);
      api.post = jest.fn().mockResolvedValue({ data: mockResponse });

      const result = await searchBooks(mockDescription);

      expect(getToken).toHaveBeenCalled();
      expect(api.post).toHaveBeenCalledWith(
        '/books/search',
        { description: mockDescription },
        {
          headers: {
            'Authorization': `Bearer ${mockToken}`
          }
        }
      );
      expect(result).toEqual(mockResponse);
    });

    it('should handle search error', async () => {
      const mockToken = 'test-token';
      const error = new Error('Search failed');

      getToken.mockReturnValue(mockToken);
      api.post = jest.fn().mockRejectedValue(error);

      await expect(searchBooks('test description')).rejects.toThrow('Search failed');
    });

    it('should include empty token if not authenticated', async () => {
      getToken.mockReturnValue(null);
      api.post = jest.fn().mockResolvedValue({ data: { items: [] } });

      await searchBooks('test');

      expect(api.post).toHaveBeenCalledWith(
        '/books/search',
        { description: 'test' },
        {
          headers: {
            'Authorization': 'Bearer null'
          }
        }
      );
    });
  });
});
