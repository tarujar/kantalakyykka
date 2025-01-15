import { render, screen, fireEvent } from '@testing-library/react';
import { GameForm } from '../GameForm';
import { mockPlayers } from '../../../mocks/testData';

describe('GameForm', () => {
  const mockSubmit = jest.fn();

  beforeEach(() => {
    mockSubmit.mockClear();
  });

  it('renders game type options', () => {
    render(<GameForm onSubmit={mockSubmit} />);
    
    expect(screen.getByText('Henkilokohtainen')).toBeInTheDocument();
    expect(screen.getByText('Pari')).toBeInTheDocument();
    expect(screen.getByText('Joukkue')).toBeInTheDocument();
  });

  it('validates player count based on game type', () => {
    render(<GameForm onSubmit={mockSubmit} />);
    
    // Valitse joukkuepeli
    const select = screen.getByRole('combobox');
    fireEvent.change(select, { target: { value: 'quartet' } });
    
    // Yritä lisätä liian vähän pelaajia
    const submitButton = screen.getByRole('button', { name: /tallenna/i });
    fireEvent.click(submitButton);
    
    expect(screen.getByText(/tarvitaan 4 pelaajaa/i)).toBeInTheDocument();
  });
}); 