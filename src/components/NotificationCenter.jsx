// Notification System with WebSocket
// Place this in: src/components/NotificationCenter.jsx

import { useState, useEffect } from 'react';
import { useWebSocket } from '../hooks/useWebSocket';

export default function NotificationCenter() {
  const [notifications, setNotifications] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [isOpen, setIsOpen] = useState(false);
  const token = localStorage.getItem('access_token');

  const { isConnected, sendMessage } = useWebSocket(
    'ws://localhost:8000/ws/notifications',
    token,
    {
      onMessage: (data) => {
        handleNotification(data);
      }
    }
  );

  const handleNotification = (data) => {
    switch (data.type) {
      case 'connection_established':
        setUnreadCount(data.unread_count);
        break;

      case 'notification':
        const notification = data.notification;
        setNotifications(prev => [notification, ...prev]);
        setUnreadCount(prev => prev + 1);
        
        // Show browser notification
        if ('Notification' in window && Notification.permission === 'granted') {
          new Notification(notification.title || 'New Notification', {
            body: notification.message,
            icon: '/logo.png'
          });
        }
        break;
    }
  };

  const markAsRead = (notificationId) => {
    sendMessage({
      type: 'mark_read',
      notification_id: notificationId
    });
    setUnreadCount(prev => Math.max(0, prev - 1));
  };

  const togglePanel = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className="notification-center">
      <button className="notification-bell" onClick={togglePanel}>
        🔔
        {unreadCount > 0 && (
          <span className="badge">{unreadCount}</span>
        )}
      </button>

      {isOpen && (
        <div className="notification-panel">
          <div className="panel-header">
            <h3>Notifications</h3>
            <span className={isConnected ? 'live' : 'offline'}>
              {isConnected ? '🟢' : '🔴'}
            </span>
          </div>

          <div className="notification-list">
            {notifications.length === 0 ? (
              <p className="no-notifications">No notifications</p>
            ) : (
              notifications.map((notif, idx) => (
                <div 
                  key={idx} 
                  className="notification-item"
                  onClick={() => markAsRead(notif.id)}
                >
                  <div className="notif-icon">
                    {notif.type === 'grade' && '📝'}
                    {notif.type === 'achievement' && '🏆'}
                    {notif.type === 'announcement' && '📢'}
                    {!['grade', 'achievement', 'announcement'].includes(notif.type) && '🔔'}
                  </div>
                  <div className="notif-content">
                    <h4>{notif.title}</h4>
                    <p>{notif.message}</p>
                    {notif.points && (
                      <span className="points">+{notif.points} points</span>
                    )}
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      )}
    </div>
  );
}
