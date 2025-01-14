import streamlit as st
import pandas as pd
import sqlite3
st.title("Octopus Call Dashboard")
st.write(
    "Overview of key metrics"
)


# Path to SQLite database file
case_study_db_file = r'C:\Users\Owner\Downloads\calls_case_study.db'

# Connect to the database
connection = sqlite3.connect(case_study_db_file)

# Create a cursor object to execute SQL queries
cursor = connection.cursor()

# Example: Get a list of all tables in the database
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables in the database:", tables)

# Close the connection when done
connection.close()

# Reconnect to the database
connection = sqlite3.connect(case_study_db_file)

# Read data from tables
account_table = "SELECT * FROM account"
account_table_df = pd.read_sql_query(account_table, connection)

calls_and_reasons = """SELECT * FROM call c
LEFT JOIN call_reason cr ON c.reason_id = cr.id"""
calls_and_reasons_df = pd.read_sql_query(call_table, connection)

# Close the connection when done
connection.close()

calls_and_reasons_df['account_id'] = calls_and_reasons_df['account_id'].astype(int)
all_data = pd.merge(calls_and_reasons_df
                    , account_table_df
                    , left_on='account_id'
                    , right_on='id'
                    , how='left')