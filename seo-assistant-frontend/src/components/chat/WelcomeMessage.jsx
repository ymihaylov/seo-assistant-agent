import React from 'react';

const WelcomeMessage = () => {
  return (
    <div className="welcome-message">
      <div className="welcome-content">
        <div className="welcome-icon">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            <path d="M2 17L12 22L22 17" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            <path d="M2 12L12 17L22 12" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </div>
        <h2>Welcome to SEO Assistant</h2>
        <p>Provide a description of your page and business, along with any details that can help optimize your content for SEO.</p>
        <div className="welcome-features">
          <div className="feature">
            <span className="feature-icon">🎯</span>
            <span><strong>Optimize</strong> page titles and content</span>
          </div>
          <div className="feature">
            <span className="feature-icon">📝</span>
            <span><strong>Generate</strong> meta descriptions</span>
          </div>
          <div className="feature">
            <span className="feature-icon">🔍</span>
            <span><strong>Suggest</strong> relevant keywords</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default WelcomeMessage;
