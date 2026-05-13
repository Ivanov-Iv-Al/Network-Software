# Финальный проект: Микросервисная система управления задачами

## Описание
Система состоит из трёх сервисов:
- **Task Service** (REST API) — управление задачами
- **Notify Service** (gRPC) — отправка уведомлений
- **PostgreSQL** — хранение данных
- **Nginx** — API Gateway

## Быстрый запуск

```bash

git clone <repo-url>
cd final-project

docker-compose up --build

curl http://localhost:8000/health