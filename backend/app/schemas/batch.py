from pydantic import BaseModel


class BatchCreate(BaseModel):
    name: str
    institution_id: int


class InviteResponse(BaseModel):
    token: str

class JoinBatchRequest(BaseModel):
    token: str