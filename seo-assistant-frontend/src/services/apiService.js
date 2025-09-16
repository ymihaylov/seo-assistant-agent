const API_URL = 'http://localhost:8000';

export class ApiService {
  constructor(auth0Client) {
    this.auth0Client = auth0Client;
  }

  async getToken() {
    return await this.auth0Client.getTokenSilently({
      authorizationParams: {
        audience: import.meta.env.VITE_AUTH0_AUDIENCE,
        scope: "openid profile email"
      },
    });
  }

  async fetchSessions() {
    const token = await this.getToken();
    const response = await fetch(`${API_URL}/sessions`, {
      headers: { 
        Authorization: `Bearer ${token}` 
      }
    });
    
    if (!response.ok) {
      throw new Error('Failed to fetch sessions');
    }
    
    return await response.json();
  }

  async createSession(message) {
    const token = await this.getToken();
    const response = await fetch(`${API_URL}/sessions/async`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({ message })
    });

    if (!response.ok) {
      throw new Error('Failed to create session');
    }

    return await response.json();
  }

  async addMessageToSession(sessionId, message) {
    const token = await this.getToken();
    const response = await fetch(`${API_URL}/sessions/${sessionId}/messages/async`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({ message })
    });

    if (!response.ok) {
      throw new Error('Failed to send message');
    }

    return await response.json();
  }

  async fetchSessionMessages(sessionId) {
    const token = await this.getToken();
    const response = await fetch(`${API_URL}/sessions/${sessionId}/messages`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    if (!response.ok) {
      throw new Error('Failed to fetch session messages');
    }

    return await response.json();
  }

  async updateSession(sessionId, title) {
    const token = await this.getToken();
    const response = await fetch(`${API_URL}/sessions/${sessionId}`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({ title })
    });

    if (!response.ok) {
      throw new Error('Failed to update session');
    }

    return await response.json();
  }

  async deleteSession(sessionId) {
    const token = await this.getToken();
    const response = await fetch(`${API_URL}/sessions/${sessionId}`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    if (!response.ok) {
      throw new Error('Failed to delete session');
    }

    return response.ok;
  }

  async getJobStatus(jobId) {
    const token = await this.getToken();
    const response = await fetch(`${API_URL}/jobs/${jobId}/status`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    if (!response.ok) {
      throw new Error('Failed to get job status');
    }

    return await response.json();
  }
}
