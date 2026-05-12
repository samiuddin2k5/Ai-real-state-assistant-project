from sqlalchemy import Column, Integer, String, Text, Float, DateTime, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from database import Base

class UserRole(str, enum.Enum):
    USER = "user"
    AGENT = "agent"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    role = Column(SQLEnum(UserRole), default=UserRole.USER)
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    properties = relationship("Property", back_populates="owner")
    chat_messages = relationship("ChatMessage", back_populates="user")

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    price = Column(Integer, nullable=False, index=True)
    location = Column(String(255), nullable=False, index=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    bedrooms = Column(Integer, default=0)
    bathrooms = Column(Integer, default=0)
    area_sqft = Column(Float, nullable=True)
    property_type = Column(String(100), nullable=False, index=True)  # apartment, house, plot, commercial
    status = Column(String(50), default="available")  # available, sold, rented
    image_url = Column(String(500), nullable=True)
    images = Column(Text, nullable=True)  # JSON array of image URLs
    
    # Investment metrics
    expected_roi = Column(Float, default=0.0)
    rental_income = Column(Float, default=0.0)
    appreciation_rate = Column(Float, default=0.0)
    
    # Metadata
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    owner = relationship("User", back_populates="properties")
    documents = relationship("Document", back_populates="property")

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(Text, nullable=False)
    response = Column(Text, nullable=True)
    context = Column(Text, nullable=True)  # JSON context about properties
    is_from_user = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="chat_messages")

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    document_type = Column(String(100), nullable=False)  # brochure, legal, contract, report
    file_size = Column(Integer, nullable=False)
    is_indexed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    property = relationship("Property", back_populates="documents")
