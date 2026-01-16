import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000'; 

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const api = {
  search: async (category, query) => {
    try {
      const response = await apiClient.post(`/search/${category}`, { query });
      return response.data;
    } catch (error) {
      console.error('Search API error:', error);
      throw error;
    }
  },

  followup: async (category, previousQuery, clarificationAnswer, turn) => {
    try {
      const response = await apiClient.post(`/search/${category}/followup`, {
        previous_query: previousQuery,
        clarification_answer: clarificationAnswer,
        turn: turn,
      });
      return response.data;
    } catch (error) {
      console.error('Followup API error:', error);
      throw error;
    }
  },
};
