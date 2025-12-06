from pydantic import BaseModel

#Entity 역할
class LikesModel(BaseModel):
    id : int
    post_id : int
    user_id : int
    likesCnt : int = 0