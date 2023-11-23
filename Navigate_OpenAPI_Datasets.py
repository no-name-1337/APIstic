# boring imports
from pymongo import MongoClient
import pandas as pd
import os

from formaters.apisguru import load_apisguru_data
from formaters.bigquery import load_bigquery_data
from formaters.github import load_github_data
# helpers imports
from helpers.helpers import filter_dataframe, search_filter, version_filter, method_filter, create_slider
from formaters.swaggerhub import load_swaggerhub_data
from layouters.Dataset_Overview import load_dataset_overview, layout_dataset_overview
from layouters.layout_apisguru import layout_apisguru
from layouters.layout_bigquery import layout_bigquery
from layouters.layout_github import layout_github
from layouters.layout_swaggerhub import layout_swaggerhub

# the imports that produce the magic
import streamlit as st
from PIL import Image
# with open("./images/apistic.logo.svg", "r") as file:
#     svg = file.read()
# #     resize the logo
# svg = svg.replace('<svg', '<svg width="200" height="80"')
# st.markdown(svg, unsafe_allow_html=True)
im = Image.open("./images/openapi-1-_1_.ico")
st.set_page_config(layout="wide",
                   page_title='APIstic: OpenAPI Metrics Datasets',
                   page_icon=im,
                   initial_sidebar_state='auto')
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go

with st.sidebar:
    # Load your SVG
    st.subheader('Select Data Source')
    dbs = ['Dataset Overview', 'SwaggerHub', 'GitHub', 'BigQuery', 'APIs.guru']
    selected_db = None
    #     add link to the dataset overview
    button_overview = st.button('Dataset Overview', use_container_width=True)
    if button_overview:
        st.experimental_set_query_params(
            db='Dataset Overview'
        )
        selected_db = 'Dataset Overview'
    button_swaggerhub = st.button('SwaggerHub', use_container_width=True)
    if button_swaggerhub:
        st.experimental_set_query_params(
            db='SwaggerHub'
        )
        selected_db = 'SwaggerHub'
    button_github = st.button('GitHub', use_container_width=True)
    if button_github:
        st.experimental_set_query_params(
            db='GitHub'
        )
        selected_db = 'GitHub'
    button_bigquery = st.button('BigQuery', use_container_width=True)
    if button_bigquery:
        st.experimental_set_query_params(
            db='BigQuery'
        )
        selected_db = 'BigQuery'
    button_apisguru = st.button('APIs.guru', use_container_width=True)
    if button_apisguru:
        st.experimental_set_query_params(
            db='APIs.guru'
        )
        selected_db = 'APIs.guru'

# Connect to MongoDB (update with your connection details)
#  use environment variables to store the connection string
MONGO_URL = st.secrets["database"]['MONGO_URL']

client = MongoClient(MONGO_URL)
dbs = {
    'SwaggerHub': st.secrets["database"]['SWAGGER_DB'],
    'GitHub': st.secrets["database"]['GITHUB_DB'],
    'BigQuery': st.secrets["database"]['BIGQUERY_DB'],
    'APIs.guru': st.secrets["database"]['APISGURU_DB']
}
source = None

if st.experimental_get_query_params():
    if st.experimental_get_query_params().get('db'):
        st.experimental_set_query_params(
            db=st.experimental_get_query_params().get('db')
        )
        selected_db = st.experimental_get_query_params().get('db')[0]

if selected_db == 'SwaggerHub':
    st.experimental_set_query_params(
        db='SwaggerHub'
    )
    st.subheader('SwaggerHub Dataset')
    db = client[dbs['SwaggerHub']]
    collection = db['apis']
    # Load data from MongoDB
    df = load_swaggerhub_data(_collection=collection)
    layout_swaggerhub(df)

if selected_db == 'GitHub':
    db = client[dbs['GitHub']]
    st.experimental_set_query_params(
        db='GitHub'
    )
    st.subheader('GitHub Dataset')
    # Load data from MongoDB
    api_specs = db['api_specs']
    commits = db['commits']

    df = load_github_data(_api_specs=api_specs, _commits=commits)
    layout_github(df)

if selected_db == 'APIs.guru':
    st.experimental_set_query_params(
        db='APIs.guru'
    )
    db = client[dbs['APIs.guru']]
    st.subheader('APIs.guru Dataset')
    collection = db['apis']
    # Load data from MongoDB
    df = load_apisguru_data(_collection=collection)
    layout_apisguru(df)

if selected_db == 'BigQuery':
    st.experimental_set_query_params(
        db='BigQuery'
    )
    st.subheader('BigQuery Dataset')
    db = client[dbs['BigQuery']]
    collection = db['apis']
    # Load data from MongoDB
    df = load_bigquery_data(_collection=collection)
    layout_bigquery(df)
    # st.data_editor(df, height=700)

if selected_db is None or selected_db == 'Dataset Overview':
    st.experimental_set_query_params(
        db='Dataset Overview'
    )
    metrics = []
    paths_values = load_dataset_overview(dbs, client)
    layout_dataset_overview(paths_values)

