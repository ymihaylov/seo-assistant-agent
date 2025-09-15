import React from 'react';
import { formatTime } from '../../utils/dateUtils';

const ChatMessage = ({ message }) => {
  return (
    <div className={`message ${message.type}`}>
      <div className="message-content">
        {message.type === 'user' ? (
          <div className="user-message">
            {message.content}
          </div>
        ) : (
          <div className="agent-message">
            <div className="message-section">
              <h4>Title</h4>
              <p className="code-block">{message.content.title}</p>
            </div>
            <div className="message-section">
              <h4>Content</h4>
              <p className="code-block">{message.content.content}</p>
            </div>
            <div className="message-section">
              <h4>Title Tag</h4>
              <p className="code-block">{message.content.titleTag}</p>
            </div>
            <div className="message-section">
              <h4>Meta Description</h4>
              <p className="code-block">{message.content.metaDescription}</p>
            </div>
            <div className="message-section">
              <h4>Meta Keywords</h4>
              <p className="code-block">
                {Array.isArray(message.content.metaKeywords) 
                  ? message.content.metaKeywords.join(', ') 
                  : message.content.metaKeywords}
              </p>
            </div>
          </div>
        )}
      </div>
      <div className="message-time">{formatTime(message.timestamp)}</div>
    </div>
  );
};

export default ChatMessage;
