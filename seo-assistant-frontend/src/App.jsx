// App.jsx
import { useEffect, useRef, useState } from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import { createAuth0Client } from "@auth0/auth0-spa-js";
import LoginPage from "./components/LoginPage";
import SessionsPage from "./components/SessionsPage";

const domain = import.meta.env.VITE_AUTH0_DOMAIN;
const clientId = import.meta.env.VITE_AUTH0_CLIENT_ID;
const audience = import.meta.env.VITE_AUTH0_AUDIENCE;
const API_URL  = import.meta.env.VITE_API_URL;

export default function App() {
  const auth0Ref = useRef(null);
  const [ready, setReady] = useState(false);
  const [isAuth, setIsAuth] = useState(false);
  const [user, setUser] = useState(null);

  useEffect(() => {
    (async () => {
      if (!auth0Ref.current) {
        auth0Ref.current = await createAuth0Client({
          domain,
          clientId,
          authorizationParams: {
            audience,
            redirect_uri: window.location.origin,
            scope: "openid profile email",
          },
          // ↓↓↓ helps "Invalid state" on some browsers
          useCookiesForTransactions: true,
          cacheLocation: "localstorage",
          useRefreshTokens: true,
        });
      }
      const client = auth0Ref.current;

      const qs = new URLSearchParams(window.location.search);
      if (qs.has("code") && qs.has("state")) {
        try {
          await client.handleRedirectCallback();
          window.history.replaceState({}, document.title, "/");
        } catch (e) {
          console.error("handleRedirectCallback error:", e);
        }
      }

      const loggedIn = await client.isAuthenticated();
      setIsAuth(loggedIn);
      if (loggedIn) setUser(await client.getUser());
      setReady(true);
    })();
  }, []);

  const login = async () => auth0Ref.current.loginWithRedirect();
  const logout = () => auth0Ref.current.logout({ logoutParams: { returnTo: window.location.origin } });

  if (!ready) {
    return (
      <div className="loading-screen">
        <div className="loading-spinner"></div>
        <p>Loading...</p>
      </div>
    );
  }

  return (
    <div className="app">
      <Routes>
        <Route 
          path="/login" 
          element={
            !isAuth ? (
              <LoginPage onLogin={login} />
            ) : (
              <Navigate to="/sessions" replace />
            )
          } 
        />
        <Route 
          path="/sessions" 
          element={
            isAuth ? (
              <SessionsPage user={user} onLogout={logout} auth0Client={auth0Ref.current} />
            ) : (
              <Navigate to="/login" replace />
            )
          } 
        />
        <Route 
          path="/sessions/:sessionId" 
          element={
            isAuth ? (
              <SessionsPage user={user} onLogout={logout} auth0Client={auth0Ref.current} />
            ) : (
              <Navigate to="/login" replace />
            )
          } 
        />
        <Route 
          path="/" 
          element={
            isAuth ? (
              <Navigate to="/sessions" replace />
            ) : (
              <Navigate to="/login" replace />
            )
          } 
        />
      </Routes>
    </div>
  );
}
