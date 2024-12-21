from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession

from .models import Book
from .schemas import BookCreateModel, BookUpdateModel


class BookService:
    async def get_all_books(self, session: AsyncSession) -> list[Book]:
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.exec(statement).all()
        return result.all()

    async def get_book(self, book_id: str, session: AsyncSession) -> Book | None:
        statement = select(Book).where(Book.id == book_id)
        result = await session.exec(statement)
        book = result.first()
        return book if book else None

    async def create_book(self, book: BookCreateModel, session: AsyncSession):
        new_book = Book(**book.model_dump())
        session.add(new_book)
        session.commit()
        return new_book

    async def update_book(
        self, book_id: str, update_data: BookUpdateModel, session: AsyncSession
    ) -> Book | None:
        book_to_update = await self.get_book(book_id, session)

        if book_to_update:
            update_data_dict = update_data.model_dump()
            for k, v in update_data_dict.items():
                setattr(book_to_update, k, v)
            await session.commit()
            return book_to_update
        return None

    async def delete_book(self, book_id: str, session: AsyncSession) -> None:
        book_to_delete = await self.get_book(book_id, session)

        if book_to_delete:
            session.delete(book_to_delete)
            await session.commit()
        return None
