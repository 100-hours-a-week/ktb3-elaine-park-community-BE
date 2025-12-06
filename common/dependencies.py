from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from common.security import SECRET_KEY, ALGORITHM
from domain.user.user_controller import USER_DB
from common.exceptions.customException import CredentialException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

async def get_current_user_id(token:str = Depends(oauth2_scheme)) -> int:
    credentials_exception = CredentialException("자격 증명을 검증할 수 업습니다.")
    
    try :
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id_str: str = payload.get("sub")
        
        if user_id_str is None:
            raise credentials_exception
        
        user_id = int(user_id_str)
    
    except JWTError:
        raise credentials_exception
    
    return user_id