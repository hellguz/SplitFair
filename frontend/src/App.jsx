// ./frontend/src/App.jsx
/**
 * @file The root component of the application, handles routing.
 */
import { Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import GroupPage from './pages/GroupPage';
import JoinGroupPage from './pages/JoinGroupPage';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>SplitFair</h1>
        <p>Fairly Simple Expenses</p>
      </header>
      <main>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/group/:groupId" element={<GroupPage />} />
          <Route path="/join/:inviteCode" element={<JoinGroupPage />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;

