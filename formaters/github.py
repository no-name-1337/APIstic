# boring imports
from pymongo import MongoClient
import pandas as pd
import os

# helpers imports
from helpers.helpers import filter_dataframe, search_filter, version_filter, method_filter, create_slider

# the imports that produce the magic
import streamlit as st


@st.cache_data
def load_github_data(_api_specs=None, _commits=None):
    # last_commits = _api_specs.distinct('latest_commit_id')
    # github_filter = {'id': {'$in': last_commits}}

    apis = _api_specs.find({}, {'id': 1,'owner': 1, 'created_at': 1, 'repo_name': 1, 'url': 1, })
    apis_df = pd.DataFrame(apis)
    github_filter = {}
    github_projection = {
        'api_spec_id': 1,
        'api.openapi': 1,
        'api.swagger': 1,
        'securityData': 1,
        'structureSize': 1,
        'schemaSize': 1,
        'documentationsData': 1,
        "api.info.title": 1,
        "api.info.description": 1,
        "commit_date": 1,
        "commis": 1,
        "api.info.version": 1,
        "version": 1,
        "url": 1,
        "info_version_category": 1,
        "sha": 1
    }
    commits_data = _commits.find(github_filter, github_projection)

    github_metadata_data = []
    github_structure_data = []
    github_schema_data = []
    github_security_data = []
    github_documentation_data = []
    github_versioning_data = []

    for doc in commits_data:

        structure_size = doc.get('structureSize', {})
        paths, operations, webhooks, used_methods, param_ops, distinct_params, param_per_opr, used_params, methods = [
                                                                                                                         0] * 8 + [
                                                                                                                         [
                                                                                                                             0] * 8]
        # For GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS, TRACE
        schema_size = doc.get('schemaSize', {})
        schemas, defined_schemas, max_properties, min_properties, distinct_properties_number, distinct_properties = [
                                                                                                                        0] * 6

        security_data = doc.get('securityData', {})
        security_schemes = security_data.get('security_schemes', {})
        average_secured_paths = security_data.get('average')

        documentation_data = doc.get('documentationsData', {})
        endpoints_desc_coverage = documentation_data.get('endpoints_desc_coverage')
        endpoints_desc = documentation_data.get('endpoints_desc')
        coleman_liau_index = documentation_data.get('coleman_liau_index')
        automated_readability_index = documentation_data.get('automated_readability_index')

        if structure_size:
            paths = structure_size.get('paths')
            operations = structure_size.get('operations')
            webhooks = structure_size.get('webhooks')
            used_methods = structure_size.get('used_methods')
            param_ops = structure_size.get('parametered_operations')
            distinct_params = len(structure_size.get('distinct_parameters'))
            param_per_opr = structure_size.get('parameters_per_operations')
            used_params = structure_size.get('used_parameters')
            for i, method in enumerate(['get', 'post', 'put', 'delete', 'patch', 'head', 'options', 'trace']):
                if isinstance(structure_size.get('methods', {}), dict):
                    # If 'methods' is a dictionary, proceed with your current logic
                    methods[i] = structure_size.get('methods', {}).get(method) if structure_size.get('methods', {}).get(
                        method) else 0
                else:
                    methods[i] = 0

        if schema_size:
            schemas = schema_size.get('schemas')
            defined_schemas = len(schema_size.get('defined_schemas')) if schema_size.get('defined_schemas') else 0
            max_properties = schema_size.get('max_properties')
            min_properties = schema_size.get('min_properties')
            distinct_properties_number = len(schema_size.get('distinct_properties'))
            distinct_properties = schema_size.get('distinct_properties')

        if security_schemes:
            # get types of schemes
            security_schemes = security_data.get('security_schemes', {})
            average_secured_paths = security_data.get('average')

        if documentation_data:
            endpoints_desc_coverage = documentation_data.get('endpoints_desc_coverage')
            endpoints_desc = documentation_data.get('endpoints_desc')
            coleman_liau_index = documentation_data.get('coleman_liau_index')
            automated_readability_index = documentation_data.get('automated_readability_index')



        meta_data_row = [

            # get the api id from the apis list
            doc.get('api_spec_id'),
            # api.get('repo_name'),
            apis_df[apis_df['id'] == doc.get('api_spec_id')]['repo_name'].values[0],
            # api.get('owner'),
            apis_df[apis_df['id'] == doc.get('api_spec_id')]['owner'].values[0],
            # api.get('created_at'),
            apis_df[apis_df['id'] == doc.get('api_spec_id')]['created_at'].values[0],
            doc.get('api', {}).get('openapi') if doc.get('api', {}).get('openapi') else doc.get('api', {}).get(
                'swagger'),
            doc.get('api', {}).get('info', {}).get('title'),
            doc.get('api', {}).get('info', {}).get('description'),
            doc.get('api', {}).get('info', {}).get('version'),
            doc.get('commit_date'),
            doc.get('sha'),
            doc.get('commits'),
            doc.get('url')
        ]
        github_metadata_data.append(meta_data_row)

        structure_size_row = [
            paths,
            operations,
            used_methods,
            param_ops,
            distinct_params,
            param_per_opr,
            used_params,
            *methods

        ]
        github_structure_data.append(structure_size_row)

        schema_size_row = [
            schemas,
            defined_schemas,
            max_properties,
            min_properties,
            distinct_properties_number,
            distinct_properties
        ]
        github_schema_data.append(schema_size_row)

        security_row = [
            average_secured_paths,
            security_schemes
        ]
        github_security_data.append(security_row)

        documentation_row = [
            endpoints_desc_coverage,
            endpoints_desc,
            coleman_liau_index,
            automated_readability_index
        ]
        github_documentation_data.append(documentation_row)

        versioning_row = [
            # doc.get('version'),
            doc.get('info_version_category')]
        github_versioning_data.append(versioning_row)

    metadata_columns = [
        'API ID',
        'Repo Name',
        'Created By',
        'Repo Created At',
        'Openapi Version',
        'API Title',
        'Description',
        'API Version',
        'Commit Date',
        'Commit SHA',
        'Commits',
        'API URL'
    ]

    structure_columns = [
        'Paths',
        'Operations',
        'Used Methods',
        'Parametered Operations',
        'Distinct Parameters',
        'Parameters per Operation',
        'Used Parameters',
        'Get',
        'Post',
        'Put',
        'Delete',
        'Patch',
        'Head',
        'Options',
        'Trace'
    ]

    schema_columns = [
        'Schemas',
        'Defined Schemas',
        'Max Properties',
        'Min Properties',
        'Distinct Properties Number',
        'Distinct Properties'
    ]

    security_columns = [
        'Average Secured Paths',
        'Security Schemes'
    ]

    documentation_columns = [
        'Endpoints Description Coverage',
        'Endpoints Description',
        'Coleman Liau Index',
        'Automated Readability Index'
    ]

    versioning_columns = [
        'Version Format'
    ]

    metadata_df = pd.DataFrame(github_metadata_data, columns=metadata_columns)
    structure_df = pd.DataFrame(github_structure_data, columns=structure_columns)
    schema_df = pd.DataFrame(github_schema_data, columns=schema_columns)
    security_df = pd.DataFrame(github_security_data, columns=security_columns)
    documentation_df = pd.DataFrame(github_documentation_data, columns=documentation_columns)
    versioning_df = pd.DataFrame(github_versioning_data, columns=versioning_columns)

    merged_df = pd.concat([metadata_df, structure_df, schema_df, security_df, documentation_df, versioning_df], axis=1)
    return merged_df
