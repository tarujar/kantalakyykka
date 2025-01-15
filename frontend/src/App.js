import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { NewGameWizard } from './components/game/NewGameWizard.tsx';

function App() {

  return (
    <Router>
      <Routes>
        <Route path="/" element={<NewGameWizard onGameCreated={(gameId) => console.log(gameId)} />} />
      </Routes>
    </Router>
  );
}

export default App; 