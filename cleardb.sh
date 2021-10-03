# Resets the database by dorpping all tables and creating them again.

cd schema
psql techinv < cleardb.sql
psql techinv < schema.sql
cd ..