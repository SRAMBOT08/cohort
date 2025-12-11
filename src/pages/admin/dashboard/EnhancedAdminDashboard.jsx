import React from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import {
    Users, UserCheck, Trophy, Bell, Shield, Settings
} from 'lucide-react';
import GlassCard from '../../../components/GlassCard';
import './SimpleDashboard.css';

function EnhancedAdminDashboard() {
    const navigate = useNavigate();


    // Simple dashboard data
    const dashboardSections = [
        {
            id: 'students',
            title: 'Total Students',
            icon: Users,
            value: '150',
            subtitle: '+12 this month',
            color: '#4CAF50',
            path: '/admin/students'
        },
        {
            id: 'mentors',
            title: 'Mentors Details',
            icon: UserCheck,
            value: '12',
            subtitle: '3 active mentors',
            color: '#2196F3',
            path: '/admin/mentors'
        },
        {
            id: 'leaderboard',
            title: 'Leaderboard',
            icon: Trophy,
            value: 'Top 10',
            subtitle: 'View rankings',
            color: '#FFB300',
            path: '/admin/leaderboard'
        },
        {
            id: 'notifications',
            title: 'Notifications',
            icon: Bell,
            value: '24',
            subtitle: '5 unread messages',
            color: '#FF5722',
            path: '/admin/notifications'
        },
        {
            id: 'roles',
            title: 'Roles',
            icon: Shield,
            value: '4',
            subtitle: 'Manage permissions',
            color: '#9C27B0',
            path: '/admin/roles'
        },
        {
            id: 'settings',
            title: 'Settings',
            icon: Settings,
            value: 'Config',
            subtitle: 'System preferences',
            color: '#607D8B',
            path: '/admin/settings'
        }
    ];

    return (
        <div className="admin-dashboard-enhanced">
            {/* Header Section */}
            <motion.div
                className="admin-header"
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
            >
                <div>
                    <h1 className="admin-title">Admin Dashboard</h1>
                    <p className="admin-subtitle">Manage students, mentors, and system settings</p>
                </div>
            </motion.div>

            {/* Dashboard Grid */}
            <div className="dashboard-grid">
                {dashboardSections.map((section, index) => (
                    <motion.div
                        key={section.id}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.4, delay: index * 0.1 }}
                        whileHover={{ scale: 1.02, y: -4 }}
                        className="dashboard-card"
                        onClick={() => navigate(section.path)}
                        style={{ cursor: 'pointer' }}
                    >
                        <GlassCard>
                            <div className="dashboard-card-content">
                                <div
                                    className="dashboard-icon"
                                    style={{
                                        backgroundColor: `${section.color}20`,
                                        color: section.color
                                    }}
                                >
                                    <section.icon size={32} />
                                </div>
                                <div className="dashboard-info">
                                    <h3 className="dashboard-card-title">{section.title}</h3>
                                    <p className="dashboard-value">{section.value}</p>
                                    <p className="dashboard-subtitle">{section.subtitle}</p>
                                </div>
                            </div>
                        </GlassCard>
                    </motion.div>
                ))}
            </div>
        </div>
    );
}

export default EnhancedAdminDashboard;
