import { useState, useEffect } from 'react';
import { GameTypesService } from '../types/services/GameTypesService';
import { GameType } from 'types';

const useGameTypes = () => {
  const [gameTypes, setGameTypes] = useState<GameType[]>([]);

  useEffect(() => {
    const fetchGameTypes = async () => {
      try {
        const response = await GameTypesService.listGameTypesApiV1GameTypesGet();
        if (response) setGameTypes(response);
      } catch (error) {
        console.error('Error fetching game types:', error);
      }
    };

    fetchGameTypes();
  }, []);

  return gameTypes;
};

export default useGameTypes;
