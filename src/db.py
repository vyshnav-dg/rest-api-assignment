from sqlalchemy.orm import DeclarativeBase
from flask_sqlalchemy import SQLAlchemy


class Base(DeclarativeBase):
    def __init__(self, dict_vals):
        for key, val in dict_vals.items():
            setattr(self, key, val)

    @classmethod
    def get_cols(cls):
        return [column.name for column in cls.__table__.columns]
    
    def update_vals(self, data):
        for key, val in data.items():
            setattr(self, key, val)

db = SQLAlchemy(model_class=Base)