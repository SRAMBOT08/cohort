import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Search, Filter, FileText, CheckCircle, XCircle, Clock,
    User, Calendar, MessageSquare, Award, Eye, Download
} from 'lucide-react';
import GlassCard from '../../../components/GlassCard';
import Button from '../../../components/Button';
import Input from '../../../components/Input';
import './SubmissionsManagement.css';

const SubmissionsManagement = () => {
    const [searchQuery, setSearchQuery] = useState('');
    const [filterStatus, setFilterStatus] = useState('all');
    const [filterPillar, setFilterPillar] = useState('all');
    const [selectedSubmission, setSelectedSubmission] = useState(null);
    const [comment, setComment] = useState('');
    const [xpAward, setXPAward] = useState('');

    // Mock submissions data
    const submissions = [
        {
            id: 1,
            studentName: 'Amal R',
            registerNumber: 'CS101',
            pillar: 'CLT',
            title: 'LinkedIn Post - Career Development',
            submittedDate: '2025-12-10',
            status: 'pending',
            description: 'Posted about career development strategies and networking tips',
            link: 'https://linkedin.com/post/123',
            mentor: 'Reshma',
            xpEarned: 0
        },
        {
            id: 2,
            studentName: 'Priya S',
            registerNumber: 'CS102',
            pillar: 'SCD',
            title: 'LeetCode Problem Solution',
            submittedDate: '2025-12-09',
            status: 'approved',
            description: 'Solved Two Sum problem with optimal solution',
            link: 'https://leetcode.com/submissions/456',
            mentor: 'Gopi',
            xpEarned: 50,
            comments: 'Excellent solution with clear explanation'
        },
        {
            id: 3,
            studentName: 'Rahul M',
            registerNumber: 'CS103',
            pillar: 'CFC',
            title: 'Community Event Participation',
            submittedDate: '2025-12-08',
            status: 'pending',
            description: 'Volunteered at local coding workshop for school students',
            link: 'https://photos.com/event',
            mentor: 'Thulasi',
            xpEarned: 0
        },
        {
            id: 4,
            studentName: 'Sneha K',
            registerNumber: 'CS104',
            pillar: 'IIPC',
            title: 'LinkedIn Profile Update',
            submittedDate: '2025-12-07',
            status: 'rejected',
            description: 'Updated LinkedIn profile with new skills',
            link: 'https://linkedin.com/in/sneha',
            mentor: 'Reshma',
            xpEarned: 0,
            comments: 'Profile needs more detailed project descriptions'
        },
        {
            id: 5,
            studentName: 'Vikram P',
            registerNumber: 'CS105',
            pillar: 'SRI',
            title: 'Skill Development - React Course',
            submittedDate: '2025-12-06',
            status: 'approved',
            description: 'Completed React fundamentals course on Udemy',
            link: 'https://udemy.com/certificate/789',
            mentor: 'Reshma',
            xpEarned: 75,
            comments: 'Great progress on React fundamentals'
        }
    ];

    const filteredSubmissions = submissions.filter(submission => {
        const matchesSearch = submission.studentName.toLowerCase().includes(searchQuery.toLowerCase()) ||
            submission.registerNumber.toLowerCase().includes(searchQuery.toLowerCase()) ||
            submission.title.toLowerCase().includes(searchQuery.toLowerCase());
        const matchesStatus = filterStatus === 'all' || submission.status === filterStatus;
        const matchesPillar = filterPillar === 'all' || submission.pillar === filterPillar;
        return matchesSearch && matchesStatus && matchesPillar;
    });

    const handleApprove = () => {
        console.log('Approving submission:', selectedSubmission.id, 'XP:', xpAward, 'Comment:', comment);
        setSelectedSubmission(null);
        setComment('');
        setXPAward('');
    };

    const handleReject = () => {
        console.log('Rejecting submission:', selectedSubmission.id, 'Comment:', comment);
        setSelectedSubmission(null);
        setComment('');
    };

    const getStatusColor = (status) => {
        switch (status) {
            case 'approved': return '#4CAF50';
            case 'rejected': return '#E53935';
            case 'pending': return '#FF9800';
            default: return '#9E9E9E';
        }
    };

    const getPillarColor = (pillar) => {
        switch (pillar) {
            case 'CLT': return '#F7C948';
            case 'SRI': return '#E53935';
            case 'CFC': return '#4CAF50';
            case 'IIPC': return '#2196F3';
            case 'SCD': return '#9C27B0';
            default: return '#9E9E9E';
        }
    };

    return (
        <div className="submissions-management-page">
            <div className="page-header">
                <div>
                    <h1 className="page-title">Submissions Management</h1>
                    <p className="page-subtitle">Review and manage student submissions across all pillars</p>
                </div>
                <Button variant="secondary">
                    <Download size={18} />
                    Export Report
                </Button>
            </div>

            {/* Filters Section */}
            <GlassCard className="filters-card">
                <div className="filters-container">
                    <div className="search-box">
                        <Input
                            icon={Search}
                            placeholder="Search submissions..."
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                        />
                    </div>
                    <div className="filter-group">
                        <select
                            className="filter-select"
                            value={filterStatus}
                            onChange={(e) => setFilterStatus(e.target.value)}
                        >
                            <option value="all">All Status</option>
                            <option value="pending">Pending</option>
                            <option value="approved">Approved</option>
                            <option value="rejected">Rejected</option>
                        </select>
                        <select
                            className="filter-select"
                            value={filterPillar}
                            onChange={(e) => setFilterPillar(e.target.value)}
                        >
                            <option value="all">All Pillars</option>
                            <option value="CLT">CLT</option>
                            <option value="SRI">SRI</option>
                            <option value="CFC">CFC</option>
                            <option value="IIPC">IIPC</option>
                            <option value="SCD">SCD</option>
                        </select>
                    </div>
                </div>
            </GlassCard>

            {/* Submissions List */}
            <div className="submissions-grid">
                {filteredSubmissions.map((submission) => (
                    <motion.div
                        key={submission.id}
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                    >
                        <GlassCard
                            className="submission-card"
                            onClick={() => setSelectedSubmission(submission)}
                        >
                            <div className="submission-header">
                                <div className="submission-badges">
                                    <span
                                        className="pillar-badge"
                                        style={{ backgroundColor: `${getPillarColor(submission.pillar)}20`, color: getPillarColor(submission.pillar) }}
                                    >
                                        {submission.pillar}
                                    </span>
                                    <span
                                        className="status-badge"
                                        style={{ backgroundColor: `${getStatusColor(submission.status)}20`, color: getStatusColor(submission.status) }}
                                    >
                                        {submission.status}
                                    </span>
                                </div>
                                <span className="submission-date">
                                    <Calendar size={14} />
                                    {submission.submittedDate}
                                </span>
                            </div>
                            <h3 className="submission-title">{submission.title}</h3>
                            <div className="submission-info">
                                <span className="submission-student">
                                    <User size={16} />
                                    {submission.studentName} ({submission.registerNumber})
                                </span>
                                <span className="submission-mentor">
                                    Mentor: {submission.mentor}
                                </span>
                            </div>
                            <p className="submission-description">{submission.description}</p>
                            {submission.xpEarned > 0 && (
                                <div className="submission-xp">
                                    <Award size={16} />
                                    {submission.xpEarned} XP Earned
                                </div>
                            )}
                        </GlassCard>
                    </motion.div>
                ))}
            </div>

            {/* Submission Detail Modal */}
            <AnimatePresence>
                {selectedSubmission && (
                    <motion.div
                        className="modal-overlay"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        onClick={() => setSelectedSubmission(null)}
                    >
                        <motion.div
                            className="modal-content"
                            initial={{ scale: 0.9, opacity: 0 }}
                            animate={{ scale: 1, opacity: 1 }}
                            exit={{ scale: 0.9, opacity: 0 }}
                            onClick={(e) => e.stopPropagation()}
                        >
                            <GlassCard className="submission-detail">
                                <div className="detail-header">
                                    <h2>{selectedSubmission.title}</h2>
                                    <div className="detail-badges">
                                        <span
                                            className="pillar-badge"
                                            style={{ backgroundColor: `${getPillarColor(selectedSubmission.pillar)}20`, color: getPillarColor(selectedSubmission.pillar) }}
                                        >
                                            {selectedSubmission.pillar}
                                        </span>
                                        <span
                                            className="status-badge"
                                            style={{ backgroundColor: `${getStatusColor(selectedSubmission.status)}20`, color: getStatusColor(selectedSubmission.status) }}
                                        >
                                            {selectedSubmission.status}
                                        </span>
                                    </div>
                                </div>

                                <div className="detail-section">
                                    <h3>Student Information</h3>
                                    <p><strong>Name:</strong> {selectedSubmission.studentName}</p>
                                    <p><strong>Register Number:</strong> {selectedSubmission.registerNumber}</p>
                                    <p><strong>Submitted Date:</strong> {selectedSubmission.submittedDate}</p>
                                    <p><strong>Assigned Mentor:</strong> {selectedSubmission.mentor}</p>
                                </div>

                                <div className="detail-section">
                                    <h3>Submission Details</h3>
                                    <p>{selectedSubmission.description}</p>
                                    <a href={selectedSubmission.link} target="_blank" rel="noopener noreferrer" className="submission-link">
                                        <Eye size={16} />
                                        View Submission
                                    </a>
                                </div>

                                {selectedSubmission.comments && (
                                    <div className="detail-section">
                                        <h3>Previous Comments</h3>
                                        <p className="previous-comment">{selectedSubmission.comments}</p>
                                    </div>
                                )}

                                {selectedSubmission.status === 'pending' && (
                                    <div className="detail-section">
                                        <h3>Review Submission</h3>
                                        <div className="review-form">
                                            <Input
                                                label="XP Award (optional)"
                                                type="number"
                                                placeholder="Enter XP amount"
                                                value={xpAward}
                                                onChange={(e) => setXPAward(e.target.value)}
                                                icon={Award}
                                            />
                                            <div className="comment-box">
                                                <label>Comment</label>
                                                <textarea
                                                    placeholder="Add your feedback..."
                                                    value={comment}
                                                    onChange={(e) => setComment(e.target.value)}
                                                    rows={4}
                                                />
                                            </div>
                                            <div className="review-actions">
                                                <Button variant="success" onClick={handleApprove}>
                                                    <CheckCircle size={18} />
                                                    Approve
                                                </Button>
                                                <Button variant="danger" onClick={handleReject}>
                                                    <XCircle size={18} />
                                                    Reject
                                                </Button>
                                                <Button variant="secondary" onClick={() => setSelectedSubmission(null)}>
                                                    Cancel
                                                </Button>
                                            </div>
                                        </div>
                                    </div>
                                )}
                            </GlassCard>
                        </motion.div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
};

export default SubmissionsManagement;
