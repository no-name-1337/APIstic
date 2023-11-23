import streamlit as st
from pathlib import Path
from openapi_spec_validator import validate
import json
from pymongo import MongoClient
import datetime
import re
import time
import pandas as pd

client = MongoClient('mongodb://localhost:27017/')
db = client['APIstic']
collection = db['apis']

github_db = client['github']
github_collection = github_db['commits']

swaggerhub_db = client['swagger']
swaggerhub_collection = swaggerhub_db['apis']

# apis_guru_db = client['apis_guru']
# apis_guru_collection = apis_guru_db['apis']




st.set_page_config(layout="wide")
def main():
    st.title('APIstic')
    st.subheader("OpenAPI Specification Uploader")
    st.markdown("A specification can be uploaded only if it is valid.")
    st.markdown("If this is a new version of a previously uploaded, please use the same identifier.")
    # Allow user to upload OpenAPI specification file
    uploaded_file = st.file_uploader("Upload OpenAPI specification file", type=["json"])
    
    if uploaded_file is not None:
        # Save uploaded file to disk
        json = display_file_content(uploaded_file)

        json = validate_file(json)
        
        # Allow user to add metadata about the OpenAPI specification
        metadata = get_metadata(json)
        
        # Save metadata to file
        # save_metadata(file_path, metadata)
        
        # st.success("OpenAPI specification imported successfully!")
    
def display_file_content(uploaded_file):
    # Display the uploaded file content 
    # (for debugging purposes)
    json_data = json.load(uploaded_file)
    file_details = {"FileName":uploaded_file.name,"FileType":uploaded_file.type,"FileSize":uploaded_file.size, "FileContent":json_data}
    st.write(file_details)

    return json_data
    # st.write(type(uploaded_file))

def validate_file(uploaded_file):
    # validate the uploaded file
    try:
        # parse string to json
        validate(uploaded_file)
    except Exception as e:
        print(e)
        st.error(e)
        st.stop()
    st.success("The file is valid")
    # return api title from info.title and api version from info.version and api description from info.description
    return { "meta": {
        "title": uploaded_file["info"]["title"],
        "version": uploaded_file["info"]["version"],
        "description": uploaded_file["info"]["description"]
    }, "content": uploaded_file
    }
    # Save uploaded file to disk

def verify_input(input_data):
    # Check for spaces
    if " " in input_data:
        return "Identifier cannot contain spaces."
    # Check for special characters
    if re.search("[^a-zA-Z0-9]", input_data):
        return "Input  cannot contain special characters."
    return True


def get_metadata(data):
    # Allow user to add metadata about the OpenAPI specification
    metadata = {}
    # add and identifier
    col1, col2 = st.columns(2)
    with col1:
        identifier = st.text_input("Identifier")
        if not verify_input(identifier)==True:
            st.error(verify_input(identifier))      
    with col2:
        metadata["name"] = st.text_input("Name", value=data["meta"]["title"])
    metadata["description"] = st.text_area("Description", value=data["meta"]["description"])
    metadata["version"] = st.text_input("Version", value=data["meta"]["version"])
    metadata["author"] = st.text_input("Author")

    if st.button("Submit") and identifier.isalnum():
        #  check if identifier already in the database
        identifier_in_db = db.metadata.find_one({"identifier": identifier})
        if identifier_in_db:
            st.error("Identifier already in use. Please use a different identifier.")
            st.stop()
        
        # Save metadata to database
        db.collection.insert_one({
            "identifier": identifier,
            "name": metadata["name"],
            "description": metadata["description"],
            "version": metadata["version"],
            "author": metadata["author"],
            "api": data["content"],
            "created_at": datetime.datetime.now()
        })
        st.success("OpenAPI specification uploaded successfully!")
        

        # find apis with similar content
        similar_apis = db.collection.find({"api": data["content"]})
        similar_apis_github = db.github_collection.find({"api": data["content"]})
        similar_apis_swaggerhub = db.swaggerhub_collection.find({"_API_spec": data["content"]})
        # similar_apis_apis_guru = db.apis_guru_collection.find({"api": data["content"]})

        # if there are similar apis, show them to the user
       
        similar_apis_df = pd.DataFrame(similar_apis)
        if not similar_apis_df.empty:
            st.subheader(f'We found {similar_apis_df._id.count()} similar APIs in our database')
            similar_apis_df.drop(['api'], axis=1, inplace=True)
            st.dataframe(similar_apis_df)

        similar_github_apis_df = pd.DataFrame(similar_apis_github)
        if not similar_github_apis_df.empty:
            st.subheader(f'We found {similar_apis_df.count()} similar APIs in Github')
            similar_github_apis_df.drop(['api'], axis=1, inplace=True)
            st.dataframe(similar_github_apis_df)
     
        
        similar_swaggerhub_apis_df = pd.DataFrame(similar_apis_swaggerhub)
        if not similar_swaggerhub_apis_df.empty:
            st.subheader(f'We found {similar_swaggerhub_apis_df.count()} similar APIs in SwaggerHub')
            similar_swaggerhub_apis_df.drop(['_API_spec'], axis=1, inplace=True)
            st.dataframe(similar_swaggerhub_apis_df)

        
        if similar_apis_df.empty and similar_github_apis_df.empty and similar_swaggerhub_apis_df.empty:
            st.subheader(f'We did not find any similar APIs')
            time.sleep(4)
            st.rerun()


    
    return metadata

def save_metadata(file_path, metadata):
    # Save metadata to file
    with open(f"{file_path}.metadata", "w") as f:
        for key, value in metadata.items():
            f.write(f"{key}: {value}\n")

if __name__ == "__main__":
    main()
