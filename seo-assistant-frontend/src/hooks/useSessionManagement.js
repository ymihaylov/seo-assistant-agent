import { useState, useRef, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ApiService } from '../services/apiService';
import { transformApiMessage, createUserMessage, createAgentMessage } from '../utils/messageUtils';

export const useSessionManagement = (auth0Client) => {
  const { sessionId } = useParams();
  const navigate = useNavigate();

  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [currentSession, setCurrentSession] = useState(null);
  const [messages, setMessages] = useState([]);
  const [isGenerating, setIsGenerating] = useState(false);
  const [currentJobId, setCurrentJobId] = useState(null);
  
  // Tracking
  const creatingSessionIdRef = useRef(null);
  const messageOperationRef = useRef(false);
  const loadingHistoryRef = useRef(false);
  
  // API service
  const apiService = new ApiService(auth0Client);

  useEffect(() => {
    fetchSessions();
  }, []);

  const fetchSessions = async () => {
    try {
      setLoading(true);
      const sessionsData = await apiService.fetchSessions();
      setSessions(sessionsData);
    } catch (error) {
      console.error('Error fetching sessions:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchSessionMessages = async (sessionId) => {
    try {
      if ((messages.length > 0 && currentSession === sessionId) || messageOperationRef.current) {
        return;
      }

      const messagesData = await apiService.fetchSessionMessages(sessionId);
      
      const transformedMessages = messagesData.map(transformApiMessage);

      loadingHistoryRef.current = true;
      setMessages(transformedMessages);
    } catch (error) {
      console.error('Error fetching session messages:', error);
      setMessages([]);
    }
  };

  const createNewSession = async (messageContent) => {
    try {
      messageOperationRef.current = true;
      creatingSessionIdRef.current = 'pending';

      const data = await apiService.createSession(messageContent);

      console.log('🔒 Setting creatingSessionId to:', data.session_id);
      creatingSessionIdRef.current = data.session_id;

      // 1. Create new session in sidebar
      const newSession = {
        id: data.session_id,
        title: data.session_title,
        last_message_at: data.user_message.updated_at
      };
      setSessions(prev => [newSession, ...prev]);

      // 2. Show user message immediately
      const userMessage = createUserMessage(data.user_message);
      setMessages([userMessage]);

      // 3. Set as current session and navigate
      setCurrentSession(data.session_id);
      navigate(`/sessions/${data.session_id}`);

      // 4. Show loader and start polling
      setIsGenerating(true);
      setCurrentJobId(data.job_id);
      pollJobStatus(data.job_id);

      // 5. Clear flags after delay
      setTimeout(() => {
        creatingSessionIdRef.current = null;
        messageOperationRef.current = false;
      }, 1000);

      return data;
    } catch (error) {
      creatingSessionIdRef.current = null;
      messageOperationRef.current = false;

      throw error;
    }
  };

  const continueExistingSession = async (messageContent) => {
    try {
      messageOperationRef.current = true;
      creatingSessionIdRef.current = currentSession;

      const data = await apiService.addMessageToSession(currentSession, messageContent);

      // 1. Show user message immediately
      const userMessage = createUserMessage(data.user_message);
      setMessages(prev => [...prev, userMessage]);

      // 2. Update session in sidebar with new timestamp and move to top
      setSessions(prev => {
        const updatedSessions = prev.map(session =>
          session.id === currentSession
            ? { ...session, last_message_at: data.user_message.updated_at }
            : session
        );
        // Move the updated session to the top
        const currentSessionData = updatedSessions.find(s => s.id === currentSession);
        const otherSessions = updatedSessions.filter(s => s.id !== currentSession);
        return [currentSessionData, ...otherSessions];
      });

      // 3. Show loader and start polling
      setIsGenerating(true);
      setCurrentJobId(data.job_id);
      pollJobStatus(data.job_id);

      // 4. Clear flags after delay
      setTimeout(() => {
        creatingSessionIdRef.current = null;
        messageOperationRef.current = false;
      }, 1000);

      return data;
    } catch (error) {
      console.error('Error sending message:', error);
      creatingSessionIdRef.current = null;
      messageOperationRef.current = false;

      throw error;
    }
  };

  const pollJobStatus = async (jobId) => {
    const pollInterval = setInterval(async () => {
      try {
        const data = await apiService.getJobStatus(jobId);

        if (data.status === 'completed') {
          clearInterval(pollInterval);
          setIsGenerating(false);
          setCurrentJobId(null);

          const agentMessage = createAgentMessage(data.agent_message);
          setMessages(prev => [...prev, agentMessage]);
        } else if (data.status === 'failed') {
          clearInterval(pollInterval);
          setIsGenerating(false);
          setCurrentJobId(null);
          console.error('Job failed:', data.error_message);
        }
      } catch (error) {
        console.error('Error polling job status:', error);
      }
    }, 2000);
  };

  const updateSession = async (sessionId, title) => {
    try {
      await apiService.updateSession(sessionId, title);
      setSessions(prev => prev.map(session => 
        session.id === sessionId 
          ? { ...session, title }
          : session
      ));
    } catch (error) {
      console.error('Error updating session:', error);
      throw error;
    }
  };

  const deleteSession = async (sessionId) => {
    try {
      await apiService.deleteSession(sessionId);
      setSessions(prev => prev.filter(session => session.id !== sessionId));
      
      if (currentSession === sessionId) {
        navigate('/sessions');
      }
    } catch (error) {
      console.error('Error deleting session:', error);

      throw error;
    }
  };

  return {
    // State
    sessions,
    loading,
    currentSession,
    setCurrentSession,
    messages,
    setMessages,
    isGenerating,
    currentJobId,
    sessionId,
    
    // Refs
    creatingSessionIdRef,
    messageOperationRef,
    loadingHistoryRef,
    
    // Actions
    fetchSessions,
    fetchSessionMessages,
    createNewSession,
    continueExistingSession,
    updateSession,
    deleteSession,
    
    // Navigation
    navigate
  };
};
