import React, { useState } from 'react';

import { useTranslation } from '../../hooks/useTranslation';
import { Player, TeamInSeries } from 'openapi';

interface Props {
  maxPlayers: number;
  onSelect: (team: TeamInSeries) => void;
  label: string;
}

export function TeamSelector({ maxPlayers = 4, onSelect, label }: Props) {
  const { t } = useTranslation();
  const [selectedPlayers, setSelectedPlayers] = useState<Player[]>([]);

  return (
    <div className="team-selector">
      <label>{label}</label>
      <div className="player-selection">
        <h5>{t('game.selectPlayers')}</h5>
        <div className="selected-players">
          {selectedPlayers.map((player, index) => (
            <div key={player.id} className="selected-player">
              <span>{index + 1}. {player.name}</span>
              <button
                type="button"
                onClick={() => {
                  setSelectedPlayers(players => 
                    players.filter(p => p.id !== player.id)
                  );
                }}
                aria-label={t('game.removePlayer', { name: player.name })}
              >
                ×
              </button>
            </div>
          ))}
        </div>

        {selectedPlayers.length < maxPlayers && (
          <div className="player-list">

          </div>
        )}

        submit
      </div>
    </div>
  );
} 