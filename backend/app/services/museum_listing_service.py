from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.museum_listings import MuseumListing
from app.models.projects import Project
from app.schemas.museum_listing_schema import MuseumListingCreate, MuseumListingUpdate

def create_museum_listing(db: Session, listing: MuseumListingCreate, project_id: int, user_id: int):
    # 1. verify that the project exists and belongs to the user
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == user_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projct not found or access denied"
        )

    # 2. enforce the 1-to-1 unique constrain cleanly before inserting
    existing_listing = db.query(MuseumListing).filter(MuseumListing.project_id == project_id).first()

    if existing_listing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="THis project has already been published to the museum."
        )

    # 3. unpack validated schema fields and attach project_id + user_id
    new_listing = MuseumListing(
        **listing.model_dump(),
        project_id=project_id,
        user_id=user_id
    )

    db.add(new_listing)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error while creating museum listing"
        )

    db.refresh(new_listing)
    return new_listing

def update_museum_listing(db: Session, listing_id: int, listing_data: MuseumListingUpdate, user_id: int):
    # fetch listing and verify ownership directily via MuseumListing.user_id
    listing = db.query(MuseumListing).filter(
        MuseumListing.id == listing_id,
        MuseumListing.user_id == user_id
    ).first()

    if not listing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=""
        )

    update_data = listing_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(listing, key, value)

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=""
        )

    db.refresh(listing)
    return listing
