In Simple Terms, LLM over here (OpenAI) writes SQL Queries based on Schema provided to it. 
The work of a data analyst is replaced by LLM 

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

-cursor.execute("""
INSERT INTO ORDER_ITEMS (order_id, product_id, quantity, subtotal) VALUES  
    (4, 4, 1, 12.00)       
""")

After inserting data you must commit.Otherwise the inserts may not persist.
-connection.commit()
-connection.close()



**Phase3: Using SQLALCHEMY GEt the SCHEMA (tablenames, column names and relationshiP) to pass to LLM**

- SQlalchemy sits on top of sqlite and get just the schema (tablenames, column names and relationshiP)
- #sqlalchemy: ✔ Inspect the database automatically it fetches table names, columns names and relationships
- Your LLM needs to write query like an analyst but instead of using values and all all it needs it table name and column names
- ##To import sqlalchemy -> uv add sqlalchemy
- from sqlalchemy import create_engine, inspect
- we need to give database type + file to sqlalchemy. #This is just a standard database connection string -> database_type:///database_name 
- for example: (bigquery://project_id/dataset)
- db_url = "sqlite:///dummy_database.db" (sqlite: This is where the data and tables actually exist.)
- engine = create_engine(db_url) ---> (connect sqlalchemy with sqlite)
- inspector = inspect(engine) --> inspector will inspect or find the tables names, columns names automatically
- NEXT, 
- we need to pass a varibale (Schema here) to LLM
- We want output to look like this -> table_name orders: [order_id, item, etc]

- schema = ""  
tables = inspector.get_table_names()
for table in tables: 
    columns = inspector.get_columns(table)
    column_name = [column['name'] for column in columns] ### best way to get the output in list
    schema = schema + f"Table_Name: {table}: {', '.join(column_name)}\n"
print("Full schema string:\n", schema)

- ', '.join(column_name) → converts the list of columns into a comma-separated string
- \n → adds a line break so each table appears on its own line
- schema += ... → appends to the existing schema string (shorter than schema = schema + ...)

**Phase4: Send Schema + User Question to LLM (write instruction)- this is exactly like writing to chatgpt**

- **Writing to LLM means writing to CHATGPT-> better to give proper instruction**
- **Act like this, this is the input, this is the question and this is how i want output to be**
-  other roles could be: 
-  system → instructions
-  assistant → model response
-  user → user question

- STEP5 : USER QUESTION
-question = input("Ask a question: ")

PROMPT_TEMPLATE = """
Role: 
You are a data assistant that answers questions about a database.

Input Data: 
{schema}

Instructions:
1. Understand the user's question.
2. Write the SQL query to answer it.
3. Output the SQL query prefixed with 'SQL:'.

User Question: 
{question}
"""

#STEP6: Insert schema into prompt
**prompt = PROMPT_TEMPLATE.format(schema = schema, question = question)**
print(prompt) 

**Phase5: LLM needs to connect to the model (OPENAI/Claude) to write the query**
1. Pass the API key
2. GEnerate response form the LLM (define model name, temperature ..etc)
   
- to import openai --> uv add openai
- from openai import OpenAI  --> import model
- import os ## operating system so it can take your key saved in your project repo
- To import dotenv --> uv add dotenv  --> to get your key in .env file
- from dotenv import load_dotenv
- load_dotenv()

- client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) 
#this line creates a connection object (called client) that will communicate with openaiAPI means will take your input and get the output , client is like a waiter

- cat .env is a terminal command that displays the contents of your .env file.
-- this is to get the response
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    temperature=0
)

full_response = response.choices[0].message.content.strip()
print("\nFull LLM Response:")
print(full_response)

**Phase5: Pass your sql query to sqlite for getting the output**

import sqlite3
connect = sqlite3.connect("dummy_database.db")

# The cursor executes SQL commands
cursor = connect.cursor()
cursor.execute(sql_query)
results = cursor.fetchall()

print("\nQuery Results:")
print(results)

# STEP 3 – ask the model to format the results -----------------------------

### PAss the output to LLM to generate user natural language answer
## to add a variable use {}
##Use an f-string so Python inserts the variables.

final_prompt = f"""
Role: 
Act as a data assistant 

Sql_Query: 
{sql_query}

Query Result:
{results}

 Question: 
 {question}
 
Instructions: 
1. Answer the user's question in clear natural language using Sql_Query and results
"""

final_response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": final_prompt}],
    temperature=0
)

final_answer = final_response.choices[0].message.content.strip()
print(final_answer)


