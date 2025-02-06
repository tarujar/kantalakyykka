import { GameType, listGameTypesApiV1GameTypesGet } from 'openapi';
import { useState, useEffect } from 'react';

const useGameTypes = () => {
  const [gameTypes, setGameTypes] = useState<GameType[]>([]);

  useEffect(() => {
    const fetchGameTypes = async () => {
      try {
        const response = await listGameTypesApiV1GameTypesGet();
        console.log('Game types:', response.data);
        if (response.data) setGameTypes(response.data);
      } catch (error) {
        console.error('Error fetching game types:', error);
      }
    };

    fetchGameTypes();
  }, []);

  return gameTypes;
};

export default useGameTypes;