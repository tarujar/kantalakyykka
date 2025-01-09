#!/bin/zsh

# Load environment variables from .env file
if [ -f .env ]; then
    set -a
    source .env
    set +a
else
    echo "Error: .env file not found."
    exit 1
fi

# Check if the postgres user exists
if id "postgres" &>/dev/null; then
    # Switch to the postgres user and create the database and user
    psql -U postgres <<EOF
CREATE DATABASE ${DB_NAME};
CREATE USER ${DB_USER} WITH PASSWORD '${DB_PASSWORD}';
GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME} TO ${DB_USER};
EOF

    # Initialize the database schema
    if [ -f database/schema.sql ]; then
        psql -U postgres -d ${DB_NAME} -f database/schema.sql
        echo "PostgreSQL database, users, and schema have been initialized."
    else
        echo "Error: database/schema.sql not found."
        exit 1
    fi
else
    echo "The 'postgres' user does not exist. Creating the 'postgres' user."
    sudo useradd postgres
    psql -U postgres <<EOF
CREATE DATABASE ${DB_NAME};
CREATE USER ${DB_USER} WITH PASSWORD '${DB_PASSWORD}';
GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME} TO ${DB_USER};
EOF

    # Initialize the database schema
    if [ -f database/schema.sql ]; then
        psql -U postgres -d ${DB_NAME} -f database/schema.sql
        echo "PostgreSQL database, users, and schema have been initialized."
    else
        echo "Error: database/schema.sql not found."
        exit 1
    fi
fi