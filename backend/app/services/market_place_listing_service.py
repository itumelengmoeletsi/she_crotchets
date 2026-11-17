from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.marketplace_listing import MarketplaceListing
from app.models.museum_listings import MuseumListing
from app.schemas.marketplace_listing_schema import MarketplaceListingCreate, MarketplaceListingUpdate

def create_marketplace_listing(db: Session, list_item: MarketplaceListingCreate, museum_listing_id: int, user_id: int):
    # 1. verify that museum item exists
    museum_item = db.query(MuseumListing).filter(
        MuseumListing.id == museum_listing_id,
        MuseumListing.user_id == user_id
    ).first()

    if not museum_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Museum listing not found or access denied."
        )

    # 2. ensure 1-to-1 unique constraint is enforced
    existing_listing = db.query(MarketplaceListing).filter(MarketplaceListing.museum_item_id == museum_listing_id).first()

    if existing_listing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This museum item has already been listed on the market"
        )

    # 3 unpack validated 
    new_listing = MarketplaceListing(
        **list_item.model_dump(), 
        museum_item_id=museum_listing_id,
    )

    db.add(new_listing)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error while creating marketplace listing"
        )

    db.refresh(new_listing)
    return new_listing

def update_marketplace_listing(db: Session, marketplace_id: int, list_item: MarketplaceListingUpdate, user_id: int):
    # join with museumlisting to verify user ownership
    market_listing = (
        db.query(MarketplaceListing)
        .join(MuseumListing, MarketplaceListing.museum_item_id == MuseumListing.id)
        .filter(
            MarketplaceListing.id == marketplace_id,
            MuseumListing.user_id == user_id
        )
        .first()
    )

    if not market_listing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            details="Marketplace listing not found or access denied."
        )

    update_data = list_item.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(market_listing, key, value)

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error while updating marketplace listing."
        )

    db.refresh(market_listing)
    return market_listing

