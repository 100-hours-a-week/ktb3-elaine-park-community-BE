from fastapi import status
from common.exceptions.BaseException import UnicornException

class InvalidLengthException(UnicornException):
    def __init__(self, message: str = "제목의 길이는 최대 26자입니다."):
        super().__init__(errorCode="POST400_1", message=message)
           
class PostNotFoundException(UnicornException):
    def __init__(self, message: str = "해당 게시글을 찾을 수 없습니다."):
        super().__init__(errorCode="POST404_1", message=message)
    
class CommentNotFoundException(UnicornException):
    def __init__(self,message:str = "해당 댓글을 찾을 수 없습니다."):
        super().__init__(errorCode="COMMENT404_1", message=message)
    
class UnauthorizedException(UnicornException):
    def __init__(self, message:str = "해당 권한을 가진 사용자가 아닙니다."):
        super().__init__(errorCode="USER403", message=message)

class UnMatchedPostCommentException(UnicornException):
    def __init__(self, message:str = "게시글 아이디와 댓글 아이디와 맞지 않습니다."):
        super().__init__(errorCode="COMMENT400_1", message=message)
        
class AlreadyEmailException(UnicornException):
    def __init__(self, message: str = "이미 존재하는 이메일입니다."):
        super().__init__(errorCode="USER409_1", message=message)

class InvalidIdPasswordException(UnicornException):
    def __init__(self, message: str = "아이디 또는 비밀번호가 잘못되었습니다."):
        super().__init__(errorCode="USER400", message=message)
        
class CredentialException(UnicornException):
    def __init__(self, message:str = "자격 증명을 검증할 수 없습니다."):
        super().__init__(errorCode="USER401", message=message)

class UserNotFoundException(UnicornException):
    def __init__(self, message:str = "해당 사용자를 찾을 수 없습니다."):
        super().__init__(errorCode="USER404", message=message)
        