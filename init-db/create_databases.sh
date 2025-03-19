#!/bin/bash
# This script creates new databases after first build of db container
set -e

#finanical_data_set_new
psql -U "$POSTGRES_USER" -d postgres -c "CREATE DATABASE $POSTGRES_DB;"
#users_flask_dash
psql -U "$POSTGRES_USER" -d postgres -c "CREATE DATABASE $POSTGRES_DB_2;"
