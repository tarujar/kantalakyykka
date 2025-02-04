DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type t
                   JOIN pg_enum e ON t.oid = e.enumtypid
                   WHERE t.typname = 'throw_result' AND e.enumlabel = 'E') THEN
        ALTER TYPE throw_result ADD VALUE 'E';
    END IF;
END $$;
