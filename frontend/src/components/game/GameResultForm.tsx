import React from 'react';
import { Series, TeamInSeries } from 'types';

interface Props {
  series: Series;
  homeTeam: TeamInSeries;
  awayTeam: TeamInSeries;
  onGameCreated: (gameId: number) => void;
}

function GameResultForm({ series, homeTeam, awayTeam, onGameCreated }: Props) {
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    // TODO: Implementoi pelin luonti
  };
return <h1>asdasda</h1>
  return (
    <div>
      <h2>Syötä pelin tiedot</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <h3>Kotijoukkue: {homeTeam.team_name}</h3>
          <h3>Vierasjoukkue: {awayTeam.team_name}</h3>
          <h3>Sarja: {series.name}</h3>
        </div>
        <button type="submit">Luo peli</button>
      </form>
    </div>
  );
}

export default GameResultForm; 