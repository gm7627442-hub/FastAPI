from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import crud, schemas

app = FastAPI(title="User Profiles API")

@app.post("/profiles", response_model=schemas.UserProfileResponse, status_code=status.HTTP_201_CREATED)
def create_profile(profile: schemas.UserProfileCreate, db: Session = Depends(get_db)):
    return crud.create_profile(db=db, profile=profile)

@app.get("/profiles", response_model=list[schemas.UserProfileResponse])
def read_profiles(age: int | None = None, db: Session = Depends(get_db)):
    return crud.get_profiles(db=db, age=age)

@app.get("/profiles/{id}", response_model=schemas.UserProfileResponse)
def read_profile(id: int, db: Session = Depends(get_db)):
    db_profile = crud.get_profile_by_id(db=db, profile_id=id)
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile

@app.put("/profiles/{id}", response_model=schemas.UserProfileResponse)
def update_profile(id: int, profile: schemas.UserProfileUpdate, db: Session = Depends(get_db)):
    db_profile = crud.update_profile(db=db, profile_id=id, profile_data=profile)
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile

@app.delete("/profiles/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_profile(id: int, db: Session = Depends(get_db)):
    success = crud.delete_profile(db=db, profile_id=id)
    if not success:
        raise HTTPException(status_code=404, detail="Profile not found")
    return None
