**Steps Taken for the Project**
*Phase1: Initialize and Project Setup*
- **Step1: Get UV manager**
- pip install uv (uv is same as pip but only thing is it is 10x faster install all packages and rememebers the versions - so less issues with the version controlling)

-- ** Step2: Project Structure 
- uv init (it add all the files required for a project - main.py, .venv etc) 

**Phase2: Input Data - CREATE DUMMY DATABASE/TABLE/VALUEs**
For this project, input data would be database/table/data so we need to create a dummy database, dummy tables and input data in it 
Remember, 
- All SQL queries run inside a database system — like Google BigQuery, PostgreSQL, SQLite, etc. These are all Relational Database Systems. Python does not run the SQL.
- When we create a database in Python (like with SQLite), we are basically creating the database file (tables, schema, columns) that normally would live inside a database system. remember in databricks, we have catalog that has similar structure (technically, take it as database file) 
- To run queries on these tables, we need a way for Python to talk to the database. That’s what a database library does (sqlite3 for SQLite, psycopg2 for PostgreSQL).
- So, technically, database library which is a sql editor is written in python. It's work is to run your database file written in python inside it.. technically, this library will act as sql editor and run your database file inside it and produces results in python
Note: you always need a database system to run sql, python never runs sql files but it calls out sql libraries (which are these database managements) and ask them to come to python and run your file inside it. 
- Python uses the sqlite3 library to connect to the database file and run queries.
-- ** Step3: Choose the Database system (or editor) that will run your sql query
- import sqlite3 (sqlite3 (Python built-in library)) 
- Create a new dummy_database.py file so that you can have your database separate

- import sqlite3 
- connection = sqlite3.connect("amazon_new.db")  #connect your database file to the sql editor so editor knows which file to take data from. make sure its .db not .py
- cursor = connection.cursor() ##The cursor is the tool that actually executes SQL commands. ## technically add your tables or input data everything is done through cursor 

Now we connected our database file to sql editor
- here, cursor helps you to create table or insert the data 
- cursor.execute("""
CREATE TABLE IF NOT EXISTS customer(
name text, 
email text 
)
""")

# Order Items
-cursor.execute("""
INSERT INTO ORDER_ITEMS (order_id, product_id, quantity, subtotal) VALUES  
    (4, 4, 1, 12.00)       
""")

After inserting data you must commit.Otherwise the inserts may not persist.
-connection.commit()
-connection.close()

**Phase3: Pass the Database to LLM**
