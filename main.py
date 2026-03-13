
import sqlite3
from sqlalchemy import create_engine, inspect

db_url = "sqlite:///amazon_new.db"
engine = create_engine(db_url)
inspector = inspect(engine)

tables = inspector.get_table_names()
print("Tables in the database:", tables)

schema_string = ""
for table in tables:
    schema_string += f"Table: {table}\nColumns: "
    columns = inspector.get_columns(table)
    column_list = [f"{col['name']} ({col['type']})" for col in columns]
    schema_string += ", ".join(column_list) + "\n\n"

print("\nFull Schema String:")
print(schema_string)

PROMPT_TEMPLATE = """
You are a data assistant that answers questions about a database.

Database Schema:
{schema}

Instructions:
1. Understand the user's question.
2. Write the SQL query to answer it.
3. Provide output only in SQL Query

User Question:
{question}
"""

# STEP5 : USER QUESTION
question = input("Ask a question: ")

#STEP6: Insert schema into prompt
prompt = PROMPT_TEMPLATE.format(schema = schema_string, question = question)

##STEP7: Connect to OPENAI

# STEP 7: connect to OpenAI
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

##dotenv is to get your API key

client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))
#or
#client = OpenAI(api_key="sk-xxxxx")

#this line creates a connection object (called client) that will communicate with openaiAPI
##OPENAI() : creates a API client think of this as connection to openai
##means sending a request to model 
# + reads the environment variable from system 

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    temperature=0
)

full_response = response.choices[0].message.content.strip()
print("\nFull LLM Response:")
print(full_response)

if full_response.startswith("SQL:"):
    sql_query = full_response[4:].strip()
else:
    raise ValueError("LLM did not provide SQL in expected format.")

print("\nGenerated SQL:")
print(sql_query)




# STEP 2 – run the query ---------------------------------------------------
conn = sqlite3.connect("amazon_new.db")
cursor = conn.cursor()
try:
    cursor.execute(sql_query)
    results = cursor.fetchall()
    print("\nQuery Results:")
    print(results)
except sqlite3.Error as e:
    print(f"SQL Error: {e}")
    results = []
conn.close()

# STEP 3 – ask the model to format the results -----------------------------
results_text = str(results)
final_prompt = f"""
Based on the SQL query: {sql_query}
And the results: {results_text}
Answer the user's question in clear natural language: {question}
"""

final_response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": final_prompt}],
    temperature=0
)

final_answer = final_response.choices[0].message.content.strip()
print("\nFinal Answer:")
print(final_answer)

##get streamlit -> uv add streamlit 
st.title("Intelligent Database Query Assistant")
st.write("Ask questions about the database in natural language.")


question = st.text_input("Enter your question")
if st.button("Generate Answer"):
    
import streamlit as st
import sqlite3
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


import streamlit as st
st.title("Intelligent Database Query Assistant")

question = st.text_input("Ask a question about the database")

if st.button("Get Answer"):

    # Example schema (use your schema generation code here)
    schema = """
    customers(customer_id, name, email, city, join_date)
    products(product_id, name, category, price)
    orders(order_id, customer_id, order_date, total_amount)
    """

    prompt = f"""
You are an expert SQL generator.

Return ONLY SQL.

Database Schema:
{schema}

Question:
{question}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        temperature=0
    )

    sql_query = response.choices[0].message.content.strip()

    st.subheader("Generated SQL")
    st.code(sql_query)

    # Run SQL on SQLite
    conn = sqlite3.connect("dummy_database.db")
    cursor = conn.cursor()

    cursor.execute(sql_query)
    results = cursor.fetchall()

    st.subheader("Query Results")
    st.write(results)

    conn.close()

