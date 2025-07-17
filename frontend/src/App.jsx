import { useContext } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { AppContext } from './context/AppContext';
import HomePage from './pages/HomePage';
import GroupPage from './pages/GroupPage';
import './App.css';

/**
 * Main application component. It handles routing and displays a loading
 * message until the user's identity is established.
 */
function App() {
  const { isLoading, error } = useContext(AppContext);

  if (isLoading) {
    return <div className="loading">Initializing...</div>;
  }

  if (error) {
      return <div className="error">Error: {error}</div>
  }

  return (
    <div className="App">
      <h1>💸 Splitter</h1>
      <main className="main-content">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/group/:groupId" element={<GroupPage />} />
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
