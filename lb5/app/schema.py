import strawberry
from typing import List, Optional
from datetime import datetime
from models import Profile as ProfileModel, ProfileCreate

profiles_db = {}
id_counter = 1

@strawberry.type
class Profile:
    """GraphQL тип Profile - соответствует варианту задания"""
    id: int
    username: str
    email: str
    full_name: str
    phone: str  # дополнительное поле из варианта
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    created_at: str
    updated_at: str

    @staticmethod
    def from_model(model: ProfileModel) -> "Profile":
        """Конвертация из Pydantic модели в GraphQL тип"""
        return Profile(
            id=model.id,
            username=model.username,
            email=model.email,
            full_name=model.full_name,
            phone=model.phone,
            bio=model.bio,
            avatar_url=model.avatar_url,
            created_at=model.created_at.isoformat(),
            updated_at=model.updated_at.isoformat()
        )

@strawberry.input
class ProfileInput:
    """Input тип для создания профиля"""
    username: str
    email: str
    full_name: str
    phone: str
    bio: Optional[str] = None
    avatar_url: Optional[str] = None

@strawberry.type
class Query:
    """GraphQL Query - получение данных"""
    
    @strawberry.field
    def profiles(self) -> List[Profile]:
        """Получение списка всех профилей (query: profiles)"""
        return [Profile.from_model(p) for p in profiles_db.values()]
    
    @strawberry.field
    def profile(self, id: int) -> Optional[Profile]:
        """Получение одного профиля по ID"""
        profile = profiles_db.get(id)
        return Profile.from_model(profile) if profile else None

@strawberry.type
class Mutation:
    """GraphQL Mutation - изменение данных"""
    
    @strawberry.mutation
    def create_profile(self, input: ProfileInput) -> Profile:
        """Создание нового профиля (mutation: createProfile)"""
        global id_counter
        
        # Создаем модель профиля
        profile = ProfileModel(
            id=id_counter,
            username=input.username,
            email=input.email,
            full_name=input.full_name,
            phone=input.phone,
            bio=input.bio,
            avatar_url=input.avatar_url,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        # Сохраняем в хранилище
        profiles_db[id_counter] = profile
        id_counter += 1
        
        return Profile.from_model(profile)

# Создаем схему GraphQL
schema = strawberry.Schema(query=Query, mutation=Mutation)