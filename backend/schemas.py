from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

# ==================== User Schemas ====================

class UserRole(str, Enum):
    USER = "user"
    AGENT = "agent"
    ADMIN = "admin"

class UserRegister(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    full_name: Optional[str] = None
    phone: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: Optional[str]
    phone: Optional[str]
    role: str
    is_verified: bool
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None

# ==================== Property Schemas ====================

class PropertyCreate(BaseModel):
    title: str = Field(..., min_length=5)
    description: Optional[str] = None
    price: int = Field(..., gt=0)
    location: str = Field(..., min_length=3)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    bedrooms: int = Field(default=0, ge=0)
    bathrooms: int = Field(default=0, ge=0)
    area_sqft: Optional[float] = None
    property_type: str  # apartment, house, plot, commercial
    status: Optional[str] = "available"
    image_url: Optional[str] = None
    images: Optional[List[str]] = None
    expected_roi: Optional[float] = 0.0
    rental_income: Optional[float] = 0.0
    appreciation_rate: Optional[float] = 0.0

class PropertyUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    area_sqft: Optional[float] = None
    property_type: Optional[str] = None
    status: Optional[str] = None
    image_url: Optional[str] = None
    images: Optional[List[str]] = None
    expected_roi: Optional[float] = None
    rental_income: Optional[float] = None
    appreciation_rate: Optional[float] = None

class PropertyResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    price: int
    location: str
    latitude: Optional[float]
    longitude: Optional[float]
    bedrooms: int
    bathrooms: int
    area_sqft: Optional[float]
    property_type: str
    status: str
    image_url: Optional[str]
    images: Optional[List[str]]
    expected_roi: float
    rental_income: float
    appreciation_rate: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PropertyFilter(BaseModel):
    min_price: Optional[int] = None
    max_price: Optional[int] = None
    location: Optional[str] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    property_type: Optional[str] = None
    status: Optional[str] = None

# ==================== Chat Schemas ====================

class ChatMessage(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    context: Optional[str] = None

class ChatResponse(BaseModel):
    id: int
    message: str
    response: str
    context: Optional[str]
    is_from_user: bool
    created_at: datetime

    class Config:
        from_attributes = True

class ChatHistory(BaseModel):
    messages: List[ChatResponse]
    total: int

# ==================== Document Schemas ====================

class DocumentResponse(BaseModel):
    id: int
    property_id: Optional[int]
    filename: str
    document_type: str
    file_size: int
    is_indexed: bool
    created_at: datetime

    class Config:
        from_attributes = True

class DocumentCreate(BaseModel):
    property_id: Optional[int] = None
    document_type: str  # brochure, legal, contract, report

# ==================== Investment Schemas ====================

class InvestmentAnalysis(BaseModel):
    property_id: int
    roi: float
    rental_income: float
    appreciation_rate: float
    risk_level: str  # low, medium, high
    recommendation: str

class MortgageCalculation(BaseModel):
    loan_amount: float
    annual_interest_rate: float
    loan_tenure_years: int

class MortgageResponse(BaseModel):
    monthly_emi: float
    total_amount: float
    total_interest: float

# ==================== Search Schemas ====================

class SmartSearch(BaseModel):
    query: str = Field(..., min_length=3, max_length=500)

class SearchResults(BaseModel):
    properties: List[PropertyResponse]
    total: int
    query: str

# ==================== WhatsApp Schemas ====================

class WhatsAppMessage(BaseModel):
    phone_number: str
    message: str
    property_id: Optional[int] = None

class WhatsAppResponse(BaseModel):
    success: bool
    message_sid: Optional[str] = None
    error: Optional[str] = None

# ==================== Admin Schemas ====================

class Analytics(BaseModel):
    total_properties: int
    total_users: int
    total_leads: int
    total_revenue: float
    avg_roi: float
    most_viewed_property: Optional[str]
    top_locations: List[str]

class AdminStats(BaseModel):
    date: datetime
    properties_added: int
    new_users: int
    new_leads: int
