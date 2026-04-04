-- Create the database if it doesn't exist
SELECT 'CREATE DATABASE digitwin'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'digitwin')\gexec

-- Create the user if it doesn't exist
DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE  rolname = 'twin') THEN
      CREATE USER twin WITH PASSWORD 'twin';
   END IF;
END
$do$;

-- Grant all privileges
GRANT ALL PRIVILEGES ON DATABASE digitwin TO twin;
ALTER DATABASE digitwin OWNER TO twin;
