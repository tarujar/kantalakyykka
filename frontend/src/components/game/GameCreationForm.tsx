/**
 * GameCreationForm vastaa uuden pelin luomisesta.
 * 
 * Komponentti:
 * 1. Näyttää yhteenvedon valituista joukkueista
 * 2. Luo uuden pelin tietokantaan
 * 3. Asettaa kotijoukkueen aloittavaksi joukkueeksi
 * 
 * Käyttö:
 * <GameCreationForm
 *   series={valittuSarja}
 *   homeTeam={kotijoukkue}
 *   awayTeam={vierasjoukkue}
 *   onGameCreated={(gameId) => navigate(`/games/${gameId}`)}
 * />
 */
import React, { useState } from 'react';
import { useTranslation } from '../../hooks/useTranslation';
import { TeamSelector } from './TeamSelector';
import { Game, GameType, TeamInSeries } from 'types';

interface Props {
  onSubmit: (game: Game) => void;
}

export function GameCreationForm({ onSubmit }: Props) {
  const { t } = useTranslation();
  const [gameType, setGameType] = useState<GameType>();
  const [team1, setTeam1] = useState<TeamInSeries | null>(null);
  const [team2, setTeam2] = useState<TeamInSeries | null>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (team1 && team2) {
      onSubmit({} as Game);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="game-creation-form">
      <div className="game-type-selection">
        <h3>{t('game.selectType')}</h3>
        <select value={gameType?.name} onChange={(e) => setGameType(gameType)}>
          <option value="single">{t('gameTypes.single')}</option>
          <option value="duo">{t('gameTypes.duo')}</option>
          <option value="quartet">{t('gameTypes.quartet')}</option>
        </select>
      </div>

      <div className="team-selection">
        <div className="team">
          <h4>{t('game.team')} 1</h4>
          <TeamSelector
            maxPlayers={4}
            onSelect={setTeam1}
            label={t('game.selectTeam', { number: 1 })}
          />
        </div>
        <div className="team">
          <h4>{t('game.team')} 2</h4>
          <TeamSelector
            maxPlayers={4}
            onSelect={setTeam2}
            label={t('game.selectTeam', { number: 2 })}
          />
        </div>
      </div>

      <button 
        type="submit" 
        disabled={!team1 || !team2}
      >
        {t('game.createGame')}
      </button>
    </form>
  );
}

