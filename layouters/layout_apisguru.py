import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
from helpers.helpers import filter_dataframe, search_filter, version_filter, method_filter, create_slider, filters_block


def layout_apisguru(df):
    with st.sidebar:
        st.subheader('Plot metric distribution over years')
        st.write('API Structure Metrics')
        metrics = ['Paths', 'Operations', 'Used Methods', 'Parametered Operations', 'Distinct Parameters',
                   'Used Parameters']
        checkbox_states = {metric: False for metric in metrics}

        # Update states based on user input
        for metric in metrics:
            if len([m for m, selected in checkbox_states.items() if selected]) < 2 or checkbox_states[metric]:
                checkbox_states[metric] = st.checkbox(metric, value=checkbox_states[metric])

        # Filter the selected metrics
        selected_structure_metric = [metric for metric, selected in checkbox_states.items() if selected]

        st.write('API Data Model Metrics')
        metrics = ['Schemas', 'Properties', 'Used Properties', 'Distinct Properties', 'Used Schemas',
                   'Distinct Schemas']
        selected_data_model_metric = [metric for metric, selected in
                                      zip(metrics, [st.checkbox(metric) for metric in metrics]) if
                                      selected]

    st.subheader('Dataset Overview')

    # Metric names
    headers = [
        "Total number of APIs",
        "Total number of API owners",
        "Total number of API versions",
        "Average number of APIs per owner",
        "Total Number Of Paths",
        "Total Number Of Operations",
        "Total Number Of Unique Schemas"
    ]

    # Corresponding values (replace with actual calculations)
    values = [
        len(df),  # replace with actual value
        len(df["Created By"].unique()),  # replace with actual value
        len(df["Openapi Version"].unique()),  # replace with actual value
        round(len(df) / len(df["Created By"].unique()), 2),  # replace with actual value
        df["Paths"].sum(),  # replace with actual value
        df["Operations"].sum(),  # replace with actual value
        df["Schemas"].sum()  # replace with actual value
    ]

    # Create a DataFrame
    metrics_df = pd.DataFrame([values], columns=headers)

    with st.expander("Data Overview", expanded=True):
        # Display the DataFrame
        st.dataframe(metrics_df)

    st.subheader(f'Dataset Navigation and Filtering')

    filtered_df = filters_block(df)
    st.subheader(f'List of API Specifications')
    st.data_editor(data=filtered_df, height=700)
    st.markdown(f'Found: {len(filtered_df)} APIs matching the criteria')


    # for metric in selected_structure_metric:
    #     col1, col2, col3 = st.columns(3)
    #     with col1:
    #         st.subheader(f'Boxplot of {metric} over Years')
    #         fig_box = px.box(df, x='Openapi Version', y=metric)
    #         st.plotly_chart(fig_box, use_container_width=True)
    #     with col2:
    #         st.subheader(f'Distribution of {metric} over Years')
    #         fig_bar = px.bar(df, x='Openapi Version', y=metric, barmode='group')
    #         st.plotly_chart(fig_bar, use_container_width=True)
    #     # list of 10 apis with the highest number of metric
    #     with col3:
    #         if metric == 'parameterised_operations':
    #             st.subheader(f'Boxplot of number of used parameters in API endpoints over Years')
    #             # add normal text to explain the metric
    #             fig_box = px.box(df, x='Created At Year', y='Used Parameters')
    #             st.plotly_chart(fig_box, use_container_width=True)
    #         else:
    #             st.subheader(f'Top 10 APIs with highest number of {metric}')
    #             st.dataframe(df.nlargest(10, metric))