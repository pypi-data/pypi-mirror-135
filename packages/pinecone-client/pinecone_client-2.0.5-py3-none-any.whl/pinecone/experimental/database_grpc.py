import atexit
import random
from functools import wraps
from abc import ABC, abstractmethod
from typing import NamedTuple, Optional, Tuple, Dict

import grpc

from pinecone.constants import Config, CLIENT_VERSION
from pinecone.utils import _generate_request_id
from pinecone.utils.sentry import sentry_decorator as sentry
from pinecone.protos.index_service_pb2_grpc import IndexServiceStub
from pinecone.retry import RetryOnRpcErrorClientInterceptor, RetryConfig
from pinecone.utils.constants import MAX_MSG_SIZE, REQUEST_ID


class GRPCClientConfig(NamedTuple):
    """
    GRPC client configuration options.

    :param secure: Whether to use encrypted protocol (SSL). defaults to True.
    :type traceroute: bool, optional
    :param timeout: defaults to 2 seconds. Fail if gateway doesn't receive response within timeout.
    :type timeout: int, optional
    :param conn_timeout: defaults to 1. Timeout to retry connection if gRPC is unavailable. 0 is no retry.
    :type conn_timeout: int, optional
    :param reuse_channel: Whether to reuse the same grpc channel for multiple requests
    :type reuse_channel: bool, optional
    :param retry_config: RetryConfig indicating how requests should be retried
    :type reuse_channel: RetryConfig, optional
    """
    secure: bool = True
    timeout: int = 20
    conn_timeout: int = 1
    reuse_channel: bool = True
    retry_config: Optional[RetryConfig] = None
    grpc_channel_options: Dict[str, str] = None

    @classmethod
    def _from_dict(cls, kwargs: dict):
        cls_kwargs = {kk: vv for kk, vv in kwargs.items() if kk in cls._fields}
        return cls(**cls_kwargs)


class GRPCDatabase(ABC):
    def __init__(self, name: str, channel=None, grpc_config: GRPCClientConfig = None, _endpoint_override: str = None):
        self.name = name
        # self.batch_size = batch_size
        # self.disable_progress_bar = disable_progress_bar

        self.grpc_client_config = grpc_config or GRPCClientConfig()
        self.retry_config = self.grpc_client_config.retry_config or RetryConfig()
        self.fixed_metadata = {
            "api-key": Config.API_KEY,
            "service-name": name,
            "client-version": CLIENT_VERSION
        }
        self._endpoint_override = _endpoint_override
        self._channel = channel or self._gen_channel()
        # self._check_readiness(grpc_config)
        # atexit.register(self.close)
        self.stub = self.stub_class(self._channel)
        super().__init__(self._channel)

    @property
    @abstractmethod
    def stub_class(self):
        pass

class DatabaseService(GRPCDatabase):
    @property
    def stub_class(self):
        return IndexServiceStub

    def create_index(self,
               request: 'index_service_pb2.CreateIndexRequest'):
        return self._wrap_grpc_call(self.stub.CreateIndex,request)

    def list_indexes(self,request:'index_service_pb2.ListIndexesRequest'):
        return self._wrap_grpc_call(self.stub.ListIndexes,request)

    def describe_index(self,
                       request:'index_service_pb2.DescribeIndexRequest'):
        return self._wrap_grpc_call(self.stub.DesribeIndex,request)

    def delete_index(self,
                     request:'index_service_pb2.DeleteIndexRequest'):
        return self._wrap_grpc_call(self.stub.DeleteIndex,request)

    def get_status(self,
                   request:'index_service_pb2.GetStatusRequest'):
        return self._wrap_grpc_call(self.stub.GetStatus,request)

    def scale_index(self,
                    request:'index_service_pb2.ScaleIndexRequest'):
        return self._wrap_grpc_call(self.stub.ScaleIndex,request)




