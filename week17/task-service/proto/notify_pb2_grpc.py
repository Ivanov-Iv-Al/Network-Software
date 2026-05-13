"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import notify_pb2 as notify__pb2

class NotifyServiceStub(object):
    """Сервис уведомлений
    """
    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SendNotification = channel.unary_unary(
                '/notify.NotifyService/SendNotification',
                request_serializer=notify__pb2.TaskUpdate.SerializeToString,
                response_deserializer=notify__pb2.NotificationResponse.FromString,
                )
        self.StreamNotifications = channel.stream_stream(
                '/notify.NotifyService/StreamNotifications',
                request_serializer=notify__pb2.TaskUpdate.SerializeToString,
                response_deserializer=notify__pb2.NotificationResponse.FromString,
                )

class NotifyServiceServicer(object):
    """Сервис уведомлений
    """
    def SendNotification(self, request, context):
        """Отправка уведомления об изменении задачи
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StreamNotifications(self, request_iterator, context):
        """Отправка потоковых уведомлений (для массовых операций)
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_NotifyServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SendNotification': grpc.unary_unary_rpc_method_handler(
                    servicer.SendNotification,
                    request_deserializer=notify__pb2.TaskUpdate.FromString,
                    response_serializer=notify__pb2.NotificationResponse.SerializeToString,
            ),
            'StreamNotifications': grpc.stream_stream_rpc_method_handler(
                    servicer.StreamNotifications,
                    request_deserializer=notify__pb2.TaskUpdate.FromString,
                    response_serializer=notify__pb2.NotificationResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'notify.NotifyService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))

# This mapping is used for reflection URI details
_GRPC_GENERATED_SERVICE = {
    "notify.NotifyService": {
        "methods": ["SendNotification", "StreamNotifications"]
    }
}