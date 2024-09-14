import streamlit as st
import os
import sqlite3
import google.generativeai as genai
from dotenv import load_dotenv
import re
import pandas as pd

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
        columns = [description[0] for description in cur.description]  # Get column names
    except sqlite3.OperationalError as e:
        return str(e), None  # Return error message and None for rows
    finally:
        conn.close()
    
    return columns, rows

# Define the prompt
prompt = [
    """
    You are an expert in converting English questions into SQL Queries to answer business-related questions by querying a PostgreSQL database.
    You have access to the following tables: sales, products, customers, and orders.
    Answer user queries based on this data.
    Try to get the basic idea when a query is asked and try things to get the desired results.
    Only return the SQL query, without any additional explanation.
    You are working with a database schema that includes four tables: **sales**, **products**, **customers**, and **orders**.
    The **sales** table contains information about each sale. It includes the **id** column, which is an auto-incremented integer serving as the primary key for each sale. The **product_name** column stores the name of the product sold. The **quantity** column indicates the number of units sold, while the **sale_date** column records the date of the sale. Finally, the **total_amount** column represents the total amount of the sale in real currency values.
    The **products** table holds data on products available for sale. The **id** column is an auto-incremented integer and serves as the primary key for each product. The **name** column provides the name of the product, and the **category** column denotes the category to which the product belongs. The **price** column contains the price of the product in real currency values.
    In the **customers** table, the **id** column is an auto-incremented integer that uniquely identifies each customer as the primary key. The **name** column records the name of the customer, while the **email** column captures the customer's email address. The **join_date** column indicates the date when the customer joined.
    Lastly, the **orders** table records each order placed by customers. The **id** column is an auto-incremented integer and serves as the primary key for each order. The **customer_id** column is a foreign key that references the **id** column in the **customers** table, linking the order to a specific customer. The **product_id** column is a foreign key that references the **id** column in the **products** table, associating the order with a specific product. The **order_date** column logs the date of the order, and the **order_amount** column represents the total amount of the order in real currency values.
    Use this schema to generate SQL queries that retrieve relevant data from these tables based on user queries.

    """
]

# Streamlit App Layout
st.title("Natural Language to SQL Query Generator")
st.write("Ask any business-related questions based on the available sales, products, customers, and orders data.")

question = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

# if submit is clicked
if submit:
    response = get_gemini_response(question, prompt)
    st.subheader("Generated SQL Query")
    st.code(response, language='sql')  # Display the SQL query

    columns, result = read_sql_query(response, "mydb.sqlite3")

    st.subheader("Query Results:")
    if isinstance(columns, str):  # If the result is an error message
        st.error(f"Error executing query: {columns}")
    elif result:
        df = pd.DataFrame(result, columns=columns)
        st.write(df)  # Display results as a table
    else:
        st.write("No results found.")
