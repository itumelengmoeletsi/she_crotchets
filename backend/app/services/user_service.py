from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.users import User
from app.schemas.user_schema import UserCreate, UserUpdate

def create_user(db: Session, user_data: UserCreate):
    existing_user = db.query(User).filter(User.email == user_data.email).first()

    if existing_user: 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists."
        )

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=user_data.password_hash
    )

    # Save to database
    db.add(new_user)
    try:
        db.commit()
    except Exception as e: 
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error during registration."
        )
    db.refresh(new_user)

    return new_user

def update_user(db: Session, user_id: int, user_data: UserUpdate):
    # fetch user
    user = db.query(User).filter(User.id == user_id).first()

    if not user: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    # update only provided fields
    update_data = user_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(user, key, value)

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error during update."
        )

    db.refresh(user)
    return user

    # add user verification here later


