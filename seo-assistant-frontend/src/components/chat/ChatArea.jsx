import React, { useRef, useEffect } from 'react';
import ChatMessage from './ChatMessage';
import LoadingIndicator from './LoadingIndicator';
import WelcomeMessage from './WelcomeMessage';
import ChatInput from './ChatInput';

const ChatArea = ({ currentSession, messages, isGenerating, loadingHistoryRef, onSubmit, autoFocus }) => {
  const messagesEndRef = useRef(null);

  const scrollToBottom = (instant = false) => {
    messagesEndRef.current?.scrollIntoView({ 
      behavior: instant ? "instant" : "smooth" 
    });
  };

  useEffect(() => {
    scrollToBottom(loadingHistoryRef.current);

    if (loadingHistoryRef.current) {
      loadingHistoryRef.current = false;
    }
  }, [messages]);

  return (
    <main className="chat-main">
      <div className="chat-messages">
        {currentSession ? (
          <>
            {messages.map(message => (
              <ChatMessage key={message.id} message={message} />
            ))}
            {isGenerating && <LoadingIndicator />}
            <div ref={messagesEndRef} />
          </>
        ) : (
          <WelcomeMessage />
        )}
      </div>

      <ChatInput
        onSubmit={onSubmit}
        isGenerating={isGenerating}
        autoFocus={autoFocus}
      />
    </main>
  );
};

export default ChatArea;
