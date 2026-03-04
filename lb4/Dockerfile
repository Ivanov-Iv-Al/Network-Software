FROM python:3.9-slim

WORKDIR /app

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/*.py .

EXPOSE 8124

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8124", "--reload"]