from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwk, jwt
from jose.utils import base64url_decode
from sqlalchemy.orm import Session

from ..database.Database import get_db
from ..managers import UserManager
from ..utils.ExceptionHandlers import UnauthorizedException

security = HTTPBearer()


def authenticate(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not credentials or credentials.scheme != "Bearer":
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = credentials.credentials
    jwks_json = {
        "keys": [
            {
                "use": "sig",
                "kty": "RSA",
                "kid": "ins_2Pyo43CnU0Wv7u3O1AdWeTOpIBb",
                "alg": "RS256",
                "n": "yRACt_t1fM8gCSLzl2v9kzA8NB4_Pwdq4xJ8tg7TPSsLwc43jp9rcUnEhfdxEc5yc5AQrWtVcKhfdwbmkfl7QgKUpEaUw8SHzehIxbPCGzgs7tpR1uon3uQL5ogBh_NRBzGFfqAWlmbeCbvZHV2btA-SxPNgWuibW1l2HamQbV6sumGX8nF1h9zqddGSRlRIX8Tnmb559L-BGtc5gwAzkkr8z2BJtk0HHx1r0793Z5gRN05Qm1QbkG_WEBcVaailLeMN2-PbJfzvUCVemYxPMuXvblC5_HNHC5G16AliGmUEnA0k2ygO8z6HcTBvP3a5jjzBFpHV17dCPnPweQ_Dqw",
                "e": "AQAB",
            }
        ]
    }

    try:
        rsa_key = next(
            (
                key
                for key in jwks_json["keys"]
                if key["kid"] == jwt.get_unverified_header(token)["kid"]
            ),
            None,
        )
        if rsa_key:
            public_key = jwk.construct(rsa_key)
            message, encoded_sig = token.rsplit(".", 1)
            decoded_sig = base64url_decode(encoded_sig.encode())
            if not public_key.verify(message.encode(), decoded_sig):
                raise JWTError("Signature verification failed.")
            claims = jwt.get_unverified_claims(token)
            user_id: str = claims["sub"]
    except JWTError as e:
        raise HTTPException(status_code=401, detail=str(e))

    return user_id


def authenitcate_tutor(
    db: Session = Depends(get_db), user_id: str = Depends(authenticate)
):
    if not UserManager.is_tutor(db, user_id=user_id):
        raise UnauthorizedException(
            user_id=user_id, custom_message=f"User with id {user_id} is not a tutor."
        )

    tutor_id = user_id
    return tutor_id


def authenitcate_student(
    db: Session = Depends(get_db), user_id: str = Depends(authenticate)
):
    if UserManager.is_tutor(db, user_id=user_id):
        raise UnauthorizedException(
            user_id=user_id, custom_message=f"User with id {user_id} is not a student."
        )

    student_id = user_id
    return student_id
