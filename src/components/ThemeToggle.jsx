import React from 'react';
import { motion } from 'framer-motion';
import { Sun, Moon } from 'lucide-react';
import { useTheme } from '../theme/ThemeContext';
import './ThemeToggle.css';

export const ThemeToggle = ({ className = '' }) => {
  const { isDark, toggleTheme } = useTheme();

  return (
    <motion.button
      className={`theme-toggle ${className}`}
      onClick={toggleTheme}
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      aria-label="Toggle theme"
<<<<<<< HEAD
      type="button"
=======
>>>>>>> 8a237f26876c53989100c758417fd3467c1cac1a
    >
      <motion.div
        className="theme-toggle-track"
        animate={{
          backgroundColor: isDark ? '#212121' : '#ffcc00',
        }}
      >
        <motion.div
          className="theme-toggle-thumb"
          animate={{
            x: isDark ? 28 : 0,
          }}
          transition={{ type: 'spring', stiffness: 500, damping: 30 }}
        >
          {isDark ? (
            <Moon size={16} className="theme-toggle-icon" />
          ) : (
            <Sun size={16} className="theme-toggle-icon" />
          )}
        </motion.div>
      </motion.div>
    </motion.button>
  );
};

export default ThemeToggle;
