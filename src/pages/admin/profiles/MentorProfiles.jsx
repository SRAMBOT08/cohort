import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Search, UserCheck, Users, CheckCircle, Clock, TrendingUp, ChevronDown, ChevronUp } from 'lucide-react';
import GlassCard from '../../../components/GlassCard';
import Input from '../../../components/Input';
import './MentorProfiles.css';

const MentorProfiles = () => {
    const [searchQuery, setSearchQuery] = useState('');
    const [selectedMentor, setSelectedMentor] = useState(null);
    const [expandedMentor, setExpandedMentor] = useState(null);

    // Mock mentor data with their students
    const mentors = [
        {
            id: 1,
            name: 'Reshma',
            email: 'reshma@mentor.com',
            phone: '+91 98765 11111',
            department: 'Computer Science',
            expertise: ['Full Stack Development', 'React', 'Node.js', 'Database Design'],
            studentsHandled: 28,
            verificationsPending: 12,
            verificationsCompleted: 156,
            avgResponseTime: '1.9 hours',
            rating: 4.9,
            floors: ['Floor A', 'Floor B'],
            students: [
                { id: 1, name: 'Amal Krishna', xp: 4850, pillarsCompleted: 5 },
                { id: 2, name: 'Sreeram', xp: 4520, pillarsCompleted: 5 },
                { id: 3, name: 'Vishnu', xp: 4200, pillarsCompleted: 4 },
                { id: 4, name: 'Athira', xp: 3890, pillarsCompleted: 4 },
            ]
        },
        {
            id: 2,
            name: 'Thulasi',
            email: 'thulasi@mentor.com',
            phone: '+91 98765 22222',
            department: 'Information Technology',
            expertise: ['Data Science', 'Python', 'Machine Learning', 'AI'],
            studentsHandled: 22,
            verificationsPending: 7,
            verificationsCompleted: 134,
            avgResponseTime: '2.1 hours',
            rating: 4.8,
            floors: ['Floor C', 'Floor D'],
            students: [
                { id: 5, name: 'Rahul', xp: 3650, pillarsCompleted: 4 },
                { id: 6, name: 'Priya', xp: 3420, pillarsCompleted: 3 },
                { id: 7, name: 'Karthik', xp: 3180, pillarsCompleted: 3 },
            ]
        },
        {
            id: 3,
            name: 'Gopi',
            email: 'gopi@mentor.com',
            phone: '+91 98765 33333',
            department: 'Computer Science',
            expertise: ['DevOps', 'Cloud Computing', 'System Design', 'Docker & Kubernetes'],
            studentsHandled: 25,
            verificationsPending: 9,
            verificationsCompleted: 148,
            avgResponseTime: '1.7 hours',
            rating: 4.9,
            floors: ['Floor A', 'Floor E'],
            students: [
                { id: 8, name: 'Anjali', xp: 2950, pillarsCompleted: 3 },
                { id: 9, name: 'Arjun', xp: 2720, pillarsCompleted: 2 },
                { id: 10, name: 'Meera', xp: 2500, pillarsCompleted: 2 },
            ]
        }
    ];

    const filteredMentors = mentors.filter(mentor =>
        mentor.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        mentor.email.toLowerCase().includes(searchQuery.toLowerCase())
    );

    return (
        <div className="mentor-profiles-page">
            <div className="page-header">
                <h1 className="page-title">Mentor Management</h1>
                <p className="page-subtitle">Manage mentors, assign students, and track performance</p>
            </div>

            <div className="profiles-layout">
                {/* Mentors List Panel */}
                <GlassCard className="mentors-list-panel">
                    <div className="search-section">
                        <Input
                            icon={Search}
                            placeholder="Search mentors..."
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                        />
                    </div>

                    <div className="mentors-list">
                        {filteredMentors.map((mentor) => (
                            <motion.div
                                key={mentor.id}
                                className={`mentor-item ${selectedMentor?.id === mentor.id ? 'active' : ''}`}
                                onClick={() => setSelectedMentor(mentor)}
                                whileHover={{ scale: 1.02 }}
                                whileTap={{ scale: 0.98 }}
                            >
                                <div className="mentor-avatar">
                                    <UserCheck size={24} />
                                </div>
                                <div className="mentor-info">
                                    <p className="mentor-name">{mentor.name}</p>
                                    <p className="mentor-email">{mentor.email}</p>
                                    <p className="mentor-stats">
                                        {mentor.studentsHandled} Students • {mentor.verificationsPending} Pending
                                    </p>
                                </div>
                            </motion.div>
                        ))}
                    </div>
                </GlassCard>

                {/* Mentor Details Panel */}
                <GlassCard className="mentor-details-panel">
                    {selectedMentor ? (
                        <div className="mentor-details">
                            <div className="profile-header">
                                <div className="profile-avatar-large">
                                    <UserCheck size={48} />
                                </div>
                                <div className="profile-info">
                                    <h2>{selectedMentor.name}</h2>
                                    <p>{selectedMentor.department}</p>
                                    <p>{selectedMentor.email}</p>
                                    <p>{selectedMentor.phone}</p>
                                </div>
                            </div>

                            <div className="profile-section">
                                <h3>Performance Metrics</h3>
                                <div className="stats-grid">
                                    <div className="stat-box">
                                        <Users size={32} color="#4CAF50" />
                                        <div>
                                            <p className="stat-value">{selectedMentor.studentsHandled}</p>
                                            <p className="stat-label">Students</p>
                                        </div>
                                    </div>
                                    <div className="stat-box">
                                        <Clock size={32} color="#FF9800" />
                                        <div>
                                            <p className="stat-value">{selectedMentor.verificationsPending}</p>
                                            <p className="stat-label">Pending</p>
                                        </div>
                                    </div>
                                    <div className="stat-box">
                                        <CheckCircle size={32} color="#2196F3" />
                                        <div>
                                            <p className="stat-value">{selectedMentor.verificationsCompleted}</p>
                                            <p className="stat-label">Completed</p>
                                        </div>
                                    </div>
                                    <div className="stat-box">
                                        <TrendingUp size={32} color="#F7C948" />
                                        <div>
                                            <p className="stat-value">{selectedMentor.rating}</p>
                                            <p className="stat-label">Rating</p>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <div className="profile-section">
                                <h3>Expertise Areas</h3>
                                <div className="expertise-tags">
                                    {selectedMentor.expertise.map((skill, index) => (
                                        <span key={index} className="expertise-tag">{skill}</span>
                                    ))}
                                </div>
                            </div>

                            <div className="profile-section">
                                <h3>Assigned Floors</h3>
                                <div className="floor-tags">
                                    {selectedMentor.floors.map((floor, index) => (
                                        <span key={index} className="floor-tag">{floor}</span>
                                    ))}
                                </div>
                            </div>

                            <div className="profile-section">
                                <h3>Students ({selectedMentor.students.length})</h3>
                                <div className="students-list">
                                    {selectedMentor.students.map((student) => (
                                        <div key={student.id} className="student-item">
                                            <div className="student-avatar">{student.name.charAt(0)}</div>
                                            <div className="student-info">
                                                <p className="student-name">{student.name}</p>
                                                <p className="student-stats">
                                                    {student.xp} XP • {student.pillarsCompleted} Pillars
                                                </p>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>
                    ) : (
                        <div className="empty-state">
                            <UserCheck size={64} />
                            <p>Select a mentor to view details</p>
                        </div>
                    )}
                </GlassCard>
            </div>

            {/* Expanded Mentor Cards with Students */}
            <div className="mentors-expanded-grid">
                {filteredMentors.map((mentor) => (
                    <motion.div
                        key={mentor.id}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.1 }}
                    >
                        <GlassCard>
                            <div className="mentor-card-expanded">
                                <div
                                    className="mentor-card-header"
                                    onClick={() => setExpandedMentor(expandedMentor === mentor.id ? null : mentor.id)}
                                    style={{ cursor: 'pointer' }}
                                >
                                    <div className="mentor-card-info">
                                        <div className="mentor-avatar-large">
                                            <UserCheck size={32} />
                                        </div>
                                        <div>
                                            <h3>{mentor.name}</h3>
                                            <p className="mentor-department">{mentor.department}</p>
                                            <p className="mentor-contact">{mentor.email}</p>
                                        </div>
                                    </div>
                                    <button className="expand-btn">
                                        {expandedMentor === mentor.id ? <ChevronUp size={24} /> : <ChevronDown size={24} />}
                                    </button>
                                </div>

                                <div className="mentor-quick-stats">
                                    <div className="quick-stat">
                                        <Users size={20} />
                                        <span>{mentor.studentsHandled} Students</span>
                                    </div>
                                    <div className="quick-stat">
                                        <CheckCircle size={20} />
                                        <span>{mentor.verificationsCompleted} Verified</span>
                                    </div>
                                    <div className="quick-stat">
                                        <Clock size={20} />
                                        <span>{mentor.avgResponseTime}</span>
                                    </div>
                                </div>

                                {expandedMentor === mentor.id && (
                                    <motion.div
                                        className="mentor-students-section"
                                        initial={{ height: 0, opacity: 0 }}
                                        animate={{ height: 'auto', opacity: 1 }}
                                        exit={{ height: 0, opacity: 0 }}
                                    >
                                        <h4>Assigned Students</h4>
                                        <div className="students-grid">
                                            {mentor.students.map((student) => (
                                                <div key={student.id} className="student-card">
                                                    <div className="student-avatar-small">
                                                        {student.name.split(' ').map(n => n[0]).join('')}
                                                    </div>
                                                    <div className="student-details">
                                                        <p className="student-name">{student.name}</p>
                                                        <p className="student-xp">{student.xp} XP</p>
                                                        <p className="student-pillars">{student.pillarsCompleted} pillars completed</p>
                                                    </div>
                                                </div>
                                            ))}
                                        </div>
                                    </motion.div>
                                )}
                            </div>
                        </GlassCard>
                    </motion.div>
                ))}
            </div>
        </div>
    );
};

export default MentorProfiles;
