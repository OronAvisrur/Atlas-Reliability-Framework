import api from './api';
import { getToken } from './authService';

export const searchBooks = async (description) => {
  const token = getToken();
  
  const response = await api.post('/books/search', 
    { description },
    {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    }
  );
  
  return response.data;
};
