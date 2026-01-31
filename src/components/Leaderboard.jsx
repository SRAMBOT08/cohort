// Live Leaderboard Component
// Place this in: src/components/Leaderboard.jsx

import { useState, useEffect } from 'react';
import { useWebSocket } from '../hooks/useWebSocket';

export default function Leaderboard() {
  const [leaderboardData, setLeaderboardData] = useState([]);
  const [lastUpdated, setLastUpdated] = useState(null);
  const token = localStorage.getItem('access_token');

  const { isConnected } = useWebSocket(
    'ws://localhost:8000/ws/leaderboard',
    token,
    {
      onMessage: (data) => {
        if (data.type === 'leaderboard_update') {
          setLeaderboardData(data.leaderboard);
          setLastUpdated(new Date());
        }
      }
    }
  );

  // Fetch initial data
  useEffect(() => {
    fetch('http://localhost:8000/api/leaderboard/', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
      .then(res => res.json())
      .then(data => setLeaderboardData(data))
      .catch(err => console.error('Failed to fetch leaderboard:', err));
  }, [token]);

  return (
    <div className="leaderboard">
      <div className="leaderboard-header">
        <h2>Leaderboard</h2>
        <div className="status">
          <span className={isConnected ? 'connected' : 'disconnected'}>
            {isConnected ? '🟢 Live Updates' : '🔴 Offline'}
          </span>
          {lastUpdated && (
            <small>Updated: {lastUpdated.toLocaleTimeString()}</small>
          )}
        </div>
      </div>

      <div className="leaderboard-list">
        {leaderboardData.map((entry, idx) => (
          <div 
            key={entry.user_id || idx} 
            className={`leaderboard-entry rank-${entry.rank}`}
          >
            <div className="rank">
              {entry.rank === 1 && '🥇'}
              {entry.rank === 2 && '🥈'}
              {entry.rank === 3 && '🥉'}
              {entry.rank > 3 && `#${entry.rank}`}
            </div>
            <div className="user-info">
              <span className="name">{entry.name}</span>
            </div>
            <div className="points">
              {entry.points} pts
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
