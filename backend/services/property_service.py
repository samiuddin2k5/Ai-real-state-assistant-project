from typing import Optional, List
from sqlalchemy.orm import Session
from models import Property, PropertyFilter
from schemas import PropertyCreate, PropertyUpdate, PropertyResponse
from sqlalchemy import and_, or_

class PropertyService:
    """Service for property operations"""
    
    @staticmethod
    def create_property(db: Session, property_data: PropertyCreate, owner_id: int) -> Property:
        """Create a new property"""
        db_property = Property(
            **property_data.dict(),
            owner_id=owner_id
        )
        db.add(db_property)
        db.commit()
        db.refresh(db_property)
        return db_property
    
    @staticmethod
    def get_property(db: Session, property_id: int) -> Optional[Property]:
        """Get property by ID"""
        return db.query(Property).filter(Property.id == property_id).first()
    
    @staticmethod
    def get_all_properties(
        db: Session,
        skip: int = 0,
        limit: int = 20,
        filters: Optional[PropertyFilter] = None
    ) -> tuple[List[Property], int]:
        """Get all properties with optional filters"""
        query = db.query(Property)
        
        if filters:
            if filters.min_price:
                query = query.filter(Property.price >= filters.min_price)
            if filters.max_price:
                query = query.filter(Property.price <= filters.max_price)
            if filters.location:
                query = query.filter(Property.location.ilike(f"%{filters.location}%"))
            if filters.bedrooms:
                query = query.filter(Property.bedrooms >= filters.bedrooms)
            if filters.bathrooms:
                query = query.filter(Property.bathrooms >= filters.bathrooms)
            if filters.property_type:
                query = query.filter(Property.property_type == filters.property_type)
            if filters.status:
                query = query.filter(Property.status == filters.status)
        
        total = query.count()
        properties = query.offset(skip).limit(limit).all()
        
        return properties, total
    
    @staticmethod
    def update_property(
        db: Session,
        property_id: int,
        property_data: PropertyUpdate
    ) -> Optional[Property]:
        """Update property"""
        db_property = db.query(Property).filter(Property.id == property_id).first()
        if not db_property:
            return None
        
        update_data = property_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_property, key, value)
        
        db.add(db_property)
        db.commit()
        db.refresh(db_property)
        return db_property
    
    @staticmethod
    def delete_property(db: Session, property_id: int) -> bool:
        """Delete property"""
        db_property = db.query(Property).filter(Property.id == property_id).first()
        if not db_property:
            return False
        
        db.delete(db_property)
        db.commit()
        return True
    
    @staticmethod
    def search_by_location(
        db: Session,
        location: str,
        limit: int = 10
    ) -> List[Property]:
        """Search properties by location"""
        return db.query(Property).filter(
            Property.location.ilike(f"%{location}%")
        ).limit(limit).all()
    
    @staticmethod
    def search_by_price_range(
        db: Session,
        min_price: int,
        max_price: int,
        limit: int = 10
    ) -> List[Property]:
        """Search properties by price range"""
        return db.query(Property).filter(
            and_(
                Property.price >= min_price,
                Property.price <= max_price
            )
        ).limit(limit).all()
    
    @staticmethod
    def get_recommendations(
        db: Session,
        bedrooms: Optional[int] = None,
        max_price: Optional[int] = None,
        location: Optional[str] = None
    ) -> List[Property]:
        """Get recommended properties based on criteria"""
        query = db.query(Property).filter(Property.status == "available")
        
        if bedrooms:
            query = query.filter(Property.bedrooms >= bedrooms)
        if max_price:
            query = query.filter(Property.price <= max_price)
        if location:
            query = query.filter(Property.location.ilike(f"%{location}%"))
        
        return query.order_by(Property.expected_roi.desc()).limit(10).all()
    
    @staticmethod
    def get_similar_properties(
        db: Session,
        property_id: int,
        limit: int = 5
    ) -> List[Property]:
        """Get similar properties"""
        base_property = db.query(Property).filter(Property.id == property_id).first()
        if not base_property:
            return []
        
        return db.query(Property).filter(
            and_(
                Property.id != property_id,
                Property.property_type == base_property.property_type,
                Property.location == base_property.location
            )
        ).limit(limit).all()
    
    @staticmethod
    def get_trending_properties(db: Session, limit: int = 10) -> List[Property]:
        """Get trending properties by ROI"""
        return db.query(Property).filter(
            Property.status == "available"
        ).order_by(Property.expected_roi.desc()).limit(limit).all()
