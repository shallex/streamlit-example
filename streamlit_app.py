from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import psycopg2


"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""


# with st.echo(code_location='below'):
#     total_points = st.slider("Number of points in spiral", 1, 5000, 2000)
#     num_turns = st.slider("Number of turns in spiral", 1, 100, 9)
#
#     Point = namedtuple('Point', 'x y')
#     data = []
#
#     points_per_turn = total_points / num_turns
#
#     for curr_point_num in range(total_points):
#         curr_turn, i = divmod(curr_point_num, points_per_turn)
#         angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn
#         radius = curr_point_num / total_points
#         x = radius * math.cos(angle)
#         y = radius * math.sin(angle)
#         data.append(Point(x, y))
#
#     st.altair_chart(alt.Chart(pd.DataFrame(data), height=500, width=500)
#         .mark_circle(color='#0068c9', opacity=0.5)
#         .encode(x='x:Q', y='y:Q'))


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


header = st.container()
bar = st.container()

# with header:
#   st.header('Users')
#   st.write(pd.DataFrame(rows))


companies = {
                # 0: 'Обычные пользователи',
                # 1: 'MH',
                2: 'Долгоруковский',
                3: 'Мичуринский',
                4: 'Севергрупп'
}

with bar:
    st.header('bar')
    df = pd.DataFrame(rows, columns=columns)
    ar = df['company'].value_counts()
    c = {}
    for k in companies:
        c[companies[k]] = int(ar[k]) if ar.get(k) is not None else 0

    c = pd.DataFrame(c.values(), index=c.keys())
    st.bar_chart(c, height=400)

