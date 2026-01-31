// WebSocket Hook for React
// Place this in: src/hooks/useWebSocket.js

import { useEffect, useRef, useState, useCallback } from 'react';

export function useWebSocket(url, token, options = {}) {
  const [isConnected, setIsConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState(null);
  const [messages, setMessages] = useState([]);
  const wsRef = useRef(null);
  const reconnectTimeoutRef = useRef(null);
  const { 
    reconnect = true, 
    reconnectInterval = 3000,
    onOpen,
    onMessage,
    onError,
    onClose 
  } = options;

  const connect = useCallback(() => {
    if (!token) return;

    const wsUrl = `${url}?token=${token}`;
    const ws = new WebSocket(wsUrl);

    ws.onopen = () => {
      console.log('WebSocket connected');
      setIsConnected(true);
      if (onOpen) onOpen();
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setLastMessage(data);
      setMessages(prev => [...prev, data]);
      if (onMessage) onMessage(data);
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      if (onError) onError(error);
    };

    ws.onclose = () => {
      console.log('WebSocket disconnected');
      setIsConnected(false);
      if (onClose) onClose();

      // Attempt to reconnect
      if (reconnect) {
        reconnectTimeoutRef.current = setTimeout(() => {
          console.log('Attempting to reconnect...');
          connect();
        }, reconnectInterval);
      }
    };

    wsRef.current = ws;
  }, [url, token, reconnect, reconnectInterval, onOpen, onMessage, onError, onClose]);

  useEffect(() => {
    connect();

    return () => {
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [connect]);

  const sendMessage = useCallback((message) => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(message));
    } else {
      console.error('WebSocket is not connected');
    }
  }, []);

  const clearMessages = useCallback(() => {
    setMessages([]);
  }, []);

  return {
    isConnected,
    lastMessage,
    messages,
    sendMessage,
    clearMessages
  };
}

// Example usage in a component:
/*
import { useWebSocket } from './hooks/useWebSocket';

function DashboardComponent() {
  const token = localStorage.getItem('access_token');
  const { isConnected, lastMessage, messages } = useWebSocket(
    'ws://localhost:8000/ws/dashboard',
    token,
    {
      onMessage: (data) => {
        console.log('Received:', data);
      }
    }
  );

  return (
    <div>
      <p>Status: {isConnected ? 'Connected' : 'Disconnected'}</p>
      {messages.map((msg, idx) => (
        <div key={idx}>{JSON.stringify(msg)}</div>
      ))}
    </div>
  );
}
*/
