import React, { useState, useEffect } from 'react';
import './App.css';
import ChatWindow from './components/ChatWindow';
import MessageInput from './components/MessageInput';

function App() {
  const [messages, setMessages] = useState([]);
  const [userId, setUserId] = useState(null);

  useEffect(() => {
    // Инициализация Telegram WebApp
    const tg = window.Telegram.WebApp;
    tg.ready();
    
    // Генерируем случайный ID для анонимного пользователя
    setUserId(Math.random().toString(36).substring(7));
  }, []);

  const sendMessage = (text) => {
    const newMessage = {
      id: Date.now(),
      text,
      userId,
      timestamp: new Date().toISOString(),
    };
    
    setMessages([...messages, newMessage]);
    // Здесь можно добавить интеграцию с бэкендом
  };

  return (
    <div className="app">
      <div className="chat-container">
        <ChatWindow messages={messages} currentUserId={userId} />
        <MessageInput onSendMessage={sendMessage} />
      </div>
    </div>
  );
}

export default App; 