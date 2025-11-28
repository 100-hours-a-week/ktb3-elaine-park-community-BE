from fastapi import status
from common.exceptions.BaseException import UnicornException

class InvalidLengthException(UnicornException):
    def __init__(self, message: str = "제목의 길이는 최대 26자입니다."):
        super().__init__(errorCode="POST400_1", message=message)
 
class FieldRequiredException(UnicornException):
    def __init__(self, message: str = "제목과 내용은 필수입니다."):
        super().__init__(errorCode="POST400_2", message=message)
           
class NotFoundException(UnicornException):
    def __init__(self, message: str = "해당 게시글을 찾을 수 없습니다."):
        super().__init__(errorCode="POST404_2", message=message)
        