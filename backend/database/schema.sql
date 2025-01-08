-- Throw result types
CREATE TYPE throw_result AS ENUM (
    'valid',       -- 2p per kyykkä (kyykät poistuvat neliöstä), 1p per kyykkä (kyykät jäävät laidalle aka pappi), 0 (osuma, mutta kyykät eivät siirry)
    'hauki',       -- H (0p, ei osumaa kyykään, hauki)
    'fault'        -- (0p, yliastuttu/hylätty heitto)
);

-- Basic structures
CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- sarja OKL-A-2024, HKL-2025, PKL-2026 jne
CREATE TABLE series (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    season_type VARCHAR(10) NOT NULL CHECK (season_type IN ('summer', 'winter')), -- kesä vs talvi pistelasku
    year INTEGER NOT NULL, -- mutta voi olla välikausi 14-15 :thinking:
    game_type VARCHAR(20) NOT NULL CHECK (game_type IN ('single', 'duo', 'quartet')),
    status VARCHAR(20) DEFAULT 'upcoming' CHECK (status IN ('upcoming', 'ongoing', 'completed')), -- onko ilmo vielä auki tms?
    registration_open BOOLEAN DEFAULT true, -- datetimefield?
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Teams that register in series // Joukkueet
CREATE TABLE teams_in_series (
    id SERIAL PRIMARY KEY,
    series_id INTEGER REFERENCES series(id),
    team_name VARCHAR(100) NOT NULL,
    team_abbreviation VARCHAR(10) NOT NULL,
    contact_player_id INTEGER REFERENCES players(id),
    -- is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(series_id, team_name)         -- Joukkueen nimi on uniikki sarjassa
    UNIQUE(series_id, team_abbreviation) -- Joukkueen lyhenne on uniikki sarjassa
);

CREATE TABLE roster_players (
    registration_id INTEGER REFERENCES teams_in_series(id),
    player_id INTEGER REFERENCES players(id),
    is_reserve BOOLEAN DEFAULT false,
    joined_date DATE NOT NULL,
    left_date DATE,
    PRIMARY KEY (registration_id, player_id, joined_date)
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

CREATE TYPE throw_result AS ENUM (
    'valid',       -- 2p per kyykkä (kyykät poistuvat neliöstä), 1p per kyykkä (kyykät jäävät laidalle aka pappi), 0 (osuma, mutta kyykät eivät siirry)
    'hauki',       -- H (0p, ei osumaa kyykään, hauki)
    'fault'        -- (0p, yliastuttu/hylätty heitto)
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
    -- scores INTEGER REFERENCES game_sets(id),
    score_1_1 INTEGER NOT NULL, -- joukkue 1 erä 1 
    score_1_2 INTEGER NOT NULL, -- joukkue 1 erä 2
    score_2_1 INTEGER NOT NULL, -- joukkue 2 erä 1
    score_2_2 INTEGER NOT NULL, -- joukkue 2 erä 2
    CONSTRAINT different_teams CHECK (team1_id != team2_id)
    UNIQUE (series_id, game_date, team_1_id, team_2_id, round)
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
    throw_4 INTEGER REFERENCES single_throw(id)
    CONSTRAINT valid_throw_position CHECK (throw_position BETWEEN 1 AND 5)
    CONSTRAINT valid_game_set_index CHECK (game_set_index BETWEEN 1 AND 2)
    UNIQUE (game_id, game_set_index, throw_position)
    UNIQUE (game_id, game_set_index)
);

-- Joukkueiden heittotulokset
CREATE TABLE single_throw (
    id SERIAL PRIMARY KEY,
    throw_type throw_result DEFAULT,
    throw_score INTEGER NOT NULL,
    CONSTRAINT valid_throw_score CHECK (
        CASE 
            WHEN throw_type IN ('valid') THEN
                throw_score BETWEEN -80 AND 80
            ELSE 
                throw_score = 0 -- Hauki, hylätty aina 0p
        END
    )
);


/*
CREATE TABLE player_throws (
    id SERIAL PRIMARY KEY,
    game_set_id INTEGER REFERENCES game_sets(id),
    player_id INTEGER REFERENCES players(id),
    team_number INTEGER CHECK (team_number IN (1, 2)),
    player_position INTEGER NOT NULL,
    throw_number INTEGER NOT NULL,
    points INTEGER DEFAULT 0,
    throw_type VARCHAR(1) CHECK (
        throw_type IS NULL OR
        throw_type IN ('H', '-', 'U')
    ),
    UNIQUE (game_set_id, player_position, throw_number),
    -- Tarkista heittojärjestys erän mukaan
    CONSTRAINT valid_throw_order CHECK (
        CASE 
            WHEN (SELECT set_number FROM game_sets WHERE id = game_set_id) = 1 THEN
                -- 1. erä: joukkue 1 aloittaa
                (team_number = 1 AND player_position <= 2) OR
                (team_number = 2 AND player_position <= 2) OR
                (team_number = 1 AND player_position > 2) OR
                (team_number = 2 AND player_position > 2)
            ELSE
                -- 2. erä: joukkue 2 aloittaa
                (team_number = 2 AND player_position <= 2) OR
                (team_number = 1 AND player_position <= 2) OR
                (team_number = 2 AND player_position > 2) OR
                (team_number = 1 AND player_position > 2)
        END
    ),
    -- Tarkista pisteiden validius
    CONSTRAINT valid_points CHECK (
        CASE 
            WHEN throw_type IS NOT NULL THEN 
                points = 0  -- H, -, U aina 0 pistettä
            WHEN points < 0 THEN 
                points = -1 -- Vain yksi kyykkä voi palata kentälle (pappi)
            ELSE 
                points >= 0 -- Positiiviset pisteet sallittuja (kyykät ulos)
        END
    )
);
*/
-- Yksinkertaiset tarkistukset tietokannassa
ALTER TABLE roster_players ADD CONSTRAINT valid_player_count
    CHECK (
        (SELECT COUNT(*) FROM roster_players WHERE registration_id = NEW.registration_id) <= 4
    );

-- Player count validation
CREATE OR REPLACE FUNCTION validate_game_players()
RETURNS TRIGGER AS $$
DECLARE
    v_game_type VARCHAR(20);
    v_active_players INTEGER;
BEGIN
    SELECT s.game_type INTO v_game_type
    FROM series s
    JOIN teams_in_series sr ON s.id = sr.series_id
    WHERE sr.id = NEW.registration_id;

    SELECT COUNT(*) INTO v_active_players
    FROM roster_players
    WHERE registration_id = NEW.registration_id
    AND is_reserve = false
    AND (left_date IS NULL OR left_date > CURRENT_DATE);

    IF NEW.is_reserve = false THEN
        CASE v_game_type
            WHEN 'single' THEN
                IF v_active_players >= 1 THEN
                    RAISE EXCEPTION 'Only one player allowed in single series';
                END IF;
            WHEN 'duo' THEN
                IF v_active_players >= 2 THEN
                    RAISE EXCEPTION 'Only two players allowed in duo series';
                END IF;
            WHEN 'quartet' THEN
                IF v_active_players >= 4 THEN
                    RAISE EXCEPTION 'Only four main players allowed in quartet series';
                END IF;
        END CASE;
    ELSIF v_game_type = 'quartet' AND NEW.is_reserve = true THEN
        SELECT COUNT(*) INTO v_active_players
        FROM roster_players
        WHERE registration_id = NEW.registration_id
        AND is_reserve = true
        AND (left_date IS NULL OR left_date > CURRENT_DATE);
        
        IF v_active_players >= 4 THEN
            RAISE EXCEPTION 'Maximum of four reserve players allowed in quartet series';
        END IF;
    ELSIF NEW.is_reserve = true AND v_game_type IN ('single', 'duo') THEN
        RAISE EXCEPTION 'Reserve players only allowed in quartet series';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER validate_game_players_trigger
BEFORE INSERT OR UPDATE ON roster_players
FOR EACH ROW
EXECUTE FUNCTION validate_game_players();

