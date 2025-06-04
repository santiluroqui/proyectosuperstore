from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base

# Define la base declarativa para todos tus modelos
Base = declarative_base()

class Order(Base):
    __tablename__ = 'orders' # Nombre de la tabla en tu base de datos

    RowID = Column(Integer, primary_key=True)
    OrderID = Column(String)
    OrderDate = Column(Date)
    ShipDate = Column(Date)
    ShipMode = Column(String)
    CustomerID = Column(String)
    CustomerName = Column(String)
    Segment = Column(String)
    Country = Column(String)
    City = Column(String)
    State = Column(String)
    PostalCode = Column(Integer)
    Region = Column(String)
    ProductID = Column(String)
    Category = Column(String)
    SubCategory = Column(String)
    ProductName = Column(String) # Usar String para ProductName
    Sales = Column(Float)
    Quantity = Column(Integer)
    Discount = Column(Float)
    Profit = Column(Float)

    def to_dict(self):
        # Método para convertir un objeto Order a un diccionario (útil para JSON)
        return {
            'RowID': self.RowID,
            'OrderID': self.OrderID,
            'OrderDate': self.OrderDate.isoformat() if self.OrderDate else None, # Formato ISO para fechas
            'ShipDate': self.ShipDate.isoformat() if self.ShipDate else None,
            'ShipMode': self.ShipMode,
            'CustomerID': self.CustomerID,
            'CustomerName': self.CustomerName,
            'Segment': self.Segment,
            'Country': self.Country,
            'City': self.City,
            'State': self.State,
            'PostalCode': self.PostalCode,
            'Region': self.Region,
            'ProductID': self.ProductID,
            'Category': self.Category,
            'SubCategory': self.SubCategory,
            'ProductName': self.ProductName,
            'Sales': self.Sales,
            'Quantity': self.Quantity,
            'Discount': self.Discount,
            'Profit': self.Profit
        }