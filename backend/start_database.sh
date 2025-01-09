#!/bin/zsh


echo "Checking if PostgreSQL is running..."
# Check if PostgreSQL is running
if pg_isready -q; then
    echo "PostgreSQL is already running."
else
    echo "Starting PostgreSQL..."
    # Start PostgreSQL
    sudo systemctl start postgresql
    if [ $? -eq 0 ]; then
        echo "PostgreSQL started successfully."
    else
        echo "Failed to start PostgreSQL. Please check the service status."
        exit 1
    fi
fi
