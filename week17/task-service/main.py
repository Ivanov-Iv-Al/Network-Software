import os
import grpc
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from . import models, schemas, database
from .proto import notify_pb2, notify_pb2_grpc

app = FastAPI(title="Task Service", version="1.0.0")

NOTIFY_HOST = os.getenv("NOTIFY_HOST", "notify-service")
NOTIFY_PORT = os.getenv("NOTIFY_PORT", "50051")
channel = grpc.insecure_channel(f"{NOTIFY_HOST}:{NOTIFY_PORT}")
notify_stub = notify_pb2_grpc.NotifyServiceStub(channel)

@app.on_event("startup")
def init_db():
    database.init_db()

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/api/v1/tasks", response_model=schemas.TaskResponse, status_code=201)
def create_task(task: schemas.TaskCreate, db: Session = Depends(database.get_db)):
    db_task = models.Task(
        title=task.title,
        description=task.description,
        user_email=task.user_email
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.get("/api/v1/tasks/{task_id}", response_model=schemas.TaskResponse)
def get_task(task_id: int, db: Session = Depends(database.get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/api/v1/tasks/{task_id}/status")
def update_task_status(
    task_id: int,
    status_update: schemas.StatusUpdate,
    db: Session = Depends(database.get_db)
):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    old_status = task.status
    task.status = status_update.status
    db.commit()
    
    try:
        notify_stub.SendNotification(
            notify_pb2.TaskUpdate(
                task_id=task.id,
                title=task.title,
                old_status=old_status,
                new_status=task.status,
                user_email=task.user_email
            ),
            timeout=3.0
        )
        return {"message": "Status updated", "notification_sent": True}
    except grpc.RpcError:
        return {"message": "Status updated", "notification_sent": False}