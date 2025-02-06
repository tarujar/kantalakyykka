import React, { useState } from 'react';
import { useTranslation } from '../../hooks/useTranslation';
import { Game } from 'openapi';

/**
 * GameForm vastaa pelin tulosten syöttämisestä.
 * 
 * Komponentti:
 * 1. Hallinnoi kahden erän heittotietoja
 * 2. Järjestää pelaajat oikeaan heittojärjestykseen
 * 3. Mahdollistaa heittojen syöttämisen ja muokkaamisen
 * 4. Lähettää tulokset tallennettavaksi
 * 
 * Käyttö:
 * <GameForm
 *   game={pelinTiedot}
 *   onSubmit={async (result) => {
 *     await saveGameResult(result);
 *     navigate('/games');
 *   }}
 * />
 */
export function GameForm({ game, onSubmit }: { game: Game, onSubmit: (result: any) => void }) {
  const { t } = useTranslation();
  const [trackThrows, setTrackThrows] = useState(false);
  const [sets, setSets] = useState<any[]>([]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await onSubmit({
      gameId: game.id,
      sets,
      trackThrows
    });
  };

  return (
    <form onSubmit={handleSubmit} className="game-form">
      <div className="form-options">
        <label>
          <input
            type="checkbox"
            checked={trackThrows}
            onChange={(e) => setTrackThrows(e.target.checked)}
          />
          {t('game.trackThrows')}
        </label>
      </div>

      {trackThrows ? (
        // Tarkka heittoseuranta
        <div>
        </div>
      ) : (
        // Yksinkertainen pistenäkymä
        <div>
          {[0, 1].map(setIndex => (
            <GameSetScore
              key={setIndex}
              setNumber={setIndex + 1}
              game={game}
              onSetComplete={(points) => {
                const newSets = [...sets];
                newSets[setIndex] = { 
                  throws: [],  // Tyhjä array täytt��mään GameSetDetails vaatimus
                  ...points 
                };
                setSets(newSets);
              }}
            />
          ))}
        </div>
      )}

      <button type="submit">{t('game.save')}</button>
    </form>
  );
}

interface GameSetScoreProps {
  setNumber: number;
  game: Game;
  onSetComplete: (points: any) => void;
}

function GameSetScore({ setNumber, game, onSetComplete }: GameSetScoreProps) {
  const [scores, setScores] = useState({
    team1Points: 0,
    team2Points: 0
  });

  // Kyykän pisteiden rajat
  const MIN_POINTS = -80;  // Kaikki kyykät kentällä
  const MAX_POINTS = 16

  const handleScoreChange = (team: 'team1' | 'team2', value: string) => {
    const points = parseInt(value) || 0;
    
    // Rajoita pisteet sallittuihin arvoihin
    const validPoints = Math.max(MIN_POINTS, Math.min(points, MAX_POINTS));
    
    const newScores = {
      ...scores,
      [`${team}Points`]: validPoints
    };
    setScores(newScores);
    onSetComplete(newScores);
  };

  return (
    <div className="game-set-score">
      <h3>Erä {setNumber}</h3>
      <div className="team-scores">
        <div>
          <label>team 1 nimi</label>
          <input 
            type="number"
            min={MIN_POINTS}
            max={MAX_POINTS}
            value={scores.team1Points}
            onChange={(e) => handleScoreChange('team1', e.target.value)}
          />
        </div>
        <div>
          <label>team 2 nimi</label>
          <input 
            type="number"
            min={MIN_POINTS}
            max={MAX_POINTS}
            value={scores.team2Points}
            onChange={(e) => handleScoreChange('team2', e.target.value)}
          />
        </div>
      </div>
      <div className="score-info">
        <small>
          Pisteet: {MIN_POINTS} - {MAX_POINTS} 
          ({game.type_id /*=== 'quartet' ? '16' : '20'*/} heittoa/erä)
        </small>
      </div>
    </div>
  );
} 