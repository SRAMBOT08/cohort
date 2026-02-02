import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Clock, Lightbulb, Flame, Calendar, HelpCircle, Trophy } from 'lucide-react';
import PropTypes from 'prop-types';
import './SelectBubblesGame.css';

const SelectBubblesGame = ({ onClose, pillarName = 'default' }) => {
    const [bubbles, setBubbles] = useState([]);
    const [selectedOrder, setSelectedOrder] = useState([]);
    const [isComplete, setIsComplete] = useState(false);
    const [showError, setShowError] = useState(false);
    const [moveCount, setMoveCount] = useState(0);
    const [timeElapsed, setTimeElapsed] = useState(0);
    const [gameStarted, setGameStarted] = useState(false);
    const [showHint, setShowHint] = useState(false);
    const [streak, setStreak] = useState(0);
    const [showRules, setShowRules] = useState(false);
    const [currentPuzzle, setCurrentPuzzle] = useState(1);
    const [allPuzzlesComplete, setAllPuzzlesComplete] = useState(false);
    const [lastPlayed, setLastPlayed] = useState(null);
    const totalPuzzles = 3;

    // Timer - runs across all 3 puzzles
    useEffect(() => {
        if (!gameStarted || allPuzzlesComplete) return;
        const timer = setInterval(() => setTimeElapsed(prev => prev + 1), 1000);
        return () => clearInterval(timer);
    }, [gameStarted, allPuzzlesComplete]);

    // Generate daily seed based on date
    const getDailySeed = () => {
        const today = new Date();
        return `${today.getFullYear()}-${today.getMonth() + 1}-${today.getDate()}-${pillarName}-selectbubbles`;
    };

    // Seeded random number generator
    const seededRandom = (seed) => {
        const x = Math.sin(seed) * 10000;
        return x - Math.floor(x);
    };

    // Load streak and check if already played today
    useEffect(() => {
        const savedData = JSON.parse(localStorage.getItem(`selectbubbles-${pillarName}`) || '{}');
        setStreak(savedData.streak || 0);
        setLastPlayed(savedData.lastPlayed || null);
        
        // Check if already completed today
        const today = new Date().toDateString();
        if (savedData.lastPlayed === today && savedData.completed) {
            setAllPuzzlesComplete(true);
            setTimeElapsed(savedData.completionTime || 0);
        }
    }, [pillarName]);

    // Generate mathematical expressions with daily seed
    useEffect(() => {
        generateBubbles(currentPuzzle);
    }, [currentPuzzle]);

    const generateBubbles = (puzzleNum = 1) => {
        // Generate seed based on date and puzzle number
        const seed = getDailySeed();
        let hashCode = 0;
        for (let i = 0; i < seed.length; i++) {
            hashCode = seed.charCodeAt(i) + ((hashCode << 5) - hashCode);
        }
        // Add puzzle number to make each puzzle different
        hashCode = hashCode + puzzleNum * 1000;
        
        const random = (index) => seededRandom(hashCode + index);
        
        const expressions = [];
        const numBubbles = 5 + Math.floor(random(0) * 3); // 5-7 bubbles

        // Generate random expressions with their solutions
        for (let i = 0; i < numBubbles; i++) {
            const expr = generateExpression(random, i);
            expressions.push({
                id: i,
                expression: expr.text,
                value: expr.value,
                position: getRandomPosition(i, numBubbles, random)
            });
        }

        setBubbles(expressions);
        setSelectedOrder([]);
        setIsComplete(false);
        setShowError(false);
        setMoveCount(0);
    };

    const generateExpression = (random, seed) => {
        const operators = ['+', '-', '*', '/'];
        const type = Math.floor(random(seed) * 4);

        switch(type) {
            case 0: { // Simple addition/subtraction
                const a = Math.floor(random(seed + 1) * 50) + 1;
                const b = Math.floor(random(seed + 2) * 30) + 1;
                const op = operators[random(seed + 3) < 0.5 ? 0 : 1];
                return {
                    text: `${a} ${op} ${b}`,
                    value: op === '+' ? a + b : a - b
                };
            }
            case 1: { // Multiplication
                const a = Math.floor(random(seed + 1) * 12) + 2;
                const b = Math.floor(random(seed + 2) * 12) + 2;
                return {
                    text: `${a} × ${b}`,
                    value: a * b
                };
            }
            case 2: { // Division
                const b = Math.floor(random(seed + 1) * 8) + 2;
                const result = Math.floor(random(seed + 2) * 15) + 1;
                const a = b * result;
                return {
                    text: `${a} ÷ ${b}`,
                    value: result
                };
            }
            case 3: { // Complex with brackets
                const a = Math.floor(random(seed + 1) * 20) + 1;
                const b = Math.floor(random(seed + 2) * 10) + 1;
                const c = Math.floor(random(seed + 3) * 10) + 1;
                const innerOp = operators[Math.floor(random(seed + 4) * 2)];
                const outerOp = operators[Math.floor(random(seed + 5) * 2)];
                
                let innerValue;
                if (innerOp === '+') innerValue = b + c;
                else if (innerOp === '-') innerValue = b - c;
                else if (innerOp === '*') innerValue = b * c;
                else innerValue = Math.floor(b / c);

                let finalValue;
                if (outerOp === '+') finalValue = a + innerValue;
                else if (outerOp === '-') finalValue = a - innerValue;
                else if (outerOp === '*') finalValue = a * innerValue;
                else finalValue = Math.floor(a / innerValue);

                return {
                    text: `${a} ${outerOp} (${b} ${innerOp} ${c})`,
                    value: finalValue
                };
            }
            default:
                return { text: '0', value: 0 };
        }
    };

    const getRandomPosition = (index, total, random) => {
        const angle = (index / total) * 2 * Math.PI + random(index * 10) * 0.5;
        const radius = 25 + random(index * 10 + 1) * 15; // Reduced from 35-50% to 25-40% to keep bubbles more centered
        
        // Calculate position with constraints to keep bubbles visible
        let x = 50 + radius * Math.cos(angle);
        let y = 50 + radius * Math.sin(angle);
        
        // Constrain x between 15% and 85% to prevent edge clipping
        x = Math.max(15, Math.min(85, x));
        // Constrain y between 15% and 85% to prevent edge clipping
        y = Math.max(15, Math.min(85, y));
        
        return { x, y };
    };

    const handleBubbleClick = (bubble) => {
        if (isComplete || selectedOrder.includes(bubble.id) || allPuzzlesComplete) return;
        if (!gameStarted) setGameStarted(true);

        const newOrder = [...selectedOrder, bubble.id];
        setSelectedOrder(newOrder);
        setMoveCount(prev => prev + 1);

        // Check if selection is correct
        const sortedBubbles = [...bubbles].sort((a, b) => a.value - b.value);
        const expectedId = sortedBubbles[newOrder.length - 1].id;

        if (bubble.id !== expectedId) {
            // Wrong selection
            setShowError(true);
            setTimeout(() => {
                setShowError(false);
                setSelectedOrder([]);
            }, 1000);
        } else if (newOrder.length === bubbles.length) {
            // Puzzle complete!
            setIsComplete(true);
            
            // Check if this was the last puzzle
            if (currentPuzzle < totalPuzzles) {
                // Move to next puzzle after a short delay
                setTimeout(() => {
                    setCurrentPuzzle(prev => prev + 1);
                    setIsComplete(false);
                }, 1500);
            } else {
                // All puzzles complete!
                setAllPuzzlesComplete(true);
                updateStreak();
            }
        }
    };

    // Update streak with proper daily tracking
    const updateStreak = () => {
        const today = new Date().toDateString();
        const savedData = JSON.parse(localStorage.getItem(`selectbubbles-${pillarName}`) || '{}');

        // If already completed today, don't update streak
        if (savedData.lastPlayed === today) {
            setStreak(savedData.streak || 1);
            return;
        }

        let newStreak = 1;
        if (savedData.lastPlayed) {
            const lastDate = new Date(savedData.lastPlayed);
            const todayDate = new Date();

            // Calculate days difference properly
            lastDate.setHours(0, 0, 0, 0);
            todayDate.setHours(0, 0, 0, 0);
            const daysDiff = Math.floor((todayDate - lastDate) / (1000 * 60 * 60 * 24));

            if (daysDiff === 1) {
                // Consecutive day - increment streak
                newStreak = (savedData.streak || 0) + 1;
            } else if (daysDiff > 1) {
                // Gap in days - reset streak
                newStreak = 1;
            }
        }

        setStreak(newStreak);
        localStorage.setItem(`selectbubbles-${pillarName}`, JSON.stringify({
            streak: newStreak,
            lastPlayed: today,
            completed: true,
            completionTime: timeElapsed
        }));
    };

    const toggleHint = () => {
        setShowHint(!showHint);
    };

    const formatTime = (seconds) => {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    };

    const getSortedBubbles = () => {
        return [...bubbles].sort((a, b) => a.value - b.value);
    };

    return (
        <div className="bubbles-game-overlay">
            <motion.div
                className="bubbles-game-container"
                initial={{ scale: 0.9, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 0.9, opacity: 0 }}
            >
                {/* Close button */}
                <button className="bubbles-close-btn" onClick={onClose}>
                    <X size={24} />
                </button>

                {/* Header */}
                <div className="bubbles-game-header">
                    <div className="bubbles-title-icon">🫧</div>
                    <h2>Select Bubbles - 3 Daily Puzzles</h2>
                </div>

                {/* Stats Bar */}
                <div className="bubbles-stats-bar">
                    <div className="bubbles-stat-card">
                        <Calendar size={18} className="bubbles-stat-icon" />
                        <div className="bubbles-stat-content">
                            <span className="bubbles-stat-value">{currentPuzzle}/{totalPuzzles}</span>
                        </div>
                    </div>
                    <div className="bubbles-stat-card bubbles-stat-card--streak">
                        <Flame size={18} className="bubbles-stat-icon" />
                        <div className="bubbles-stat-content">
                            <span className="bubbles-stat-value">{streak}</span>
                            <span className="bubbles-stat-label">Day Streak</span>
                        </div>
                    </div>
                    <div className="bubbles-stat-card">
                        <Clock size={18} className="bubbles-stat-icon" />
                        <div className="bubbles-stat-content">
                            <span className="bubbles-stat-value">{formatTime(timeElapsed)}</span>
                        </div>
                    </div>
                    <button 
                        className="bubbles-stat-card bubbles-rules-btn"
                        onClick={() => setShowRules(!showRules)}
                    >
                        <HelpCircle size={18} className="bubbles-stat-icon" />
                        <div className="bubbles-stat-content">
                            <span className="bubbles-stat-value">Rules</span>
                        </div>
                    </button>
                </div>

                {/* Game Area */}
                <div className={`bubbles-game-area ${showError ? 'shake' : ''}`}>
                    {bubbles.map((bubble, index) => {
                        const isSelected = selectedOrder.includes(bubble.id);
                        const selectionIndex = selectedOrder.indexOf(bubble.id);

                        return (
                            <motion.div
                                key={bubble.id}
                                className={`bubble ${isSelected ? 'selected' : ''} ${isComplete ? 'complete' : ''}`}
                                style={{
                                    left: `${bubble.position.x}%`,
                                    top: `${bubble.position.y}%`
                                }}
                                onClick={() => handleBubbleClick(bubble)}
                                whileHover={{ scale: isSelected ? 1 : 1.1 }}
                                whileTap={{ scale: 0.9 }}
                                initial={{ scale: 0, opacity: 0 }}
                                animate={{ scale: 1, opacity: 1 }}
                                transition={{ delay: index * 0.1 }}
                            >
                                <div className="bubble-content">
                                    <div className="bubble-expression">{bubble.expression}</div>
                                    {showHint && (
                                        <div className="bubble-hint">= {bubble.value}</div>
                                    )}
                                    {isSelected && (
                                        <div className="bubble-order">{selectionIndex + 1}</div>
                                    )}
                                </div>
                            </motion.div>
                        );
                    })}
                </div>

                {/* Controls */}
                <div className="bubbles-controls">
                    <button 
                        className="bubbles-control-btn bubbles-btn-secondary"
                        onClick={() => setSelectedOrder([])} 
                        title="Clear Selection"
                        disabled={selectedOrder.length === 0 || allPuzzlesComplete}
                    >
                        Clear
                    </button>
                    <button 
                        className={`bubbles-control-btn bubbles-btn-hint ${showHint ? 'active' : ''}`}
                        onClick={toggleHint} 
                        title="Show/Hide Solutions"
                        disabled={allPuzzlesComplete}
                    >
                    >
                        <Lightbulb size={18} />
                        Hint
                    </button>
                </div>

                {/* Progress Indicator */}
                <div className="bubbles-progress">
                    <span>{selectedOrder.length}/{bubbles.length} bubbles selected</span>
                </div>

                {/* Success Message - Only show after all 3 puzzles */}
                <AnimatePresence>
                    {allPuzzlesComplete && (
                        <motion.div
                            className="bubbles-completion-overlay"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                        >
                            <motion.div
                                className="bubbles-completion-modal"
                                initial={{ scale: 0.8, opacity: 0 }}
                                animate={{ scale: 1, opacity: 1 }}
                                exit={{ scale: 0.8, opacity: 0 }}
                            >
                                <div className="bubbles-completion-icon">
                                    <Trophy size={48} />
                                </div>
                                <h2 className="bubbles-completion-title">All Puzzles Complete! 🎉</h2>
                                
                                <div className="bubbles-completion-time">
                                    <p className="bubbles-completion-label">Completed in:</p>
                                    <p className="bubbles-completion-value">{formatTime(timeElapsed)}</p>
                                </div>

                                <p className="bubbles-completion-streak">
                                    Your streak: <span className="bubbles-streak-highlight">{streak} days</span>
                                </p>

                                <p className="bubbles-completion-message">
                                    Come back tomorrow for 3 new challenges!
                                </p>

                                <button 
                                    className="bubbles-completion-close"
                                    onClick={onClose}
                                >
                                    Close
                                </button>
                            </motion.div>
                        </motion.div>
                    )}
                </AnimatePresence>

                {/* Puzzle Complete Indicator - Show briefly between puzzles */}
                <AnimatePresence>
                    {isComplete && !allPuzzlesComplete && (
                        <motion.div
                            className="bubbles-next-puzzle"
                            initial={{ scale: 0, opacity: 0 }}
                            animate={{ scale: 1, opacity: 1 }}
                            exit={{ scale: 0, opacity: 0 }}
                        >
                            <h3>✓ Puzzle {currentPuzzle} Complete!</h3>
                            <p>Loading puzzle {currentPuzzle + 1}...</p>
                        </motion.div>
                    )}
                </AnimatePresence>

                {/* Error Message */}
                <AnimatePresence>
                    {showError && (
                        <motion.div
                            className="bubbles-error"
                            initial={{ opacity: 0, y: -20 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0 }}
                        >
                            ❌ Wrong order! Try again.
                        </motion.div>
                    )}
                </AnimatePresence>

                {/* Rules Modal */}
                <AnimatePresence>
                    {showRules && (
                        <motion.div
                            className="bubbles-rules-overlay"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            onClick={() => setShowRules(false)}
                        >
                            <motion.div
                                className="bubbles-rules-modal"
                                initial={{ scale: 0.8, opacity: 0 }}
                                animate={{ scale: 1, opacity: 1 }}
                                exit={{ scale: 0.8, opacity: 0 }}
                                onClick={(e) => e.stopPropagation()}
                            >
                                <div className="bubbles-rules-header">
                                    <h3>🫧 Game Rules</h3>
                                    <button 
                                        className="bubbles-rules-close"
                                        onClick={() => setShowRules(false)}
                                    >
                                        <X size={24} />
                                    </button>
                                </div>
                                <div className="bubbles-rules-content">
                                    <h4>How to Play:</h4>
                                    <ul>
                                        <li><strong>Solve expressions:</strong> Calculate the value of each mathematical expression in the bubbles</li>
                                        <li><strong>Select in order:</strong> Click bubbles from smallest to largest value</li>
                                        <li><strong>Watch for negatives:</strong> Negative numbers are smaller than positive ones</li>
                                        <li><strong>Check brackets:</strong> Solve operations inside brackets first</li>
                                    </ul>
                                    <h4>Tips:</h4>
                                    <ul>
                                        <li>Use the Hint button to reveal the calculated values</li>
                                        <li>Clear button removes all selections</li>
                                        <li>Complete all selections before checking your solution</li>
                                    </ul>
                                </div>
                            </motion.div>
                        </motion.div>
                    )}
                </AnimatePresence>
            </motion.div>
        </div>
    );
};

SelectBubblesGame.propTypes = {
    onClose: PropTypes.func.isRequired,
    pillarName: PropTypes.string
};

export default SelectBubblesGame;
