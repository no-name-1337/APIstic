# boring imports
from pymongo import MongoClient
import pandas as pd
import os

# helpers imports
from helpers.helpers import filter_dataframe, search_filter, version_filter, method_filter, create_slider

# the imports that produce the magic
import streamlit as st

apisguru_fileter = {

}

apisguru_projection = {
    'api.openapi': 1,
    'api.swagger': 1,
    'securityData': 1,
    'structureSize': 1,
    'schemaSize': 1,
    'documentationsData': 1,
    "api.info.title": 1,
    "api.info.description": 1,
    "commit_date": 1,
    "isValid": 1,
    "category": 1,
    "api.info.version": 1,
    "filename": 1
}


@st.cache_data
def load_apisguru_data(_collection):
    apisguru_filter = {
    }

    apisguru_projection = {
        'api': 1,
        'securityData': 1,
        'structureSize': 1,
        'schemaSize': 1,
        'documentationsData': 1,
        "isValid": 1,
        "category": 1,
        "filename": 1
    }

    apisguru_data = _collection.find(apisguru_filter, apisguru_projection)
    print('Fetching data from MongoDB')

    apisguru_metadata_data = []
    apisguru_structure_data = []
    apisguru_schema_data = []
    apisguru_security_data = []
    apisguru_documentation_data = []
    # apisguru_versioning_data = []

    for doc in apisguru_data:
        structure_size = doc.get('structureSize', {})
        paths, operations, webhooks, used_methods, param_ops, distinct_params, param_per_opr, used_params, methods = [
                                                                                                                         0] * 8 + [
                                                                                                                      [                                                                                                             0] * 8]
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
            param_per_opr = structure_size.get('parameters_per_operation')
            used_params = structure_size.get('used_parameters')

        if schema_size:
            schemas = schema_size.get('schemas')
            defined_schemas = schema_size.get('defined_schemas')
            max_properties = schema_size.get('max_properties')
            min_properties = schema_size.get('min_properties')
            distinct_properties_number = schema_size.get('distinct_properties_number')
            distinct_properties = schema_size.get('distinct_properties')
            params_per_ops = structure_size.get('parameters_per_operations')

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
            doc.get('api', {}).get('openapi') if doc.get('api', {}).get('openapi') else doc.get('api', {}).get(
                'swagger'),
            doc.get('api', {}).get('info', {}).get('title'),
            doc.get('api', {}).get('info', {}).get('description'),
            doc.get('api', {}).get('info', {}).get('version'),
            doc.get('api', {}).get('info', {}).get('x-apisguru-categories'),
            # doc.get('api.info.x-providerName'),
            doc.get('api', {}).get('info', {}).get('x-origin')[0].get('url') if doc.get('api', {}).get('info',
                                                                                                        {}).get(
                'x-origin') else None,
            doc.get('filename'),

            doc.get('isValid'),
            # doc.get('api.info.x-origin')[0].url if doc.get('api.info.x-origin') else None
            doc.get('api', {}).get('info', {}).get('x-origin')[0].get('url') if doc.get('api', {}).get('info',
                                                                                                        {}).get(
                'x-origin') else None
        ]
        apisguru_metadata_data.append(meta_data_row)

        structure_row = [
            paths, operations, webhooks, used_methods, param_ops, distinct_params, params_per_ops, used_params, *methods
        ]
        apisguru_structure_data.append(structure_row)

        schema_row = [
            schemas, defined_schemas, max_properties, min_properties, distinct_properties_number,
            distinct_properties
        ]
        apisguru_schema_data.append(schema_row)

        security_row = [
            security_schemes, average_secured_paths
        ]
        apisguru_security_data.append(security_row)

        documentation_row = [
            endpoints_desc_coverage, endpoints_desc, coleman_liau_index, automated_readability_index
        ]
        apisguru_documentation_data.append(documentation_row)

    metadata_columns = [
        'Openapi Version',
        'API Title',
        'Description',
        'API Version',
        'API Category',
        'Created By',
        'Filename',
        'isValid',
        'Url'
    ]
    structure_columns = [
        'Paths',
        'Operations',
        'Webhooks',
        'Used Methods',
        'Parameterised Operations',
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
        'Security Schemes',
        'Average Secured Paths'
    ]

    documentation_columns = [
        'Endpoints Description Coverage',
        'Endpoints Description',
        'Coleman Liau Index',
        'Automated Readability Index'
    ]

    # versioning_columns = [
    #     'API Version Category'
    # ]

    apisguru_metadata_df = pd.DataFrame(apisguru_metadata_data, columns=metadata_columns)
    apisguru_structure_df = pd.DataFrame(apisguru_structure_data, columns=structure_columns)
    apisguru_schema_df = pd.DataFrame(apisguru_schema_data, columns=schema_columns)
    apisguru_security_df = pd.DataFrame(apisguru_security_data, columns=security_columns)
    apisguru_documentation_df = pd.DataFrame(apisguru_documentation_data, columns=documentation_columns)

    # apisguru_versioning_df = pd.DataFrame(apisguru_versioning_data, columns=versioning_columns)

    merged_df = pd.concat(
        [apisguru_metadata_df, apisguru_structure_df, apisguru_schema_df, apisguru_security_df,
         apisguru_documentation_df], axis=1)
    print(merged_df)
    return merged_df
