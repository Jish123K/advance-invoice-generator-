from typing import List, Optional

from datetime import datetime

from pydantic import BaseModel, EmailStr

from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey

from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# Database configuration

SQLALCHEMY_DATABASE_URL = "sqlite:///./invoices.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Pydantic models for request and response validation/serialization

class ProductBase(BaseModel):

    product_name: str

    quantity_init: int

class ProductCreate(ProductBase):

    pass

class Product(ProductBase):

    id: int

    quantity_left: int

    created_at: datetime

    class Config:

        orm_mode = True

class UserBase(BaseModel):

    username: str

    email: EmailStr

class UserCreate(UserBase):

    password: str

class UserLogin(BaseModel):

    email: EmailStr

    password: str

class Token(BaseModel):

    access_token: str

    token_type: str

class TokenData(BaseModel):

    id: Optional[str] = None

class InvoiceItem(BaseModel):

    product_name: str

    quantity: int

    prix_unit: int

class InvoiceBase(BaseModel):

    reference: str

    value_net: int

    actual_payment: int

class InvoiceCreate(InvoiceBase):

    items: List[InvoiceItem]

class Invoice(InvoiceBase):

    id: int

    invoice_owner_id: int

    paid: bool

    created_at: datetime

    class Config:

        orm_mode = True

class UserOut(BaseModel):

    id: int

    username: str

    email: EmailStr

    created_at: datetime

    invoices: List[Invoice]

    class Config:

        orm_mode = True

class InvoiceItemOut(BaseModel):

    id: int

    product_name: str

    quantity: int

    prix_unit: int

    created_at: datetime

    class Config:

        orm_mode = True

class InvoiceOut(BaseModel):

    id: int

    reference: str

    value_net: int

    actual_payment: int

    payment_due: int

    invoice_owner_id: int

    paid: bool

    created_at: datetime

    items: List[InvoiceItemOut]

    class Config:

        orm_mode = True

class UserInvoices(BaseModel):

    username: str

    email: EmailStr

    created_at: datetime

    invoices: List[InvoiceOut]

    class Config:

        orm_mode = True

# SQLAlchemy models for database table creation and mapping

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String, unique=True, index=True)

    email = Column(String, unique=True, index=True)

    password = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)

    invoices = relationship("Invoice", back_populates="invoice_owner")

class Product(Base):

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    product_name = Column(String, index=True)

    quantity_init = Column(Integer)

    quantity_left = Column(Integer)

    created_at = Column(DateTime, default=datetime.utcnow)

class InvoiceItem(Base):

    __tablename__ = "invoice_items"

    id = Column(Integer, primary...keys=True, index=True)

product_name = Column(String, index=True)

quantity = Column(Integer)

prix_unit = Column(Integer)

invoice_id = Column(Integer, ForeignKey("invoices.id"))

class Invoice(Base):

tablename = "invoices
id = Column(Integer, primary_key=True, index=True)

reference = Column(String, index=True)

value_net = Column(Integer)

payment_due = Column(Integer)

actual_payment = Column(Integer)

invoice_owner_id = Column(Integer, ForeignKey("users.id"))

paid = Column(Boolean, default=False)

created_at = Column(DateTime, default=datetime.utcnow)

items = relationship("InvoiceItem", back_populates="invoice")
id = Column(Integer, primary_key=True, index=True)

reference = Column(String, index=True)

value_net = Column(Integer)

payment_due = Column(Integer)

actual_payment = Column(Integer)

invoice_owner_id = Column(Integer, ForeignKey("users.id"))

paid = Column(Boolean, default=False)

created_at = Column(DateTime, default=datetime.utcnow)

items = relationship("InvoiceItem", back_populates="invoice")



