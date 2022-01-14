from typing import TypeVar, Generic, Type, Any, Optional, List, Union, Dict, Sequence
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session, load_only

from app.db import Base
from setting import settings

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
            self, db: Session, *, page: int = 1, page_size: int = 100, retrieve_model: Optional[ModelType] = None
    ) -> List[ModelType]:
        temp_page = (page - 1) * page_size
        if not retrieve_model:
            return db.query(self.model).offset(temp_page).limit(page_size).all()
        else:
            return db.query(self.model).options(load_only(*retrieve_model.__fields__.keys())).offset(temp_page).limit(
                page_size).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, id: int, *, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        db_obj = db.query(self.model).filter(self.model.id == id).first()
        for field in update_data:
            setattr(db_obj, field, update_data[field])
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).filter(self.model.id == id).update({self.model.is_delete: 1})
        # db.delete(obj)
        db.commit()
        return obj

    def multi_delete(self, db: Session, *, ids: Sequence[int]) -> ModelType:
        obj = db.query(self.model).filter(self.model.id.in_(ids)).delete(synchronize_session=False)
        db.commit()
        return obj

    def get_multi_local(
            self, db: Session, *, page: int = 1, page_size: int = 100
    ) -> List[ModelType]:
        temp_page = (page - 1) * page_size
        return db.query(self.model).filter(self.model.position == settings.LOCAL_POSITION).offset(temp_page).limit(
            page_size).all()

    def multi_create(self, db: Session, *, obj_list: Sequence[CreateSchemaType]) -> List[ModelType]:
        db_obj = [self.model(**jsonable_encoder(obj_data)) for obj_data in obj_list]
        db.bulk_save_objects(db_obj)
        db.commit()
        return db_obj
