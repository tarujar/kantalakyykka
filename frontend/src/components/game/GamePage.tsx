import React from 'react';
import { useParams } from 'react-router-dom';
import { GameForm } from './GameForm';
import { useGame } from '../../hooks/useGame';
import { useTranslation } from '../../hooks/useTranslation';

export function GamePage() {
  const { t } = useTranslation();
  const { gameId } = useParams();
  const { game, isLoading, error } = useGame(parseInt(gameId!));

  const handleSubmit = async (result: any

  ) => {
    // Tähän tulee tulosten tallennus
  };

  if (isLoading) return <div>{t('game.loading')}</div>;
  if (error) return <div>{t('game.error')} {error}</div>;
  if (!game) return <div>{t('game.notFound')}</div>;

  const startingTeam = {name: ""}/*game.teams.team1.id === game ? 
    game.teams.team1 : game.teams.team2;

    */
  return (
    <div className="game-page">
      <header>
        <h2>{game.type_id}</h2>
        <div className="game-info">
          <h3>
              a vs b
          </h3>
          <p>
            {t('game.starting')} {game.type_id}: {startingTeam.name}
          </p>
        </div>
      </header>

      <GameForm game={game} onSubmit={handleSubmit} />
    </div>
  );
} 