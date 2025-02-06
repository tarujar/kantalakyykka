import React, { useState } from 'react';
import { PlayerRow } from './PlayerRow';
import { useTranslation } from '../../hooks/useTranslation';
import { Game } from 'openapi';

interface Props {
  setNumber: number;
  game: Game;
  onThrowChange: (playerIndex: number, throwIndex: number, value: string) => void;
}

export function GameSet({ setNumber, game, onThrowChange }: Props) {
  const { t } = useTranslation();
  const [error, setError] = useState<string | null>(null);


  const players =[]// game.teams.team1.players.concat(game.teams.team2.players);

  const roundCount = 4 //|| 5;

  return (
    <div className="game-set">
      <h3>{t('game.set')} {setNumber}</h3>
      {error && <div className="error-message">{error}</div>}
      <div className="rounds">
        {Array.from({ length: roundCount }).map((_, roundIndex) => (
          <div key={roundIndex} className="round">
            {/*players.map((player, playerIndex) => (
              <PlayerRow
                key={`${player.id}-${roundIndex}-${playerIndex}`}
                player={player}
                teamName={game.teams.team1.players.includes(player) ? 
                  game.teams.team1.name : game.teams.team2.name}
                throws={throws[playerIndex]?.inputs.slice(roundIndex * 4, (roundIndex + 1) * 4) || ['', '', '', '']}
                onThrowChange={(throwIndex, value) => {
                  const actualIndex = roundIndex * 4 + throwIndex;
                  handleThrowChange(playerIndex, actualIndex, value);
                }}
                gameType={game.type}
                round={roundIndex + 1}
              />
            ))*/}
          </div>
        ))}
      </div>
      <small>{t(`game.throwsPerRound`)}: 4</small>
    </div>
  );
} 