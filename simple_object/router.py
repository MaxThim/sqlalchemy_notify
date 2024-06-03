from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from shared.database import get_db, notify_channel
from simple_object.models import SimpleOBjectDB
from simple_object.schemas import SimpleObject

router = APIRouter(
    prefix="/simple_object",
    tags=["simple_object"],
)

@router.get("/", response_model=list[SimpleObject])
async def get_objects(db: Session = Depends(get_db)):
    return [SimpleObject.from_db_object(obj) for obj in db.query(SimpleOBjectDB).all()]

@router.get("/{object_id}", response_model=SimpleObject)
async def get_object(object_id: int, db: Session = Depends(get_db)):
    return SimpleObject.from_db_object(db.query(SimpleOBjectDB).get(object_id))

@router.post("/", response_model=SimpleObject)
async def create_object(obj: SimpleObject, db: Session = Depends(get_db)):
    db_obj = SimpleOBjectDB(**obj.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    notify_channel(db, 'object_changes', f'CREATE {db_obj.id}')
    return SimpleObject.from_db_object(db_obj)

@router.put("/{object_id}", response_model=SimpleObject)
async def update_object(object_id: int, obj: SimpleObject, db: Session = Depends(get_db)):
    db_obj = db.query(SimpleOBjectDB).get(object_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail=f"Todo not found with id: {object_id}")
    for key, value in obj.model_dump().items():
        setattr(db_obj, key, value)
    db.commit()
    db.refresh(db_obj)
    notify_channel(db, 'object_changes', f'UPDATE {db_obj.id}')
    return SimpleObject.from_db_object(db_obj)

@router.delete("/{object_id}")
async def delete_object(object_id: int, db: Session = Depends(get_db)):
    db_obj = db.query(SimpleOBjectDB).get(object_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail=f"Todo not found with id: {object_id}")
    db.delete(db_obj)
    db.commit()
    notify_channel(db, 'object_changes', f'DELETE {object_id}')
    return {"message": "Object deleted successfully"}

