import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ClientProvider } from './contexts/ClientProvider';
import HomePage from './pages/HomePage';
import GroupPage from './pages/GroupPage';
import JoinGroupPage from './pages/JoinGroupPage';
import './index.css';

/**
 * The main application component that sets up routing.
 * @returns {JSX.Element} The rendered App component.
 */
function App() {
  return (
    <ClientProvider>
      <Router>
        <div className="container">
          <header className="app-header">
            <h1>SplitShare</h1>
            <p>Split expenses with ease.</p>
          </header>
          <main>
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/group/:groupId" element={<GroupPage />} />
              <Route path="/join/:inviteCode" element={<JoinGroupPage />} />
            </Routes>
          </main>
        </div>
      </Router>
    </ClientProvider>
  );
}

export default App;

