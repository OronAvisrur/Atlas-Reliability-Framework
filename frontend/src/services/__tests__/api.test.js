import axios from 'axios';
import { fetchMetrics } from '../api';

jest.mock('axios');

describe('API Service', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('fetchMetrics', () => {
    it('should fetch metrics successfully', async () => {
      const mockMetricsData = 'http_requests_total 100\nactive_requests 5';
      
      axios.create.mockReturnValue({
        get: jest.fn().mockResolvedValue({ data: mockMetricsData })
      });

      const result = await fetchMetrics();

      expect(result).toBe(mockMetricsData);
    });

    it('should handle fetch error', async () => {
      const error = new Error('Network error');
      
      axios.create.mockReturnValue({
        get: jest.fn().mockRejectedValue(error)
      });

      await expect(fetchMetrics()).rejects.toThrow('Network error');
    });
  });
});
