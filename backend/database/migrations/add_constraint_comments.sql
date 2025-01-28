-- Add comments to existing constraints
COMMENT ON CONSTRAINT unique_team_name_in_series ON teams_in_series IS 'Team name must be unique within the series';
COMMENT ON CONSTRAINT unique_team_abbr_in_series ON teams_in_series IS 'Team abbreviation must be unique within the series';
