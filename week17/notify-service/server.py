import grpc
import logging
import uuid
from concurrent import futures
from datetime import datetime

from proto import notify_pb2, notify_pb2_grpc

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NotifyServicer(notify_pb2_grpc.NotifyServiceServicer):
    
    def SendNotification(self, request, context):
        notification_id = str(uuid.uuid4())[:8]
        
        logger.info(f"[{notification_id}] Уведомление для: {request.user_email}")
        logger.info(f"  Задача: {request.title} (ID: {request.task_id})")
        logger.info(f"  Статус: {request.old_status} → {request.new_status}")
        
        return notify_pb2.NotificationResponse(
            success=True,
            message="Уведомление отправлено",
            notification_id=notification_id
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    notify_pb2_grpc.add_NotifyServiceServicer_to_server(NotifyServicer(), server)
    server.add_insecure_port('[::]:50051')
    logger.info("Notify Service запущен на порту 50051")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()