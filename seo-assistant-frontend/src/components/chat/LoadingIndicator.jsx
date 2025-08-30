import React from 'react';

const LoadingIndicator = () => {
  return (
    <div className="message agent">
      <div className="message-content">
        <div className="agent-message">
          <div className="generating-indicator">
            <div className="loading-spinner"></div>
            <p>Generating SEO optimization...</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoadingIndicator;
