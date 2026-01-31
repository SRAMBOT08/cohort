// Dashboard with Real-Time Updates
// Place this in: src/components/Dashboard.jsx

import { useEffect, useState } from 'react';
import { useWebSocket } from '../hooks/useWebSocket';

export default function Dashboard() {
  const [submissions, setSubmissions] = useState([]);
  const [grades, setGrades] = useState([]);
  const token = localStorage.getItem('access_token');

  const { isConnected, lastMessage } = useWebSocket(
    'ws://localhost:8000/ws/dashboard',
    token,
    {
      onMessage: (data) => {
        handleWebSocketMessage(data);
      }
    }
  );

  const handleWebSocketMessage = (data) => {
    switch (data.type) {
      case 'submission_created':
        setSubmissions(prev => [data.submission, ...prev]);
        // Show toast notification
        showNotification('New Submission', data.submission.student_name);
        break;

      case 'grade_updated':
        setGrades(prev => [data.grade, ...prev]);
        showNotification('Grade Updated', 'A submission has been graded');
        break;

      case 'dashboard_update':
        // Handle general dashboard updates
        console.log('Dashboard update:', data.data);
        break;
    }
  };

  const showNotification = (title, message) => {
    // Use your notification system (toast, alert, etc.)
    if ('Notification' in window && Notification.permission === 'granted') {
      new Notification(title, { body: message });
    }
  };

  return (
    <div className="dashboard">
      <div className="status-bar">
        <span className={isConnected ? 'status-connected' : 'status-disconnected'}>
          {isConnected ? '🟢 Live' : '🔴 Offline'}
        </span>
      </div>

      <div className="submissions-section">
        <h2>Recent Submissions</h2>
        {submissions.map(submission => (
          <div key={submission.id} className="submission-card">
            <h3>{submission.student_name}</h3>
            <p>{submission.assignment_title}</p>
            <small>{new Date(submission.submitted_at).toLocaleString()}</small>
          </div>
        ))}
      </div>

      <div className="grades-section">
        <h2>Recent Grades</h2>
        {grades.map((grade, idx) => (
          <div key={idx} className="grade-card">
            <p>Grade: {grade.score}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
