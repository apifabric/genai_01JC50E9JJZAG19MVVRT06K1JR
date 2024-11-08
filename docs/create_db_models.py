# created from response - used to create database and project
#  should run without error
#  if not, check for decimal, indent, or import issues

import decimal

import logging



logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

import sqlalchemy



from sqlalchemy.sql import func  # end imports from system/genai/create_db_models_inserts/create_db_models_prefix.py

from logic_bank.logic_bank import Rule

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

class Customer(Base):
    """description: Stores customer details with balance and credit limit."""
    __tablename__ = 'customer'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    balance = Column(Float, default=0.0)
    credit_limit = Column(Float, nullable=False)


class Order(Base):
    """description: Records customer orders with a reference to customers and the total amount."""
    __tablename__ = 'order'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    order_date = Column(DateTime, default=datetime.datetime.now)
    amount_total = Column(Float, default=0.0)
    notes = Column(Text, nullable=True)
    date_shipped = Column(DateTime, nullable=True)


class Item(Base):
    """description: Items within each order, including quantity, unit price and amount."""
    __tablename__ = 'item'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    amount = Column(Float, default=0.0)


class Product(Base):
    """description: Available products, with pricing information for each item type."""
    __tablename__ = 'product'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    unit_price = Column(Float, nullable=False)


class Address(Base):
    """description: Stores customer addresses, with customer reference."""
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    street = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    zip_code = Column(String, nullable=False)


class Supplier(Base):
    """description: Suppliers providing products to the system."""
    __tablename__ = 'supplier'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    contact_info = Column(String, nullable=True)


class Inventory(Base):
    """description: Inventory levels of products, linked with suppliers."""
    __tablename__ = 'inventory'

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    supplier_id = Column(Integer, ForeignKey('supplier.id'), nullable=False)
    quantity_in_stock = Column(Integer, nullable=False)


class Review(Base):
    """description: Reviews provided by customers for products."""
    __tablename__ = 'review'

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)


class Shipment(Base):
    """description: Shipments associated with orders indicating delivery status."""
    __tablename__ = 'shipment'

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)
    shipment_date = Column(DateTime, nullable=True)
    status = Column(String, nullable=False)


class Payment(Base):
    """description: Payments made by customers for orders."""
    __tablename__ = 'payment'

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)
    payment_date = Column(DateTime, default=datetime.datetime.now)
    amount = Column(Float, nullable=False)


class Return(Base):
    """description: Returns processed for orders."""
    __tablename__ = 'return'

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)
    return_date = Column(DateTime, nullable=True)
    reason = Column(Text, nullable=True)


class Category(Base):
    """description: Categories for organizing products."""
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)


def create_and_populate_database():
    engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Creating sample data

    # Products
    product1 = Product(name='Laptop', unit_price=1000.0)
    product2 = Product(name='Smartphone', unit_price=500.0)

    # Categories
    category1 = Category(name='Electronics')
    category2 = Category(name='Accessories')

    # Suppliers
    supplier1 = Supplier(name='Supplier A', contact_info='supplierA@example.com')
    
    # Customers
    customer1 = Customer(name='John Doe', balance=0.0, credit_limit=1500.0)
    customer2 = Customer(name='Jane Smith', balance=200.0, credit_limit=1000.0)

    # Addresses
    address1 = Address(customer_id=1, street='123 Elm St', city='Springfield', state='IL', zip_code='62701')
    address2 = Address(customer_id=2, street='456 Oak St', city='Springfield', state='IL', zip_code='62701')

    # Orders
    order1 = Order(customer_id=1, amount_total=0.0, notes='Fast delivery requested.')
    order2 = Order(customer_id=2, amount_total=0.0)

    # Items
    item1 = Item(order_id=1, product_id=1, quantity=1, unit_price=1000.0, amount=1000.0)
    item2 = Item(order_id=2, product_id=2, quantity=2, unit_price=500.0, amount=1000.0)

    # Inventory
    inventory1 = Inventory(product_id=1, supplier_id=1, quantity_in_stock=50)
    inventory2 = Inventory(product_id=2, supplier_id=1, quantity_in_stock=100)

    # Reviews
    review1 = Review(product_id=1, customer_id=1, rating=5, comment='Excellent product!')
    
    # Shipments
    shipment1 = Shipment(order_id=1, shipment_date=datetime.datetime.now(), status='Delivered')

    # Payments
    payment1 = Payment(order_id=1, amount=1000.0)

    # Returns
    return1 = Return(order_id=1, return_date=datetime.datetime.now(), reason='Damaged on arrival')

    # Add and commit all
    session.add_all([product1, product2, category1, category2, supplier1, customer1, customer2, 
                     address1, address2, order1, order2, item1, item2, inventory1, inventory2, 
                     review1, shipment1, payment1, return1])
    
    session.commit()

create_and_populate_database()
