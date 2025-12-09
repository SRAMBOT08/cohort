import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

/**
 * Authentication API Service
 * Handles login, logout, token refresh, and user management
 */

export const authService = {
  /**
   * Login user and get JWT tokens
   * @param {string} username - Username or email
   * @param {string} password - Password
   * @returns {Promise} - User data with tokens
   */
  login: async (username, password) => {
    const response = await axios.post(`${API_BASE_URL}/auth/token/`, {
      username,
      password,
    });
    
    const { access, refresh } = response.data;
    // For now, create a basic user object (will be enhanced with profile endpoint later)
    const user = { username, id: null, email: null };
    
    // Store tokens in localStorage
    localStorage.setItem('accessToken', access);
    localStorage.setItem('refreshToken', refresh);
    localStorage.setItem('user', JSON.stringify(user));
    
    return response.data;
  },

  /**
   * Logout user and clear tokens
   */
  logout: () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('user');
  },

  /**
   * Refresh access token using refresh token
   * @returns {Promise} - New access token
   */
  refreshToken: async () => {
    const refreshToken = localStorage.getItem('refreshToken');
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }

    const response = await axios.post(`${API_BASE_URL}/auth/token/refresh/`, {
      refresh: refreshToken,
    });

    const { access } = response.data;
    localStorage.setItem('accessToken', access);
    
    return access;
  },

  /**
   * Get current user from localStorage
   * @returns {Object|null} - User object or null
   */
  getCurrentUser: () => {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
  },

  /**
   * Check if user is authenticated
   * @returns {boolean}
   */
  isAuthenticated: () => {
    return !!localStorage.getItem('accessToken');
  },

  /**
   * Get access token
   * @returns {string|null}
   */
  getAccessToken: () => {
    return localStorage.getItem('accessToken');
  },
};

export default authService;
