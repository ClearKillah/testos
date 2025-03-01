import React, { useState, useEffect } from 'react';
import './App.css';
import ChatWindow from './components/ChatWindow';
import MessageInput from './components/MessageInput';
import ProfileSetup from './components/ProfileSetup';

function App() {
  const [messages, setMessages] = useState([]);
  const [userId, setUserId] = useState(null);
  const [profile, setProfile] = useState(null);
  const [partner, setPartner] = useState(null);
  const [chatStatus, setChatStatus] = useState('Настройте профиль для начала общения');
  const [isSearching, setIsSearching] = useState(false);

  useEffect(() => {
    // Инициализация Telegram WebApp
    const tg = window.Telegram.WebApp;
    tg.ready();
    
    // Генерируем случайный ID для анонимного пользователя
    setUserId(Math.random().toString(36).substring(7));
  }, []);

  const handleProfileComplete = (profileData) => {
    setProfile(profileData);
    setChatStatus('Нажмите "Искать собеседника" для начала общения');
  };

  const startSearch = () => {
    setIsSearching(true);
    setChatStatus('Поиск собеседника...');
    // Имитация поиска собеседника
    setTimeout(() => {
      const mockPartner = {
        nickname: 'Аноним',
        age: '25',
        gender: Math.random() > 0.5 ? 'male' : 'female',
        interests: ['Музыка', 'Спорт', 'Путешествия']
      };
      setPartner(mockPartner);
      setIsSearching(false);
      setChatStatus('Собеседник найден! Можете начинать общение');
      setTimeout(() => setChatStatus(''), 3000);
    }, 2000);
  };

  const handleNextPartner = () => {
    setPartner(null);
    setMessages([]);
    setChatStatus('Поиск нового собеседника...');
    startSearch();
  };

  const sendMessage = (text) => {
    if (!partner) return;

    const newMessage = {
      id: Date.now(),
      text,
      userId,
      timestamp: new Date().toISOString(),
    };
    
    setMessages([...messages, newMessage]);
    // Здесь можно добавить интеграцию с бэкендом
  };

  if (!profile) {
    return <ProfileSetup onComplete={handleProfileComplete} />;
  }

  return (
    <div className="app">
      <div className="chat-container">
        {!partner && !isSearching && (
          <button className="search-btn" onClick={startSearch}>
            Искать собеседника
          </button>
        )}
        <ChatWindow 
          messages={messages} 
          currentUserId={userId}
          partner={partner}
          onNextPartner={handleNextPartner}
          status={chatStatus}
        />
        {partner && <MessageInput onSendMessage={sendMessage} />}
      </div>
    </div>
  );
}

export default App; 