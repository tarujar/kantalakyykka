import React, { useState, useEffect } from 'react';
import GameResultForm from './GameResultForm';
import { Series, TeamInSeries as Team } from 'openapi';

interface Props {
  onGameCreated: (gameId: number) => void;
}

/**
 * NewGameWizard ohjaa käyttäjän pelin luomisprosessin läpi.
 * 
 * Vaiheet:
 * 1. Sarjan valinta
 * 2. Joukkueiden valinta (koti- ja vierasjoukkue)
 * 3. Pelin luonti GameCreationForm-komponentin avulla
 * 
 * Huomiot:
 * - Kotijoukkue aloittaa aina ensimmäisen erän
 * - Vierasjoukkue aloittaa toisen erän
 * - Joukkueiden pelaajat haetaan sarjarekisteröinneistä
 * 
 * Käyttö:
 * <NewGameWizard onGameCreated={(gameId) => navigate(`/games/${gameId}`)} />
 */
export function NewGameWizard({ onGameCreated }: Props) {
  const [step, setStep] = useState<'series' | 'teams' | 'game'>('series');
  const [selectedSeries, setSelectedSeries] = useState<Series | null>(null);
  const [selectedTeams, setSelectedTeams] = useState<{
    homeTeam: Team | null;
    awayTeam: Team | null;
  }>({ homeTeam: null, awayTeam: null });
  return (
    <div className="game-wizard">
      {step === 'series' && (
        <SeriesSelection 
          onSelect={(series) => {
            setSelectedSeries(series);
            setStep('teams');
          }}
        />
      )}

      {step === 'teams' && selectedSeries && (
        <TeamSelection 
          series={selectedSeries}
          onSelect={(homeTeam, awayTeam) => {
            setSelectedTeams({ homeTeam, awayTeam });
            setStep('game');
          }}
        />
      )}

      {step === 'game' && selectedSeries && selectedTeams.homeTeam && selectedTeams.awayTeam && (
        <GameResultForm
          series={selectedSeries}
          homeTeam={selectedTeams.homeTeam}
          awayTeam={selectedTeams.awayTeam}
          onGameCreated={onGameCreated}
        />
      )}
    </div>
  );
}

function SeriesSelection({ onSelect }: { onSelect: (series: Series) => void }) {
  const [series, setSeries] = useState<Series[]>([]);

  useEffect(() => {
    // Hae sarjat API:sta
    // api.getActiveSeries().then(setSeries);
  }, []);
  console.log("sarjat",series)
  return (
    <div>
      <h2>Valitse sarja</h2>
      aaa
      <div className="series-grid">
        {series.map(s => (
          <button 
            key={s.id}
            onClick={() => onSelect(s)}
            className="series-button"
          >
            {s.name} 
          </button>
        ))}
      </div>
    </div>
  );
}

function TeamSelection({ 
  series,
  onSelect 
}: { 
  series: Series;
  onSelect: (homeTeam: Team, awayTeam: Team) => void;
}) {
  const [teams, setTeams] = useState<Team[]>([]);
  const [homeTeam, setHomeTeam] = useState<Team | null>(null);


  return (
    <div>
      <h2>Valitse joukkueet</h2>
      
      {!homeTeam ? (
        <>
          <h3>Valitse kotijoukkue (aloittaa 1. erän)</h3>
          <div className="teams-grid">
            {teams.map(team => (
              <button
                key={team.id}
                onClick={() => setHomeTeam(team)}
                className="team-button"
              >
                {team.team_name}
              </button>
            ))}
          </div>
        </>
      ) : (
        <>
          <h3>Valitse vierasjoukkue</h3>
          <div className="teams-grid">
            {teams
              .filter(t => t.id !== homeTeam.id)
              .map(team => (
                <button
                  key={team.id}
                  onClick={() => onSelect(homeTeam, team)}
                  className="team-button"
                >
                  {team.team_name}
                </button>
              ))}
          </div>
        </>
      )}
    </div>
  );
} 