#!/bin/bash
# create_databases.sh
set -e

# Tworzenie pierwszej bazy danych
psql -U "$POSTGRES_USER" -d postgres -c "CREATE DATABASE $POSTGRES_DB;"
psql -U "$POSTGRES_USER" -d postgres -c "CREATE DATABASE $POSTGRES_DB_2;"

echo "Bazy danych $POSTGRES_DB i $POSTGRES_DB_2 zostały utworzone"