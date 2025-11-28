from typing import Dict, Any, List
from common.exceptions.customException import InvalidLengthException
from common.apiResponse import CommonResponse

# DB 역할
DUMMY_DB : List[Dict[str, Any]] = [
    {"postId" : 1, "title" : "제목1", "content" : "내용1", "imageId": 1},
    {"postId" : 2, "title" : "제목2", "content" : "내용2", "imageId": 0},
]
NEXT_ID = 3

def create_post(title: str, content: str, image_id : int) -> Dict[str, Any]:
    global NEXT_ID
        
    if len(title) > 26:
        raise InvalidLengthException("제목의 길이는 26자를 초과할 수 없습니다.")
    
    new_post = {
        "postId" : NEXT_ID,
        "title" : title,
        "content" : content,
        "imageId" : image_id
    }
    
    DUMMY_DB.append(new_post)
    NEXT_ID += 1
    
    return new_post