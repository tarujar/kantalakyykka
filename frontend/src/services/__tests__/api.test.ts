import { fetchGames, createGame } from '../api';
import { mockGames, mockPlayers } from '../../mocks/testData';

describe('API', () => {
  beforeEach(() => {
    global.fetch = jest.fn();
  });

  it('fetches games successfully', async () => {
    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => mockGames,
    });

    const result = await fetchGames();
    expect(result).toEqual(mockGames);
  });

  it('creates new game successfully', async () => {
    const newGame = {
      gameType: 'single' as GameType,
      players: [mockPlayers[0].id],
      pointsMultiplier: 1
    };

    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ ...newGame, id: 4 }),
    });

    const result = await createGame(newGame);
    expect(result.id).toBe(4);
    expect(result.gameType).toBe('single');
  });
}); 