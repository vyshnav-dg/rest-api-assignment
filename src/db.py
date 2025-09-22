from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String, Numeric, Boolean, Date, SmallInteger, Integer
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

class Base(DeclarativeBase):
    def __init__(self, dict_vals):
        for key, val in dict_vals.items():
            col = self.__table__.columns[key]
            setattr(self, key, self._convert_to_type(val, col.type))

    def _convert_to_type(self, val, col_type):
        # Convert the string form values to the assosciated python type
        # by checking with the Column type
        if(isinstance(col_type, Integer) or isinstance(col_type, SmallInteger)):
            return int(val)
        elif(isinstance(col_type, Numeric)):
            return float(val)
        elif(isinstance(col_type, Date)):
            return datetime.strptime(val, "%Y-%m-%d").date()
        return val

    @classmethod
    def get_cols(cls):
        return [column.name for column in cls.__table__.columns]
    
    def update_vals(self, data):
        for key, val in data.items():
            setattr(self, key, val)

db = SQLAlchemy(model_class=Base)