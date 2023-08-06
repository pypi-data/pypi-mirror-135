from typing import Union
import asyncio
import socket
from grpc import Server, aio
from grpc_reflection.v1alpha import reflection
from grpc_health.v1 import health, health_pb2_grpc
from grpc_health.v1.health_pb2 import _HEALTH
from delphai_utils.logging import logging
from google.protobuf.descriptor import FileDescriptor
from delphai_utils.gateway import start_gateway
from delphai_utils.keycloak import update_public_keys
from prometheus_client import start_http_server
import functools
from grpc.aio import AioRpcError
from grpc import StatusCode
from delphai_utils.interceptors.metrics import MetricsInterceptor
from delphai_utils.interceptors.authentication import AuthenticationInterceptor

shutdown_event = asyncio.Event()


def grpc_error(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        context = args[2]
        try:
            result = await func(*args, **kwargs)
            return result
        except AioRpcError as ex:
            await context.abort(ex.code(), ex.details())
        except Exception as ex:
            await context.abort(StatusCode.INTERNAL, str(ex))

    return wrapper


def is_port_free(host, port):
    """
    determine whether `host` has the `port` free

    From: https://www.thepythoncode.com/article/make-port-scanner-python
    """
    s = socket.socket()
    try:
        s.connect((host, port))
    except Exception:
        return True
    else:
        return False


class NoPortFoundError(Exception):
    ...


def find_free_port(start: int, host="127.0.0.1", num_tries=4) -> int:
    for port in range(start, start + num_tries):
        if is_port_free(host, port):
            return port
        else:
            logging.info(f"Port {port} already in use.")
    message = f"No free port found in range [{start}, {start + num_tries - 1}]"
    logging.error(message)
    raise NoPortFoundError(message)


def create_grpc_server(descriptor: FileDescriptor):
    max_length = 512 * 1024 * 1024
    server_options = [
        ("grpc.max_send_message_length", max_length),
        ("grpc.max_receive_message_length", max_length),
    ]
    server = aio.server(
        options=server_options,
        interceptors=(
            AuthenticationInterceptor(),
            MetricsInterceptor(),
        ),
    )
    server.__dict__["descriptor"] = descriptor
    health_servicer = health.HealthServicer(experimental_non_blocking=True)
    health_pb2_grpc.add_HealthServicer_to_server(health_servicer, server)
    services = descriptor.services_by_name.keys()
    service_full_names = list(
        map(lambda service: descriptor.services_by_name[service].full_name, services)
    )
    service_names = (
        *service_full_names,
        _HEALTH.full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(service_names, server)
    return server


def start_server(
    server: Server,
    gateway: bool = True,
    grpc_port: Union[int, None] = None,
    http_port: Union[int, None] = None,
    metrics_port: Union[int, None] = None,
):
    logging.info("starting grpc server...")
    if not grpc_port:
        grpc_port = find_free_port(8080)
    server.add_insecure_port(f"[::]:{grpc_port}")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(server.start())
    logging.info(f"started grpc server on port {grpc_port}")
    if not metrics_port:
        metrics_port = find_free_port(9191)
    start_http_server(metrics_port)
    logging.info(f"started metrics server on port {metrics_port}")
    try:
        if gateway:
            if not http_port:
                http_port = find_free_port(7070)
            gateway = start_gateway(server.__dict__["descriptor"], grpc_port, http_port)
            loop.create_task(gateway)
        loop.create_task(server.wait_for_termination())
        loop.create_task(update_public_keys())
        loop.run_forever()
    except KeyboardInterrupt:
        logging.info("stopped server (keyboard interrupt)")
