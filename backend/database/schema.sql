-- Throw result types
CREATE TYPE throw_result AS ENUM (
    'valid',       -- 2p per kyykkä (kyykät poistuvat neliöstä), 1p per kyykkä (kyykät jäävät laidalle aka pappi), 0 (osuma, mutta kyykät eivät siirry)
    'hauki',       -- H (0p, ei osumaa kyykään, hauki)
    'fault'        -- (0p, yliastuttu/hylätty heitto)
);

-- single(1), duo(2), quartet(4), team(4-8 players)
CREATE TABLE game_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    max_players INTEGER NOT NULL CHECK (max_players > 0),
    UNIQUE (name),
    UNIQUE (max_players)
);

-- Basic structures
CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    email VARCHAR(100) NOT NULL,
    UNIQUE (email),
    CONSTRAINT valid_email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

-- sarja OKL-A-2024, HKL-2025, PKL-2026 jne
CREATE TABLE series (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    season_type VARCHAR(10) NOT NULL DEFAULT 'winter' CHECK (season_type IN ('summer', 'winter')), -- kesä vs talvi pistelasku
    year INTEGER NOT NULL, -- mutta voi olla välikausi 14-15 :thinking:
    status VARCHAR(20) DEFAULT 'upcoming' CHECK (status IN ('upcoming', 'ongoing', 'completed')), -- onko ilmo vielä auki tms?
    registration_open BOOLEAN DEFAULT true, -- datetimefield?
    game_type_id INTEGER REFERENCES game_types(id) NOT NULL, -- Viittaus pelityyppiin
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (name, year)
);

-- Teams that register in series // Joukkueet
CREATE TABLE teams_in_series (
    id SERIAL PRIMARY KEY,
    series_id INTEGER REFERENCES series(id),
    team_name VARCHAR(100) NOT NULL,
    team_abbreviation VARCHAR(10) NOT NULL,
    contact_player_id INTEGER REFERENCES players(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(series_id, team_name),         -- Joukkueen nimi on uniikki sarjassa
    UNIQUE(series_id, team_abbreviation) -- Joukkueen lyhenne on uniikki sarjassa
);

CREATE TABLE roster_players_in_series (
    registration_id INTEGER REFERENCES teams_in_series(id),
    player_id INTEGER REFERENCES players(id),
    UNIQUE(registration_id, player_id)
);

CREATE TABLE team_history (
    id SERIAL PRIMARY KEY,
    previous_registration_id INTEGER REFERENCES teams_in_series(id),
    next_registration_id INTEGER REFERENCES teams_in_series(id),
    relation_type VARCHAR(50) CHECK (relation_type IN ('continuation', 'split', 'merge')),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(previous_registration_id, next_registration_id)
);

-- Games and scoring  // Pelitulokset
CREATE TABLE games (
    id SERIAL PRIMARY KEY,
    round TEXT NULL,
    is_playoff BOOLEAN DEFAULT false,
    series_id INTEGER REFERENCES series(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    game_date DATE NOT NULL,
    team_1_id INTEGER REFERENCES teams_in_series(id), -- kotijoukkue
    team_2_id INTEGER REFERENCES teams_in_series(id),
    score_1_1 INTEGER NOT NULL, -- joukkue 1 erä 1 
    score_1_2 INTEGER NOT NULL, -- joukkue 1 erä 2
    score_2_1 INTEGER NOT NULL, -- joukkue 2 erä 1
    score_2_2 INTEGER NOT NULL, -- joukkue 2 erä 2
    CONSTRAINT different_teams CHECK (team_1_id != team_2_id),
    UNIQUE (series_id, game_date, team_1_id, team_2_id, round)
);

-- Joukkueiden heittotulokset
CREATE TABLE single_throw (
    id SERIAL PRIMARY KEY,
    throw_type throw_result,
    throw_score INTEGER NOT NULL,
    CONSTRAINT valid_throw_score CHECK (
        CASE 
            WHEN throw_type = 'valid' THEN
                throw_score BETWEEN -80 AND 80
            ELSE 
                throw_score = 0 -- Hauki, hylätty aina 0p
        END
    )
);

-- jokaisessa erässä on 4 tai 5 heittokierrosta
-- 1 erän 1 heittokierros on yhden pelaajan 4 heittoa
-- 2 erän 1 heittokierros on yhden pelaajan 4 heittoa jne
CREATE TABLE single_round_throws (
    id SERIAL PRIMARY KEY,
    game_id INTEGER REFERENCES games(id),
    game_set_index INTEGER NOT NULL,
    throw_position INTEGER NOT NULL,
    home_team BOOLEAN NOT NULL,
    player_id INTEGER REFERENCES players(id),
    throw_1 INTEGER REFERENCES single_throw(id),
    throw_2 INTEGER REFERENCES single_throw(id),
    throw_3 INTEGER REFERENCES single_throw(id),
    throw_4 INTEGER REFERENCES single_throw(id),
    CONSTRAINT valid_throw_position CHECK (throw_position BETWEEN 1 AND 5),
    CONSTRAINT valid_game_set_index CHECK (game_set_index BETWEEN 1 AND 2),
    UNIQUE (game_id, game_set_index, throw_position),
    UNIQUE (game_id, game_set_index)
);



-- Yksinkertaiset tarkistukset tietokannassa
CREATE OR REPLACE FUNCTION validate_team_player_count()
RETURNS TRIGGER AS $$
DECLARE
    v_max_players INTEGER;
    v_active_players INTEGER;
BEGIN
    -- Hae pelityypin maksimipelaajamäärä
    SELECT gt.max_players INTO v_max_players
    FROM game_types gt
    JOIN series s ON gt.id = s.game_type_id
    JOIN teams_in_series t ON s.id = t.series_id
    WHERE t.id = NEW.registration_id;

    -- Lasketaan aktiivisten pelaajien määrä joukkueessa
    SELECT COUNT(*) INTO v_active_players
    FROM roster_players_in_series
    WHERE registration_id = NEW.registration_id;

    -- Tarkista, ettei aktiivisten pelaajien määrä ylitä rajaa
    IF v_active_players >= v_max_players THEN
        RAISE EXCEPTION 'Player limit exceeded: Only % players allowed for this game type',
            v_max_players;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggerin luominen
CREATE TRIGGER validate_team_player_count_trigger
BEFORE INSERT OR UPDATE ON roster_players_in_series
FOR EACH ROW
EXECUTE FUNCTION validate_team_player_count();