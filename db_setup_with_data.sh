#!/bin/bash -x

# Make sure you have following for DB schema creation and dummy data insertion
# Create a DB with name `weatherdb` and provide assess to `Postgres` User with password `1234`
# Below Script automatically creates `weatherwise` schema and its related tables with
# some dummy data inserted.
# If needed modify python script accordingly at path app/scripts/

# Replace with your Flask app's file name
python app/scripts/create_postgres_db.py