import streamlit as st
import sqlite3
from sqlalchemy import create_engine, inspect
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("Intelligent Database Query Assistant")

# STEP 1 & 2: Connect to DB and fetch schema
db_url = "sqlite:///dummy_database.db"
engine = create_engine(db_url)
inspector = inspect(engine)

schema = ""
tables = inspector.get_table_names()
for table in tables:
    columns = inspector.get_columns(table)
    column_name = [column['name'] for column in columns]
    schema += f"Table_Name: {table}: {', '.join(column_name)}\n"

st.subheader("Database Schema (For reference)")
st.text(schema)

# STEP 5: User question
question = st.text_input("Enter your question:")

if st.button("Generate Answer") and question.strip() != "":
    
    # STEP 6: Create prompt for SQL generation
    PROMPT_TEMPLATE = """
Role: You are a data assistant that answers questions about a database.

Input: {schema}

Instructions:
1. Understand the user's question.
2. Write the SQL query to answer it.
3. No explanation. Only SQL Query
4. Do NOT include explanations.
5. Do NOT include markdown formatting.

Question: {question}
"""
    prompt = PROMPT_TEMPLATE.format(schema=schema, question=question)
    
    # STEP 6.1: Get SQL query from LLM
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    sql_query = response.choices[0].message.content.strip()
    st.subheader("Generated SQL Query")
    st.code(sql_query)

    # STEP 6.2: Execute SQL
    connect = sqlite3.connect("dummy_database.db")
    cursor = connect.cursor()
    try:
        cursor.execute(sql_query)
        results = cursor.fetchall()
    except Exception as e:
        results = []
        st.error(f"SQL Execution Error: {e}")



    # STEP 7: Send results + SQL + question to LLM to get natural language answer
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
    
    st.subheader("Answer")
    st.write(final_answer)
    
    
    
    