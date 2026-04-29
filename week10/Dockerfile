# Stage 1: Builder
FROM python:3.11-slim AS builder
WORKDIR /build
COPY requirements.txt .
# Устанавливаем только зависимости в отдельную папку
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim
WORKDIR /app
# Копируем только установленные пакеты из builder
COPY --from=builder /root/.local /root/.local
COPY main.py .
# Обновляем PATH
ENV PATH=/root/.local/bin:$PATH
EXPOSE 8106
CMD ["python", "main.py"]