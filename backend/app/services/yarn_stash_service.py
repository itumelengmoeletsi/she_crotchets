from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.yarn_stash import YarnStash
from app.schemas.yarn_stash_schema import YarnStashCreate, YarnStashUpdate

def create_yarn_stash(db: Session, stash: YarnStashCreate, stash_id: int, user_id: int):
    new_stash = YarnStash(
        **stash.model_dump(),
        user_id=user_id
    )

    db.add(new_stash)
    try:
        db.commit()
    except Exception:
        HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error while creating new stash"
        )
    db.refresh(new_stash)
    return new_stash

def update_yarn_stash(db: Session, stash_id: int, stash_data: YarnStashUpdate, user_id: int):
    stash_item = db.query(YarnStash).filter(
        YarnStash.id == stash_id,
        YarnStash.user_id == user_id
    ).first()

    if not stash_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Yarn stash item not found or acces denied."
        )

    update_data = stash_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(stash_item, key, value)

    try:
        db.commit()
    except Exception:
        HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Databse error while updating yarn stash."
        )

    db.refresh(stash_item)
    return stash_item