from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import SessionLocal, get_db
from . import schemas
from . import crud

router = APIRouter()

# Endpoint to create a subscription
@router.post("/create/", response_model=schemas.Subscription)
def create_new_subscription(db: Session = Depends(get_db), 
                        username: str = None, 
                        categories: dict = None):
    
    # Get or create the user
    user = get_or_create_user(db, username=username)

    # Create the subscription
    for category in categories:
        category = get_or_create_category(db, name=category)
        
        subscription = crud.get_subscriptions_by_username_and_category_id(db, username=username, category_id=category.id)
        if subscription:
            continue
        subscription = crud.create_subscription(db, username=username, category_id=category.id)
    
    return {"message": "Subscription created successfully"}


# Endpoint to update User Firebase Token
@router.put("/update-token/", response_model=schemas.DeviceToken)
def update_user_token(db: Session = Depends(get_db), 
                        username: str = None, 
                        token: str = None):
    
    # Get or create the user
    user = get_or_create_user(db, username=username)

    # Update the device token
    device_token = crud.get_device_token_by_user_id(db, user_id=user.id)
    if device_token:
        device_token = crud.update_device_token(db, user_id=user.id, token=token)
    else:
        device_token = crud.create_device_token(db, user_id=user.id, token=token)

def get_or_create_user(db: Session, username: str):
    """
    Get or create a user
    """
    user = crud.get_user_by_username(db, username=username)
    if user:
        return user
    return crud.create_user(db, username=username)

def get_or_create_category(db: Session, name: str):
    """
    Get or create a category
    """
    category = crud.get_category_by_name(db, name=name)
    if category:
        return category
    return crud.create_category(db, name=name)