from pydantic import BaseModel

class SimpleObject(BaseModel):
    id: int
    name: str

    @staticmethod
    def from_db_object(db_object):
        return SimpleObject(id=db_object.id, name=db_object.name)