import streamlit as st
import pandas as pd
import sqlite3

def main():
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

    # Ensure `called_at` is in datetime format
    all_data['call_date'] = pd.to_datetime(all_data['called_at'])

    # Current date derived from the data
    current_date = all_data['call_date'].max()

    # Sidebar for filters
    st.sidebar.title("Filters")
    time_filter = st.sidebar.selectbox(
        "Select Time Period",
        options=["Current Day", "Last Week", "Last Month"],
        index=0
    )
    top_bottom_filter = st.sidebar.radio(
        "Select Display Mode",
        options=["Top 10", "Bottom 10"],
        index=0
    )

    # Filter data based on the selected time period
    if time_filter == "Current Day":
        filtered_data = all_data[all_data['call_date'].dt.date == current_date.date()]
    elif time_filter == "Last Week":
        filtered_data = all_data[
            (all_data['call_date'] >= current_date - pd.Timedelta(days=7))
            & (all_data['call_date'] <= current_date)
        ]
    elif time_filter == "Last Month":
        filtered_data = all_data[
            (all_data['call_date'] >= current_date - pd.Timedelta(days=30))
            & (all_data['call_date'] <= current_date)
        ]

    # Calculate average talk time per agent_id
    average_talk_time = (
        filtered_data.groupby('agent_id')['talk_time']
        .mean()
        .reset_index()
        .rename(columns={'talk_time': 'average_talk_time'})
    )

    # Sort data based on top or bottom 10
    if top_bottom_filter == "Top 10":
        average_talk_time = average_talk_time.sort_values(by='average_talk_time', ascending=False)
    else:
        average_talk_time = average_talk_time.sort_values(by='average_talk_time', ascending=True)

    # Limit to 10 rows
    average_talk_time = average_talk_time.head(10)

    # Title and subtitle
    st.title("Agent Performance Dashboard")
    st.subheader("Analyze agent talk times")

    # Display table
    st.write("Average Talk Time by Agent")
    st.table(average_talk_time)


if __name__ == "__main__":
    main()