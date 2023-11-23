import pandas as pd
import streamlit as st

swagger_filter = {}
swagger_projection = {
        'securityData': 1,
        'structureSize': 1,
        'schemaSize': 1,
        'documentationsData': 1,
        '_created_at': 1,
        '_last_modified': 1,
        '_created_by': 1,
        '_OPENAPI_version': 1,
        '_name': 1,
        '_description': 1,
        '_API_url': 1,
        '_version': 1,
        '_id': 0
    }
@st.cache_data
def load_swaggerhub_data(_collection):

    _projection = swagger_projection
    _query = swagger_filter
    print('Fetching data from MongoDB')

    documents = _collection.find(_query, _projection)

    swagger_metadata_data = []
    swagger_structure_data = []
    swagger_schema_data = []
    swagger_security_data = []
    swagger_documentation_data = []

    for doc in documents:
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
                methods[i] = structure_size.get('methods', {}).get(method) if structure_size.get('methods', {}).get(
                    method) else 0

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
            doc.get('_OPENAPI_version'),
            doc.get('_name'),
            doc.get('_version'),
            doc.get('_description'),
            doc.get('_created_by'),
            doc.get('_created_at'),
            doc.get('_last_modified'),
            doc.get('_API_url'),
        ]
        swagger_metadata_data.append(meta_data_row)

        structure_row = [
            paths, operations, webhooks, used_methods, param_ops, distinct_params, used_params, *methods
        ]
        swagger_structure_data.append(structure_row)

        schema_row = [
            schemas, defined_schemas, max_properties, min_properties, distinct_properties_number,
            distinct_properties
        ]
        swagger_schema_data.append(schema_row)

        security_row = [
            security_schemes, average_secured_paths
        ]
        swagger_security_data.append(security_row)

        documentation_row = [
            endpoints_desc_coverage, endpoints_desc, coleman_liau_index, automated_readability_index
        ]
        swagger_documentation_data.append(documentation_row)

    # Define the columns, remove dashes, and capitalize each word
    metadata_columns = [
        'Openapi Version', 'API Title', 'Version', 'Description', 'Created By', 'Created At', 'Last Modified', 'API Url'
    ]

    structure_columns = [
        'Paths', 'Operations', 'Webhooks', 'Used Methods', 'Parameterised Operations', 'Distinct Parameters',
        'Used Parameters',
        'Get', 'Post', 'Put', 'Delete', 'Patch', 'Head', 'Options', 'Trace'
    ]

    schema_columns = [
        'Schemas', 'Defined Schemas', 'Max Properties', 'Min Properties', 'Distinct Properties Number',
        'Distinct Properties'
    ]

    security_columns = [
        'Security Schemes', 'Average Secured Paths'
    ]

    documentation_columns = [
        'Endpoints Description Coverage', 'Endpoints Description', 'Coleman Liau Index',
        'Automated Readability Index'
    ]

    metadata_df = pd.DataFrame(swagger_metadata_data, columns=metadata_columns)
    structure_df = pd.DataFrame(swagger_structure_data, columns=structure_columns)
    schema_df = pd.DataFrame(swagger_schema_data, columns=schema_columns)
    security_df = pd.DataFrame(swagger_security_data, columns=security_columns)
    documentation_df = pd.DataFrame(swagger_documentation_data, columns=documentation_columns)

    # merge the dataframes
    merged_df = pd.concat([metadata_df, structure_df, schema_df, security_df, documentation_df], axis=1)
    # df.drop(['Distinct Parameters'], axis=1, inplace=True)
    return merged_df
