import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useParams, useNavigate } from 'react-router-dom';
import { Users, UserCheck, Clock, ChevronRight, ArrowLeft, Layers, Building2, FileText, AlertCircle } from 'lucide-react';
import GlassCard from '../../../components/GlassCard';
import Button from '../../../components/Button';
import { getCampusOverview } from '../../../services/admin';
import { getCampusFullName } from '../../../utils/campusNames';
import './CampusOverview.css';

function CampusOverview() {
    const { campus } = useParams();
    const navigate = useNavigate();
    const [loading, setLoading] = useState(true);
    const [campusData, setCampusData] = useState(null);

    useEffect(() => {
        loadCampusData();
    }, [campus]);

    const loadCampusData = async () => {
        try {
            const data = await getCampusOverview(campus);
            setCampusData(data);
        } catch (error) {
            console.error('Failed to load campus data:', error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="campus-overview-container">
                <div className="loading-state">
                    <div className="loading-spinner"></div>
                    <p>Loading campus data...</p>
                </div>
            </div>
        );
    }

    if (!campusData) {
        return (
            <div className="campus-overview-container">
                <GlassCard>
                    <div className="error-state">
                        <AlertCircle size={48} color="#E53935" />
                        <h3>Failed to load campus data</h3>
                        <Button onClick={() => navigate('/admin/campus-select')}>
                            Back to Campus Selection
                        </Button>
                    </div>
                </GlassCard>
            </div>
        );
    }

    // Calculate summary stats
    const totalStudents = campusData.floors?.reduce((sum, floor) => sum + (floor.total_students || 0), 0) || 0;
    const totalMentors = campusData.floors?.reduce((sum, floor) => sum + (floor.total_mentors || 0), 0) || 0;
    const totalFloorWings = campusData.floors?.filter(floor => floor.floor_wing).length || 0;
    const totalSubmissions = campusData.floors?.reduce((sum, floor) => {
        if (floor.submissions) {
            return sum + floor.submissions.approved + floor.submissions.pending + floor.submissions.rejected;
        }
        return sum;
    }, 0) || 0;

    return (
        <div className="campus-overview-container">
            {/* Header */}
            <motion.div
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="campus-overview-header"
            >
                <Button
                    variant="secondary"
                    size="small"
                    onClick={() => navigate('/admin/campus-select')}
                    className="back-button"
                >
                    <ArrowLeft size={16} />
                    Back
                </Button>
                <h1 className="campus-overview-title">{getCampusFullName(campus)}</h1>
                <p className="campus-overview-subtitle">
                    Manage floors, mentors, students, and track submissions
                </p>
            </motion.div>

            {/* Summary Stats */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.1 }}
                className="summary-stats"
            >
                <GlassCard className="stat-card">
                    <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #4CAF50, #8BC34A)' }}>
                        <Layers size={24} />
                    </div>
                    <div className="stat-content">
                        <div className="stat-value">{campusData.floors?.length || 0}</div>
                        <div className="stat-label">Total Floors</div>
                    </div>
                </GlassCard>

                <GlassCard className="stat-card">
                    <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #2196F3, #03A9F4)' }}>
                        <Users size={24} />
                    </div>
                    <div className="stat-content">
                        <div className="stat-value">{totalStudents}</div>
                        <div className="stat-label">Total Students</div>
                    </div>
                </GlassCard>

                <GlassCard className="stat-card">
                    <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #FF9800, #FF5722)' }}>
                        <UserCheck size={24} />
                    </div>
                    <div className="stat-content">
                        <div className="stat-value">{totalMentors}</div>
                        <div className="stat-label">Total Mentors</div>
                    </div>
                </GlassCard>

                <GlassCard className="stat-card">
                    <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #9C27B0, #E91E63)' }}>
                        <Building2 size={24} />
                    </div>
                    <div className="stat-content">
                        <div className="stat-value">{totalFloorWings}</div>
                        <div className="stat-label">Floor Wings</div>
                    </div>
                </GlassCard>

                <GlassCard className="stat-card">
                    <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #F7C948, #E53935)' }}>
                        <FileText size={24} />
                    </div>
                    <div className="stat-content">
                        <div className="stat-value">{totalSubmissions}</div>
                        <div className="stat-label">Submissions</div>
                    </div>
                </GlassCard>
            </motion.div>

            {/* Floors Listing */}
            <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.5, delay: 0.2 }}
                className="floors-section"
            >
                <h2 className="section-title">Floors</h2>
                
                {campusData.floors && campusData.floors.length > 0 ? (
                    <div className="floors-grid">
                        {campusData.floors.map((floor, index) => (
                            <motion.div
                                key={floor.floor}
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ duration: 0.5, delay: 0.3 + index * 0.1 }}
                            >
                                <GlassCard
                                    hoverable
                                    onClick={() => navigate(`/admin/campus/${campus}/floor/${floor.floor}`)}
                                    className="floor-card-wrapper"
                                >
                                    <div className="floor-card">
                                        <div className="floor-header">
                                            <div className="floor-info">
                                                <h3 className="floor-title">Floor {floor.floor}</h3>
                                                <p className="floor-subtitle">{floor.floor_name}</p>
                                            </div>
                                            <div className="floor-action-icon">
                                                <ChevronRight size={24} />
                                            </div>
                                        </div>

                                        <div className="floor-stats-row">
                                            <div className="floor-stat-item">
                                                <Users size={18} />
                                                <div>
                                                    <div className="stat-number">{floor.total_students}</div>
                                                    <div className="stat-label">Students</div>
                                                </div>
                                            </div>
                                            <div className="floor-stat-item">
                                                <UserCheck size={18} />
                                                <div>
                                                    <div className="stat-number">{floor.total_mentors}</div>
                                                    <div className="stat-label">Mentors</div>
                                                </div>
                                            </div>
                                        </div>

                                        <div className="floor-wing-badge">
                                            {floor.floor_wing ? (
                                                <>
                                                    <Building2 size={16} />
                                                    <span>Floor Wing: {floor.floor_wing}</span>
                                                </>
                                            ) : (
                                                <>
                                                    <Clock size={16} />
                                                    <span>No Floor Wing assigned</span>
                                                </>
                                            )}
                                        </div>

                                        {floor.submissions && (
                                            <div className="floor-submissions">
                                                <div className="submission-progress">
                                                    <div 
                                                        className="progress-fill"
                                                        style={{ 
                                                            width: `${floor.submissions.progress_percentage || 0}%`
                                                        }}
                                                    />
                                                </div>
                                                <div className="submission-summary">
                                                    <span className="submission-item approved">
                                                        ✓ {floor.submissions.approved}
                                                    </span>
                                                    <span className="submission-item pending">
                                                        ⏳ {floor.submissions.pending}
                                                    </span>
                                                    <span className="submission-item rejected">
                                                        ✗ {floor.submissions.rejected}
                                                    </span>
                                                </div>
                                            </div>
                                        )}
                                    </div>
                                </GlassCard>
                            </motion.div>
                        ))}
                    </div>
                ) : (
                    <GlassCard>
                        <div className="empty-state">
                            <Layers size={48} color="rgba(255, 255, 255, 0.3)" />
                            <h3>No Floors Available</h3>
                            <p>This campus doesn't have any floors configured yet.</p>
                        </div>
                    </GlassCard>
                )}
            </motion.div>
        </div>
    );
}

export default CampusOverview;
