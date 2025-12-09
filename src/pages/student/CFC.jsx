import React, { useState } from 'react';
// eslint-disable-next-line no-unused-vars
import { motion, AnimatePresence } from 'framer-motion';
import { Trophy, Video, Briefcase, Brain, Upload, CheckCircle, ExternalLink } from 'lucide-react';
import GlassCard from '../../components/GlassCard';
import Button from '../../components/Button';
import Input from '../../components/Input';
import './CFC.css';

const TABS = [
  { id: 'hackathon', label: 'Hackathon', icon: Trophy },
  { id: 'bmc', label: 'BMC Video', icon: Video },
  { id: 'internship', label: 'Internship', icon: Briefcase },
  { id: 'genai', label: 'GenAI Project', icon: Brain },
];

export const CFC = () => {
  const [activeTab, setActiveTab] = useState('hackathon');

  // Hackathon state
  const [certificate, setCertificate] = useState(null);
  const [certificatePreview, setCertificatePreview] = useState(null);
  const [hackathonName, setHackathonName] = useState('');
  const [hackathonMode, setHackathonMode] = useState('');
  const [registrationDate, setRegistrationDate] = useState('');
  const [participationDate, setParticipationDate] = useState('');

  // BMC Video state
  const [videoUrl, setVideoUrl] = useState('');
  const [videoPreview, setVideoPreview] = useState(null);

  // Internship state
  const [internshipData, setInternshipData] = useState({
    company: '',
    mode: '',
    role: '',
    duration: '',
    completionCertificate: null,
    letterOfRecommendation: null,
  });
  const [completionCertPreview, setCompletionCertPreview] = useState(null);
  const [lorPreview, setLorPreview] = useState(null);

  // GenAI state
  const [genAIData, setGenAIData] = useState({
    problemStatement: '',
    solutionType: '',
    innovationTechnology: '',
    innovationIndustry: '',
    githubRepo: '',
  });

  const handleCertificateUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setCertificate(file);
      setCertificatePreview(URL.createObjectURL(file));
    }
  };

  const handleCompletionCertUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setInternshipData({ ...internshipData, completionCertificate: file });
      setCompletionCertPreview(URL.createObjectURL(file));
    }
  };

  const handleLorUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setInternshipData({ ...internshipData, letterOfRecommendation: file });
      setLorPreview(URL.createObjectURL(file));
    }
  };

  const handleVideoUrlChange = (e) => {
    const url = e.target.value;
    setVideoUrl(url);

    // Extract YouTube video ID
    const youtubeRegex = /(?:youtube\.com\/(?:[^/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?/\s]{11})/;
    const match = url.match(youtubeRegex);
    if (match) {
      setVideoPreview(`https://img.youtube.com/vi/${match[1]}/mqdefault.jpg`);
    }
  };

  return (
    <div className="cfc-container">
      {/* Header */}
      <motion.div
        className="cfc-header"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <h1 className="cfc-title">Center for Creativity</h1>
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

              <div className="cfc-input-group">
                <label className="cfc-label">Mode of Participation</label>
                <div className="cfc-radio-group">
                  <label className="cfc-radio-label">
                    <input
                      type="radio"
                      name="hackathonMode"
                      value="online"
                      checked={hackathonMode === 'online'}
                      onChange={(e) => setHackathonMode(e.target.value)}
                      className="cfc-radio-input"
                    />
                    <span className="cfc-radio-custom"></span>
                    <span className="cfc-radio-text">Online</span>
                  </label>
                  <label className="cfc-radio-label">
                    <input
                      type="radio"
                      name="hackathonMode"
                      value="offline"
                      checked={hackathonMode === 'offline'}
                      onChange={(e) => setHackathonMode(e.target.value)}
                      className="cfc-radio-input"
                    />
                    <span className="cfc-radio-custom"></span>
                    <span className="cfc-radio-text">Offline</span>
                  </label>
                </div>
              </div>

              <Input
                label="Date of Registration"
                type="date"
                value={registrationDate}
                onChange={(e) => setRegistrationDate(e.target.value)}
                floatingLabel
              />

              <Input
                label="Date of Participation"
                type="date"
                value={participationDate}
                onChange={(e) => setParticipationDate(e.target.value)}
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
                <Button
                  variant="primary"
                  onClick={() => {
                    if (certificate && hackathonName && hackathonMode && registrationDate && participationDate) {
                      alert('Hackathon submission successful!');
                      setCertificate(null);
                      setCertificatePreview(null);
                      setHackathonName('');
                      setHackathonMode('');
                      setRegistrationDate('');
                      setParticipationDate('');
                    } else {
                      alert('Please fill in all required fields');
                    }
                  }}
                >
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
                <Button
                  variant="primary"
                  onClick={() => {
                    if (videoUrl) {
                      alert('BMC Video submitted successfully!');
                      setVideoUrl('');
                      setVideoPreview(null);
                    } else {
                      alert('Please enter a video URL');
                    }
                  }}
                >
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

              <Input
                label="Company Name"
                placeholder="Enter company name"
                value={internshipData.company}
                onChange={(e) => setInternshipData({ ...internshipData, company: e.target.value })}
                floatingLabel
              />

              <div className="cfc-input-group">
                <label className="cfc-label">Mode of Internship</label>
                <div className="cfc-radio-group">
                  <label className="cfc-radio-label">
                    <input
                      type="radio"
                      name="internshipMode"
                      value="online"
                      checked={internshipData.mode === 'online'}
                      onChange={(e) => setInternshipData({ ...internshipData, mode: e.target.value })}
                      className="cfc-radio-input"
                    />
                    <span className="cfc-radio-custom"></span>
                    <span className="cfc-radio-text">Online</span>
                  </label>
                  <label className="cfc-radio-label">
                    <input
                      type="radio"
                      name="internshipMode"
                      value="offline"
                      checked={internshipData.mode === 'offline'}
                      onChange={(e) => setInternshipData({ ...internshipData, mode: e.target.value })}
                      className="cfc-radio-input"
                    />
                    <span className="cfc-radio-custom"></span>
                    <span className="cfc-radio-text">Offline</span>
                  </label>
                </div>
              </div>

              <Input
                label="Role"
                placeholder="e.g., Software Development Intern"
                value={internshipData.role}
                onChange={(e) => setInternshipData({ ...internshipData, role: e.target.value })}
                floatingLabel
              />

              <Input
                label="Duration of Internship"
                placeholder="e.g., 3 months or 01/2025 - 04/2025"
                value={internshipData.duration}
                onChange={(e) => setInternshipData({ ...internshipData, duration: e.target.value })}
                floatingLabel
              />

              {/* Completion Certificate Upload */}
              <div className="cfc-upload-section">
                <label className="cfc-label">Internship Completion Certificate *</label>

                {!completionCertPreview ? (
                  <label className="cfc-upload-card">
                    <input
                      type="file"
                      accept="image/*,.pdf"
                      onChange={handleCompletionCertUpload}
                      className="cfc-file-input"
                    />
                    <motion.div
                      className="cfc-upload-content"
                      whileHover={{ scale: 1.02 }}
                    >
                      <Upload size={40} className="cfc-upload-icon" />
                      <h3 className="cfc-upload-title">Upload Certificate</h3>
                      <p className="cfc-upload-subtitle">Click to browse</p>
                    </motion.div>
                  </label>
                ) : (
                  <motion.div
                    className="cfc-preview-card"
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                  >
                    {internshipData.completionCertificate.type.startsWith('image/') ? (
                      <img src={completionCertPreview} alt="Certificate" className="cfc-preview-image" />
                    ) : (
                      <div className="cfc-preview-pdf">
                        <Upload size={48} />
                        <p>{internshipData.completionCertificate.name}</p>
                      </div>
                    )}
                    <button
                      className="cfc-preview-remove"
                      onClick={() => {
                        setInternshipData({ ...internshipData, completionCertificate: null });
                        setCompletionCertPreview(null);
                      }}
                    >
                      Change
                    </button>
                  </motion.div>
                )}
              </div>

              {/* Letter of Recommendation Upload (Optional) */}
              <div className="cfc-upload-section">
                <label className="cfc-label">Letter of Recommendation (Optional)</label>

                {!lorPreview ? (
                  <label className="cfc-upload-card">
                    <input
                      type="file"
                      accept="image/*,.pdf"
                      onChange={handleLorUpload}
                      className="cfc-file-input"
                    />
                    <motion.div
                      className="cfc-upload-content"
                      whileHover={{ scale: 1.02 }}
                    >
                      <Upload size={40} className="cfc-upload-icon" />
                      <h3 className="cfc-upload-title">Upload Letter</h3>
                      <p className="cfc-upload-subtitle">Click to browse</p>
                    </motion.div>
                  </label>
                ) : (
                  <motion.div
                    className="cfc-preview-card"
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                  >
                    {internshipData.letterOfRecommendation.type.startsWith('image/') ? (
                      <img src={lorPreview} alt="Letter" className="cfc-preview-image" />
                    ) : (
                      <div className="cfc-preview-pdf">
                        <Upload size={48} />
                        <p>{internshipData.letterOfRecommendation.name}</p>
                      </div>
                    )}
                    <button
                      className="cfc-preview-remove"
                      onClick={() => {
                        setInternshipData({ ...internshipData, letterOfRecommendation: null });
                        setLorPreview(null);
                      }}
                    >
                      Change
                    </button>
                  </motion.div>
                )}
              </div>

              <div className="cfc-actions">
                <Button
                  variant="primary"
                  onClick={() => {
                    if (internshipData.company && internshipData.mode && internshipData.role && internshipData.duration && internshipData.completionCertificate) {
                      alert('Internship details submitted successfully!');
                      setInternshipData({
                        company: '',
                        mode: '',
                        role: '',
                        duration: '',
                        completionCertificate: null,
                        letterOfRecommendation: null,
                      });
                      setCompletionCertPreview(null);
                      setLorPreview(null);
                    } else {
                      alert('Please fill in all required fields');
                    }
                  }}
                >
                  Submit
                </Button>
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

              <div className="cfc-textarea-group">
                <label className="cfc-label">Problem Statement</label>
                <textarea
                  className="cfc-textarea"
                  rows="4"
                  placeholder="Describe the problem your GenAI project addresses..."
                  value={genAIData.problemStatement}
                  onChange={(e) => setGenAIData({ ...genAIData, problemStatement: e.target.value })}
                />
              </div>

              <Input
                label="Solution Type"
                placeholder="e.g., Website, Web App, Mobile App, Desktop App"
                value={genAIData.solutionType}
                onChange={(e) => setGenAIData({ ...genAIData, solutionType: e.target.value })}
                floatingLabel
              />

              <Input
                label="Innovation Technology"
                placeholder="e.g., Machine Learning, NLP, Computer Vision"
                value={genAIData.innovationTechnology}
                onChange={(e) => setGenAIData({ ...genAIData, innovationTechnology: e.target.value })}
                floatingLabel
              />

              <Input
                label="Innovation Industry"
                placeholder="e.g., Healthcare, Finance, Education, E-commerce"
                value={genAIData.innovationIndustry}
                onChange={(e) => setGenAIData({ ...genAIData, innovationIndustry: e.target.value })}
                floatingLabel
              />

              <Input
                label="GitHub Repository"
                placeholder="https://github.com/username/repository"
                value={genAIData.githubRepo}
                onChange={(e) => setGenAIData({ ...genAIData, githubRepo: e.target.value })}
                icon={<ExternalLink size={20} />}
                floatingLabel
              />

              <div className="cfc-actions">
                <Button
                  variant="primary"
                  onClick={() => {
                    if (genAIData.problemStatement && genAIData.solutionType && genAIData.innovationTechnology && genAIData.innovationIndustry && genAIData.githubRepo) {
                      alert('GenAI Project submitted successfully!');
                      setGenAIData({
                        problemStatement: '',
                        solutionType: '',
                        innovationTechnology: '',
                        innovationIndustry: '',
                        githubRepo: '',
                      });
                    } else {
                      alert('Please fill in all required fields');
                    }
                  }}
                >
                  Submit Project
                </Button>
              </div>
            </GlassCard>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default CFC;
