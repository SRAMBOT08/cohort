import React, { useState } from 'react';
// eslint-disable-next-line no-unused-vars
import { motion } from 'framer-motion';
import { Users, CheckCircle, Clock, XCircle, Lightbulb, Heart, Trophy, Linkedin, Code, Search } from 'lucide-react';
import GlassCard from '../../components/GlassCard';
import './MentorDashboard.css';

function MentorDashboard() {
    const [selectedStudent, setSelectedStudent] = useState(null);
    const [searchQuery, setSearchQuery] = useState('');

    // Mock data for students assigned to this mentor
    const students = [
        {
            id: 1,
            name: 'Amal R',
            email: 'amal@student.com',
            rollNo: 'CS101',
            submissions: {
                clt: { status: 'completed', count: 5, lastSubmission: '2 days ago' },
                sri: { status: 'pending', count: 2, lastSubmission: '5 hours ago' },
                cfc: { status: 'completed', count: 3, lastSubmission: '1 week ago' },
                iipc: { status: 'completed', count: 1, lastSubmission: '3 days ago' },
                scd: { status: 'not-started', count: 0, lastSubmission: 'Never' },
            }
        },
        {
            id: 2,
            name: 'Priya S',
            email: 'priya@student.com',
            rollNo: 'CS102',
            submissions: {
                clt: { status: 'completed', count: 4, lastSubmission: '1 day ago' },
                sri: { status: 'completed', count: 3, lastSubmission: '2 days ago' },
                cfc: { status: 'pending', count: 2, lastSubmission: '3 hours ago' },
                iipc: { status: 'not-started', count: 0, lastSubmission: 'Never' },
                scd: { status: 'completed', count: 2, lastSubmission: '4 days ago' },
            }
        },
        {
            id: 3,
            name: 'Raj K',
            email: 'raj@student.com',
            rollNo: 'CS103',
            submissions: {
                clt: { status: 'pending', count: 3, lastSubmission: '1 hour ago' },
                sri: { status: 'completed', count: 4, lastSubmission: '1 week ago' },
                cfc: { status: 'completed', count: 5, lastSubmission: '2 days ago' },
                iipc: { status: 'pending', count: 1, lastSubmission: '6 hours ago' },
                scd: { status: 'completed', count: 3, lastSubmission: '5 days ago' },
            }
        },
        {
            id: 4,
            name: 'Meera L',
            email: 'meera@student.com',
            rollNo: 'CS104',
            submissions: {
                clt: { status: 'completed', count: 6, lastSubmission: '3 days ago' },
                sri: { status: 'not-started', count: 0, lastSubmission: 'Never' },
                cfc: { status: 'pending', count: 1, lastSubmission: '2 hours ago' },
                iipc: { status: 'completed', count: 2, lastSubmission: '1 week ago' },
                scd: { status: 'completed', count: 4, lastSubmission: '6 days ago' },
            }
        },
        {
            id: 5,
            name: 'Karthik M',
            email: 'karthik@student.com',
            rollNo: 'CS105',
            submissions: {
                clt: { status: 'completed', count: 3, lastSubmission: '4 days ago' },
                sri: { status: 'completed', count: 2, lastSubmission: '1 day ago' },
                cfc: { status: 'completed', count: 4, lastSubmission: '3 days ago' },
                iipc: { status: 'completed', count: 3, lastSubmission: '2 days ago' },
                scd: { status: 'pending', count: 1, lastSubmission: '8 hours ago' },
            }
        },
    ];

    const categories = [
        { id: 'clt', name: 'Creative Learning Track', icon: Lightbulb, color: '#F7C948' },
        { id: 'sri', name: 'Social Responsibility Initiative', icon: Heart, color: '#E53935' },
        { id: 'cfc', name: 'Career Future & Competency', icon: Trophy, color: '#FFC107' },
        { id: 'iipc', name: 'Industry Institute Partnership Cell', icon: Linkedin, color: '#0A66C2' },
        { id: 'scd', name: 'Skill & Career Development', icon: Code, color: '#FF5722' },
    ];

    const getStatusIcon = (status) => {
        switch (status) {
            case 'completed':
                return <CheckCircle size={20} color="#4CAF50" />;
            case 'pending':
                return <Clock size={20} color="#FF9800" />;
            case 'not-started':
                return <XCircle size={20} color="#9E9E9E" />;
            default:
                return null;
        }
    };

    const getStatusText = (status) => {
        switch (status) {
            case 'completed':
                return 'Completed';
            case 'pending':
                return 'Pending Review';
            case 'not-started':
                return 'Not Started';
            default:
                return 'Unknown';
        }
    };

    const filteredStudents = students.filter(student =>
        student.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        student.rollNo.toLowerCase().includes(searchQuery.toLowerCase())
    );

    return (
        <div className="mentor-dashboard">
            {/* Header */}
            <motion.div
                className="mentor-header"
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
            >
                <h1 className="mentor-title">Mentor Dashboard</h1>
                <p className="mentor-subtitle">Monitor and review your assigned students</p>
            </motion.div>

            {/* Two Column Layout */}
            <div className="mentor-content">
                {/* Left Side - Student List */}
                <motion.div
                    className="students-panel"
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.5, delay: 0.2 }}
                >
                    <GlassCard>
                        <div className="students-section">
                            <div className="students-header">
                                <h2 className="section-title">
                                    <Users size={24} />
                                    Assigned Students ({students.length})
                                </h2>
                                <div className="search-box">
                                    <Search size={18} />
                                    <input
                                        type="text"
                                        placeholder="Search students..."
                                        value={searchQuery}
                                        onChange={(e) => setSearchQuery(e.target.value)}
                                        className="search-input"
                                    />
                                </div>
                            </div>
                            <div className="students-list">
                                {filteredStudents.map((student) => (
                                    <div
                                        key={student.id}
                                        className={`student-card ${selectedStudent?.id === student.id ? 'active' : ''}`}
                                        onClick={() => setSelectedStudent(student)}
                                    >
                                        <div className="student-avatar">
                                            {student.name.charAt(0)}
                                        </div>
                                        <div className="student-info">
                                            <h3 className="student-name">{student.name}</h3>
                                            <p className="student-roll">{student.rollNo}</p>
                                            <p className="student-email">{student.email}</p>
                                        </div>
                                        <div className="student-status-summary">
                                            {Object.values(student.submissions).filter(s => s.status === 'pending').length > 0 && (
                                                <span className="pending-badge">
                                                    {Object.values(student.submissions).filter(s => s.status === 'pending').length} Pending
                                                </span>
                                            )}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </GlassCard>
                </motion.div>

                {/* Right Side - Student Details */}
                <motion.div
                    className="details-panel"
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.5, delay: 0.3 }}
                >
                    {selectedStudent ? (
                        <div className="student-details">
                            <GlassCard>
                                <div className="details-header">
                                    <div>
                                        <h2 className="details-title">{selectedStudent.name}</h2>
                                        <p className="details-subtitle">{selectedStudent.rollNo} • {selectedStudent.email}</p>
                                    </div>
                                </div>
                            </GlassCard>

                            <div className="submissions-grid">
                                {categories.map((category) => {
                                    const submission = selectedStudent.submissions[category.id];
                                    const Icon = category.icon;
                                    return (
                                        <motion.div
                                            key={category.id}
                                            initial={{ opacity: 0, y: 20 }}
                                            animate={{ opacity: 1, y: 0 }}
                                            transition={{ duration: 0.3 }}
                                        >
                                            <GlassCard>
                                                <div className="submission-card">
                                                    <div className="submission-card-header">
                                                        <div className="category-icon" style={{ backgroundColor: `${category.color}20` }}>
                                                            <Icon size={24} color={category.color} />
                                                        </div>
                                                        <div className="category-info">
                                                            <h3 className="category-name">{category.name}</h3>
                                                            <p className="category-id">{category.id.toUpperCase()}</p>
                                                        </div>
                                                    </div>
                                                    <div className="submission-card-body">
                                                        <div className="submission-status">
                                                            {getStatusIcon(submission.status)}
                                                            <span className={`status-text status-${submission.status}`}>
                                                                {getStatusText(submission.status)}
                                                            </span>
                                                        </div>
                                                        <div className="submission-stats">
                                                            <div className="stat-item">
                                                                <span className="stat-label">Submissions:</span>
                                                                <span className="stat-value">{submission.count}</span>
                                                            </div>
                                                            <div className="stat-item">
                                                                <span className="stat-label">Last Activity:</span>
                                                                <span className="stat-value">{submission.lastSubmission}</span>
                                                            </div>
                                                        </div>
                                                        {submission.status === 'pending' && (
                                                            <button className="review-btn-small">Review Now</button>
                                                        )}
                                                        {submission.status === 'completed' && (
                                                            <button className="view-btn-small">View Details</button>
                                                        )}
                                                    </div>
                                                </div>
                                            </GlassCard>
                                        </motion.div>
                                    );
                                })}
                            </div>
                        </div>
                    ) : (
                        <GlassCard>
                            <div className="no-selection">
                                <Users size={64} opacity={0.3} />
                                <h3>Select a Student</h3>
                                <p>Click on a student from the list to view their submission details</p>
                            </div>
                        </GlassCard>
                    )}
                </motion.div>
            </div>
        </div>
    );
}

export default MentorDashboard;
