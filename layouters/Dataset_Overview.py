import streamlit as st
import plotly.graph_objs as go
import numpy as np
import math
import pandas as pd
import os


@st.cache_data
def load_dataset_overview(_dbs, _client):
    st.subheader('Dataset Overview')
    # from each dataset get structureSize,
    projections = {
        # 'securityData': 1,
        'structureSize.paths': 1,
        'structureSize.operations': 1,
        'schemaSize.schemas': 1,
        # 'documentationsData': 1,
    }

    apisguru_db = _client[_dbs['APIs.guru']]
    apisguru_collection = apisguru_db[st.secrets["database"]['APISGURU_APIS_COLLECTION']]
    apisguru_data = apisguru_collection.find({}, projections)
    apisguru_data_df = pd.DataFrame(list(apisguru_data))
    print(len(apisguru_data_df))

    github_db = _client[_dbs['GitHub']]
    github_collection = github_db[st.secrets["database"]['GITHUB_COMMIT_COLLECTION']]
    github_data = github_collection.find({}, projections)
    github_data_df = pd.DataFrame(list(github_data))
    print(len(github_data_df))

    swaggerhub_db = _client[_dbs['SwaggerHub']]
    swaggerhub_collection = swaggerhub_db[st.secrets["database"]['SWAGGER_APIS_COLLECTION']]
    swaggerhub_data = swaggerhub_collection.find({'structureSize': {'$exists': True}}, projections)
    swaggerhub_data_df = pd.DataFrame(list(swaggerhub_data))
    print(len(swaggerhub_data_df))

    bigquery_db = _client[_dbs['BigQuery']]
    bigquery_collection = bigquery_db[st.secrets["database"]['BIGQUERY_APIS_COLLECTION']]
    bigquery_data = bigquery_collection.find({}, projections)
    bigquery_data_df = pd.DataFrame(list(bigquery_data))
    return {

        'GitHub':
            {
                'paths': github_data_df['structureSize'].apply(
                    lambda x: x['paths'] if isinstance(x, dict) and 'paths' in x else None).tolist(),
                'operations': github_data_df['structureSize'].apply(
                    lambda x: x['operations'] if isinstance(x, dict) and 'operations' in x else None).tolist(),
                'schemas': github_data_df['schemaSize'].apply(
                    lambda x: x['schemas'] if isinstance(x, dict) and 'schemas' in x else None).tolist(),

            },

        'SwaggerHub':
            {
                'paths': swaggerhub_data_df['structureSize'].apply(
                    lambda x: x['paths'] if isinstance(x, dict) and 'paths' in x else None).tolist(),
                'operations': swaggerhub_data_df['structureSize'].apply(
                    lambda x: x['operations'] if isinstance(x, dict) and 'operations' in x else None).tolist(),
                'schemas': swaggerhub_data_df['schemaSize'].apply(
                    lambda x: x['schemas'] if isinstance(x, dict) and 'schemas' in x else None).tolist(),

            },
        'BigQuery':
            {
                'paths': bigquery_data_df['structureSize'].apply(
                    lambda x: x['paths'] if isinstance(x, dict) and 'paths' in x else None).tolist(),
                'operations': bigquery_data_df['structureSize'].apply(
                    lambda x: x['operations'] if isinstance(x, dict) and 'operations' in x else None).tolist(),
                'schemas': bigquery_data_df['schemaSize'].apply(
                    lambda x: x['schemas'] if isinstance(x, dict) and 'schemas' in x else None).tolist(),

            }
        ,
        'APIs.guru':
            {
                'paths':
                    apisguru_data_df['structureSize'].apply(
                        lambda x: x['paths'] if isinstance(x, dict) and 'paths' in x else None).tolist(),
                'operations':
                    apisguru_data_df['structureSize'].apply(
                        lambda x: x['operations'] if isinstance(x, dict) and 'operations' in x else None).tolist(),
                'schemas':
                    apisguru_data_df['schemaSize'].apply(
                        lambda x: x['schemas'] if isinstance(x, dict) and 'schemas' in x else None).tolist(),
            }

    }



@st.cache_data
def layout_dataset_overview(paths_values):
    st.write("""
            **This dataset contains a collection of OpenAPI specifications gathered from various sources. 
            The dataset is updated on a weekly basis and is available in a downloadable .csv format.**
            """)
    st.write("""
             We collected up to today more than half a million OpenAPI specifications from different sources.
                Here are some statistics about the dataset:
            """)


    # get the total number of APIs
    total_apis = len(paths_values['GitHub']['paths']) + len(paths_values['SwaggerHub']['paths']) + len(
        paths_values['BigQuery']['paths']) + len(
        paths_values['APIs.guru']['paths'])

    github_total_apis = len(paths_values['GitHub']['paths'])
    swaggerhub_total_apis = len(paths_values['SwaggerHub']['paths'])
    bigquery_total_apis = len(paths_values['BigQuery']['paths'])
    apisguru_total_apis = len(paths_values['APIs.guru']['paths'])

    github_total_apis_paths = sum(
        value for value in paths_values['GitHub']['paths'] if value is not None and not math.isnan(value))
    swaggerhub_total_apis_paths = sum(
        value for value in paths_values['SwaggerHub']['paths'] if value is not None and not math.isnan(value))
    bigquery_total_apis_paths = sum(
        value for value in paths_values['BigQuery']['paths'] if value is not None and not math.isnan(value))
    apisguru_total_apis_paths = sum(
        value for value in paths_values['APIs.guru']['paths'] if value is not None and not math.isnan(value))
    total_apis_paths = github_total_apis_paths + swaggerhub_total_apis_paths + bigquery_total_apis_paths + apisguru_total_apis_paths

    github_total_apis_operations = sum(
        value for value in paths_values['GitHub']['operations'] if value is not None and not math.isnan(value))
    swaggerhub_total_apis_operations = sum(
        value for value in paths_values['SwaggerHub']['operations'] if value is not None and not math.isnan(value))
    bigquery_total_apis_operations = sum(
        value for value in paths_values['BigQuery']['operations'] if value is not None and not math.isnan(value))
    apisguru_total_apis_operations = sum(
        value for value in paths_values['APIs.guru']['operations'] if value is not None and not math.isnan(value))
    total_apis_operations = github_total_apis_operations + swaggerhub_total_apis_operations + bigquery_total_apis_operations + apisguru_total_apis_operations

    github_total_apis_schemas = sum(
        value for value in paths_values['GitHub']['schemas'] if value is not None and not math.isnan(value))
    swaggerhub_total_apis_schemas = sum(
        value for value in paths_values['SwaggerHub']['schemas'] if value is not None and not math.isnan(value))
    bigquery_total_apis_schemas = sum(
        value for value in paths_values['BigQuery']['schemas'] if value is not None and not math.isnan(value))
    apisguru_total_apis_schemas = sum(
        value for value in paths_values['APIs.guru']['schemas'] if value is not None and not math.isnan(value))
    total_apis_schemas = github_total_apis_schemas + swaggerhub_total_apis_schemas + bigquery_total_apis_schemas + apisguru_total_apis_schemas

    data = {
        "Source": ["GitHub", "SwaggerHub", "BigQuery", "APIs.guru", "Total"],
        "Total APIs": [github_total_apis, swaggerhub_total_apis, bigquery_total_apis, apisguru_total_apis, total_apis],
        "Total Paths": [github_total_apis_paths, swaggerhub_total_apis_paths, bigquery_total_apis_paths,
                        apisguru_total_apis_paths, total_apis_paths],
        "Total Operations": [github_total_apis_operations, swaggerhub_total_apis_operations,
                             bigquery_total_apis_operations,
                             apisguru_total_apis_operations, total_apis_operations],
        "Total Schemas": [github_total_apis_schemas, swaggerhub_total_apis_schemas, bigquery_total_apis_schemas,
                          apisguru_total_apis_schemas, total_apis_schemas]
    }

    df = pd.DataFrame(data)
    st.data_editor(df, width=1000)


    with st.expander("Metrics Definition", expanded=True):
        st.markdown("""
    #### API Structure Metrics 
    These metrics evaluate the size and complexity of the operational features of the API, providing insights into its functional scope and diversity.

    - **Paths**: The number of paths in the API. This metric indicates the breadth of the API's functionality, with each path representing the address of a different communication endpoint, resource, or service provided by the API.
    - **Operations**: The total count of operations available in the API. This reflects the API's operational capabilities, encompassing all possible actions that can be performed through it.
    - **Used Methods**: The number of distinct HTTP methods (GET, POST, PUT, DELETE, etc) used across the API operations. It signifies the diversity in the API's interaction modes.
    - **Parametric Operations**: The number of operations that use path or query parameters. This metric helps in understanding the complexity and customization potential of the API operations.
    - **Distinct Parameters**: The count of unique parameter names used across the API. It representing the variety of parameters that the API can accept, reflecting its versatility.
    - **Used Parameters**: The total number of times parameters are used in the API. This indicates how frequently the API relies on parameterization for its operations.

    #### API Data Model Metrics
    This set of metrics delves into the structure and usage of data models within the API, highlighting the size and complexity of its data representation.

    - **Defined Schemas**: The number of schemas defined in the API description, gauging the size of the API data model.
    - **Distinct Schemas**: The total number of distinct schemas mentioned in API request or response messages, reflecting the practical application of the API data models.
    - **Properties**: The total count of properties within schemas, representing the granularity and detail of the data models used.
    - **Used Properties**: The number of properties explicitly used in API request or response messages, indicating the usability extent of the API data model.
    - **Distinct Properties**: The count of unique property names, indicating the diversity of data attributes the API handles.

    #### API Natural Language Descriptions Metrics
    These metrics focus on the quality and thoroughness of the API's natural language documentation, augmenting its machine-readable, structured description.

    - **Endpoints Description Coverage**: A percentage value indicating the proportion of API endpoints with a non-empty description, measuring the completeness of endpoint documentation.
    - **Coleman-Liau Index**: A readability index based on characters per word and sentences per 100 words, gauging text understandability.
    - **Automated Readability Index**: An index estimating text understandability based on character, word, and sentence counts.

    #### Versioning
    These metrics categorize the versioning strategy adopted by the API developers.

    - **Version Identifier Format**: Categorizes the API version information in the info section or API endpoints, identifying the use of semantic, time-based, numeric, or other versioning schemes.
    - **Versioning Placement**: Categorizes the placement of versioning information within the API description, such as Metadata-based, URL-based, or Header-based.
    - **Release Type**: Categorizes the type of release (stable or preview) described by the API artifact.

    #### API Security Metrics
    This section assesses the security protocols and strategies implemented in the API.

    - **Security Schemes**: The number of each type of security scheme listed in the API security component.
    - **Secured Endpoints**: The number of API endpoints employing specific security schemes.
    """)

    # draw violins that shows the distribution of the structureSize.paths

    # Create a list to hold the violin plot objects

    @st.cache_data
    def create_violin(metric):
        violin_plots = []

        # Iterate over each category and create a violin plot for each
        for category in paths_values.keys():
            violin_plot = go.Violin(
                y=[value for value in paths_values[category][metric] if value is not None],  # Filter out None values
                name=category,  # Name of the category
                box_visible=True,  # Show the inner box plot
                meanline_visible=True  # Show the mean line
            )
            violin_plots.append(violin_plot)

        # Create the figure with the violin plots
        fig = go.Figure(data=violin_plots)

        # Update layout if needed, e.g., title, axis labels
        fig.update_layout(
            title=f'Violin Plots of {metric} in Each Dataset',
            yaxis_title=f'Number of {metric}',
            xaxis_title='Dataset'
        )

        return fig

    # 2 columns
    with st.spinner('Loading Violin Plots...'):
        col1, col2 = st.columns(2)
        with col1:
            fig_paths = create_violin('paths')
            st.plotly_chart(fig_paths, use_container_width=True, height=600)
        with col2:
            fig_operations = create_violin('operations')
            st.plotly_chart(fig_operations, use_container_width=True, height=600)

        fig_schemas = create_violin('schemas')
        st.plotly_chart(fig_schemas, use_container_width=True, height=400)
