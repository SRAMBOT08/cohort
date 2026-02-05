import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { Lock, ArrowRight, Lightbulb, CheckCircle } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import GlassCard from '../components/GlassCard';
import { Input } from '../components/Input';
import { Button } from '../components/Button';
import '../pages/Login.css';

export const ResetPassword = () => {
  const navigate = useNavigate();
  const { updatePassword, user } = useAuth();

  const [formData, setFormData] = useState({
    password: '',
    confirmPassword: '',
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [tokenValid, setTokenValid] = useState(false);

  useEffect(() => {
    if (user) {
      setTokenValid(true);
    } else {
      setError('Invalid or expired reset link. Please request a new one.');
    }
  }, [user]);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
    setError('');
  };

  const validateForm = () => {
    if (!formData.password) {
      setError('Password is required');
      return false;
    }
    if (formData.password.length < 8) {
      setError('Password must be at least 8 characters long');
      return false;
    }
    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return false;
    }
    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validateForm()) return;

    setIsSubmitting(true);
    setError('');

    try {
      const { error: updateError } = await updatePassword(formData.password);
      if (updateError) {
        setError(updateError.message || 'Failed to update password');
        return;
      }
      setSuccess(true);
      setTimeout(() => {
        navigate('/login');
      }, 2000);
    } catch (err) {
      console.error('Password update error:', err);
      setError('An unexpected error occurred. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (!tokenValid && !error) {
    return (
      <div className="login-page">
        <div className="login-background">
          <motion.div className="login-gradient-orb login-gradient-orb--2" animate={{ scale: [1, 1.1, 1] }} transition={{ duration: 2, repeat: Infinity }} />
        </div>
        <div className="login-container" style={{ display: 'flex', justifyContent: 'center' }}>
          <GlassCard className="login-card" style={{ textAlign: 'center' }}>
            <div className="spinner" style={{ margin: '0 auto' }}></div>
            <h2 style={{ marginTop: '1rem', color: 'var(--text-primary)' }}>Verifying Link...</h2>
          </GlassCard>
        </div>
      </div>
    );
  }

  return (
    <div className="login-page">
      {/* Animated Background */}
      <div className="login-background">
        <motion.div
          className="login-gradient-orb login-gradient-orb--1"
          animate={{ x: [0, 100, 0], y: [0, -50, 0], scale: [1, 1.2, 1] }}
          transition={{ duration: 8, repeat: Infinity, ease: 'easeInOut' }}
        />
        <motion.div
          className="login-gradient-orb login-gradient-orb--2"
          animate={{ x: [0, -80, 0], y: [0, 100, 0], scale: [1, 1.1, 1] }}
          transition={{ duration: 10, repeat: Infinity, ease: 'easeInOut' }}
        />
        <motion.div
          className="login-gradient-orb login-gradient-orb--3"
          animate={{ x: [0, 60, 0], y: [0, -80, 0], scale: [1, 1.3, 1] }}
          transition={{ duration: 12, repeat: Infinity, ease: 'easeInOut' }}
        />
      </div>

      <div className="login-container" style={{ gridTemplateColumns: '1fr', maxWidth: '500px' }}>
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          style={{ width: '100%' }}
        >
          <GlassCard className="login-card" hoverable={false}>
            <div className="login-card-header">
              <motion.div
                className="login-logo"
                style={{ width: '64px', height: '64px' }}
                whileHover={{ rotate: 360 }}
                transition={{ duration: 0.6 }}
              >
                <Lightbulb size={32} />
              </motion.div>
              <h2 className="login-card-title">Reset Password</h2>
              <p className="login-card-description">Create a new secure password</p>
            </div>

            {success ? (
              <div style={{ textAlign: 'center' }}>
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ type: 'spring', stiffness: 260, damping: 20 }}
                  style={{ margin: '2rem 0', color: '#4caf50' }}
                >
                  <CheckCircle size={64} />
                </motion.div>
                <h3 style={{ color: 'var(--text-primary)', marginBottom: '0.5rem' }}>Password Updated!</h3>
                <p style={{ color: 'var(--text-secondary)' }}>Redirecting to login...</p>
              </div>
            ) : (
              <form onSubmit={handleSubmit} className="login-form">
                {error && (
                  <div className="login-error-summary">
                    <div className="login-error-item">{error}</div>
                  </div>
                )}

                <Input
                  label="New Password"
                  name="password"
                  type="password"
                  value={formData.password}
                  onChange={handleChange}
                  icon={<Lock size={20} />}
                  placeholder="At least 8 characters"
                  floatingLabel={false}
                  disabled={!tokenValid || isSubmitting}
                />

                <Input
                  label="Confirm Password"
                  name="confirmPassword"
                  type="password"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  icon={<Lock size={20} />}
                  placeholder="Re-enter password"
                  floatingLabel={false}
                  disabled={!tokenValid || isSubmitting}
                />

                <Button
                  type="submit"
                  variant="primary"
                  size="large"
                  withGlow
                  className="login-submit-button"
                  disabled={!tokenValid || isSubmitting}
                >
                  {isSubmitting ? 'Updating...' : 'Reset Password'}
                  {!isSubmitting && <ArrowRight size={20} />}
                </Button>
              </form>
            )}
          </GlassCard>
        </motion.div>
      </div>
    </div>
  );
};
