from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from auth import get_current_user, get_current_admin
from models import User, ChatMessage, Document
from schemas import ChatMessage as ChatSchema, ChatResponse, ChatHistory
from services.rag_system import rag_system
import json

router = APIRouter(prefix="/api/chat", tags=["chat"])

@router.post("/", response_model=ChatResponse)
async def send_message(
    chat_msg: ChatSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Send message to AI chatbot"""
    try:
        # Get response from RAG system
        ai_response = rag_system.query(chat_msg.message, chat_msg.context)
        
        # Save to database
        db_message = ChatMessage(
            user_id=current_user.id,
            message=chat_msg.message,
            response=ai_response,
            context=chat_msg.context,
            is_from_user=True
        )
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        
        return db_message
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing message: {str(e)}"
        )

@router.get("/history", response_model=ChatHistory)
async def get_chat_history(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's chat history"""
    messages = db.query(ChatMessage).filter(
        ChatMessage.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    
    total = db.query(ChatMessage).filter(
        ChatMessage.user_id == current_user.id
    ).count()
    
    return {
        "messages": messages,
        "total": total
    }

@router.delete("/{message_id}")
async def delete_message(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a chat message"""
    message = db.query(ChatMessage).filter(
        ChatMessage.id == message_id,
        ChatMessage.user_id == current_user.id
    ).first()
    
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    
    db.delete(message)
    db.commit()
    
    return {"success": True, "message": "Message deleted"}

@router.delete("/")
async def clear_chat_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Clear all chat history for user"""
    db.query(ChatMessage).filter(
        ChatMessage.user_id == current_user.id
    ).delete()
    db.commit()
    
    return {"success": True, "message": "Chat history cleared"}

@router.post("/property/{property_id}")
async def chat_about_property(
    property_id: int,
    chat_msg: ChatSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Chat about specific property"""
    from models import Property
    
    # Get property
    property = db.query(Property).filter(Property.id == property_id).first()
    if not property:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    
    # Get property context
    property_context = {
        "id": property.id,
        "title": property.title,
        "price": property.price,
        "location": property.location,
        "bedrooms": property.bedrooms,
        "bathrooms": property.bathrooms,
        "area_sqft": property.area_sqft,
        "property_type": property.property_type
    }
    
    # Get response from RAG with property context
    ai_response = rag_system.query(chat_msg.message, property_context)
    
    # Save message
    db_message = ChatMessage(
        user_id=current_user.id,
        message=chat_msg.message,
        response=ai_response,
        context=json.dumps(property_context),
        is_from_user=True
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    
    return db_message
