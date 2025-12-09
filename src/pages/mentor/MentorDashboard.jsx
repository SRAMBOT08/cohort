import React from 'react';
import { motion } from 'framer-motion';
import { Users, CheckCircle, Clock, MessageSquare } from 'lucide-react';
import GlassCard from '../../components/GlassCard';
import './MentorDashboard.css';

function MentorDashboard() {
    const stats = [
        { label: 'Assigned Students', value: '15', icon: Users, color: '#2196F3' },
        { label: 'Completed Reviews', value: '28', icon: CheckCircle, color: '#4CAF50' },
        { label: 'Pending Reviews', value: '7', icon: Clock, color: '#FF9800' },
        { label: 'Messages', value: '12', icon: MessageSquare, color: '#9C27B0' },
    ];

    const recentSubmissions = [
        { student: 'Amal R', category: 'Creative Learning Track', time: '2 hours ago', status: 'pending' },
        { student: 'Priya S', category: 'Social Responsibility Initiative', time: '5 hours ago', status: 'pending' },
        { student: 'Raj K', category: 'Career Future & Competency', time: '1 day ago', status: 'pending' },
    ];

    return (
        <div className="mentor-dashboard">
            <motion.div
                className="mentor-header"
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
            >
                <h1 className="mentor-title">Mentor Dashboard</h1>
                <p className="mentor-subtitle">Guide and review student progress</p>
            </motion.div>

            <div className="mentor-stats-grid">
                {stats.map((stat, index) => (
                    <motion.div
                        key={index}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5, delay: index * 0.1 }}
                    >
                        <GlassCard>
                            <div className="stat-card">
                                <div className="stat-icon" style={{ backgroundColor: `${stat.color}20` }}>
                                    <stat.icon size={32} color={stat.color} />
                                </div>
                                <div className="stat-content">
                                    <h3 className="stat-value">{stat.value}</h3>
                                    <p className="stat-label">{stat.label}</p>
                                </div>
                            </div>
                        </GlassCard>
                    </motion.div>
                ))}
            </div>

            <motion.div
                className="mentor-submissions"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.5, delay: 0.4 }}
            >
                <GlassCard>
                    <div className="submissions-section">
                        <h2 className="section-title">Recent Submissions</h2>
                        <div className="submissions-list">
                            {recentSubmissions.map((submission, index) => (
                                <div key={index} className="submission-item">
                                    <div className="submission-info">
                                        <h3 className="submission-student">{submission.student}</h3>
                                        <p className="submission-category">{submission.category}</p>
                                        <p className="submission-time">{submission.time}</p>
                                    </div>
                                    <button className="review-btn">Review</button>
                                </div>
                            ))}
                        </div>
                    </div>
                </GlassCard>
            </motion.div>

            <motion.div
                className="mentor-actions"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.5, delay: 0.6 }}
            >
                <GlassCard>
                    <div className="action-section">
                        <h2 className="section-title">Quick Actions</h2>
                        <div className="action-buttons">
                            <button className="action-btn">
                                <Users size={20} />
                                View All Students
                            </button>
                            <button className="action-btn">
                                <CheckCircle size={20} />
                                Review Queue
                            </button>
                            <button className="action-btn">
                                <MessageSquare size={20} />
                                Messages
                            </button>
                        </div>
                    </div>
                </GlassCard>
            </motion.div>
        </div>
    );
}

export default MentorDashboard;
