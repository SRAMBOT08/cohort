import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Link, useNavigate } from 'react-router-dom';
import { Mail, ArrowRight, Lightbulb, ArrowLeft, CheckCircle } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import GlassCard from '../components/GlassCard';
import { Input } from '../components/Input';
import { Button } from '../components/Button';
import '../pages/Login.css';

export const ForgotPassword = () => {
  const { requestResetCode } = useAuth();
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!email) {
      setError('Email is required');
      return;
    }
    if (!/\S+@\S+\.\S+/.test(email)) {
      setError('Please enter a valid email address');
      return;
    }

    setIsSubmitting(true);
    setError('');

    try {
      const { error: resetError } = await requestResetCode(email.trim());
      if (resetError) {
        setError(resetError.message || 'Failed to send code');
      } else {
        // Redirect to Verification Page with Email State
        sessionStorage.setItem('resetEmail', email.trim());
        navigate('/verify-reset-code', { state: { email: email.trim() } });
      }
    } catch (err) {
      console.error('Password reset error:', err);
      setError('An unexpected error occurred. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

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
              <Link to="/login" style={{ display: 'inline-block', marginBottom: '1rem' }}>
                <motion.div
                  className="login-logo"
                  style={{ width: '64px', height: '64px' }}
                  whileHover={{ rotate: 360 }}
                  transition={{ duration: 0.6 }}
                >
                  <Lightbulb size={32} />
                </motion.div>
              </Link>
              <h2 className="login-card-title">Forgot Password</h2>
              <p className="login-card-description">
                {success
                  ? `We've sent a recovery link to ${email}`
                  : "Enter your email to receive a password reset link"}
              </p>
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
                <Link to="/login">
                  <Button variant="primary" size="large" withGlow className="login-submit-button">
                    Back to Login
                  </Button>
                </Link>
                <button
                  onClick={() => setSuccess(false)}
                  className="btn btn-secondary"
                  style={{ marginTop: '1rem', background: 'transparent', border: 'none', color: '#ffcc00', cursor: 'pointer' }}
                >
                  Try another email
                </button>
              </div>
            ) : (
              <form onSubmit={handleSubmit} className="login-form">
                <Input
                  label="Email Address"
                  name="email"
                  type="email"
                  value={email}
                  onChange={(e) => {
                    setEmail(e.target.value);
                    setError('');
                  }}
                  error={error}
                  icon={<Mail size={20} />}
                  placeholder="your@email.com"
                  floatingLabel={false}
                />

                <Button
                  type="submit"
                  variant="primary"
                  size="large"
                  withGlow
                  className="login-submit-button"
                  disabled={isSubmitting}
                >
                  {isSubmitting ? 'Sending Code...' : 'Send Verification Code'}
                  {!isSubmitting && <ArrowRight size={20} />}
                </Button>

                <div className="login-card-footer">
                  <p>
                    Remember your password?
                    <Link to="/login" className="login-forgot" style={{ display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
                      <ArrowLeft size={16} />
                      Back to Login
                    </Link>
                  </p>
                </div>
              </form>
            )}
          </GlassCard>
        </motion.div>
      </div>
    </div>
  );
};
