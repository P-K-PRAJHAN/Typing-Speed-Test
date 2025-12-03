import axios from 'axios';

// Set base URL for API requests
const API_BASE_URL = 'http://localhost:5000/api';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('firebaseToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// API functions
export const generateText = async (difficulty = 'easy', sentences = 3) => {
  try {
    const response = await api.post('/generate-text', { difficulty, sentences });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.error || 'Failed to generate text');
  }
};

export const submitTest = async (testData) => {
  try {
    const response = await api.post('/submit-test', testData);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.error || 'Failed to submit test');
  }
};

export const getUserHistory = async () => {
  try {
    const response = await api.get('/user-history');
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.error || 'Failed to fetch history');
  }
};

export const getAnalytics = async () => {
  try {
    const response = await api.get('/analytics');
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.error || 'Failed to fetch analytics');
  }
};

export const predictDifficulty = async (text) => {
  try {
    const response = await api.post('/predict-difficulty', { text });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.error || 'Failed to predict difficulty');
  }
};

export const getUserProfile = async () => {
  try {
    const response = await api.get('/user-profile');
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.error || 'Failed to fetch profile');
  }
};

export default api;