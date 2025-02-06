import React from 'react';
import { useParams } from 'react-router-dom';
import { GameForm } from './GameForm';
import { useTranslation } from '../../hooks/useTranslation';
import { Game } from 'openapi';

export function GamePage() {
  const { t } = useTranslation();
  const { gameId } = useParams();
  
  // Mock game data
  const mockGame:Game = {
    id: parseInt(gameId!),
    type_id: 1,
    series_id: 1,
  };

  const { game, isLoading, error } = { game: mockGame, isLoading: false, error: null };

  const handleSubmit = async (result: any) => {
    // Tähän tulee tulosten tallennus
    console.log('Submitted result:', result);
  };

  if (isLoading) return <div>{t('game.loading')}</div>;
  if (error) return <div>{t('game.error')} {error}</div>;
  if (!game) return <div>{t('game.notFound')}</div>;

  const startingTeam = 1//game.teams.team1.id === game.id ? game.teams.team1 : game.teams.team2;

  return (
    <div className="game-page">
      <header>
        <h2>{game.type_id}</h2>
        <div className="game-info">
          <h3>
          a vs b
          </h3>
          <p>
            {t('game.starting')} {game.type_id}: team1
          </p>
        </div>
      </header>

      <GameForm game={game} onSubmit={handleSubmit} />
    </div>
  );
}