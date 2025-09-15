import React from 'react';
import { formatRelativeTime } from '../../utils/dateUtils';

const SessionItem = ({ 
  session, 
  isActive, 
  isEditing, 
  editTitle, 
  onSessionClick, 
  onEditStart, 
  onEditSave, 
  onEditCancel, 
  onEditTitleChange, 
  onDeleteStart 
}) => {
  return (
    <div className={`session-item ${isActive ? 'active' : ''}`}>
      {isEditing ? (
        <div className="session-edit-mode" onClick={(e) => e.stopPropagation()}>
          <input
            type="text"
            value={editTitle}
            onChange={(e) => onEditTitleChange(e.target.value)}
            className="session-edit-input"
            autoFocus
            onKeyDown={(e) => {
              if (e.key === 'Enter') {
                onEditSave(session.id);
              } else if (e.key === 'Escape') {
                onEditCancel();
              }
            }}
          />
          <div className="session-edit-actions">
            <button
              className="session-action-btn save-btn"
              onClick={() => onEditSave(session.id)}
              title="Save"
            >
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M20 6L9 17L4 12" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </button>
            <button
              className="session-action-btn cancel-btn"
              onClick={onEditCancel}
              title="Cancel"
            >
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M18 6L6 18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M6 6L18 18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </button>
          </div>
        </div>
      ) : (
        <div className="session-content" onClick={() => onSessionClick(session.id)}>
          <div className="session-title">{session.title}</div>
          <div className="session-time">{formatRelativeTime(session.last_message_at)}</div>
        </div>
      )}
      
      {!isEditing && (
        <div className="session-actions">
          <button
            className="session-action-btn edit-btn"
            onClick={(e) => {
              e.stopPropagation();
              onEditStart(session);
            }}
            title="Edit session"
          >
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M11 4H4C3.46957 4 2.96086 4.21071 2.58579 4.58579C2.21071 4.96086 2 5.46957 2 6V20C2 20.5304 2.21071 21.0391 2.58579 21.4142C2.96086 21.7893 3.46957 22 4 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V13" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M18.5 2.5C18.8978 2.10218 19.4374 1.87868 20 1.87868C20.5626 1.87868 21.1022 2.10218 21.5 2.5C21.8978 2.89782 22.1213 3.43739 22.1213 4C22.1213 4.56261 21.8978 5.10218 21.5 5.5L12 15L8 16L9 12L18.5 2.5Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </button>
          <button
            className="session-action-btn delete-btn"
            onClick={(e) => {
              e.stopPropagation();
              onDeleteStart(session.id);
            }}
            title="Delete session"
          >
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M3 6H5H21" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M8 6V4C8 3.46957 8.21071 2.96086 8.58579 2.58579C8.96086 2.21071 9.46957 2 10 2H14C14.5304 2 15.0391 2.21071 15.4142 2.58579C15.7893 2.96086 16 3.46957 16 4V6M19 6V20C19 20.5304 18.7893 21.0391 18.4142 21.4142C18.0391 21.7893 17.5304 22 17 22H7C6.46957 22 5.96086 21.7893 5.58579 21.4142C5.21071 21.0391 5 20.5304 5 20V6H19Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M10 11V17" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M14 11V17" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </button>
        </div>
      )}
    </div>
  );
};

export default SessionItem;
