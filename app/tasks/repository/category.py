from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.exception import CategoryNotFound
from app.infrastructure.database.models import Categories



class TaskCategoryRepository:

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_category(self, category_id: int, user_id: int) -> Categories | None:
        query = select(Categories).where(Categories.id == category_id, Categories.user_id == user_id)
        async with self.db_session as session:
            category: Categories =  (await session.execute(query)).scalar_one_or_none()
        if category == None:
            raise CategoryNotFound
        return category


    async def get_categories(self, user_id: int) -> list[Categories] | None:
        query = select(Categories).where(Categories.user_id == user_id)
        async with self.db_session as session:
            categories: list[Categories] = list((await session.execute(query)).scalars().all())
        if len(categories) == 0:
            raise CategoryNotFound
        return categories

    async def create_category(self, name: str, user_id: int) -> int:
        category_model = Categories(
            name=name,
            user_id=user_id
        )
        async with self.db_session as session:
            session.add(category_model)
            await session.commit()
            return category_model.id

    async def delete_category(self, category_id: int, user_id: int) -> None:
        query = delete(Categories).where(Categories.id == category_id, Categories.user_id == user_id)
        async with self.db_session as session:
            await session.execute(query)
            await session.commit()