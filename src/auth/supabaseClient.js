import { createClient } from '@supabase/supabase-js';

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseAnonKey) {
  throw new Error('Missing Supabase environment variables');
}

export const supabase = createClient(supabaseUrl, supabaseAnonKey, {
  auth: {
    autoRefreshToken: true,
    persistSession: true,
    detectSessionInUrl: true,
    storageKey: 'cohort-supabase-auth',
  },
});

/**
 * Authentication methods for Supabase
 * NOTE: Signup is disabled - users are pre-created by admin
 */
export const auth = {
  /**
   * Sign in with email and password
   * Users must be pre-created by admin in Supabase
   */
  signIn: async (email, password) => {
    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password,
    });
    return { 
      user: data?.user, 
      session: data?.session,
      accessToken: data?.session?.access_token,
      error 
    };
  },

  /**
   * Sign out current user
   */
  signOut: async () => {
    const { error } = await supabase.auth.signOut();
    return { error };
  },

  /**
   * Get current session with JWT token
   */
  getSession: async () => {
    const { data, error } = await supabase.auth.getSession();
    return { 
      session: data?.session,
      accessToken: data?.session?.access_token,
      error 
    };
  },

  /**
   * Get current user
   */
  getUser: async () => {
    const { data, error } = await supabase.auth.getUser();
    return { user: data?.user, error };
  },

  /**
   * Send password reset email
   * User will receive email with reset link
   */
  requestPasswordReset: async (email) => {
    const { error } = await supabase.auth.resetPasswordForEmail(email, {
      redirectTo: `${window.location.origin}/reset-password`,
    });
    return { error };
  },

  /**
   * Update user password after reset
   * Called from reset-password page with token in URL
   */
  updatePassword: async (newPassword) => {
    const { data, error } = await supabase.auth.updateUser({
      password: newPassword,
    });
    return { user: data?.user, error };
  },

  /**
   * Subscribe to auth state changes
   */
  onAuthStateChange: (callback) => {
    return supabase.auth.onAuthStateChange(callback);
  },

  /**
   * Get access token for Django API requests
   */
  getAccessToken: async () => {
    const { data, error } = await supabase.auth.getSession();
    if (error || !data.session) {
      return null;
    }
    return data.session.access_token;
  },
};
