# Аудит безопасности сервиса "bookings-s04"

**Проект:** Сервис бронирований  
**Группа:** 331  
**Студент:** s04  
**Дата:** 2026-05-05  

---

## 1. Область аудита

| Параметр | Значение |
|----------|----------|
| Целевой сервис | bookings-svc-s04 |
| Порт | 8172 |
| Эндпоинты | /api/bookings (REST, gRPC, GraphQL) |
| Версия | 1.0.0 |

---

## 2. Чек-лист OWASP Top 10 (Web 2021)

| № | Категория | Проверка | Статус | Доказательство |
|---|-----------|----------|--------|----------------|
| A01 | Broken Access Control | Проверка ролей на всех эндпоинтах |  Частично | PUT /bookings/{id} доступен любому user |
| A02 | Cryptographic Failures | HTTPS включён? |  Нет | Только HTTP на порту 8172 |
| A03 | Injection | SQL Injection защита |  Критически | Конкатенация в поиске |
| A04 | Insecure Design | Rate limiting |  Нет | /login без защиты |
| A05 | Security Misconfiguration | CORS настройки |  Да | Только localhost |
| A06 | Vulnerable Components | Проверка зависимостей |  Нет | Нет SCA в CI |
| A07 | Identification Failures | JWT проверка |  Да | Есть проверка exp и signature |
| A08 | Software Integrity | Подпись зависимостей |  Нет | Нет проверки контрольных сумм |
| A09 | Logging Failures | Логирование атак |  Да | Логируются 4xx и 5xx |
| A10 | SSRF | Защита от внутренних запросов |  Нет | Можно запросить 127.0.0.1 |

---

## 3. Найденные уязвимости

### 3.1 Критическая: SQL Injection

**Эндпоинт:** `GET /api/bookings?search=`

**Запрос:**
```http
GET /api/bookings?search=' OR '1'='1