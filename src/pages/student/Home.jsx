import React from 'react';
// eslint-disable-next-line no-unused-vars
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { Lightbulb, Heart, Trophy, Linkedin, Code, ArrowRight, Sparkles } from 'lucide-react';
import GlassCard from '../../components/GlassCard';
import './Home.css';

const PILLARS = [
  {
    id: 'clt',
    title: 'Center for Learning and Teaching',
    description: 'Document your creative projects and showcase your learning journey',
    icon: Lightbulb,
    color: '#F7C948',
    path: '/clt',
  },
  {
    id: 'sri',
    title: 'Social Responsibility Initiatives',
    description: 'Track your community service and social impact activities',
    icon: Heart,
    color: '#E53935',
    path: '/sri',
  },
  {
    id: 'cfc',
    title: 'Center for Creativity',
    description: 'Build your professional portfolio and track career development',
    icon: Trophy,
    color: '#FFC107',
    path: '/cfc',
  },
  {
    id: 'iipc',
    title: 'Industry Institute Partnership Cell',
    description: 'Verify your LinkedIn activity and professional network',
    icon: Linkedin,
    color: '#0A66C2',
    path: '/iipc',
  },
  {
    id: 'scd',
    title: 'Skill and Career Development',
    description: 'Track your coding skills and competitive programming journey',
    icon: Code,
    color: '#FF5722',
    path: '/scd',
  },
];

export const HomePage = () => {
  return (
    <div className="home-container">
      {/* Animated Background */}
      <div className="home-background">
        <motion.div
          className="home-bg-gradient home-bg-gradient-1"
          animate={{
            scale: [1, 1.2, 1],
            rotate: [0, 90, 0],
            opacity: [0.3, 0.5, 0.3],
          }}
          transition={{
            duration: 20,
            repeat: Infinity,
            ease: 'easeInOut',
          }}
        />
        <motion.div
          className="home-bg-gradient home-bg-gradient-2"
          animate={{
            scale: [1, 1.3, 1],
            rotate: [0, -90, 0],
            opacity: [0.2, 0.4, 0.2],
          }}
          transition={{
            duration: 25,
            repeat: Infinity,
            ease: 'easeInOut',
            delay: 2,
          }}
        />
      </div>

      {/* Hero Section */}
      <motion.div
        className="home-hero"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
      >
        <motion.div
          className="home-hero-badge"
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.3 }}
        >
          <Sparkles size={16} />
          <span>Educational Excellence Platform</span>
        </motion.div>

        <h1 className="home-title">
          Welcome to{' '}
          <span className="home-title-gradient">Cohort Web</span>
        </h1>

        <p className="home-subtitle">
          Your comprehensive platform for tracking academic excellence, social responsibility,
          and professional development across five key pillars of growth
        </p>

        <motion.div
          className="home-stats"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
        >
          <div className="home-stat">
            <div className="home-stat-value">5</div>
            <div className="home-stat-label">Pillars</div>
          </div>
          <div className="home-stat-divider" />
          <div className="home-stat">
            <div className="home-stat-value">100%</div>
            <div className="home-stat-label">Progress Tracking</div>
          </div>
          <div className="home-stat-divider" />
          <div className="home-stat">
            <div className="home-stat-value">24/7</div>
            <div className="home-stat-label">Access</div>
          </div>
        </motion.div>
      </motion.div>

      {/* Pillars Grid */}
      <div className="home-pillars">
        <motion.h2
          className="home-section-title"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
        >
          Explore Our Pillars
        </motion.h2>

        <div className="home-pillars-grid">
          {PILLARS.map((pillar, index) => {
            const Icon = pillar.icon;

            return (
              <motion.div
                key={pillar.id}
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.7 + index * 0.1 }}
              >
                <Link to={pillar.path} className="home-pillar-link">
                  <GlassCard
                    variant="medium"
                    hoverable
                    className="home-pillar-card"
                  >
                    <motion.div
                      className="home-pillar-icon"
                      style={{ backgroundColor: `${pillar.color}20` }}
                      whileHover={{ scale: 1.1, rotate: 5 }}
                      transition={{ type: 'spring', stiffness: 400 }}
                    >
                      <Icon size={32} style={{ color: pillar.color }} />
                    </motion.div>

                    <h3 className="home-pillar-title">{pillar.title}</h3>
                    <p className="home-pillar-description">{pillar.description}</p>

                    <motion.div
                      className="home-pillar-arrow"
                      whileHover={{ x: 5 }}
                      transition={{ type: 'spring', stiffness: 400 }}
                    >
                      <ArrowRight size={20} style={{ color: pillar.color }} />
                    </motion.div>
                  </GlassCard>
                </Link>
              </motion.div>
            );
          })}
        </div>
      </div>

      {/* Features Section */}
      <motion.div
        className="home-features"
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 1.2 }}
      >
        <GlassCard variant="heavy" className="home-features-card">
          <h2 className="home-features-title">Built for Excellence</h2>

          <div className="home-features-grid">
            <div className="home-feature-item">
              <div className="home-feature-icon">✨</div>
              <h4 className="home-feature-title">Modern UI</h4>
              <p className="home-feature-text">
                Beautiful glassmorphism design with smooth animations
              </p>
            </div>

            <div className="home-feature-item">
              <div className="home-feature-icon">🌓</div>
              <h4 className="home-feature-title">Dark Mode</h4>
              <p className="home-feature-text">
                Comfortable viewing experience in any lighting condition
              </p>
            </div>

            <div className="home-feature-item">
              <div className="home-feature-icon">📊</div>
              <h4 className="home-feature-title">Progress Tracking</h4>
              <p className="home-feature-text">
                Real-time monitoring of your academic and professional growth
              </p>
            </div>

            <div className="home-feature-item">
              <div className="home-feature-icon">🔒</div>
              <h4 className="home-feature-title">Secure</h4>
              <p className="home-feature-text">
                Your data is protected with industry-standard security
              </p>
            </div>
          </div>
        </GlassCard>
      </motion.div>
    </div>
  );
};

export default HomePage;
