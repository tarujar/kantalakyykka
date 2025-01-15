export const translations = {
  gameTypes: {
    single: 'Henkilökohtainen peli',
    duo: 'Paripeli',
    quartet: 'Joukkuepeli'
  },
  teamLabels: {
    single: 'Pelaaja',
    duo: 'Pari',
    quartet: 'Joukkue'
  },
  game: {
    starting: 'Aloittava',
    throws: 'Heitot',
    points: 'Pisteet',
    save: 'Tallenna tulos',
    loading: 'Ladataan...',
    error: 'Virhe:',
    notFound: 'Peliä ei löytynyt',
    trackThrows: 'Seuraa heittoja',
    set: 'Erä',
    throwsPerSet: {
      single: '20 heittoa/erä',
      duo: '20 heittoa/erä',
      quartet: '16 heittoa/erä'
    },
    team: 'Joukkue',
    throw: 'Heitto {{number}}',
    throwNumber: 'Heitto',
    player: 'Pelaaja',
    playerName: 'Pelaajan nimi',
    teamName: 'Joukkueen nimi',
    selectPlayers: 'Valitse pelaajat',
    confirmSelection: 'Vahvista valinnat',
    throwOrder: 'Heittojärjestys',
    selectType: 'Valitse pelityyppi',
    selectTeam: 'Valitse {{number}}. joukkue',
    createGame: 'Luo peli',
    throwInput: {
      placeholder: 'Syötä pisteet',
      invalidInput: 'Vain numerot sallittu'
    },
    removePlayer: 'Poista pelaaja {{name}}',
    searchPlayers: 'Hae pelaajia',
    noPlayersFound: 'Pelaajia ei löytynyt',
    playerAdded: 'Pelaaja {{name}} lisätty',
    playerRemoved: 'Pelaaja {{name}} poistettu'
  },
  validation: {
    pointLimits: 'Pisteet: -80 - {{max}}',
    requiredField: 'Pakollinen kenttä',
    invalidTeamSize: 'Väärä pelaajamäärä pelityypille',
    teamRequired: 'Valitse molemmat joukkueet'
  }
};

export type TranslationKey = keyof typeof translations; 