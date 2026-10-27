from sqlalchemy.orm import Session
import models, schemas

def get_profiles(db: Session, age: int | None = None):
    query = db.query(models.UserProfile)
    if age is not None:
        query = query.filter(models.UserProfile.age == age)
    return query.all()

def get_profile_by_id(db: Session, profile_id: int):
    return db.query(models.UserProfile).filter(models.UserProfile.id == profile_id).first()

def create_profile(db: Session, profile: schemas.UserProfileCreate):
    db_profile = models.UserProfile(
        username=profile.username,
        email=profile.email,
        age=profile.age
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

def update_profile(db: Session, profile_id: int, profile_data: schemas.UserProfileUpdate):
    db_profile = get_profile_by_id(db, profile_id)
    if db_profile:
        db_profile.username = profile_data.username
        db_profile.email = profile_data.email
        db_profile.age = profile_data.age
        db.commit()
        db.refresh(db_profile)
    return db_profile

def delete_profile(db: Session, profile_id: int):
    db_profile = get_profile_by_id(db, profile_id)
    if db_profile:
        db.delete(db_profile)
        db.commit()
        return True
    return False
