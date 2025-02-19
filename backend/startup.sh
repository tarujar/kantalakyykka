#!/bin/zsh

# Source the .env file
if [ -f .env ]; then
    source .env
else
    echo ".env file not found"
    exit 1
fi

echo "Navigating to the project directory..."
cd "$(dirname "$0")"

# Check if port 8000 is in use and kill the process if it exists
echo "Checking if port 8000 is in use..."
if lsof -i :8000 > /dev/null; then
    echo "Port 8000 is in use. Killing existing process..."
    lsof -ti :8000 | xargs kill -9
fi

# Kill any existing Gunicorn processes
echo "Cleaning up existing Gunicorn processes..."
pkill -f gunicorn

echo "Checking if PostgreSQL is running..."
# Check if PostgreSQL is running
if ! pg_isready -q; then
    echo "PostgreSQL is not running. Please run ./start_database.sh first"
    exit 1
fi

echo "Setting up the virtual environment..."
# Set up a virtual environment
python3 -m venv venv

echo "Activating the virtual environment..."
# Activate the virtual environment
source venv/bin/activate

echo "Adding virtual environment to PATH..."
# Add virtual environment to PATH
export PATH="$PWD/venv/bin:$PATH"

echo "Installing the required dependencies..."
# Install the required dependencies
if [ -f requirements.txt ]; then
    python3 -m pip install --upgrade --requirement requirements.txt
else
    echo "requirements.txt not found"
    exit 1
fi

echo "Compiling translations..."
# Compile translations
pybabel compile -d translations

echo "Setting up the database..."
# Check if database exists and create it if it doesn't
if ! psql -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME"; then
    echo "Creating database '$DB_NAME'..."
    createdb "$DB_NAME"
    echo "Initializing schema for new database..."
    psql -d "$DB_NAME" -f database/schema.sql
    echo "Database created and schema initialized."
fi

# Then run the structural changes
echo "2. Adding new columns and constraints..."
psql -d "$DB_NAME" -f database/migrations/002_add_throw_index_and_team_references.sql

echo "Running any remaining Alembic migrations..."
source venv/bin/activate
alembic upgrade head

echo "Creating admin user if it doesn't exist..."
# Create admin user if it doesn't exist
./create_admin_user.sh

echo "Running the Flask application with Gunicorn..."
# Run the Flask application with Gunicorn
# Added timeout to allow for proper startup
gunicorn -w 4 -b 127.0.0.1:8000 --reload --timeout 120 --reload-extra-file ./app/templates app.main:app
