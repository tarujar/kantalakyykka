-- Add max_throw_index to game_types
ALTER TABLE game_types 
    ADD COLUMN max_throw_index INTEGER NOT NULL DEFAULT 20;

-- Add new columns to single_throw
ALTER TABLE single_throw 
    ADD COLUMN player_id INTEGER REFERENCES players(id),
    ADD COLUMN throw_index INTEGER;

-- Add constraint after data is potentially migrated
ALTER TABLE single_throw 
    ALTER COLUMN throw_index SET NOT NULL,
    ADD CONSTRAINT valid_throw_index CHECK (throw_index > 0 AND throw_index <= 20);

-- Add team_id to single_round_throws
ALTER TABLE single_round_throws 
    ADD COLUMN team_id INTEGER REFERENCES teams_in_series(id);

-- Remove player_id from single_round_throws
-- Note: Ensure any existing player_id data is migrated before running this
ALTER TABLE single_round_throws 
    DROP COLUMN IF EXISTS player_id;

-- Add indexes for performance
CREATE INDEX idx_single_throw_player ON single_throw(player_id);
CREATE INDEX idx_single_throw_index ON single_throw(throw_index);
CREATE INDEX idx_single_round_throws_team ON single_round_throws(team_id);

-- Create function to validate throw_index against game_type
CREATE OR REPLACE FUNCTION validate_throw_index()
RETURNS TRIGGER AS $$
DECLARE
    v_max_throw_index INTEGER;
BEGIN
    -- Get max_throw_index from game_type through the chain of relationships
    SELECT gt.max_throw_index INTO v_max_throw_index
    FROM single_round_throws srt
    JOIN games g ON srt.game_id = g.id
    JOIN series s ON g.series_id = s.id
    JOIN game_types gt ON s.game_type_id = gt.id
    WHERE srt.throw_1 = NEW.id 
       OR srt.throw_2 = NEW.id 
       OR srt.throw_3 = NEW.id 
       OR srt.throw_4 = NEW.id;

    IF NEW.throw_index > v_max_throw_index THEN
        RAISE EXCEPTION 'throw_index (%) exceeds maximum allowed (%) for this game type', 
            NEW.throw_index, v_max_throw_index;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger
CREATE TRIGGER validate_throw_index_trigger
BEFORE INSERT OR UPDATE ON single_throw
FOR EACH ROW
EXECUTE FUNCTION validate_throw_index();

-- Add indexes for performance
CREATE INDEX idx_games_series_id ON games(series_id);
CREATE INDEX idx_series_game_type_id ON series(game_type_id);
