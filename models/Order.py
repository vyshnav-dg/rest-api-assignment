from db import db
from sqlalchemy import String, Integer, Date, Numeric
from sqlalchemy.orm import mapped_column

class Order(db.Model):
    __tablename__ = "Orders"

    OrderID = mapped_column(Integer, primary_key=True)
    CustomerID = mapped_column(String(10))
    EmployeeID = mapped_column(Integer)
    OrderDate = mapped_column(Date)
    RequiredDate = mapped_column(Date)
    ShippedDate = mapped_column(Date)
    ShipVia = mapped_column(Integer)
    Freight = mapped_column(Numeric(10, 2))
    ShipName = mapped_column(String(100))
    ShipAddress = mapped_column(String(255))
    ShipCity = mapped_column(String(100))
    ShipRegion = mapped_column(String(50))
    ShipPostalCode = mapped_column(String(20))
    ShipCountry = mapped_column(String(50))
