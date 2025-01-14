import streamlit as st
import pandas as pd
import sqlite3
st.title("Octopus Call Dashboard")
st.write(
    "Overview of key metrics"
)


db_path = r'/workspaces/Call_dashboard/data files/calls_case_study.db'  # Replace with the path to your .db file
connection = sqlite3.connect(db_path)

# Verify and check available tables first (you can skip this part once you know the table names)
cursor = connection.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

call_table_df = pd.read_sql_query("SELECT * FROM call", connection)
account_table_df = pd.read_sql_query("SELECT * FROM account", connection)
call_reason_df = pd.read_sql_query("SELECT * FROM call_reason", connection)


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