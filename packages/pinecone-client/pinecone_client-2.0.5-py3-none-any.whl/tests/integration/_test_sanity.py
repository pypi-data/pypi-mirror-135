import argparse
import logging
import random
import time

import numpy as np
from google.protobuf import json_format
from tqdm import trange

import pinecone
# from pinecone.experimental.index_grpc import Index, CIndex
from pinecone.experimental.openapi import ApiClient
from pinecone.experimental.openapi import Configuration
from pinecone.experimental.openapi.model.anonymous_vector import AnonymousVector
from pinecone.experimental.openapi.model.dense_vector import DenseVector
from pinecone.experimental.openapi.model.query_request import QueryRequest
from pinecone.experimental.openapi.model.upsert_request import UpsertRequest
from pinecone.experimental.openapi.model.query_request_query_vector import QueryRequestQueryVector
from pinecone.experimental.openapi.model.create_request import CreateRequest
from pinecone.experimental.openapi.model.patch_request import PatchRequest
from pinecone.experimental.openapi.model.approximated_config import ApproximatedConfig
from pinecone.grpc import GRPCClient
from pinecone.protos import vector_service_pb2, vector_column_service_pb2
from pinecone.utils import dump_numpy_public, dump_strings_public


def test_grpc_upsert_ok(index):
    request = vector_service_pb2.UpsertRequest(
            vectors=[
                vector_service_pb2.DenseVector(id='A', values=[0.1] * 35, metadata='{"genre":"action"}'),
                vector_service_pb2.DenseVector(id='B', values=[0.2] * 35, metadata='{"genre":"documentary"}'),
                vector_service_pb2.DenseVector(id='C', values=[0.3] * 35, metadata='{"genre":"documentary"}'),
            ]
        )
    logging.debug('sending grpc upsert request: %s', json_format.MessageToJson(request))
    upsert_resp = index.upsert(request)
    logging.info('got grpc upsert response: %s', json_format.MessageToJson(upsert_resp))


def test_grpc_upsert_bad_dimension(index):
    logging.info('sending upsert with wrong dimension vector expecting exception...')
    try:
        request = vector_service_pb2.UpsertRequest(
                vectors=[
                    vector_service_pb2.DenseVector(id='D', values=[0.4] * 35, metadata='{}'),
                    vector_service_pb2.DenseVector(id='E', values=[0.5] * 10, metadata='{}'),
                ]
            )
        logging.debug('sending grpc upsert request: %s', json_format.MessageToJson(request))
        index.upsert(request)
    except:
        logging.exception("got exception")


def test_grpc_fetch_ok(index):
    request = vector_service_pb2.FetchRequest(ids=['A', 'B'])
    logging.debug('sending grpc fetch request: %s', json_format.MessageToJson(request))
    fetch_resp = index.fetch(request)
    logging.info('got grpc fetch response: %s', json_format.MessageToJson(fetch_resp))


def test_grpc_fetch_bad_id(index):
    try:
        logging.info('sending fetch request with nonexistent id expecting exception...')
        request = vector_service_pb2.FetchRequest(ids=['A', 'bad_id'])
        logging.debug('sending grpc fetch request: %s', json_format.MessageToJson(request))
        fetch_resp = index.fetch(request)
        logging.info('got grpc fetch response: %s', json_format.MessageToJson(fetch_resp))
    except:
        logging.exception("got exception")


def test_grpc_summarize_ok(index):
    request = vector_service_pb2.SummarizeRequest()
    logging.debug('sending grpc summarize request: %s', json_format.MessageToJson(request))
    summarize_resp = index.summarize(request)
    logging.info('got grpc summarize response: %s', json_format.MessageToJson(summarize_resp))


def test_grpc_delete_ok(index):
    request = vector_service_pb2.DeleteRequest(ids=['A', 'B'])
    logging.debug('sending grpc delete request: %s', json_format.MessageToJson(request))
    delete_resp = index.delete(request)
    logging.info('got grpc delete response: %s', json_format.MessageToJson(delete_resp))


def test_grpc_delete_all_ok(index):
    request = vector_service_pb2.DeleteRequest(delete_all=True)
    logging.debug('sending grpc delete request: %s', json_format.MessageToJson(request))
    delete_resp = index.delete(request)
    logging.info('got grpc delete all response: %s', json_format.MessageToJson(delete_resp))


def test_grpc_delete_bad_id(index):
    try:
        logging.info('sending delete request with nonexistent id expecting exception...')
        request = vector_service_pb2.DeleteRequest(ids=['A', 'bad_id'])
        logging.debug('sending grpc delete request: %s', json_format.MessageToJson(request))
        delete_resp = index.delete(request)
        logging.info('got grpc delete response: %s', json_format.MessageToJson(delete_resp))
    except:
        logging.exception('got exception')


def test_grpc_query_ok(index):
    request = vector_service_pb2.QueryRequest(
            queries=[
                vector_service_pb2.QueryRequest.QueryVector(
                    vector=vector_service_pb2.AnonymousVector(values=[0.1] * 35)
                ),
                vector_service_pb2.QueryRequest.QueryVector(
                    vector=vector_service_pb2.AnonymousVector(values=[0.1] * 35)
                )
            ],
            request_default_top_k=2,
            include_data=True
        )
    logging.debug('sending grpc query request: %s', json_format.MessageToJson(request))
    query_resp = index.query(request)
    logging.info('got grpc query response: %s', json_format.MessageToJson(query_resp))


def test_grpc_vcs_upsert_ok(index):
    request = vector_column_service_pb2.UpsertRequest(
        ids=dump_strings_public(['A', 'B']),
        data=dump_numpy_public(np.asarray([[0.1]*35, [0.2]*35]))
    )
    logging.debug('sending grpc upsert request: %s', json_format.MessageToJson(request))
    upsert_resp = index.upsert(request)
    logging.info('got grpc upsert response: %s', json_format.MessageToJson(upsert_resp))


def test_grpc_vcs_fetch_ok(index):
    # TODO: update all test_grpc_vcs_* to use correct vector_column_service_pb2 api
    request = vector_column_service_pb2.FetchRequest(ids=['A', 'B'])
    logging.debug('sending grpc fetch request: %s', json_format.MessageToJson(request))
    fetch_resp = index.fetch(request)
    logging.info('got grpc fetch response: %s', json_format.MessageToJson(fetch_resp))


def test_grpc_vcs_fetch_bad_id(index):
    try:
        logging.info('sending fetch request with nonexistent id expecting exception...')
        request = vector_column_service_pb2.FetchRequest(ids=['A', 'bad_id'])
        logging.debug('sending grpc fetch request: %s', json_format.MessageToJson(request))
        fetch_resp = index.fetch(request)
        logging.info('got grpc fetch response: %s', json_format.MessageToJson(fetch_resp))
    except:
        logging.exception("got exception")


def test_grpc_vcs_summarize_ok(index):
    request = vector_column_service_pb2.SummarizeRequest()
    logging.debug('sending grpc summarize request: %s', json_format.MessageToJson(request))
    summarize_resp = index.summarize(request)
    logging.info('got grpc summarize response: %s', json_format.MessageToJson(summarize_resp))


def test_grpc_vcs_delete_ok(index):
    request = vector_column_service_pb2.DeleteRequest(ids=['A', 'B'])
    logging.debug('sending grpc delete request: %s', json_format.MessageToJson(request))
    delete_resp = index.delete(request)
    logging.info('got grpc delete response: %s', json_format.MessageToJson(delete_resp))


def test_grpc_vcs_delete_all_ok(index):
    request = vector_column_service_pb2.DeleteRequest(delete_all=True)
    logging.debug('sending grpc delete request: %s', json_format.MessageToJson(request))
    delete_resp = index.delete(request)
    logging.info('got grpc delete all response: %s', json_format.MessageToJson(delete_resp))


def test_grpc_vcs_delete_bad_id(index):
    try:
        logging.info('sending delete request with nonexistent id expecting exception...')
        request = vector_column_service_pb2.DeleteRequest(ids=['A', 'bad_id'])
        logging.debug('sending grpc delete request: %s', json_format.MessageToJson(request))
        delete_resp = index.delete(request)
        logging.info('got grpc delete response: %s', json_format.MessageToJson(delete_resp))
    except:
        logging.exception('got exception')


def test_grpc_vcs_query_ok(index):
    request = vector_column_service_pb2.QueryRequest(
            queries=[
                vector_column_service_pb2.QueryRequest.QueryVector(
                    vector=vector_column_service_pb2.AnonymousVector(values=[0.1] * 35)
                ),
                vector_column_service_pb2.QueryRequest.QueryVector(
                    vector=vector_column_service_pb2.AnonymousVector(values=[0.1] * 35)
                )
            ],
            request_default_top_k=2,
            include_data=True
        )
    logging.debug('sending grpc query request: %s', json_format.MessageToJson(request))
    query_resp = index.query(request)
    logging.info('got grpc query response: %s', json_format.MessageToJson(query_resp))


def manual_test_grpc(index_name):
    # index = Index(index_name)
    index = ''
    test_grpc_upsert_ok(index)
    test_grpc_upsert_bad_dimension(index)

    test_grpc_fetch_ok(index)
    test_grpc_fetch_bad_id(index)

    test_grpc_summarize_ok(index)

    test_grpc_delete_ok(index)
    test_grpc_delete_bad_id(index)

    test_grpc_query_ok(index)

    test_grpc_delete_all_ok(index)


def manual_test_grpc_vcs(index_name):
    # index = CIndex(index_name)
    index = ''
    test_grpc_vcs_upsert_ok(index)
    # test_grpc_vcs_upsert_bad_dimension(index)

    test_grpc_vcs_fetch_ok(index)
    test_grpc_vcs_fetch_bad_id(index)

    test_grpc_vcs_summarize_ok(index)

    test_grpc_vcs_delete_ok(index)
    test_grpc_vcs_delete_bad_id(index)

    test_grpc_vcs_query_ok(index)

    test_grpc_vcs_delete_all_ok(index)


def manual_test_openapi(args):
    import pinecone.experimental.openapi
    from pinecone.experimental.openapi.api import default_api
    from pinecone.experimental.index_openapi import PineconeApiClient
    openapi_client_config = Configuration.get_default_copy()
    openapi_client_config.verify_ssl = False
    openapi_client_config.proxy = "http://localhost:8081"

    pinecone.init(api_key=args.api_key, environment=args.pinecone_env)
    with PineconeApiClient(args.index_name, openapi_client_config=openapi_client_config) as api_client:
        api_instance = default_api.DefaultApi(api_client)
        try:
            api_response = api_instance.upsert(
                UpsertRequest(
                    vectors=[
                        DenseVector(id="vec1", values=[0.1] * 35, metadata="{}"),
                        DenseVector(id="vec2", values=[0.2] * 35, metadata="{}")
                    ],
                    namespace="ns1",
                )
            )
            logging.info('got openapi upsert response: %s', api_response)
        except pinecone.experimental.openapi.OpenApiException:
            logging.exception("got exception")

        try:
            api_response = api_instance.summarize()
            logging.info('got openapi summarize response: %s', api_response)
        except pinecone.experimental.openapi.OpenApiException:
            logging.exception("got exception")

        try:
            api_response = api_instance.list_namespaces()
            logging.info('got openapi list_namespaces response: %s', api_response)
        except pinecone.experimental.openapi.OpenApiException:
            logging.exception("got exception")

        try:
            api_response = api_instance.list(namespace="example-namespace")
            logging.info('got openapi list response: %s', api_response)
        except pinecone.experimental.openapi.OpenApiException:
            logging.exception("got exception")

        try:
            api_response = api_instance.query(
                QueryRequest(
                    queries=[
                        QueryRequestQueryVector(vector=AnonymousVector(values=[0.1] * 35), filter='{}',
                                                top_k=5),
                        QueryRequestQueryVector(vector=AnonymousVector(values=[0.2] * 35), filter='{}'),
                    ],
                    request_default_namespace="example-namespace",
                    request_default_top_k=10,
                    include_data=True,
                    include_metadata=True
                )
            )
            logging.info('got openapi query response: %s', api_response)
        except pinecone.experimental.openapi.OpenApiException:
            logging.exception("got exception")

        try:
            api_response = api_instance.delete(ids=["vec1", "vec2"], namespace="example-namespace")
            logging.info('got openapi delete response: %s', api_response)
        except pinecone.experimental.openapi.OpenApiException:
            logging.exception("got exception")


def manual_test_all_legacy():
    # Create an index
    logging.info('create_index result: %s', pinecone.create_index("hello-pinecone-index", metric="euclidean"))

    # Connect to the index
    index = pinecone.Index("hello-pinecone-index")

    # Insert the data
    ids = ["A", "B", "C", "D", "E"],
    vectors = [[1]*3, [2]*3, [3]*3, [4]*3, [5]*3]
    logging.info('upsert result: %s', index.upsert(items=zip(ids, vectors)))

    # Fetch data
    logging.info('fetch result: %s', index.fetch(ids=ids[1:3]))

    # Query the index and get similar vectors
    logging.info('query result: %s', index.query(queries=[[0, 1]], top_k=3))

    # Delete data
    logging.info('delete result: %s', index.delete(ids=ids[1:3]))

    # Get index info
    logging.info('info result: %s', index.info())

    # Delete the index
    logging.info('delete_index result: %s', pinecone.delete_index("hello-pinecone-index"))


def manual_test_misc(args):
    client = GRPCClient(host=f'{args.index_name}-{args.project_name}.svc.{args.pinecone_env}.pinecone.io', port=443,
                        service_name=args.index_name, api_key=args.api_key, secure=True, conn_timeout=5)

    logging.info('fetch result: %s', client.send_request(client.get_fetch_request(ids=['A', 'B', 'C'], path='read')))

    logging.info('query result: %s',
                 client.send_request(client.get_query_request(top_k=1, data=np.random.random((35,)))))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--api-key')
    parser.add_argument('--project-name')
    parser.add_argument('--pinecone-env')
    parser.add_argument('--index-name')
    parser.add_argument('--use-existing', action='store_true')
    parser.add_argument('--verify-ssl')
    args = parser.parse_args()
    # print(args)
    logging.basicConfig(level=logging.INFO)
    logging.info('invoked with args: %s', args)
    # pinecone.init(project_name=args.project_name, api_key=args.api_key, environment=args.pinecone_env)

    from pinecone.experimental.openapi.api import default_api
    from pinecone.experimental.index_openapi import PineconeApiClient

    openapi_client_config = Configuration.get_default_copy()
    openapi_client_config.verify_ssl = False
    openapi_client_config.proxy = "http://localhost:8081"

    pinecone.init(api_key=args.api_key, environment=args.pinecone_env)
    logging.info('config: %s', pinecone.Config._config._asdict())
    api_client = PineconeApiClient(args.index_name, openapi_client_config=openapi_client_config)
    api_instance = default_api.DefaultApi(api_client)
    config = ApproximatedConfig(kbits=1024)
    api_instance.create_index(create_request=CreateRequest(name=args.index_name, dimension=35,index_type='approximated',metric='cosine',replicas=1,shards=1,index_config={
        'kbits':1024},kind='database'))
    api_instance.scale_index(args.index_name, patch_request=PatchRequest(replicas=4))
    info = api_instance.describe_index(args.index_name)
    print(info)
    # index_name = args.index_name or f'test-index-{random.randint(0, 1000)}'
    # if not args.use_existing:
    #     logging.info("not use existing")
    #     indexes = api_instance.list_indexes()
    #     api_instance.scale_index('test',patch_request=PatchRequest(replicas=4))
    #     info = api_instance.describe_index('test')
    #     logging.info('current indexes: %s', indexes)
    #     logging.info('index meta: ', info)
    #     if index_name in indexes:
    #         logging.info('stopping index %s ...', 'test')
    #         api_instance.delete_index('test')
    #     api_instance.get_status('test')
    #     logging.info('creating index %s ...', index_name)
    #     # api_instance.create_index(create_request=CreateRequest(name=index_name, dimensions=35))
    #     logging.info('sleeping while index gets ready...')
    #     # for _ in trange(300):
    #     #     time.sleep(1)
    #     # logging.info('done sleeping')

    try:
        # manual_test_grpc(index_name)
        # manual_test_grpc_vcs(index_name)
        # manual_test_misc(args)
        manual_test_openapi(args)
        # manual_test_all_legacy()
    finally:
        if not args.use_existing and False:
            default_api.api_instance(index_name)
