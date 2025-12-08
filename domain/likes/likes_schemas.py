from pydantic import BaseModel

#Entity 역할
class LikesResponse(BaseModel):
    flag : str
    likesCnt : int = 0