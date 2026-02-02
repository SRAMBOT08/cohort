import { createClient } from '@supabase/supabase-js';
import { API_CONFIG } from '../config';

// Initialize Supabase client
const supabaseUrl = import.meta.env.VITE_SUPABASE_URL || 'https://yfoopcuwdyotlukbkoej.supabase.co';
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlmb29wY3V3ZHlvdGx1a2Jrb2VqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njk4MDA4NDEsImV4cCI6MjA4NTM3Njg0MX0.YK5uw24Grhc2TPYnF98i0eORgZHNHLJMdd5akenvKRs';

const supabase = createClient(supabaseUrl, supabaseAnonKey);

/**
 * Authentication API Service using Supabase
 * Handles login, logout, and user management
 */

export const authService = {
  /**
   * Login user with Supabase
   * @param {string} email - User email
   * @param {string} password - Password
   * @returns {Promise} - User data with session
   */
  login: async (email, password) => {
    console.log('Auth service - attempting Supabase login with:', email);
    
    try {
      const { data, error } = await supabase.auth.signInWithPassword({
        email,
        password,
      });
      
      if (error) {
        console.error('Auth service - Supabase login error:', error);
        throw error;
      }
      
      console.log('Auth service - Supabase login successful');
      
      // Store session data
      if (data.session) {
        localStorage.setItem('supabase_access_token', data.session.access_token);
        localStorage.setItem('supabase_refresh_token', data.session.refresh_token);
      }
      
      // Store user data
      if (data.user) {
        localStorage.setItem('user', JSON.stringify({
          id: data.user.id,
          email: data.user.email,
          username: data.user.email.split('@')[0],
        }));
      }
      
      return data;
    } catch (error) {
      console.error('Auth service - login error:', error);
      throw error;
    }
  },

  /**
   * Logout user and clear session
   */
  logout: async () => {
    try {
      await supabase.auth.signOut();
    } catch (error) {
      console.error('Logout error:', error);
    }
    
    localStorage.removeItem('supabase_access_token');
    localStorage.removeItem('supabase_refresh_token');
    localStorage.removeItem('user');
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
    return !!localStorage.getItem('supabase_access_token');
  },

  /**
   * Get access token
   * @returns {string|null}
   */
  getAccessToken: () => {
    return localStorage.getItem('supabase_access_token');
  },

  /**
   * Get Supabase client
   * @returns {object} - Supabase client
   */
  getSupabaseClient: () => {
    return supabase;
  },
};

export default authService;
