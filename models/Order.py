from db import db
from sqlalchemy import String, Integer, Date, Numeric
from sqlalchemy.orm import mapped_column

class Order(db.Model):
    __tablename__ = "Orders"

    OrderID = mapped_column(Integer, primary_key=True)
    CustomerID = mapped_column(String(10), nullable=True)
    EmployeeID = mapped_column(Integer, nullable=True)
    OrderDate = mapped_column(Date, nullable=True)
    RequiredDate = mapped_column(Date, nullable=True)
    ShippedDate = mapped_column(Date, nullable=True)
    ShipVia = mapped_column(Integer, nullable=True)
    Freight = mapped_column(Numeric(10, 2), nullable=True)
    ShipName = mapped_column(String(100), nullable=True)
    ShipAddress = mapped_column(String(255), nullable=True)
    ShipCity = mapped_column(String(100), nullable=True)
    ShipRegion = mapped_column(String(50), nullable=True)
    ShipPostalCode = mapped_column(String(20), nullable=True)
    ShipCountry = mapped_column(String(50), nullable=True)
