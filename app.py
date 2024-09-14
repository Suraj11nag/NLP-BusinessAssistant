import streamlit as st
import os
import sqlite3
import google.generativeai as genai
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

# Configure the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini model
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    # Clean up the SQL query
    cleaned_response = re.sub(r'```sql|```', '', response.text).strip()
    return cleaned_response

# Function to retrieve query from SQLite database
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    try:
        cur.execute(sql)
        rows = cur.fetchall()
    except sqlite3.OperationalError as e:
        return str(e)  # Return the error message
    finally:
        conn.close()
    
    return rows

# Define the prompt
prompt = [
    """
    You are an expert in converting English questions into SQL Queries to answer business-related questions by querying a SQLite database.
    You have access to the following tables: sales, products, customers, and orders.
    Answer user queries based on this data.
    IMPORTANT: Your response should ONLY include the SQL query, nothing else.
    """
]

# Streamlit App Layout
st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Gemini App To Retrieve SQL Data")

question = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

# if submit is clicked
if submit:
    response = get_gemini_response(question, prompt)
    st.subheader("Generated SQL Query")
    st.code(response, language='sql')  # Display the SQL query

    result = read_sql_query(response, "mydb.sqlite3")
    
    st.subheader("The Response is")
    if isinstance(result, str):  # If the result is an error message
        st.error(result)
    else:
        # Display data in a table format
        st.write(result)
