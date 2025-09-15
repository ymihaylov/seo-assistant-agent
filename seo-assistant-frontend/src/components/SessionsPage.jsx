import React, { useState, useEffect } from 'react';
import { useSessionManagement } from '../hooks/useSessionManagement';
import SessionsList from './sessions/SessionsList';
import ChatArea from './chat/ChatArea';
import DeleteConfirmModal from './sessions/DeleteConfirmModal';

const SessionsPage = ({ user, onLogout, auth0Client }) => {
  const {
    sessions,
    loading,
    currentSession,
    setCurrentSession,
    messages,
    isGenerating,
    sessionId,
    creatingSessionIdRef,
    messageOperationRef,
    loadingHistoryRef,
    fetchSessionMessages,
    createNewSession,
    continueExistingSession,
    updateSession,
    deleteSession,
    navigate
  } = useSessionManagement(auth0Client);

  // Local state for UI interactions
  const [editingSession, setEditingSession] = useState(null);
  const [editTitle, setEditTitle] = useState('');
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(null);

  // Detect direct URL access
  useEffect(() => {
    if (sessionId && sessions.length > 0 && !currentSession && !messageOperationRef.current) {
      creatingSessionIdRef.current = null;
    }
  }, [sessionId, sessions.length, currentSession]);

  // Handle URL parameter changes - only for direct URL access and session switching
  useEffect(() => {
    if (sessionId && sessions.length > 0) {
      const session = sessions.find(s => s.id === sessionId);
      if (session) {
        setCurrentSession(sessionId);
        // Only fetch messages if we're not in the middle of a message operation
        if (!messageOperationRef.current && creatingSessionIdRef.current !== sessionId) {
          console.log('CALLING fetchSessionMessages for session:', sessionId);
          fetchSessionMessages(sessionId);
        } else {
          console.log('SKIPPING fetch for session:', sessionId, 'reason:', {
            messageOperation: messageOperationRef.current,
            creatingSession: creatingSessionIdRef.current === sessionId
          });
        }
      } else {
        navigate('/sessions');
      }
    } else if (!sessionId && !messageOperationRef.current) {
      setCurrentSession(null);
    }
  }, [sessionId, sessions, navigate, fetchSessionMessages, setCurrentSession, currentSession, messages.length]);

  useEffect(() => {
    const handleKeyDown = (event) => {
      if (event.key === 'Escape') {
        if (showDeleteConfirm) {
          setShowDeleteConfirm(null);
        }
        if (editingSession) {
          handleCancelEdit();
        }
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => {
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, [showDeleteConfirm, editingSession]);

  const handleSubmit = async (messageContent) => {
    if (!currentSession) {
      await createNewSession(messageContent);
    } else {
      await continueExistingSession(messageContent);
    }
  };

  const handleNewSession = () => {
    navigate('/sessions');
  };

  const handleExistingSessionClick = (sessionId) => {
    creatingSessionIdRef.current = null;
    messageOperationRef.current = false;
    navigate(`/sessions/${sessionId}`);
  };

  const handleEditSession = (session) => {
    setEditingSession(session.id);
    setEditTitle(session.title);
  };

  const handleCancelEdit = () => {
    setEditingSession(null);
    setEditTitle('');
  };

  const handleSaveEdit = async (sessionId) => {
    if (!editTitle.trim()) return;

    try {
      await updateSession(sessionId, editTitle.trim());
      setEditingSession(null);
      setEditTitle('');
    } catch (error) {
      console.error('Failed to update session:', error);
    }
  };

  const handleEditTitleChange = (title) => {
    setEditTitle(title);
  };

  const handleDeleteStart = (sessionId) => {
    setShowDeleteConfirm(sessionId);
  };

  const handleDeleteConfirm = async (sessionId) => {
    try {
      await deleteSession(sessionId);
      setShowDeleteConfirm(null);
    } catch (error) {
      console.error('Failed to delete session:', error);
    }
  };

  const handleDeleteCancel = () => {
    setShowDeleteConfirm(null);
  };


  return (
    <div className="sessions-page">
      <header className="app-header">
                  <div className="header-left">
            <div className="logo" onClick={() => navigate('/sessions')}>
              <span className="logo-text">SEO Assistant</span>
            </div>
          </div>
        <div className="header-right">
          <div className="user-info">
            <div className="user-avatar">
              {user?.picture ? (
                <img src={user.picture} alt={user.name} />
              ) : (
                <div className="avatar-placeholder">
                  {user?.name?.charAt(0) || 'U'}
                </div>
              )}
            </div>
            <span className="user-name">{user?.name || 'User'}</span>
            <button className="logout-button" onClick={onLogout} title="Logout">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M9 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V5C3 4.46957 3.21071 3.96086 3.58579 3.58579C3.96086 3.21071 4.46957 3 5 3H9" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M16 17L21 12L16 7" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M21 12H9" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </button>
          </div>
        </div>
      </header>

      <div className="sessions-layout">
        <SessionsList
          sessions={sessions}
          loading={loading}
          currentSession={currentSession}
          editingSession={editingSession}
          editTitle={editTitle}
          onSessionClick={handleExistingSessionClick}
          onEditStart={handleEditSession}
          onEditSave={handleSaveEdit}
          onEditCancel={handleCancelEdit}
          onEditTitleChange={handleEditTitleChange}
          onDeleteStart={handleDeleteStart}
          onNewSession={handleNewSession}
        />
        
        <ChatArea
          currentSession={currentSession}
          messages={messages}
          isGenerating={isGenerating}
          loadingHistoryRef={loadingHistoryRef}
          onSubmit={handleSubmit}
          autoFocus={!sessionId && !loading}
        />
      </div>

      <DeleteConfirmModal
        session={sessions.find(s => s.id === showDeleteConfirm)}
        onConfirm={handleDeleteConfirm}
        onCancel={handleDeleteCancel}
      />
    </div>
  );
};

export default SessionsPage;
