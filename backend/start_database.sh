#!/bin/zsh

# Source the .env file
if [ -f .env ]; then
    source .env
else
    echo ".env file not found"
    exit 1
fi

echo "Checking if PostgreSQL is running..."
# Check if PostgreSQL is running
if pg_isready -q; then
    echo "PostgreSQL is already running."
else
    echo "Starting PostgreSQL..."
    # Start PostgreSQL
    sudo systemctl start postgresql
    if [ $? -ne 0 ]; then
        echo "Failed to start PostgreSQL. Please check the service status."
        exit 1
    fi
    echo "PostgreSQL started successfully."
fi

echo "Setting up the database..."
# Check if database exists and create it if it doesn't
if ! psql -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME"; then
    echo "Creating database '$DB_NAME'..."
    createdb "$DB_NAME"
    echo "Initializing schema for new database..."
    psql -d "$DB_NAME" -f database/schema.sql
    echo "Database created and schema initialized."
fi

# Run all SQL migrations in the migrations directory
echo "Running SQL migrations..."
for migration in database/migrations/*.sql; do
    if [ -f "$migration" ]; then
        echo "Applying migration: $(basename "$migration")"
        psql -d "$DB_NAME" -f "$migration"
        if [ $? -ne 0 ]; then
            echo "Failed to apply migration: $(basename "$migration")"
            exit 1
        fi
    fi
done

echo "Database setup completed successfully."
