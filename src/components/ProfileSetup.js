import React, { useState } from 'react';
import './ProfileSetup.css';

const INTERESTS = [
  "Музыка", "Спорт", "Путешествия", "Кино", "Книги",
  "Технологии", "Искусство", "Игры", "Кулинария", "Наука"
];

function ProfileSetup({ onComplete }) {
  const [profile, setProfile] = useState({
    nickname: '',
    gender: '',
    age: '',
    interests: []
  });

  const handleInterestToggle = (interest) => {
    setProfile(prev => ({
      ...prev,
      interests: prev.interests.includes(interest)
        ? prev.interests.filter(i => i !== interest)
        : [...prev.interests, interest]
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (profile.nickname && profile.gender && profile.age) {
      onComplete(profile);
    }
  };

  return (
    <div className="profile-setup">
      <h2>Создайте профиль</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Ваш ник"
          value={profile.nickname}
          onChange={(e) => setProfile(prev => ({ ...prev, nickname: e.target.value }))}
        />
        
        <input
          type="number"
          placeholder="Ваш возраст"
          min="18"
          max="100"
          value={profile.age}
          onChange={(e) => setProfile(prev => ({ ...prev, age: e.target.value }))}
        />

        <div className="gender-selection">
          <button
            type="button"
            className={`gender-btn ${profile.gender === 'male' ? 'active male' : ''}`}
            onClick={() => setProfile(prev => ({ ...prev, gender: 'male' }))}
          >
            Мужской
          </button>
          <button
            type="button"
            className={`gender-btn ${profile.gender === 'female' ? 'active female' : ''}`}
            onClick={() => setProfile(prev => ({ ...prev, gender: 'female' }))}
          >
            Женский
          </button>
        </div>

        <div className="interests-section">
          <h3>Выберите интересы:</h3>
          <div className="interests-grid">
            {INTERESTS.map(interest => (
              <button
                key={interest}
                type="button"
                className={`interest-btn ${profile.interests.includes(interest) ? 'active' : ''}`}
                onClick={() => handleInterestToggle(interest)}
              >
                {interest}
              </button>
            ))}
          </div>
        </div>

        <button 
          type="submit" 
          className="submit-btn"
          disabled={!profile.nickname || !profile.gender || !profile.age}
        >
          Начать поиск
        </button>
      </form>
    </div>
  );
}

export default ProfileSetup; 