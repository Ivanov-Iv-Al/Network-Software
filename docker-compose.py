version: '3.8'

services:
  tickets-service:
    build: .
    container_name: tickets-svc-s10
    ports:
      - "8124:8124"
    environment:
      - SERVICE_NAME=tickets-svc-s10
      - SERVICE_PORT=8124
    restart: unless-stopped
