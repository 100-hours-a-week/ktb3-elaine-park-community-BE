from typing import List, Dict, Any
from datetime import datetime

POST_DB : List[Dict[str, Any]] = [
    {"id" : 1, 
     "userId" : 1, 
     "title" : "제목1", 
     "content" : "내용1", 
     "imageId": 1, 
     "createdAt": datetime.now(),
     "updatedAt" : datetime.now(),
     "likesCnt" : 0,
     "viewsCnt" : 0,
     "commentCnt" : 0,
     "comments" : []
     },
    {"id" : 2, 
     "userId" : 1, 
     "title" : "제목2", 
     "content" : "내용2", 
     "imageId": 0, 
     "createdAt": datetime.now(),
     "updatedAt" : datetime.now(),
     "likesCnt" : 0,
     "viewsCnt" : 0,
     "commentCnt" : 0,
     "comments" : []
     },
]

COMMENT_DB : List[Dict[str, Any]] = [
    {"id" : 1, 
     "author" : {
         "userId" : 1,
         "nickname" : "작성자1",
     },
     "postId" : 1,
     "content" : "댓글내용1",
     "createdAt" : datetime.now()
    },
    {"id" : 2,
     "author" : {
         "userId" : 1,
         "nickname" : "작성자1"
    },
     "postId" : 2,
     "content" : "댓글내용2",
     "createdAt" : datetime.now()
    }
]

USER_DB : List[Dict[str, Any]] = []
LIKES_DB : List[Dict[str, Any]] = []
IMAGE_DB : List[Dict[str, Any]] = []

NEXT_USER_ID = 1
NEXT_POST_ID = 3
NEXT_LIKES_ID = 1
NEXT_COMMENT_ID = 3
NEXT_IMAGE_ID = 1