from pydantic import BaseModel, ConfigDict

orm_config = ConfigDict(from_attributes=True)

class TagBase(BaseModel):
    name: str

class TagCreateRequest(TagBase):
    pass

class TagUpdateRequest(TagBase):
    pass

class TagResponse(TagBase):
    model_config = orm_config
    id: int