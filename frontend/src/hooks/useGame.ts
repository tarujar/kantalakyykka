import { useState, useEffect } from 'react';
import { getGame } from '../services/api';
import { Game } from 'types';

export function useGame(gameId: number) {
  const [game, setGame] = useState<Game>();
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string>();

  useEffect(() => {
    getGame(gameId)
      .then(setGame)
      .catch(err => setError(err.message))
      .finally(() => setIsLoading(false));
  }, [gameId]);

  return { game, isLoading, error };
} 