from fastapi import HTTPException
from psycopg2.errors import UniqueViolation
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from domain.entities.user_entity import UserEntity
from data.models.user_model import UserModel

class UserRepository:
    def create_user(database_session: Session, user_entity: UserEntity):
        user_model_mapped = UserModel(
            username=user_entity.username, 
            email=user_entity.email, 
            password_hash=user_entity.password_hash
        )
        database_session.add(user_model_mapped)
        try:
            database_session.commit()
            database_session.refresh(user_model_mapped)
        except IntegrityError as e:
            database_session.rollback()
            
            if isinstance(e.orig, UniqueViolation): # Detecta violación de UNIQUE
                raise HTTPException(
                    status_code=400,
                    detail="Usuario o contraseña ya existe"
                )
            else:
                raise HTTPException(
                    status_code=500,
                    detail="Error interno de la base de datos"
                )
        return user_model_mapped

    def get_users(database_session: Session):
        users_data = database_session.query(UserModel).all()
        return [
            UserEntity(
                id=user.id,
                username=user.username,
                email=user.email,
            )
            for user in users_data
        ]

    def get_user_by_id(database_session: Session, user_id: int):
        user_data = database_session.query(UserModel).filter(UserModel.id == user_id).first()
        if not user_data:
            return None
        
        return UserEntity(
            id=user_data.id,
            username=user_data.username,
            email=user_data.email
        )
