import React, { useState, useRef } from 'react';

const ChatInput = ({ onSubmit, isGenerating, autoFocus = false }) => {
  const [inputValue, setInputValue] = useState('');
  const inputRef = useRef(null);

  // Auto-focus effect
  React.useEffect(() => {
    if (autoFocus && inputRef.current) {
      setTimeout(() => {
        inputRef.current?.focus();
      }, 100);
    }
  }, [autoFocus]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    const messageContent = inputValue.trim();
    setInputValue('');

    // Reset textarea height to initial
    if (inputRef.current) {
      inputRef.current.style.height = 'auto';
    }

    onSubmit(messageContent);
  };

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
    
    const textarea = e.target;
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
  };

  const handleKeyDown = (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      handleSubmit(e);
    }
  };

  return (
    <div className="chat-input-area">
      <form onSubmit={handleSubmit} className="input-form">
        <div className="input-container">
          <textarea
            ref={inputRef}
            value={inputValue}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            placeholder="Ask me to optimize your content for SEO..."
            className="message-input"
            rows="1"
            disabled={isGenerating}
          />
          <button 
            type="submit" 
            className="send-button"
            disabled={!inputValue.trim() || isGenerating}
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M22 2L11 13" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M22 2L15 22L11 13L2 9L22 2Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </button>
        </div>
        <div className="input-hint">
          Press <kbd>Cmd/Ctrl</kbd> + <kbd>Enter</kbd> to send
        </div>
      </form>
    </div>
  );
};

export default ChatInput;
