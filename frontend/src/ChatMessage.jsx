// frontend/src/ChatMessage.jsx

import React from 'react';
import { FaUser, FaRobot } from 'react-icons/fa';
import { TypeAnimation } from 'react-type-animation';

const ChatMessage = ({ message }) => {
  const { sender, text, thinking } = message;

  return (
    <div className={`message ${sender} ${thinking ? 'thinking' : ''}`}>
      <span className="icon">
        {sender === 'user' ? <FaUser /> : <FaRobot />}
      </span>
      <div className="text-content">
        {sender === 'bot' && !thinking ? (
          <TypeAnimation
            cursor={false}
            sequence={[text, 1000]}
            wrapper="p"
            speed={60}
            style={{ margin: 0, whiteSpace: 'pre-wrap' }}
            repeat={0}
          />
        ) : (
          <p>{text}</p>
        )}
      </div>
    </div>
  );
};

export default ChatMessage;