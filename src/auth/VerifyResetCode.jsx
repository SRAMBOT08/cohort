import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { Key, ArrowRight, Lightbulb, ArrowLeft, CheckCircle, Lock } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import GlassCard from '../components/GlassCard';
import { Input } from '../components/Input';
import { Button } from '../components/Button';
import '../pages/Login.css';

export const VerifyResetCode = () => {
    const { verifyResetCode } = useAuth();
    const navigate = useNavigate();
    const location = useLocation();

    const [email, setEmail] = useState('');
    const [code, setCode] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');

    const [error, setError] = useState('');
    const [success, setSuccess] = useState(false);
    const [isSubmitting, setIsSubmitting] = useState(false);

    useEffect(() => {
        const stateEmail = location.state?.email;
        const storageEmail = sessionStorage.getItem('resetEmail');

        if (stateEmail || storageEmail) {
            setEmail(stateEmail || storageEmail);
        } else {
            // If no email in state or storage, redirect back to forgot password
            navigate('/forgot-password');
        }
    }, [location, navigate]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!code || !newPassword || !confirmPassword) {
            setError('All fields are required');
            return;
        }

        if (newPassword !== confirmPassword) {
            setError('Passwords do not match');
            return;
        }

        if (newPassword.length < 6) {
            setError('Password must be at least 6 characters');
            return;
        }

        setIsSubmitting(true);
        setError('');

        try {
            const { error: verifyError } = await verifyResetCode(email, code, newPassword);
            if (verifyError) {
                setError(verifyError.message || 'Invalid code or failed to update password');
            } else {
                setSuccess(true);
                // Optional: Auto redirect after few seconds
                setTimeout(() => navigate('/login'), 3000);
            }
        } catch (err) {
            console.error('Verification error:', err);
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
                            <h2 className="login-card-title">Reset Password</h2>
                            <p className="login-card-description">
                                {success
                                    ? "Password updated successfully!"
                                    : `Enter the code sent to ${email}`}
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
                                <div style={{ marginBottom: '1rem', color: '#fff' }}>
                                    Your password has been reset securely.
                                </div>
                                <Link to="/login">
                                    <Button variant="primary" size="large" withGlow className="login-submit-button">
                                        Login Now
                                    </Button>
                                </Link>
                            </div>
                        ) : (
                            <form onSubmit={handleSubmit} className="login-form">
                                <Input
                                    label="Verification Code"
                                    name="code"
                                    type="text"
                                    value={code}
                                    onChange={(e) => {
                                        setCode(e.target.value);
                                        setError('');
                                    }}
                                    error={error && !code ? 'Required' : ''}
                                    icon={<Key size={20} />}
                                    placeholder="e.g. 123456"
                                    floatingLabel={false}
                                />

                                <Input
                                    label="New Password"
                                    name="newPassword"
                                    type="password"
                                    value={newPassword}
                                    onChange={(e) => {
                                        setNewPassword(e.target.value);
                                        setError('');
                                    }}
                                    icon={<Lock size={20} />}
                                    placeholder="Enter new password"
                                    floatingLabel={false}
                                />

                                <Input
                                    label="Confirm Password"
                                    name="confirmPassword"
                                    type="password"
                                    value={confirmPassword}
                                    onChange={(e) => {
                                        setConfirmPassword(e.target.value);
                                        setError('');
                                    }}
                                    error={error}
                                    icon={<Lock size={20} />}
                                    placeholder="Confirm new password"
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
                                    {isSubmitting ? 'Verifying...' : 'Reset Password'}
                                    {!isSubmitting && <ArrowRight size={20} />}
                                </Button>

                                <div className="login-card-footer">
                                    <Link to="/forgot-password" className="login-forgot" style={{ display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
                                        <ArrowLeft size={16} />
                                        Back (Resend Code)
                                    </Link>
                                </div>
                            </form>
                        )}
                    </GlassCard>
                </motion.div>
            </div>
        </div>
    );
};
