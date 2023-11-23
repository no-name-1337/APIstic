import streamlit as st
#  use wide mode for the page
st.set_page_config(layout="wide")
def about_page():
    st.title('About This App')
    col1, col2 = st.columns(2)
    with col1:
        st.write("""
        ## What is APIstic About?
        This application serves as a comprehensive resource for exploring a wide range of OpenAPI specifications. 
        Mined from various sources, our dataset offers users the ability to delve into diverse API specifications. 
        Whether you're a developer, researcher, or API enthusiast, this tool will help you filter and discover 
        API specifications based on a variety of metrics and search inputs.
        """)

    with col2:
        st.write("""
        ## Background and Purpose
        The motivation behind this application is to simplify the discovery and analysis of OpenAPI specifications. 
        By aggregating data from various sources into a single, searchable platform, we aim to facilitate better 
        understanding and utilization of APIs in the development community.
        """)

    col1, col2 = st.columns(2)
    with col1:
        st.write("""
        ## Key Features
        - **Rich Dataset**: Access a diverse collection of OpenAPI specifications gathered from multiple sources.
        - **Advanced Filtering**: Utilize various metrics to filter the dataset and find exactly what you need.
        - **Search Functionality**: Easily navigate through the dataset with user-friendly search features.
        - **Downloadable Dataset**: Download the dataset in a .csv format to your local machine.
        """)

    with col2:
        st.write("""
        ## How to Use
    To make the most out of this interface:
    1. Use the search bars, the check boxes and the sliders to input your query or keyword.
    2. Filter the results using the available metrics to narrow down your search.
    3. Browse through the results or download the dataset in a .csv to your local machine.
    """)


    st.write("""
    ## Feedback and Contributions
    Your feedback is valuable in helping us improve this dataset. If you have suggestions, encounter any issues, 
    or wish to contribute to the dataset, please reach out to us.

    ## Contact Information
    For further inquiries, feedback, or support, feel free to contact us at [hidden for review].

    ## Acknowledgments
    Special thanks to all the contributors and sources that have made this dataset possible.
    """)

if __name__ == "__main__":
    about_page()

