-- Create the Northwind database for text-to-SQL demo
CREATE DATABASE northwind;

-- Create a read-only role for the SQL agent
CREATE ROLE rag_readonly WITH LOGIN PASSWORD 'readonly_password';

-- Grant connect to northwind
GRANT CONNECT ON DATABASE northwind TO rag_readonly;
