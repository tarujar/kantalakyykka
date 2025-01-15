#!/bin/bash

# Script to set up the database

echo "Setting up the database..."

# Add commands to set up the database here
# For example:
createdb kyykkakanta
psql kyykkakanta < ./../database/schema.sql

echo "Database setup complete."
