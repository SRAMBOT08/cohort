import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Upload, FileText, CheckCircle, Image as ImageIcon } from 'lucide-react';
import { useTheme } from '../theme/ThemeContext';
import GlassCard from '../components/GlassCard';
import Button from '../components/Button';
import Input from '../components/Input';
import ProgressBar from '../components/ProgressBar';
import cltService from '../services/clt';
import './CLT.css';

export const CLT = () => {
  const { theme } = useTheme();
  const [currentStep, setCurrentStep] = useState(1);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    platform: '',
    completionDate: '',
    files: [],
  });
  const [isDragging, setIsDragging] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submissions, setSubmissions] = useState([]);
  const [stats, setStats] = useState(null);
  const [error, setError] = useState(null);

  const steps = [
    { id: 1, label: 'Course Details', icon: FileText },
    { id: 2, label: 'Learning Evidence', icon: ImageIcon },
    { id: 3, label: 'Review & Submit', icon: CheckCircle },
  ];

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const files = Array.from(e.dataTransfer.files);
    setFormData({ ...formData, files: [...formData.files, ...files] });
  };

  const handleFileInput = (e) => {
    const files = Array.from(e.target.files);
    // Validate file size (10MB max per file)
    const validFiles = files.filter(file => {
      if (file.size > 10 * 1024 * 1024) {
        alert(`File ${file.name} exceeds 10MB limit`);
        return false;
      }
      return true;
    });
    setFormData({ ...formData, files: [...formData.files, ...validFiles] });
  };

  // Load submissions and stats on component mount
  useEffect(() => {
    loadSubmissions();
    loadStats();
  }, []);

  const loadSubmissions = async () => {
    try {
      const data = await cltService.getSubmissions();
      setSubmissions(data.results || data);
    } catch (err) {
      console.error('Failed to load submissions:', err);
      setError('Failed to load submissions. Please ensure you are logged in.');
    }
  };

  const loadStats = async () => {
    try {
      const data = await cltService.getStats();
      setStats(data);
    } catch (err) {
      console.error('Failed to load stats:', err);
    }
  };

  const handleSubmit = async () => {
    setIsSubmitting(true);
    setError(null);

    try {
      // Simulate upload progress for better UX
      const progressInterval = setInterval(() => {
        setUploadProgress(prev => Math.min(prev + 10, 90));
      }, 200);

      // Create submission with files
      const submissionData = {
        title: formData.title,
        description: formData.description,
        platform: formData.platform,
        completion_date: formData.completionDate,
        files: formData.files,
      };

      const createdSubmission = await cltService.createSubmission(submissionData);

      clearInterval(progressInterval);
      setUploadProgress(100);

      // Wait a moment to show 100% progress
      setTimeout(async () => {
        // Submit the submission for review
        await cltService.submitForReview(createdSubmission.id);

        alert('Submission successful! Your submission is now under review.');
        
        // Reset form
        setFormData({ 
          title: '', 
          description: '', 
          platform: '', 
          completionDate: '', 
          files: [] 
        });
        setCurrentStep(1);
        setUploadProgress(0);
        setIsSubmitting(false);

        // Reload data
        loadSubmissions();
        loadStats();
      }, 500);

    } catch (err) {
      console.error('Submission failed:', err);
      setError(err.response?.data?.message || 'Submission failed. Please try again.');
      setIsSubmitting(false);
      setUploadProgress(0);
      alert('Submission failed: ' + (err.response?.data?.message || err.message));
    }
  };

  return (
    <div className="clt-container">

      {/* Header */}
      <motion.div
        className="clt-header"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <h1 className="clt-title">Creative Learning Track</h1>
        <p className="clt-subtitle">
          Document your creative projects and learning journey
        </p>
      </motion.div>

      {/* Step Indicators */}
      <div className="clt-steps">
        {steps.map((step, index) => {
          const StepIcon = step.icon;
          const isActive = currentStep === step.id;
          const isCompleted = currentStep > step.id;

          return (
            <React.Fragment key={step.id}>
              <motion.div
                className={`clt-step ${isActive ? 'clt-step--active' : ''} ${isCompleted ? 'clt-step--completed' : ''}`}
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: index * 0.1 }}
              >
                <div className="clt-step-icon">
                  <StepIcon size={20} />
                  {isCompleted && (
                    <motion.div
                      className="clt-step-check"
                      initial={{ scale: 0 }}
                      animate={{ scale: 1 }}
                      transition={{ type: 'spring' }}
                    >
                      <CheckCircle size={16} />
                    </motion.div>
                  )}
                </div>
                <span className="clt-step-label">{step.label}</span>
              </motion.div>

              {index < steps.length - 1 && (
                <div className="clt-step-connector">
                  <motion.div
                    className="clt-step-connector-fill"
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

      {/* Form Content */}
      <GlassCard variant="medium" className="clt-form-card">
        <AnimatePresence mode="wait">
          {currentStep === 1 && (
            <motion.div
              key="step1"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.3 }}
              className="clt-step-content"
            >
              <h2 className="clt-form-title">Course Details</h2>

              <Input
                label="Course Title"
                placeholder="Enter course title"
                value={formData.title}
                onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                floatingLabel
              />

              <div className="clt-textarea-wrapper">
                <label className="clt-textarea-label">Course Description</label>
                <textarea
                  className="clt-textarea"
                  rows="5"
                  placeholder="Describe the course you had completed..."
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                />
              </div>

              <Input
                label="Platform"
                placeholder="e.g., Coursera, Udemy, edX"
                value={formData.platform}
                onChange={(e) => setFormData({ ...formData, platform: e.target.value })}
                floatingLabel
              />

              <Input
                label="Completion Date"
                type="date"
                value={formData.completionDate}
                onChange={(e) => setFormData({ ...formData, completionDate: e.target.value })}
                floatingLabel
              />

              <div className="clt-form-actions">
                <Button
                  variant="primary"
                  onClick={() => {
                    if (formData.title && formData.description) {
                      setCurrentStep(2);
                    } else {
                      alert('Please fill in all required fields');
                    }
                  }}
                >
                  Next Step
                </Button>
              </div>
            </motion.div>
          )}

          {currentStep === 2 && (
            <motion.div
              key="step2"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.3 }}
              className="clt-step-content"
            >
              <h2 className="clt-form-title">Upload Evidence</h2>

              <motion.div
                className={`clt-upload-zone ${isDragging ? 'clt-upload-zone--dragging' : ''}`}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                whileHover={{ scale: 1.01 }}
                transition={{ duration: 0.2 }}
              >
                <input
                  type="file"
                  multiple
                  accept="image/*,.pdf"
                  onChange={handleFileInput}
                  className="clt-upload-input"
                  id="file-upload"
                />

                <label htmlFor="file-upload" className="clt-upload-label">
                  <motion.div
                    className="clt-upload-icon"
                    animate={{
                      y: isDragging ? -10 : 0,
                    }}
                  >
                    <Upload size={48} />
                  </motion.div>

                  <h3 className="clt-upload-title">
                    {isDragging ? 'Drop files here' : 'Drag & drop files'}
                  </h3>
                  <p className="clt-upload-subtitle">or click to browse</p>
                  <p className="clt-upload-hint">Supports images and PDF files</p>
                </label>
              </motion.div>

              {/* File Preview Cards */}
              {formData.files.length > 0 && (
                <div className="clt-file-grid">
                  {formData.files.map((file, index) => (
                    <motion.div
                      key={index}
                      className="clt-file-card"
                      initial={{ opacity: 0, scale: 0.8 }}
                      animate={{ opacity: 1, scale: 1 }}
                      whileHover={{ y: -4 }}
                      transition={{ delay: index * 0.1 }}
                    >
                      <div className="clt-file-icon">
                        <FileText size={24} />
                      </div>
                      <div className="clt-file-info">
                        <p className="clt-file-name">{file.name}</p>
                        <p className="clt-file-size">
                          {(file.size / 1024).toFixed(2)} KB
                        </p>
                      </div>
                      <button
                        className="clt-file-remove"
                        onClick={() => {
                          const newFiles = formData.files.filter((_, i) => i !== index);
                          setFormData({ ...formData, files: newFiles });
                        }}
                      >
                        ×
                      </button>
                    </motion.div>
                  ))}
                </div>
              )}

              <div className="clt-form-actions">
                <Button
                  variant="outline"
                  onClick={() => setCurrentStep(1)}
                >
                  Back
                </Button>
                <Button
                  variant="primary"
                  onClick={() => {
                    if (formData.files.length > 0) {
                      setCurrentStep(3);
                    } else {
                      alert('Please upload at least one file');
                    }
                  }}
                >
                  Next Step
                </Button>
              </div>
            </motion.div>
          )}

          {currentStep === 3 && (
            <motion.div
              key="step3"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.3 }}
              className="clt-step-content"
            >
              <h2 className="clt-form-title">Review & Submit</h2>

              <div className="clt-review-section">
                <h3 className="clt-review-label">Course Title</h3>
                <p className="clt-review-value">{formData.title}</p>
              </div>

              <div className="clt-review-section">
                <h3 className="clt-review-label">Description</h3>
                <p className="clt-review-value">{formData.description}</p>
              </div>

              <div className="clt-review-section">
                <h3 className="clt-review-label">Platform</h3>
                <p className="clt-review-value">{formData.platform}</p>
              </div>

              <div className="clt-review-section">
                <h3 className="clt-review-label">Completion Date</h3>
                <p className="clt-review-value">{formData.completionDate}</p>
              </div>

              <div className="clt-review-section">
                <h3 className="clt-review-label">Uploaded Files</h3>
                <p className="clt-review-value">{formData.files.length} file(s)</p>
              </div>

              {error && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="clt-error-section"
                  style={{
                    padding: '1rem',
                    marginBottom: '1rem',
                    backgroundColor: 'rgba(239, 68, 68, 0.1)',
                    border: '1px solid rgba(239, 68, 68, 0.3)',
                    borderRadius: '0.5rem',
                    color: '#ef4444'
                  }}
                >
                  <p>{error}</p>
                </motion.div>
              )}

              {isSubmitting && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="clt-progress-section"
                >
                  <p className="clt-progress-label">Uploading your submission...</p>
                  <ProgressBar progress={uploadProgress} animated />
                </motion.div>
              )}

              <div className="clt-form-actions">
                <Button
                  variant="outline"
                  onClick={() => setCurrentStep(2)}
                  disabled={isSubmitting}
                >
                  Back
                </Button>
                <Button
                  variant="primary"
                  withGlow
                  onClick={handleSubmit}
                  disabled={isSubmitting}
                >
                  {isSubmitting ? 'Submitting...' : 'Finalize Submission'}
                </Button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </GlassCard>
    </div>
  );
};

export default CLT;
