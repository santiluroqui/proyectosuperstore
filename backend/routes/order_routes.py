from flask import Blueprint, jsonify, request
from backend.__init__ import db # Importa db de la inicialización de Flask
from backend.models.order import Order
from datetime import datetime

order_bp = Blueprint('orders', __name__, url_prefix='/api/orders')

@order_bp.route('/', methods=['GET'])
def get_orders():
    orders = db.session.execute(db.select(Order)).scalars().all()
    return jsonify([order.to_dict() for order in orders])

@order_bp.route('/<int:row_id>', methods=['GET'])
def get_order(row_id):
    order = db.session.execute(db.select(Order).filter_by(RowID=row_id)).scalar_one_or_404()
    return jsonify(order.to_dict())

@order_bp.route('/', methods=['POST'])
def create_order():
    data = request.get_json()
    new_order = Order(
        OrderID=data.get('OrderID'),
        OrderDate=datetime.fromisoformat(data['OrderDate']) if data.get('OrderDate') else None,
        ShipDate=datetime.fromisoformat(data['ShipDate']) if data.get('ShipDate') else None,
        ShipMode=data.get('ShipMode'),
        CustomerID=data.get('CustomerID'),
        CustomerName=data.get('CustomerName'),
        Segment=data.get('Segment'),
        Country=data.get('Country'),
        City=data.get('City'),
        State=data.get('State'),
        PostalCode=data.get('PostalCode'),
        Region=data.get('Region'),
        ProductID=data.get('ProductID'),
        Category=data.get('Category'),
        SubCategory=data.get('SubCategory'),
        ProductName=data.get('ProductName'),
        Sales=data.get('Sales'),
        Quantity=data.get('Quantity'),
        Discount=data.get('Discount'),
        Profit=data.get('Profit')
    )
    db.session.add(new_order)
    db.session.commit()
    return jsonify(new_order.to_dict()), 201

@order_bp.route('/<int:row_id>', methods=['PUT'])
def update_order(row_id):
    order = db.session.execute(db.select(Order).filter_by(RowID=row_id)).scalar_one_or_404()
    data = request.get_json()

    order.OrderID = data.get('OrderID', order.OrderID)
    order.OrderDate = datetime.fromisoformat(data['OrderDate']) if data.get('OrderDate') else order.OrderDate
    order.ShipDate = datetime.fromisoformat(data['ShipDate']) if data.get('ShipDate') else order.ShipDate
    order.ShipMode = data.get('ShipMode', order.ShipMode)
    order.CustomerID = data.get('CustomerID', order.CustomerID)
    order.CustomerName = data.get('CustomerName', order.CustomerName)
    order.Segment = data.get('Segment', order.Segment)
    order.Country = data.get('Country', order.Country)
    order.City = data.get('City', order.City)
    order.State = data.get('State', order.State)
    order.PostalCode = data.get('PostalCode', order.PostalCode)
    order.Region = data.get('Region', order.Region)
    order.ProductID = data.get('ProductID', order.ProductID)
    order.Category = data.get('Category', order.Category)
    order.SubCategory = data.get('SubCategory', order.SubCategory)
    order.ProductName = data.get('ProductName', order.ProductName)
    order.Sales = data.get('Sales', order.Sales)
    order.Quantity = data.get('Quantity', order.Quantity)
    order.Discount = data.get('Discount', order.Discount)
    order.Profit = data.get('Profit', order.Profit)

    db.session.commit()
    return jsonify(order.to_dict())

@order_bp.route('/<int:row_id>', methods=['DELETE'])
def delete_order(row_id):
    order = db.session.execute(db.select(Order).filter_by(RowID=row_id)).scalar_one_or_404()
    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'Order deleted successfully'}), 204