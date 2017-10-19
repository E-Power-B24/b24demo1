from sqlalchemy import Column, Integer, Numeric, String, Boolean, DateTime, Sequence, Unicode, Text, UnicodeText, ForeignKey
from sqlalchemy.orm import relationship, remote
from sqlalchemy.ext.declarative import declarative_base,declared_attr
from datetime import datetime
from common.json_helpers import json, ExtEncoder
from b24demo1.core.models.helper import *

Base = declarative_base()

String = Unicode
Text = UnicodeText

def current_user():
    return "-"

def get_current_user():
    return current_user()

class TrackMixin(object):
    @declared_attr
    def created_date(cls):
        return Column(String, default=datetime.now)
    @declared_attr
    def create_by(cls):
        return Column(String, default=get_current_user)
    @declared_attr
    def last_modified_date(cls):
        return Column(String, onupdate=datetime.now)
    @declared_attr
    def last_modified_by(cls):
        return Column(String, onupdate=get_current_user)
    @declared_attr
    def is_active(cls):
        return Column(Boolean, default=True)

    def __str__(self):
        if hasattr(self,'code') and hasattr(self,'name'):
            return '% - %'%(self.code, self.name)
        if hasattr(self,'code'):
            return getattr(self,'code')
        if hasattr(self,'name'):
            return getattr(self,'name')
        return str(self.id)


class User(Base, TrackMixin):
    __tablename__ = 'users'
    id = Column(Integer, Sequence(__tablename__+'_id_seq'),primary_key=True)
    name = Column(String(50))
    full_name = Column(String(50))
    email = Column(String)
    password = Column(String)

class Product(Base, TrackMixin):
    __tablename__ = 'products'
    id = Column(Integer, Sequence(__tablename__+'_id_seq'),primary_key=True)
    code = Column(String)
    name = Column(String)
    price = Column(Numeric(18,2))
    category_id = Column(Integer)
    vendor_id = Column(Integer)

    vendor = relationship('Vendor', primaryjoin = 'foreign(Product.vendor_id) == remote(Vendor.id)')
    category = relationship('Category', primaryjoin = 'foreign(Product.category_id) == remote(Category.id)')

class Category(Base, TrackMixin):
    __tablename__ = 'categories'
    id = Column(Integer, Sequence(__tablename__+'_id_seq'), primary_key=True)
    code = Column(String(50))
    name = Column(String(50))

class Invoice(Base, TrackMixin):
    __tablename__ ='invoices'
    id = Column(Integer, Sequence(__tablename__+'_id_seq'),primary_key=True)
    code = Column(String)
    date = Column(DateTime)
    total_amount = Column(Numeric(18,2))
    exchange_rate = Column(Numeric(18,2))
    paid = Column(Numeric(18,2))
    change = Column(Numeric(18,2))
    customer_id = Column(Integer)
    details_data = Column(String)

    @property
    def details_json(self):
        return json.dumps([to_dict(d, ignores=json_ignores) for d in self.details if d.is_active], cls = ExtEncoder);

    customer = relationship('Customer', primaryjoin = 'foreign(Invoice.customer_id) == remote(Customer.id)')
    details = relationship('InvoiceDetail',primaryjoin = 'foreign(Invoice.id) == remote(InvoiceDetail.invoice_id)', uselist= True, viewonly=True)


    # details = relationship('InvoiceDetail',primaryjoin = 'foreign(Invoice.id) == remote(InvoiceDetail.invoice_id)', uselist= True, viewonly=True)
    # customer = relationship('Customer', primaryjoin='foreign(Invoice.customer_id) == remote(Customer.id)')

class InvoiceDetail(Base, TrackMixin):
    __tablename__ = 'invoice_details'
    id = Column(Integer,Sequence(__tablename__+'_id_seq'), primary_key=True)
    invoice_id = Column(Integer)
    product_id = Column(Integer)
    product_code = Column(Integer)
    product_name = Column(String)
    quantity = Column(Integer)
    price = Column(Numeric(18,2))
    amount = Column(Integer)

    invoice = relationship('Invoice', primaryjoin='foreign(InvoiceDetail.invoice_id) == remote(Invoice.id)')

class Customer(Base, TrackMixin):
    __tablename__ = 'customers'
    id = Column(Integer, Sequence(__tablename__+'_id_seq'),primary_key=True)
    name = Column(String)
    phone = Column(String)
    address = Column(String)

class Vendor(Base, TrackMixin):
    __tablename__ = 'vendors'
    id = Column(Integer, Sequence(__tablename__ + '_id_seq'), primary_key=True)
    name = Column(String)
    phone = Column(String)
    address = Column(String)

class ExchangeRate(Base, TrackMixin):
    __tablename__ = 'exchange_rates'
    id = Column(Integer, Sequence(__tablename__ + '_id_seq'), primary_key=True)
    name = Column(String)
    value = Column(Numeric(18,2))