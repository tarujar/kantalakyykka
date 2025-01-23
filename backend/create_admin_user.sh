#!/bin/zsh

echo "Creating admin user if it doesn't exist..."

# Load environment variables from .env file
export $(grep -v '^#' .env | xargs)

# Check if the admin user already exists
USER_EXISTS=$(psql -U $DB_USER -d $DB_NAME -tAc "SELECT 1 FROM users WHERE username='$ADMIN_USERNAME'")

if [ "$USER_EXISTS" != "1" ]; then
    # Hash the password using openssl
    HASHED_PASSWORD=$(openssl passwd -6 "$ADMIN_PASSWORD")

    # Create the admin user
    psql -U $DB_USER -d $DB_NAME -c "INSERT INTO users (username, email, hashed_password) VALUES ('$ADMIN_USERNAME', '$ADMIN_EMAIL', '$HASHED_PASSWORD')"
    echo "Admin user created."
else
    echo "Admin user already exists."
fi
