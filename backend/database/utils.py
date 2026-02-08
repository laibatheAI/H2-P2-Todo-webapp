"""
Utility functions for database operations in the Todo AI Chatbot application.
"""
from sqlmodel import Session, select, func
from typing import List, Optional, TypeVar, Generic, Type, Any
from uuid import UUID


T = TypeVar('T')


class CRUDOperations(Generic[T]):
    """
    Generic CRUD operations class for database operations.
    """

    def __init__(self, model: Type[T]):
        self.model = model

    def create(self, db: Session, obj: T) -> T:
        """
        Create a new object in the database.
        """
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def get_by_id(self, db: Session, id: UUID) -> Optional[T]:
        """
        Get an object by its ID.
        """
        statement = select(self.model).where(self.model.id == id)
        return db.exec(statement).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[T]:
        """
        Get all objects with optional pagination.
        """
        statement = select(self.model).offset(skip).limit(limit)
        results = db.exec(statement).all()
        return results

    def update(self, db: Session, id: UUID, obj_data: dict) -> Optional[T]:
        """
        Update an object by ID with the provided data.
        """
        db_obj = self.get_by_id(db, id)
        if db_obj:
            for key, value in obj_data.items():
                setattr(db_obj, key, value)
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: UUID) -> bool:
        """
        Delete an object by ID.
        """
        obj = self.get_by_id(db, id)
        if obj:
            db.delete(obj)
            db.commit()
            return True
        return False


def get_user_filtered_statement(model: Type[T], user_id: UUID):
    """
    Helper function to create a select statement filtered by user_id.
    This helps ensure user data isolation.
    """
    statement = select(model).where(model.user_id == user_id)
    return statement


def get_count(db: Session, model: Type[T], user_id: UUID) -> int:
    """
    Get the count of objects for a specific user.
    """
    statement = select(func.count(model.id)).where(model.user_id == user_id)
    count = db.exec(statement).one()
    return count