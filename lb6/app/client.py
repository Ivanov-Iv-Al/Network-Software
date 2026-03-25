"""
GraphQL клиент для работы с API профилей.
Реализует функции построения запросов и отправки на сервер.
"""
import json
import requests
from typing import Dict, Any, Optional, List
from datetime import datetime


def build_payload(query: str, variables: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Формирует payload для отправки на GraphQL сервер.
    
    Аргументы:
        query: строка с GraphQL запросом
        variables: словарь с переменными (опционально)
        
    Возвращает:
        Словарь, готовый для отправки в JSON (стандартный формат GraphQL)
    """
    payload = {"query": query}
    
    if variables:
        payload["variables"] = variables
    
    return payload


class GraphQLClient:
    """
    Клиент для взаимодействия с GraphQL API.
    """
    
    def __init__(self, endpoint: str):
        """
        Инициализация клиента.
        
        Аргументы:
            endpoint: URL GraphQL эндпоинта (например, http://localhost:8145/graphql)
        """
        self.endpoint = endpoint
        self.session = requests.Session()
    
    def _send_request(self, query: str, variables: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Отправляет запрос к GraphQL серверу.
        
        Аргументы:
            query: строка с GraphQL запросом
            variables: словарь с переменными
            
        Возвращает:
            Ответ сервера в виде словаря
        """
        payload = build_payload(query, variables)
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        try:
            response = self.session.post(
                self.endpoint,
                json=payload,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return {
                "errors": [
                    {
                        "message": f"Network error: {str(e)}",
                        "type": "NETWORK_ERROR"
                    }
                ],
                "data": None
            }
    
    def execute(self, query: str, variables: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Выполняет GraphQL запрос и возвращает результат.
        
        Аргументы:
            query: строка с GraphQL запросом
            variables: словарь с переменными
            
        Возвращает:
            Словарь с полями data и/или errors
        """
        result = self._send_request(query, variables)
        
        # Выводим ошибки, если они есть
        if "errors" in result:
            print(f"\n{'='*50}")
            print("ОШИБКИ GRAPHQL:")
            print(f"{'='*50}")
            for error in result["errors"]:
                print(f"  - {error.get('message', 'Unknown error')}")
                if "locations" in error:
                    print(f"    Location: line {error['locations'][0]['line']}, "
                          f"column {error['locations'][0]['column']}")
                if "path" in error:
                    print(f"    Path: {' -> '.join(map(str, error['path']))}")
            print(f"{'='*50}\n")
        
        return result
    
    def get_profiles(self, fields: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Получение списка всех профилей.
        
        Аргументы:
            fields: список полей для запроса (если None - все поля)
            
        Возвращает:
            Ответ сервера с данными
        """
        if fields is None:
            fields_str = """
                id
                username
                email
                fullName
                phone
                bio
                avatarUrl
                createdAt
                updatedAt
            """
        else:
            fields_str = "\n                ".join(fields)
        
        query = f"""
        query {{
            profiles {{
                {fields_str}
            }}
        }}
        """
        
        return self.execute(query)
    
    def get_profile(self, profile_id: int, fields: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Получение профиля по ID.
        
        Аргументы:
            profile_id: ID профиля
            fields: список полей для запроса
            
        Возвращает:
            Ответ сервера с данными
        """
        if fields is None:
            fields_str = """
                id
                username
                email
                fullName
                phone
                bio
                avatarUrl
                createdAt
                updatedAt
            """
        else:
            fields_str = "\n                ".join(fields)
        
        query = """
        query GetProfile($id: Int!) {
            profile(id: $id) {
                %s
            }
        }
        """ % fields_str
        
        variables = {"id": profile_id}
        
        return self.execute(query, variables)
    
    def create_profile(self, username: str, email: str, full_name: str, 
                      phone: str, bio: Optional[str] = None, 
                      avatar_url: Optional[str] = None) -> Dict[str, Any]:
        """
        Создание нового профиля.
        
        Аргументы:
            username: имя пользователя
            email: электронная почта
            full_name: полное имя
            phone: номер телефона
            bio: биография (опционально)
            avatar_url: URL аватара (опционально)
            
        Возвращает:
            Ответ сервера с созданным профилем
        """
        query = """
        mutation CreateProfile($input: ProfileInput!) {
            createProfile(input: $input) {
                id
                username
                email
                fullName
                phone
                bio
                avatarUrl
                createdAt
                updatedAt
            }
        }
        """
        
        variables = {
            "input": {
                "username": username,
                "email": email,
                "fullName": full_name,
                "phone": phone
            }
        }
        
        if bio:
            variables["input"]["bio"] = bio
        if avatar_url:
            variables["input"]["avatarUrl"] = avatar_url
        
        return self.execute(query, variables)
    
    def print_result(self, result: Dict[str, Any]):
        """
        Красивый вывод результата запроса.
        
        Аргументы:
            result: результат выполнения запроса
        """
        if "data" in result and result["data"]:
            print(json.dumps(result["data"], indent=2, ensure_ascii=False))
        elif "errors" in result:
            print("Запрос завершился с ошибками (см. выше)")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("ДЕМОНСТРАЦИЯ РАБОТЫ build_payload")
    print("="*60)
    
    query = "query { profiles { id name } }"
    variables = {"id": 1}
    
    payload = build_payload(query, variables)
    print("Payload без переменных:")
    print(json.dumps(payload, indent=2))
    
    payload_no_vars = build_payload(query)
    print("\nPayload с переменными:")
    print(json.dumps(payload_no_vars, indent=2))