-- Throw result types
CREATE TYPE throw_result AS ENUM (
    'VALID',       -- 2p per kyykkä (kyykät poistuvat neliöstä), 1p per kyykkä (kyykät jäävät laidalle aka pappi), 0 (osuma, mutta kyykät eivät siirry)
    'HAUKI',       -- H (0p, ei osumaa kyykään, hauki)
    'FAULT',       -- (0p, yliastuttu/hylätty heitto)
    'E'            -- (Käyttämättä jäänyt heitto, 0 tai pelin lopussa 1p jos kenttä on tyhjä)
);

-- single(1), duo(2), quartet(4), team(4-8 players)
CREATE TABLE game_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    max_players INTEGER NOT NULL CHECK (max_players > 0),
    throw_round_amount INTEGER NOT NULL DEFAULT 4,
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
    gdpr_consent BOOLEAN NOT NULL DEFAULT false,
    CONSTRAINT valid_email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

-- Add the users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (username),
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
    is_cup_league BOOLEAN DEFAULT false, -- onko cup vai normi sarja
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
    group VARCHAR(50) DEFAULT NULL,
    CONSTRAINT unique_team_name_in_series UNIQUE(series_id, team_name),         -- Joukkueen nimi on uniikki sarjassa
    CONSTRAINT unique_team_abbr_in_series UNIQUE(series_id, team_abbreviation) -- Joukkueen lyhenne on uniikki sarjassa
);

-- Add custom error messages for the constraints
COMMENT ON CONSTRAINT unique_team_name_in_series ON teams_in_series IS 'Team name must be unique within the series';
COMMENT ON CONSTRAINT unique_team_abbr_in_series ON teams_in_series IS 'Team abbreviation must be unique within the series';

CREATE TABLE roster_players_in_series (
    registration_id INTEGER REFERENCES teams_in_series(id),
    player_id INTEGER REFERENCES players(id),
    PRIMARY KEY (registration_id, player_id),
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
    -- type_id INTEGER REFERENCES game_types(id) NOT NULL,
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
            WHEN throw_type = 'VALID' THEN
                throw_score BETWEEN -80 AND 80
            WHEN throw_type = 'E' THEN
                throw_score = 1
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
    UNIQUE (game_id, game_set_index, throw_position, home_team)
);

-- Yksinkertaiset tarkistukset tietokannassa
CREATE OR REPLACE FUNCTION validate_team_player_count()
RETURNS TRIGGER AS $$
DECLARE
    v_max_players INTEGER;
    v_active_players INTEGER;
    v_game_type_name VARCHAR(100);
BEGIN
    -- Hae pelityypin maksimipelaajamäärä ja nimi
    SELECT gt.max_players, gt.name INTO v_max_players, v_game_type_name
    FROM game_types gt
    JOIN series s ON gt.id = s.game_type_id
    JOIN teams_in_series t ON s.id = t.series_id
    WHERE t.id = NEW.registration_id;

    -- Lasketaan aktiivisten pelaajien määrä joukkueessa, mukaan lukien uusi pelaaja
    SELECT COUNT(*) + 1 INTO v_active_players
    FROM roster_players_in_series
    WHERE registration_id = NEW.registration_id;

    -- Tarkista, ettei aktiivisten pelaajien määrä ylitä rajaa
    IF v_active_players > v_max_players THEN
        RAISE EXCEPTION 'Player limit exceeded: Only % players allowed for the game type % (% players currently registered)',
            v_max_players, v_game_type_name, v_active_players - 1;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggerin luominen
CREATE TRIGGER validate_team_player_count_trigger
BEFORE INSERT OR UPDATE ON roster_players_in_series
FOR EACH ROW
EXECUTE FUNCTION validate_team_player_count();

CREATE OR REPLACE FUNCTION validate_game_teams()
RETURNS TRIGGER AS $$
DECLARE
    team_1_series_id INTEGER;
    team_2_series_id INTEGER;
    is_cup BOOLEAN;
BEGIN
    -- Tarkista, onko sarja cup-sarja
    SELECT is_cup_league INTO is_cup FROM series WHERE id = NEW.series_id;

    -- Hae joukkueiden alkuperäiset sarjat
    SELECT series_id INTO team_1_series_id FROM teams_in_series WHERE id = NEW.team_1_id;
    SELECT series_id INTO team_2_series_id FROM teams_in_series WHERE id = NEW.team_2_id;

    -- Normaalissa sarjassa joukkueiden täytyy olla samasta sarjasta
    IF NOT is_cup AND team_1_series_id != team_2_series_id THEN
        RAISE EXCEPTION 'In regular series games, both teams must belong to the same series';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggerin asettaminen games-tauluun
CREATE TRIGGER validate_game_teams_trigger
BEFORE INSERT OR UPDATE ON games
FOR EACH ROW
EXECUTE FUNCTION validate_game_teams();

-- Rename round_amount column to throw_round_amount in game_types table
ALTER TABLE game_types RENAME COLUMN round_amount TO throw_round_amount;


