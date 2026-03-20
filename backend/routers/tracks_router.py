from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models, schemas, auth

router = APIRouter(prefix="/tracks", tags=["tracks"])

@router.get("/", response_model=List[schemas.TrackResponse])
def get_tracks(db: Session = Depends(get_db)):
    return db.query(models.Track).all()

@router.post("/", response_model=schemas.TrackResponse)
def create_track(track: schemas.TrackCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    new_track = models.Track(title=track.title, duration=track.duration, author_id=current_user.id)
    db.add(new_track)
    db.commit()
    db.refresh(new_track)
    return new_track
