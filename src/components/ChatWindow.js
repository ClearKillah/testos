import React, { useEffect, useRef } from 'react';
import './ChatWindow.css';

function ChatWindow({ messages, currentUserId, partner, onNextPartner, status }) {
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <div className="chat-window">
      {partner && (
        <div className="chat-header">
          <div className="partner-info">
            <span className={`partner-gender ${partner.gender}`}>
              {partner.nickname}, {partner.age}
            </span>
            <div className="partner-interests">
              {partner.interests.map(interest => (
                <span key={interest} className="interest-tag">{interest}</span>
              ))}
            </div>
          </div>
          <button className="next-partner-btn" onClick={onNextPartner}>
            Следующий
          </button>
        </div>
      )}

      {status && (
        <div className="chat-status">
          {status}
        </div>
      )}

      <div className="messages-container">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`message ${message.userId === currentUserId ? 'own-message' : 'other-message'}`}
          >
            <div className="message-content">
              {message.text}
            </div>
            <div className="message-time">
              {new Date(message.timestamp).toLocaleTimeString()}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
}

export default ChatWindow; 