from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import psycopg2


# """
# # Welcome to Streamlit!
#
# Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:
#
# If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
# forums](https://discuss.streamlit.io).
#
# In the meantime, below is an example of what you can do with just a few lines of code:
# """


# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])


conn = init_connection()


# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        columns = [desc[0] for desc in cur.description]
        return cur.fetchall(), columns


rows, columns = run_query("SELECT * from users;")

with conn.cursor() as cur:
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
    tables = cur.fetchall()
tables = [t[0] for t in tables]

header = st.container()
bar = st.container()

with header:
    input = st.text_input('Password')
    if input == 'VladaLoveMcDonalds':
        table = st.selectbox('Choose table to display', options=tables)
        st.header(table)
        rows1, columns1 = run_query(f"SELECT * from {table};")
        df1 = pd.DataFrame(rows1, columns=columns1)
        st.write(df1)

companies = {
    # 0: 'Обычные пользователи',
    # 1: 'MH',
    2: 'Долгоруковский',
    3: 'Мичуринский',
    4: 'Севергрупп'
}

with bar:
    if input == 'VladaLoveMcDonalds':
        st.header('Clients')
        df = pd.DataFrame(rows, columns=columns)
        ar = df['company'].value_counts()
        c = {}
        for k in companies:
            # c[k] = int(ar[k]) if ar.get(k) is not None else 0
            c[companies[k]] = int(ar[k]) if ar.get(k) is not None else 0

        c = pd.DataFrame(c.values(), index=c.keys())
        st.write(c.T)

    # st.bar_chart(c, height=400)
    #####
    # st.bar_chart(c.T, height=400)
