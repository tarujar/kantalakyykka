#!/bin/zsh

#set -e  # Exit immediately if a command exits with a non-zero status
#set -x  # Print commands and their arguments as they are executed

echo "Navigating to the project directory..."
# Navigate to the project directory
cd "$(dirname "$0")"

#echo "Killing existing Python and Uvicorn processes..."
# Kill existing Python and Uvicorn processes
#pkill -f python
#pkill -f uvicorn

echo "Checking if PostgreSQL is running..."
# Check if PostgreSQL is running
if ! pg_isready -q; then
    echo "PostgreSQL is not running. Please start the database server."
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
# Set up the database (if using Alembic for migrations)
source venv/bin/activate  # Ensure alembic is available in the virtual environment
alembic upgrade head

echo "Creating admin user if it doesn't exist..."
# Create admin user if it doesn't exist
./create_admin_user.sh

echo "Running the Flask application with Gunicorn..."
# Run the Flask application with Gunicorn
gunicorn -w 4 -b 127.0.0.1:8000 --reload app.main:app
