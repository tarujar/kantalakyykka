import React from 'react';
import { ThrowInput } from './ThrowInput';
import { useTranslation } from '../../hooks/useTranslation';
import { GameType } from 'types';

interface Props {
  player: any;
  teamName: string;
  throws: string[];
  onThrowChange: (throwIndex: number, value: string) => void;
  gameType: GameType;
  round: number;
}

export function PlayerRow({ player, teamName, throws, onThrowChange, gameType, round }: Props) {
  const { t } = useTranslation();
  const THROWS_PER_ROUND = 4;

  return (
    <div className="player-row">
      <div className="player-info">
        <span className="player-name">{player.name}</span>
        <span className="team-name">({teamName})</span>
        <span className="round-number">{t('game.round')} {round}</span>
      </div>
      <div className="throws">
        {Array.from({ length: THROWS_PER_ROUND }).map((_, index) => (
          <ThrowInput
            key={index}
            throwNumber={index + 1}
            value={throws[index] || ''}
            onChange={(value) => onThrowChange(index, value)}
            gameType={gameType}
            label={t('game.throw')}
          />
        ))}
      </div>
    </div>
  );
} 