import React from 'react';
import SessionItem from './SessionItem';

const SessionsList = ({ 
  sessions, 
  loading, 
  currentSession, 
  editingSession, 
  editTitle, 
  onSessionClick, 
  onEditStart, 
  onEditSave, 
  onEditCancel, 
  onEditTitleChange, 
  onDeleteStart,
  onNewSession 
}) => {
  return (
    <aside className="sessions-sidebar">
      <div className="sidebar-header">
        <h3>Chat Sessions</h3>
        <button 
          className="new-session-button"
          onClick={onNewSession}
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 5V19" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            <path d="M5 12H19" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
          New Session
        </button>
      </div>
      <div className="sessions-list">
        {loading ? (
          <div className="loading-sessions">
            <div className="loading-spinner"></div>
            <p>Loading sessions...</p>
          </div>
        ) : sessions.length > 0 ? (
          sessions.map(session => (
            <SessionItem
              key={session.id}
              session={session}
              isActive={currentSession === session.id}
              isEditing={editingSession === session.id}
              editTitle={editTitle}
              onSessionClick={onSessionClick}
              onEditStart={onEditStart}
              onEditSave={onEditSave}
              onEditCancel={onEditCancel}
              onEditTitleChange={onEditTitleChange}
              onDeleteStart={onDeleteStart}
            />
          ))
        ) : (
          <div className="no-sessions">
            <p>No sessions yet</p>
            <p>Start chatting to create your first session!</p>
          </div>
        )}
      </div>
    </aside>
  );
};

export default SessionsList;
