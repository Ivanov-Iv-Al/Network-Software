#!/usr/bin/env python3
"""
GraphQL клиент для работы с сервисом профилей.
Выполняет запросы на получение и создание профилей.
"""
import sys
import time
from typing import Dict, Any

from client import GraphQLClient


def print_separator(title: str = ""):
    """Выводит разделитель с заголовком."""
    print("\n" + "="*70)
    if title:
        print(f" {title}")
        print("="*70)
    else:
        print("="*70)


def main():
    """Основная функция клиента."""
    
    # Настройка подключения
    endpoint = "http://localhost:8145/graphql"
    
    print_separator("GRAPHQL КЛИЕНТ - СЕРВИС ПРОФИЛЕЙ")
    print(f"Endpoint: {endpoint}")
    print(f"Версия: 1.0.0")
    print(f"Вариант: profiles-s10")
    
    # Создаем клиент
    client = GraphQLClient(endpoint)
    
    # Тест 1: Проверка доступности сервера
    print_separator("1. ПРОВЕРКА ДОСТУПНОСТИ СЕРВЕРА")
    try:
        response = client.execute("{ __typename }")
        if "data" in response:
            print("✓ Сервер доступен")
        else:
            print("✗ Сервер недоступен или вернул ошибку")
            sys.exit(1)
    except Exception as e:
        print(f"✗ Ошибка подключения: {e}")
        print("Убедитесь, что сервер запущен на порту 8145")
        sys.exit(1)
    
    # Тест 2: Создание профилей (Mutation)
    print_separator("2. СОЗДАНИЕ ПРОФИЛЕЙ (MUTATION)")
    
    # Создаем первого пользователя
    print("\n▶ Создание профиля: Иван Петров")
    result = client.create_profile(
        username="ivan123",
        email="ivan@example.com",
        full_name="Иван Петров",
        phone="+7-999-123-45-67",
        bio="Python разработчик, любитель GraphQL",
        avatar_url="https://example.com/avatars/ivan.jpg"
    )
    
    if "data" in result and result["data"]:
        profile = result["data"]["createProfile"]
        print(f"✓ Профиль создан (ID: {profile['id']})")
        print(f"  Имя: {profile['fullName']}")
        print(f"  Email: {profile['email']}")
        print(f"  Телефон: {profile['phone']}")
        print(f"  Создан: {profile['createdAt']}")
    
    time.sleep(1)
    
    # Создаем второго пользователя
    print("\n▶ Создание профиля: Мария Сидорова")
    result = client.create_profile(
        username="maria87",
        email="maria@example.com",
        full_name="Мария Сидорова",
        phone="+7-999-765-43-21",
        bio="Тестировщик, изучает GraphQL"
    )
    
    if "data" in result and result["data"]:
        profile = result["data"]["createProfile"]
        print(f"✓ Профиль создан (ID: {profile['id']})")
        print(f"  Имя: {profile['fullName']}")
        print(f"  Email: {profile['email']}")
        print(f"  Телефон: {profile['phone']}")
    
    time.sleep(1)
    
    # Создаем третьего пользователя с минимальными данными
    print("\n▶ Создание профиля: Алексей Смирнов")
    result = client.create_profile(
        username="alex89",
        email="alex@example.com",
        full_name="Алексей Смирнов",
        phone="+7-999-111-22-33"
    )
    
    if "data" in result and result["data"]:
        profile = result["data"]["createProfile"]
        print(f"✓ Профиль создан (ID: {profile['id']})")
        print(f"  Имя: {profile['fullName']}")
        print(f"  Телефон: {profile['phone']}")
    
    # Тест 3: Получение всех профилей (Query)
    print_separator("3. ПОЛУЧЕНИЕ ВСЕХ ПРОФИЛЕЙ (QUERY)")
    
    print("\n▶ Запрос всех профилей (все поля):")
    result = client.get_profiles()
    
    if "data" in result and result["data"]:
        profiles = result["data"]["profiles"]
        print(f"✓ Получено профилей: {len(profiles)}")
        for profile in profiles:
            print(f"\n  [{profile['id']}] {profile['fullName']}")
            print(f"      Email: {profile['email']}")
            print(f"      Телефон: {profile['phone']}")
            if profile.get('bio'):
                print(f"      Bio: {profile['bio'][:50]}...")
    
    # Тест 4: Получение только нужных полей (гибкость GraphQL)
    print_separator("4. ГИБКИЙ ЗАПРОС (ТОЛЬКО НУЖНЫЕ ПОЛЯ)")
    
    print("\n▶ Запрос только имен и телефонов:")
    result = client.get_profiles(fields=["fullName", "phone"])
    
    if "data" in result and result["data"]:
        profiles = result["data"]["profiles"]
        print(f"✓ Получено профилей: {len(profiles)}")
        for profile in profiles:
            print(f"  - {profile['fullName']}: {profile['phone']}")
    
    print("\n▶ Запрос только ID, username и email:")
    result = client.get_profiles(fields=["id", "username", "email"])
    
    if "data" in result and result["data"]:
        profiles = result["data"]["profiles"]
        print(f"✓ Получено профилей: {len(profiles)}")
        for profile in profiles:
            print(f"  - [{profile['id']}] {profile['username']}: {profile['email']}")
    
    # Тест 5: Получение конкретного профиля по ID
    print_separator("5. ПОЛУЧЕНИЕ КОНКРЕТНОГО ПРОФИЛЯ (QUERY С ПЕРЕМЕННЫМИ)")
    
    print("\n▶ Запрос профиля с ID=1 (все поля):")
    result = client.get_profile(1)
    
    if "data" in result and result["data"]:
        profile = result["data"]["profile"]
        if profile:
            print(f"✓ Найден профиль:")
            print(f"  ID: {profile['id']}")
            print(f"  Имя: {profile['fullName']}")
            print(f"  Email: {profile['email']}")
            print(f"  Телефон: {profile['phone']}")
            print(f"  Bio: {profile.get('bio', 'не указана')}")
            print(f"  Создан: {profile['createdAt']}")
        else:
            print("✗ Профиль не найден")
    
    print("\n▶ Запрос профиля с ID=2 (только имя и телефон):")
    result = client.get_profile(2, fields=["fullName", "phone", "email"])
    
    if "data" in result and result["data"]:
        profile = result["data"]["profile"]
        if profile:
            print(f"✓ Найден профиль:")
            print(f"  Имя: {profile['fullName']}")
            print(f"  Email: {profile['email']}")
            print(f"  Телефон: {profile['phone']}")
        else:
            print("✗ Профиль не найден")
    
    print_separator("6. ОБРАБОТКА ОШИБОК")
    
    print("\n▶ Попытка получить несуществующий профиль (ID=999):")
    result = client.get_profile(999)
    
    if "data" in result and result["data"]:
        profile = result["data"]["profile"]
        if profile is None:
            print("  ✓ Профиль не найден (корректная обработка)")
        else:
            print(f"  Найден профиль (неожиданно): {profile}")
    
    print_separator("7. СТАТИСТИКА")
    
    result = client.get_profiles()
    if "data" in result and result["data"]:
        profiles = result["data"]["profiles"]
        print(f"Всего профилей: {len(profiles)}")
        
        has_bio = sum(1 for p in profiles if p.get('bio'))
        has_avatar = sum(1 for p in profiles if p.get('avatarUrl'))
        
        print(f"Профилей с bio: {has_bio}")
        print(f"Профилей с аватаром: {has_avatar}")
    
    print_separator("ЗАВЕРШЕНИЕ РАБОТЫ")
    print("Клиент успешно выполнил все запросы\n")

main()