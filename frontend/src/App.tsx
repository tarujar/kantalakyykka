import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { NewGameWizard } from 'components/game/NewGameWizard';
import { useTranslation } from 'hooks/useTranslation';
import AddSeriesView from 'views/AddSeriesView';

function App() {
  const { t } = useTranslation();
  const navLinks = [
    { to: '/', label: 'nav.home' },
    { to: '/games', label: 'nav.games' },
    { to: '/teams', label: 'nav.teams' },
    { to: '/players', label: 'nav.players' },
    { to: '/series', label: 'nav.series' },
  ];

  return (
    <>
      <nav>{navLinks.map(link => 
        <a key={link.label}  
          href={link.to} 
          style={{ marginRight: '10px' }}
        >{t(link.label)}</a>
      )}
      </nav>
      <Router>
        <Routes>
          <Route path="/series" element={<AddSeriesView />} />
          <Route path="/games" element={<NewGameWizard onGameCreated={(gameId) => console.log(gameId)} />} />
        </Routes>
      </Router>
    </>
  );
}

export default App;