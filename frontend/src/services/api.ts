import axios from 'axios';
import { Game, GameCreate, GameType, GameTypeCreate, Player, PlayerCreate, Series, SeriesCreate, TeamInSeries } from '../types';
const API_BASE_URL = 'http://localhost:8000/api/v1';

// Series API
export const createSeries = async (series: SeriesCreate): Promise<Series> => {
  const response = await axios.post(`${API_BASE_URL}/series`, series);
  return response.data;
};

export const getSeries = async (seriesId: number): Promise<Series> => {
  const response = await axios.get(`${API_BASE_URL}/series/${seriesId}`);
  return response.data;
};

export const listSeries = async (): Promise<Series[]> => {
  const response = await axios.get(`${API_BASE_URL}/series`);
  return response.data;
};

export const addTeamToSeries = async (seriesId: number, team: TeamInSeries): Promise<TeamInSeries> => {
  const response = await axios.post(`${API_BASE_URL}/series/${seriesId}/teams`, team);
  return response.data;
};

// Player API
export const createPlayer = async (player: PlayerCreate): Promise<Player> => {
  const response = await axios.post(`${API_BASE_URL}/players`, player);
  return response.data;
};

export const getPlayer = async (playerId: number): Promise<Player> => {
  const response = await axios.get(`${API_BASE_URL}/players/${playerId}`);
  return response.data;
};

export const listPlayers = async (): Promise<Player[]> => {
  const response = await axios.get(`${API_BASE_URL}/players`);
  return response.data;
};

export const updatePlayer = async (playerId: number, player: PlayerCreate): Promise<Player> => {
  const response = await axios.put(`${API_BASE_URL}/players/${playerId}`, player);
  return response.data;
};

export const deletePlayer = async (playerId: number): Promise<void> => {
  await axios.delete(`${API_BASE_URL}/players/${playerId}`);
};

// Game API
export const createGame = async (game: GameCreate): Promise<Game> => {
  const response = await axios.post(`${API_BASE_URL}/games`, game);
  return response.data;
};

export const getGame = async (gameId: number): Promise<Game> => {
  const response = await axios.get(`${API_BASE_URL}/games/${gameId}`);
  return response.data;
};

export const listGames = async (): Promise<Game[]> => {
  const response = await axios.get(`${API_BASE_URL}/games`);
  return response.data;
};

// Game Type API
export const createGameType = async (gameType: GameTypeCreate): Promise<GameType> => {
  const response = await axios.post(`${API_BASE_URL}/game_types`, gameType);
  return response.data;
};

export const getGameType = async (gameTypeId: number): Promise<GameType> => {
  const response = await axios.get(`${API_BASE_URL}/game_types/${gameTypeId}`);
  return response.data;
};

export const listGameTypes = async (): Promise<GameType[]> => {
  const response = await axios.get(`${API_BASE_URL}/game_types`);
  return response.data;
};

export const updateGameType = async (gameTypeId: number, gameType: GameTypeCreate): Promise<GameType> => {
  const response = await axios.put(`${API_BASE_URL}/game_types/${gameTypeId}`, gameType);
  return response.data;
};

export const deleteGameType = async (gameTypeId: number): Promise<void> => {
  await axios.delete(`${API_BASE_URL}/game_types/${gameTypeId}`);
};
