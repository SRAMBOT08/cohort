import React from 'react';
// eslint-disable-next-line no-unused-vars
import { motion } from 'framer-motion';
import { Users, FileText, Settings, BarChart3 } from 'lucide-react';
import GlassCard from '../../components/GlassCard';
import './AdminDashboard.css';

function AdminDashboard() {
    const stats = [
        { label: 'Total Students', value: '150', icon: Users, color: '#4CAF50' },
        { label: 'Total Mentors', value: '12', icon: Users, color: '#2196F3' },
        { label: 'Submissions', value: '342', icon: FileText, color: '#FF9800' },
        { label: 'Completion Rate', value: '78%', icon: BarChart3, color: '#9C27B0' },
    ];

    return (
        <div className="admin-dashboard">
            <motion.div
                className="admin-header"
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
            >
                <h1 className="admin-title">Admin Dashboard</h1>
                <p className="admin-subtitle">Manage and monitor the cohort program</p>
            </motion.div>

            <div className="admin-stats-grid">
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
                className="admin-actions"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.5, delay: 0.4 }}
            >
                <GlassCard>
                    <div className="action-section">
                        <h2 className="section-title">Quick Actions</h2>
                        <div className="action-buttons">
                            <button className="action-btn">
                                <Users size={20} />
                                Manage Students
                            </button>
                            <button className="action-btn">
                                <Users size={20} />
                                Manage Mentors
                            </button>
                            <button className="action-btn">
                                <FileText size={20} />
                                Review Submissions
                            </button>
                            <button className="action-btn">
                                <Settings size={20} />
                                Settings
                            </button>
                        </div>
                    </div>
                </GlassCard>
            </motion.div>
        </div>
    );
}

export default AdminDashboard;
