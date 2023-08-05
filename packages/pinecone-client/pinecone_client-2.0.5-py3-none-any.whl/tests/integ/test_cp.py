import time

import pinecone
import uuid
import numpy as np
import random
import sys
import pytest
from pinecone_nuts.utils import vs_adapter
import pinecone
from loguru import logger
from pinecone import QueryVector, Vector, Index, PineconeProtocolError, ApiKeyError, ApiException
from pinecone.core.client import Configuration
# from pinecone.core.client.model.upsert_response import UpsertResponse
# from pinecone import QueryVector
from pinecone.core.grpc.index_grpc import GRPCIndex, GRPCVector, GRPCQueryVector
from pinecone.core.grpc.protos import vector_column_service_pb2
from pinecone.core.utils import dump_numpy_public, dict_to_proto_struct
from pinecone.core.grpc.protos import vector_service_pb2
import cProfile, pstats
from pinecone.core.grpc.protos.vector_column_service_pb2 import NdArray
from google.protobuf.struct_pb2 import Struct

from google.protobuf import json_format
from munch import munchify
import pandas as pd
from pandas import DataFrame


def test_gong_size():
    # df = pd.read_parquet('/Users/rajat/Downloads/gong.parquet', engine='pyarrow')
    # df = df[:10000]
    # df.to_parquet('gong_small.parquet',engine='pyarrow')
    pinecone.init(api_key='076a7136-9e84-45d0-b802-bd33861c5dc8', environment='gong-poc-us-east1-gcp')
    # pinecone.delete_index('upsert-billion-bert')
    # pinecone.create_index('upsert-billion-bert', 768, shards=250,
    #                       index_config={"hybrid": True, "deduplicate": True, "k_bits": 1024})
    for i in range(10):
        index = pinecone.GRPCIndex('test-{}'.format(i))
        ds = index.describe_index_stats().namespaces
        vc = 0
        # print(ds)
        for ns in ds:
            # print(ds[ns]['vector_count'])
            vc += ds[ns]['vector_count']
        print(vc)
        print(len(ds))



def test_delete_all():
    pinecone.init(api_key='2c80b666-82a2-4e24-abd1-15fa467c770c', environment='us-west1-gcp')
    index = pinecone.Index('test')
    index2 = pinecone.Index('rajat')
    print(index.describe_index_stats())
    # index.delete(delete_all=True, namespace='smt')
    print(index2.describe_index_stats())
    # print(index.fetch(ids=['1'],namespace='sm'))
    # print(index.fetch(ids=['1'], namespace='sm2'))
    # print(index.fetch(ids=['1'], namespace='smt'))


def test_customer():
    pinecone.init(api_key='e5a254ec-fe3d-49c0-9479-85774003d170', environment='us-west1-gcp')
    print(pinecone.list_indexes())
    index = Index('delomore-10-300-logid-uuid-s1-v2')
    print(index.describe_index_stats())


def test_grpc():
    pinecone.init(api_key='2c80b666-82a2-4e24-abd1-15fa467c770c', environment='us-west1-gcp')
    # pinecone.delete_index('test')
    # pinecone.create_index('mdim', 15000)
    index = GRPCIndex('mdim')
    # pinecone.init(api_key='', environment='us-west1-gcp')
    # pinecone.list_indexes()

    # index = Index('test')
    n = 100
    vecs = [np.random.rand(15000).tolist() for i in range(n)]
    ids = [str(i) for i in range(n)]
    meta = [{'yo lo': 1, 'yelo': 2, 'oloy': 3} for i in range(n)]
    data = tuple(zip(ids, vecs, meta))
    batch = 10

    # index = GRPCIndex('test')
    # print(index.describe_index_stats())
    def chunker(seq, size):
        return (seq[pos:pos + size] for pos in range(0, len(seq), size))

    #
    s = time.perf_counter()
    res = []
    for chunk in chunker(data, batch):
        res.append(index.upsert(vectors=chunk, async_req=False, namespace='smtv'))

    # qvec = [0.1]*768
    # filter = {'yelo':{'$eq':3}}
    # fr = index.fetch(ids=ids)
    # print(len(fr['vectors']))
    # res =index.query(queries=[qvec],top_k=10,filter=filter)
    # print(res)
    # rs = [r.result() for r in res]
    e = time.perf_counter()
    print(e - s)
    # print(async_results)

    # print([async_result.result() for async_result in async_results])
    # for chunk in chunker(data, batch):
    #     # res = index.async_upsert(5,chunk)
    #     index.upsert(vectors=chunk)
    # from concurrent.futures import ThreadPoolExecutor
    # with ThreadPoolExecutor(max_workers=10) as executor:
    #     for chunk in chunker(data, batch):
    #         future_results = executor.submit(index.upsert, chunk)
    #     rset= future_results.result()
    # print(res)
    # profiler.disable()
    # stats = pstats.Stats(profiler).sort_stats('tottime')
    # stats.print_stats()

    print(index.describe_index_stats())


def test_s():
    pinecone.init(api_key='9a1ca6b7-84e3-4669-b1d2-ce63a7cb8046', environment='us-west1-gcp')
    index = GRPCIndex('index-s1-1')
    # print(pinecone.list_indexes())
    # print(pinecone.describe_index('index-s1-1'))
    # print(index.describe_index_stats())
    qvec = [0.1] * 768
    res = index.query(queries=[qvec], top_k=10)
    print(res)
    n = 10
    vecs = [np.random.rand(768).tolist() for i in range(n)]
    ids = [str(uuid.uuid4()) for i in range(n)]
    data = tuple(zip(ids, vecs))
    index.upsert(vectors=data)


def test_delete():
    pinecone.init(api_key='2c80b666-82a2-4e24-abd1-15fa467c770c', environment='us-west1-gcp')
    # for index in pinecone.list_indexes():
    #     pinecone.delete_index(index)
    print(pinecone.whoami())
