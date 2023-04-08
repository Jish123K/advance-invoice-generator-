from dataclasses import dataclass

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, BigInteger, TIMESTAMP

from sqlalchemy.orm import relationship

@dataclass

class Product:

    id: int = Column(Integer, primary_key=True, nullable=False)

    product_name: str = Column(String(255), nullable=False)

    quantity_init: int = Column(Integer(), nullable=True)

    quantity_left: int = Column(Integer(), nullable=True)

    created_at: str = Column(TIMESTAMP(timezone=True), nullable=False)

    deleted: bool = Column(Boolean, server_default='False', nullable=False)

@dataclass

class Invoice:

    id: int = Column(Integer, primary_key=True, nullable=False)

    reference: str = Column(String(255), nullable=False)

    value_net: int = Column(BigInteger(), nullable=False)

    actual_payment: int = Column(BigInteger(), nullable=False)

    payment_due: int = Column(BigInteger(), nullable=False)

    created_at: str = Column(TIMESTAMP(timezone=True), nullable=False)

    paid: bool = Column(Boolean, server_default='False', nullable=False)

    deleted: bool = Column(Boolean, server_default='False', nullable=False)

    invoice_owner_id: int = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    items: relationship = relationship("InvoiceItem", backref="owner")

@dataclass

class InvoiceItem:

    id: int = Column(Integer, primary_key=True, nullable=False)

    product_name: str = Column(String(255), nullable=False)

    quantity: int = Column(Integer(), nullable=False)

    prix_unit: int = Column(BigInteger(), nullable=False)

    created_at: str = Column(TIMESTAMP(timezone=True), nullable=False)

    deleted: bool = Column(Boolean, server_default='False', nullable=False)

    invoice_id: int = Column(Integer, ForeignKey("invoices.id", ondelete="CASCADE"), nullable=False)

@dataclass

class User:

    id: int = Column(Integer, primary_key=True, nullable=False)

    username: str = Column(String(255), nullable=False)

    email: str = Column(String, nullable=False, unique=True)

    password: str = Column(String, nullable=False)

    created_at: str = Column(TIMESTAMP(timezone=True), nullable=False)

    invoices: relationship = relationship("Invoice", backref="creator")

