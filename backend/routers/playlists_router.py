from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models, schemas, auth

router = APIRouter(prefix="/playlists", tags=["playlists"])

@router.get("/", response_model=List[schemas.PlaylistResponse])
def get_playlists(db: Session = Depends(get_db)):
    return db.query(models.Playlist).all()

@router.get("/my", response_model=List[schemas.PlaylistResponse])
def get_my_playlists(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    return db.query(models.Playlist).filter(models.Playlist.user_id == current_user.id).all()

@router.get("/{playlist_id}", response_model=schemas.PlaylistResponse)
def get_playlist(playlist_id: int, db: Session = Depends(get_db)):
    playlist = db.query(models.Playlist).filter(models.Playlist.id == playlist_id).first()
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    return playlist

@router.post("/", response_model=schemas.PlaylistResponse)
def create_playlist(playlist: schemas.PlaylistCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    new_playlist = models.Playlist(title=playlist.title, user_id=current_user.id)
    db.add(new_playlist)
    db.commit()
    db.refresh(new_playlist)
    return new_playlist

@router.post("/{playlist_id}/tracks", response_model=schemas.PlaylistResponse)
def add_track_to_playlist(playlist_id: int, track_data: schemas.PlaylistAddTrack, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    playlist = db.query(models.Playlist).filter(models.Playlist.id == playlist_id).first()
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    if playlist.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this playlist")
    
    track = db.query(models.Track).filter(models.Track.id == track_data.track_id).first()
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    
    if track not in playlist.tracks:
        playlist.tracks.append(track)
        db.commit()
    
    db.refresh(playlist)
    return playlist

@router.delete("/{playlist_id}/tracks/{track_id}", response_model=schemas.PlaylistResponse)
def remove_track_from_playlist(playlist_id: int, track_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    playlist = db.query(models.Playlist).filter(models.Playlist.id == playlist_id).first()
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    if playlist.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this playlist")
    
    track = db.query(models.Track).filter(models.Track.id == track_id).first()
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    
    if track in playlist.tracks:
        playlist.tracks.remove(track)
        db.commit()
    
    db.refresh(playlist)
    return playlist

@router.delete("/{playlist_id}")
def delete_playlist(playlist_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    playlist = db.query(models.Playlist).filter(models.Playlist.id == playlist_id).first()
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    if playlist.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this playlist")
    
    db.delete(playlist)
    db.commit()
    return {"message": "Playlist deleted"}
