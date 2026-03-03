# app/infrastructure/database/models.py
from app.infrastructure.database.database import Base # Импортируем сам Base
from app.users.user_profile.models import UserProfile
from app.tasks.models import Tasks, Categories

# Теперь Base доступен как models.Base
__all__ = [
    "Base",
    "UserProfile",
    "Tasks",
    "Categories"
]