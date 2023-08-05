import pinecone.experimental.controlplane.openapi
from pinecone.experimental.controlplane.openapi.api import default_api
from pinecone.experimental.controlplane.openapi.model import create_request
from pinecone.experimental.controlplane.openapi.model import patch_request
from pinecone.experimental.controlplane.openapi.model import approximated_config
from pinecone.experimental.controlplane.openapi.model import hnsw_config
from pinecone.experimental.controlplane.openapi.model import status_response
from pinecone.experimental.controlplane.openapi.model import index_meta
import argparse
import logging
import random
import time

import numpy as np
from google.protobuf import json_format
from tqdm import trange
from pinecone.experimental.database_openapi import PineconeApiClient
import pinecone


def manual_test(args):
    pinecone.init(api_key='oMis9xXVY7N43xI5ElNDYTpKx3b98iwv', environment='rajat-dev')
    with PineconeApiClient(args.index_name) as api_client:
        api_instance = default_api.DefaultApi(api_client)
        try:
            api_response =  api_instance.create_index(create_request(name='index',dimensions=128))
            print(api_response)
        except pinecone.experimental.openapi.OpenApiException:
            print('exception occurred')

        try:
            api_response = api_instance.get_indexes()
            print(api_response)
        except:
            print('exception occurred')

        try:
            api_response = api_instance.scale_index(patch_request(replicas=4))
            print(api_response)
        except:
            print('exception occurred')

        try:
            api_response = api_instance.describe_index(indexName='index')
            print(api_response)
        except:
            print('exception occurred')

        try:
            api_response = api_instance.delete_index(indexName='index')
            print(api_response)
        except:
            print('exception occurred')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--api-key')
    parser.add_argument('--pinecone-env')
    parser.add_argument('--index-name')
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    logging.info('invoked with args: %s', args)
    pinecone.init(project_name=args.project_name, api_key=args.api_key, environment=args.pinecone_env)
    logging.info('config: %s', pinecone.Config._config._asdict())

    index_name = args.index_name or f'test-index-{random.randint(0, 1000)}'

    try:
        pass
        # manual_test_grpc(index_name)
        # manual_test_grpc_vcs(index_name)
        # manual_test_misc(args)
        manual_test(args)
        # manual_test_all_legacy()
    finally:
        print('done')