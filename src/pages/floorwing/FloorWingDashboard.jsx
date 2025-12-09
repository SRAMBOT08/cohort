import React from 'react';
// eslint-disable-next-line no-unused-vars
import { motion } from 'framer-motion';
import { Users, CheckCircle, Clock, FileText, TrendingUp, Award } from 'lucide-react';
import GlassCard from '../../components/GlassCard';
import './FloorWingDashboard.css';

function FloorWingDashboard() {
    const stats = [
        { label: 'Students in Wing', value: '45', icon: Users, color: '#2196F3' },
        { label: 'Verified Submissions', value: '32', icon: CheckCircle, color: '#4CAF50' },
        { label: 'Pending Verification', value: '8', icon: Clock, color: '#FF9800' },
        { label: 'Total Submissions', value: '40', icon: FileText, color: '#9C27B0' },
    ];

    const recentActivities = [
        { student: 'Amal R', activity: 'CLT Submission', status: 'Verified', time: '1 hour ago' },
        { student: 'Priya S', activity: 'SRI Activity', status: 'Pending', time: '3 hours ago' },
        { student: 'Raj K', activity: 'CFC Achievement', status: 'Verified', time: '5 hours ago' },
        { student: 'Meera L', activity: 'IIPC Post', status: 'Pending', time: '1 day ago' },
    ];

    return (
        <div className="floorwing-dashboard">
            <motion.div
                className="floorwing-header"
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
            >
                <h1 className="floorwing-title">Floor Wing Dashboard</h1>
                <p className="floorwing-subtitle">Monitor and verify student activities in your wing</p>
            </motion.div>

            <div className="floorwing-stats-grid">
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
                className="floorwing-activities"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.5, delay: 0.4 }}
            >
                <GlassCard>
                    <div className="activities-section">
                        <h2 className="section-title">Recent Activities</h2>
                        <div className="activities-list">
                            {recentActivities.map((activity, index) => (
                                <div key={index} className="activity-item">
                                    <div className="activity-info">
                                        <h3 className="activity-student">{activity.student}</h3>
                                        <p className="activity-type">{activity.activity}</p>
                                        <p className="activity-time">{activity.time}</p>
                                    </div>
                                    <div className="activity-status-wrapper">
                                        <span className={`activity-status ${activity.status.toLowerCase()}`}>
                                            {activity.status}
                                        </span>
                                        {activity.status === 'Pending' && (
                                            <button className="verify-btn">Verify</button>
                                        )}
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </GlassCard>
            </motion.div>

            <motion.div
                className="floorwing-actions"
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
                                <FileText size={20} />
                                Verification Queue
                            </button>
                            <button className="action-btn">
                                <TrendingUp size={20} />
                                Wing Analytics
                            </button>
                            <button className="action-btn">
                                <Award size={20} />
                                Top Performers
                            </button>
                        </div>
                    </div>
                </GlassCard>
            </motion.div>
        </div>
    );
}

export default FloorWingDashboard;
