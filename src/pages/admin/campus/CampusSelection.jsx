import React from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { Building2, GraduationCap, Users, UserCheck, Layers } from 'lucide-react';
import GlassCard from '../../../components/GlassCard';
import { CAMPUS_NAMES } from '../../../utils/campusNames';
import './CampusSelection.css';

function CampusSelection() {
    const navigate = useNavigate();

    const campuses = [
        {
            id: 'TECH',
            name: CAMPUS_NAMES.TECH.full,
            type: CAMPUS_NAMES.TECH.type,
            icon: Building2,
            color: '#F7C948',
            gradient: 'linear-gradient(135deg, #F7C948 0%, #E53935 100%)',
            floors: 4,
            students: 250,
            mentors: 15,
            path: '/admin/campus/TECH'
        },
        {
            id: 'ARTS',
            name: CAMPUS_NAMES.ARTS.full,
            type: CAMPUS_NAMES.ARTS.type,
            icon: GraduationCap,
            color: '#9C27B0',
            gradient: 'linear-gradient(135deg, #9C27B0 0%, #E91E63 100%)',
            floors: 3,
            students: 180,
            mentors: 10,
            path: '/admin/campus/ARTS'
        }
    ];

    return (
        <div className="campus-selection-container">
            <motion.div
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="campus-selection-header"
            >
                <h1 className="campus-selection-title">Campus Management</h1>
                <p className="campus-selection-subtitle">
                    Select a campus to manage floors, students, and mentors
                </p>
            </motion.div>

            <div className="campus-cards-grid">
                {campuses.map((campus, index) => (
                    <motion.div
                        key={campus.id}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5, delay: index * 0.15 }}
                        whileHover={{ y: -8 }}
                        className="campus-card-wrapper"
                    >
                        <GlassCard
                            hoverable
                            onClick={() => navigate(campus.path)}
                            style={{ cursor: 'pointer', height: '100%' }}
                        >
                            <div className="campus-card">
                                <div 
                                    className="campus-icon"
                                    style={{ background: campus.gradient }}
                                >
                                    <campus.icon size={48} color="#fff" strokeWidth={2.5} />
                                </div>
                                
                                <div className="campus-info">
                                    <h2 className="campus-name">{campus.name}</h2>
                                    <span className="campus-type">{campus.type}</span>
                                </div>

                                <div className="campus-stats-grid">
                                    <div className="campus-stat-item">
                                        <Layers size={18} />
                                        <div>
                                            <span className="stat-value">{campus.floors}</span>
                                            <span className="stat-label">Floors</span>
                                        </div>
                                    </div>
                                    <div className="campus-stat-item">
                                        <Users size={18} />
                                        <div>
                                            <span className="stat-value">{campus.students}</span>
                                            <span className="stat-label">Students</span>
                                        </div>
                                    </div>
                                    <div className="campus-stat-item">
                                        <UserCheck size={18} />
                                        <div>
                                            <span className="stat-value">{campus.mentors}</span>
                                            <span className="stat-label">Mentors</span>
                                        </div>
                                    </div>
                                </div>

                                <div className="campus-action">
                                    <span>View Campus</span>
                                    <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                                        <path d="M7 4L13 10L7 16" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                                    </svg>
                                </div>
                            </div>
                        </GlassCard>
                    </motion.div>
                ))}
            </div>
        </div>
    );
}

export default CampusSelection;
