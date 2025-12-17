import axios from 'axios';

const api = axios.create({
  baseURL: '/',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const fetchMetrics = async () => {
  const response = await api.get('/metrics');
  return response.data;
};

export default api;
