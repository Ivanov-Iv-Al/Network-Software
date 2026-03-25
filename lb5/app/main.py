from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
import uvicorn

from schema import schema

# Создаем FastAPI приложение
app = FastAPI(
    title="Profiles GraphQL API",
    description="API для работы с профилями пользователей через GraphQL",
    version="1.0.0"
)

# Создаем GraphQL роутер
graphql_app = GraphQLRouter(schema)

# Подключаем GraphQL эндпоинт
app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
async def root():
    return {
        "message": "Profiles GraphQL API",
        "graphql_endpoint": "/graphql",
        "documentation": "Open /graphql in browser for GraphiQL interface"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "profiles-svc-s10"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8145,  # Порт из варианта
        reload=True
    )