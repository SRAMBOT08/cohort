import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Trophy, Video, Briefcase, Brain, Upload, CheckCircle, ExternalLink } from 'lucide-react';
import { useTheme } from '../theme/ThemeContext';
import GlassCard from '../components/GlassCard';
import Button from '../components/Button';
import Input from '../components/Input';
import './CFC.css';

const TABS = [
  { id: 'hackathon', label: 'Hackathon', icon: Trophy },
  { id: 'bmc', label: 'BMC Video', icon: Video },
  { id: 'internship', label: 'Internship', icon: Briefcase },
  { id: 'genai', label: 'GenAI Project', icon: Brain },
];

export const CFC = () => {
  const { theme } = useTheme();
  const [activeTab, setActiveTab] = useState('hackathon');

  // Hackathon state
  const [certificate, setCertificate] = useState(null);
  const [certificatePreview, setCertificatePreview] = useState(null);
  const [hackathonName, setHackathonName] = useState('');

  // BMC Video state
  const [videoUrl, setVideoUrl] = useState('');
  const [videoPreview, setVideoPreview] = useState(null);

  // Internship state
  const [internshipData, setInternshipData] = useState({
    company: '',
    role: '',
    duration: '',
    description: '',
  });
  const [internshipStatus, setInternshipStatus] = useState(1); // 1-4 steps

  // GenAI state
  const [genAIData, setGenAIData] = useState({
    courseName: '',
    platform: '',
    completionDate: '',
    certificate: null,
  });
  const [genAIStatus, setGenAIStatus] = useState(1);

  const handleCertificateUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setCertificate(file);
      setCertificatePreview(URL.createObjectURL(file));
    }
  };

  const handleVideoUrlChange = (e) => {
    const url = e.target.value;
    setVideoUrl(url);

    // Extract YouTube video ID
    const youtubeRegex = /(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})/;
    const match = url.match(youtubeRegex);
    if (match) {
      setVideoPreview(`https://img.youtube.com/vi/${match[1]}/mqdefault.jpg`);
    }
  };

  const statusSteps = ['Application', 'Interview', 'Offer', 'Completion'];

  return (
    <div className="cfc-container">
      {/* Header */}
      <motion.div
        className="cfc-header"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <h1 className="cfc-title">Career, Future & Competency Development</h1>
        <p className="cfc-subtitle">
          Build your professional portfolio and track your career development
        </p>
      </motion.div>

      {/* Tabs */}
      <div className="cfc-tabs">
        <div className="cfc-tabs-list">
          {TABS.map((tab) => {
            const TabIcon = tab.icon;
            const isActive = activeTab === tab.id;

            return (
              <motion.button
                key={tab.id}
                className={`cfc-tab ${isActive ? 'cfc-tab--active' : ''}`}
                onClick={() => setActiveTab(tab.id)}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                <TabIcon size={20} />
                <span>{tab.label}</span>

                {isActive && (
                  <motion.div
                    className="cfc-tab-indicator"
                    layoutId="activeTab"
                    transition={{ type: 'spring', stiffness: 500, damping: 30 }}
                  />
                )}
              </motion.button>
            );
          })}
        </div>
      </div>

      {/* Tab Content */}
      <AnimatePresence mode="wait">
        {activeTab === 'hackathon' && (
          <motion.div
            key="hackathon"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
          >
            <GlassCard variant="medium" className="cfc-content-card">
              <div className="cfc-section-header">
                <Trophy size={32} className="cfc-section-icon" />
                <div>
                  <h2 className="cfc-section-title">Hackathon Participation</h2>
                  <p className="cfc-section-subtitle">
                    Upload your hackathon certificates and achievements
                  </p>
                </div>
              </div>

              <Input
                label="Hackathon Name"
                placeholder="e.g., Smart India Hackathon 2025"
                value={hackathonName}
                onChange={(e) => setHackathonName(e.target.value)}
                floatingLabel
              />

              <div className="cfc-upload-section">
                <label className="cfc-label">Certificate</label>

                {!certificatePreview ? (
                  <label className="cfc-upload-card">
                    <input
                      type="file"
                      accept="image/*,.pdf"
                      onChange={handleCertificateUpload}
                      className="cfc-file-input"
                    />
                    <motion.div
                      className="cfc-upload-content"
                      whileHover={{ scale: 1.02 }}
                    >
                      <Upload size={48} className="cfc-upload-icon" />
                      <h3 className="cfc-upload-title">Upload Certificate</h3>
                      <p className="cfc-upload-subtitle">Click to browse or drag & drop</p>
                    </motion.div>
                  </label>
                ) : (
                  <motion.div
                    className="cfc-preview-card"
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                  >
                    {certificate.type.startsWith('image/') ? (
                      <img src={certificatePreview} alt="Certificate" className="cfc-preview-image" />
                    ) : (
                      <div className="cfc-preview-pdf">
                        <Upload size={64} />
                        <p>{certificate.name}</p>
                      </div>
                    )}

                    <motion.div
                      className="cfc-verified-badge"
                      initial={{ scale: 0, rotate: -180 }}
                      animate={{ scale: 1, rotate: 0 }}
                      transition={{ delay: 0.3, type: 'spring' }}
                    >
                      <CheckCircle size={24} />
                      <span>Verified</span>
                    </motion.div>

                    <button
                      className="cfc-preview-remove"
                      onClick={() => {
                        setCertificate(null);
                        setCertificatePreview(null);
                      }}
                    >
                      Change
                    </button>
                  </motion.div>
                )}
              </div>

              <div className="cfc-actions">
                <Button variant="primary" disabled={!certificate || !hackathonName}>
                  Submit
                </Button>
              </div>
            </GlassCard>
          </motion.div>
        )}

        {activeTab === 'bmc' && (
          <motion.div
            key="bmc"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
          >
            <GlassCard variant="medium" className="cfc-content-card">
              <div className="cfc-section-header">
                <Video size={32} className="cfc-section-icon" />
                <div>
                  <h2 className="cfc-section-title">BMC Video Submission</h2>
                  <p className="cfc-section-subtitle">
                    Share your Business Model Canvas presentation
                  </p>
                </div>
              </div>

              <Input
                label="YouTube Video URL"
                placeholder="https://youtube.com/watch?v=..."
                value={videoUrl}
                onChange={handleVideoUrlChange}
                icon={<ExternalLink size={20} />}
                floatingLabel
              />

              {videoPreview && (
                <motion.div
                  className="cfc-video-preview"
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                >
                  <img src={videoPreview} alt="Video thumbnail" className="cfc-video-thumbnail" />
                  <motion.button
                    className="cfc-watch-button"
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.9 }}
                    animate={{
                      boxShadow: [
                        '0 0 20px rgba(247, 201, 72, 0.4)',
                        '0 0 40px rgba(247, 201, 72, 0.8)',
                        '0 0 20px rgba(247, 201, 72, 0.4)',
                      ],
                    }}
                    transition={{ duration: 2, repeat: Infinity }}
                  >
                    <Video size={32} />
                  </motion.button>
                </motion.div>
              )}

              <div className="cfc-actions">
                <Button variant="primary" disabled={!videoUrl}>
                  Submit Video
                </Button>
              </div>
            </GlassCard>
          </motion.div>
        )}

        {activeTab === 'internship' && (
          <motion.div
            key="internship"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
          >
            <GlassCard variant="medium" className="cfc-content-card">
              <div className="cfc-section-header">
                <Briefcase size={32} className="cfc-section-icon" />
                <div>
                  <h2 className="cfc-section-title">Internship Tracker</h2>
                  <p className="cfc-section-subtitle">
                    Log and track your internship journey
                  </p>
                </div>
              </div>

              {/* Status Tracker */}
              <div className="cfc-status-tracker">
                {statusSteps.map((step, index) => {
                  const stepNumber = index + 1;
                  const isActive = internshipStatus === stepNumber;
                  const isCompleted = internshipStatus > stepNumber;

                  return (
                    <React.Fragment key={step}>
                      <motion.div
                        className={`cfc-status-step ${isActive ? 'cfc-status-step--active' : ''} ${isCompleted ? 'cfc-status-step--completed' : ''}`}
                        initial={{ opacity: 0, scale: 0.8 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ delay: index * 0.1 }}
                        onClick={() => setInternshipStatus(stepNumber)}
                      >
                        <div className="cfc-status-number">
                          {isCompleted ? <CheckCircle size={16} /> : stepNumber}
                        </div>
                        <div className="cfc-status-label">{step}</div>
                      </motion.div>

                      {index < statusSteps.length - 1 && (
                        <div className="cfc-status-line">
                          <motion.div
                            className="cfc-status-line-fill"
                            initial={{ width: 0 }}
                            animate={{ width: isCompleted ? '100%' : '0%' }}
                            transition={{ duration: 0.5 }}
                          />
                        </div>
                      )}
                    </React.Fragment>
                  );
                })}
              </div>

              <Input
                label="Company Name"
                placeholder="Enter company name"
                value={internshipData.company}
                onChange={(e) => setInternshipData({ ...internshipData, company: e.target.value })}
                floatingLabel
              />

              <Input
                label="Role"
                placeholder="e.g., Software Development Intern"
                value={internshipData.role}
                onChange={(e) => setInternshipData({ ...internshipData, role: e.target.value })}
                floatingLabel
              />

              <Input
                label="Duration"
                placeholder="e.g., 3 months"
                value={internshipData.duration}
                onChange={(e) => setInternshipData({ ...internshipData, duration: e.target.value })}
                floatingLabel
              />

              <div className="cfc-textarea-group">
                <label className="cfc-label">Description</label>
                <textarea
                  className="cfc-textarea"
                  rows="4"
                  placeholder="Describe your role and responsibilities..."
                  value={internshipData.description}
                  onChange={(e) => setInternshipData({ ...internshipData, description: e.target.value })}
                />
              </div>

              <div className="cfc-actions">
                <Button variant="primary">Save Progress</Button>
              </div>
            </GlassCard>
          </motion.div>
        )}

        {activeTab === 'genai' && (
          <motion.div
            key="genai"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
          >
            <GlassCard variant="medium" className="cfc-content-card">
              <div className="cfc-section-header">
                <Brain size={32} className="cfc-section-icon" />
                <div>
                  <h2 className="cfc-section-title">GenAI Project Completion</h2>
                  <p className="cfc-section-subtitle">
                    Track your AI/ML project progress and certifications
                  </p>
                </div>
              </div>

              {/* Status Tracker */}
              <div className="cfc-status-tracker">
                {['Enrolled', 'In Progress', 'Completed', 'Certified'].map((step, index) => {
                  const stepNumber = index + 1;
                  const isActive = genAIStatus === stepNumber;
                  const isCompleted = genAIStatus > stepNumber;

                  return (
                    <React.Fragment key={step}>
                      <motion.div
                        className={`cfc-status-step ${isActive ? 'cfc-status-step--active' : ''} ${isCompleted ? 'cfc-status-step--completed' : ''}`}
                        initial={{ opacity: 0, scale: 0.8 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ delay: index * 0.1 }}
                        onClick={() => setGenAIStatus(stepNumber)}
                      >
                        <div className="cfc-status-number">
                          {isCompleted ? <CheckCircle size={16} /> : stepNumber}
                        </div>
                        <div className="cfc-status-label">{step}</div>
                      </motion.div>

                      {index < 3 && (
                        <div className="cfc-status-line">
                          <motion.div
                            className="cfc-status-line-fill"
                            initial={{ width: 0 }}
                            animate={{ width: isCompleted ? '100%' : '0%' }}
                            transition={{ duration: 0.5 }}
                          />
                        </div>
                      )}
                    </React.Fragment>
                  );
                })}
              </div>

              <Input
                label="Course Name"
                placeholder="e.g., Introduction to Generative AI"
                value={genAIData.courseName}
                onChange={(e) => setGenAIData({ ...genAIData, courseName: e.target.value })}
                floatingLabel
              />

              <Input
                label="Platform"
                placeholder="e.g., Coursera, edX, Udacity"
                value={genAIData.platform}
                onChange={(e) => setGenAIData({ ...genAIData, platform: e.target.value })}
                floatingLabel
              />

              <Input
                label="Completion Date"
                type="date"
                value={genAIData.completionDate}
                onChange={(e) => setGenAIData({ ...genAIData, completionDate: e.target.value })}
              />

              <div className="cfc-actions">
                <Button variant="primary">Submit Course</Button>
              </div>
            </GlassCard>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default CFC;
