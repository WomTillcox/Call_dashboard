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
call_reason_table = "SELECT * FROM call_reason"
call_reason_df = pd.read_sql_query(call_reason_table, connection)

account_table = "SELECT * FROM account"
account_table_df = pd.read_sql_query(account_table, connection)

call_table = "SELECT * FROM call"
call_table_df = pd.read_sql_query(call_table, connection)

# Close the connection when done
connection.close()

call_reason_df.rename(columns={'id':'reason_id'}, inplace=True)
account_table_df.rename(columns={'id':'account_id'}, inplace=True)

call_table_df['reason_id'] = pd.to_numeric(call_table_df['reason_id'], errors='coerce')  # Coerce invalid values to NaN
call_table_df['reason_id'] = call_table_df['reason_id'].astype('Int64')

calls_and_reasons_df = pd.merge(call_table_df
                                , call_reason_df
                                , how='left'
                                , on='reason_id')
calls_and_reasons_df['account_id'] = calls_and_reasons_df['account_id'].astype(int)
all_data = pd.merge(calls_and_reasons_df
                    , account_table_df
                    , on='account_id'
                    , how='left')
all_data['called_at'] = pd.to_datetime(all_data['called_at'])
current_date = all_data['called_at'].max().date()