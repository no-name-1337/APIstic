import streamlit as st


@st.cache_data
def filter_dataframe(_df, column_name, min_val, max_val):
    return _df[(_df[column_name] >= min_val) & (_df[column_name] <= max_val)]


@st.cache_data
def search_filter(_df, search_query):
    if search_query:
        return _df[_df['API Title'].str.contains(search_query) | _df['Description'].str.contains(search_query) | _df[
            'Endpoints Description'].str.contains(search_query)]
    return _df


@st.cache_data
def version_filter(_df, selected_versions):
    if selected_versions:
        return _df[_df['Openapi Version'].isin(selected_versions)]
    return _df


@st.cache_data
def method_filter(_df, selected_methods):
    if selected_methods:
        condition1 = _df[selected_methods].sum(axis=1) == _df['Used Methods']
        condition2 = _df[selected_methods].gt(0).all(axis=1)
        return _df[condition1 & condition2]
    return _df


def create_slider(column_name, _df):
    min_val, max_val = int(_df[column_name].min()), int(_df[column_name].max())
    if min_val == max_val:
        return None, None
    return st.slider(f'Select {column_name}', min_value=min_val, max_value=max_val,
                     value=[min_val, max_val], key=column_name)


@st.cache_data(experimental_allow_widgets=True)
def filters_block(_df):
    with st.expander("Dataset Navigation and Filtering", expanded=True):
        col3, col4, col5 = st.columns(3)
        with col3:
            search_query = st.text_input("Search by API title or description", key='search_query')
            filtered__df = search_filter(_df, search_query)

        with col4:
            unique_versions = [value for value in _df['Openapi Version'].unique() if value is not None]
            selected_versions = st.multiselect('Select Swagger/OpenAPI versions', unique_versions, key='versions')
            filtered__df = version_filter(filtered__df, selected_versions)

        with col5:
            unique_methods = filtered__df[
                ['Get', 'Post', 'Put', 'Delete', 'Patch', 'Head', 'Options', 'Trace']].sum().reset_index(name='count')
            selected_methods = st.multiselect('Select HTTP methods', unique_methods['index'], key='methods')
            filtered__df = method_filter(filtered__df, selected_methods)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            min_paths, max_paths = create_slider('Paths', _df)
        filtered__df = filter_dataframe(filtered__df, 'Paths', min_paths, max_paths)

        with col2:
            min_operations, max_operations = create_slider('Operations', filtered__df)
        filtered__df = filter_dataframe(filtered__df, 'Operations', min_operations, max_operations)
        with col3:
            min_schemas, max_schemas = create_slider('Schemas', filtered__df)
        filtered__df = filter_dataframe(filtered__df, 'Schemas', min_schemas, max_schemas)
        with col4:
            min_used_parameters, max_used_parameters = create_slider('Used Parameters', filtered__df)
            if min_used_parameters and max_used_parameters:
                filtered__df = filter_dataframe(filtered__df, 'Distinct Parameters', min_used_parameters,
                                                max_used_parameters)

        col1, col2 = st.columns(2)
        with col1:
            min_desc_coverage, max_desc_coverages = create_slider('Endpoints Description Coverage', filtered__df)
            if min_desc_coverage and max_desc_coverages:
                filtered__df = filter_dataframe(filtered__df, 'Endpoints Description Coverage', min_desc_coverage,
                                                max_desc_coverages)
        with col2:
            min_security_coverage, max_security_coverage = create_slider('Average Secured Paths', filtered__df)
            if min_security_coverage and max_security_coverage:
                filtered__df = filter_dataframe(filtered__df, 'Average Secured Paths', min_security_coverage,
                                                max_security_coverage)

        return filtered__df
