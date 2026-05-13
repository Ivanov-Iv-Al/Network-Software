# Архитектура микросервисной системы

## Диаграмма

[Клиент] → REST → [Task Service:8000] → SQL → [PostgreSQL:5432]
↓
gRPC
↓
[Notify Service:50051]
↓
[Логирование]


## Компоненты

### Task Service (REST)
- **Технологии**: Python, FastAPI, SQLAlchemy
- **Порт**: 8000
- **Эндпоинты**:
  - `POST /api/v1/tasks` — создание
  - `GET /api/v1/tasks/{id}` — получение
  - `PUT /api/v1/tasks/{id}/status` — обновление статуса

### Notify Service (gRPC)
- **Технологии**: Python, gRPC
- **Порт**: 50051
- **Метод**: `SendNotification(TaskUpdate) → NotificationResponse`

### PostgreSQL
- **Версия**: 15
- **Порт**: 5432
- **Таблицы**: tasks (id, title, status, user_email, created_at)

## Выбор протоколов

| Протокол | Где | Причина |
|----------|-----|---------|
| REST | Клиент ↔ Task Service | Простота, кэширование |
| gRPC | Task Service ↔ Notify Service | Скорость, строгий контракт |