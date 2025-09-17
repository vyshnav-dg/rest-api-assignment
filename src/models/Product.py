from src.db import db
from sqlalchemy import Integer, String, Numeric, SmallInteger, Boolean
from sqlalchemy.orm import mapped_column

class Product(db.Model):
    __tablename__ = 'Products'

    ProductID = mapped_column(Integer, primary_key=True)
    ProductName = mapped_column(String(100))
    SupplierID = mapped_column(Integer)
    CategoryID = mapped_column(Integer)
    QuantityPerUnit = mapped_column(String(50))
    UnitPrice = mapped_column(Numeric(10, 2))
    UnitsInStock = mapped_column(SmallInteger)
    UnitsOnOrder = mapped_column(SmallInteger)
    ReorderLevel = mapped_column(SmallInteger)
    Discontinued = mapped_column(Boolean)
