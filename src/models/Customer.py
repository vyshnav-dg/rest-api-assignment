from db import db
from sqlalchemy import String
from sqlalchemy.orm import mapped_column

class Customer(db.Model):
    __tablename__ = "Customers"

    CustomerID = mapped_column(String(10), primary_key=True, nullable=False)
    CompanyName = mapped_column(String(100))
    ContactName = mapped_column(String(100))
    ContactTitle = mapped_column(String(50))
    Address = mapped_column(String(255))
    City = mapped_column(String(100))
    Region = mapped_column(String(50))
    PostalCode = mapped_column(String(20))
    Country = mapped_column(String(50))
    Phone = mapped_column(String(30))
    Fax = mapped_column(String(30))