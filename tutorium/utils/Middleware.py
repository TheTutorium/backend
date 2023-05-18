from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwk, jwt
from jose.utils import base64url_decode

security = HTTPBearer()


# Define a dependency that handles authentication
def authenticate(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # Implement your authentication logic here
    # You can check the credentials and perform any necessary validation
    # For example, you might validate JWT tokens or check username/password

    # If authentication fails, raise an HTTPException with appropriate status code and message
    if not credentials or credentials.scheme != "Bearer":
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # If authentication succeeds, you can return the authenticated user or any other relevant data
    # In this example, we are simply returning the username
    token = credentials.credentials
    jwks_json = {
        "keys": [
            {
                "use": "sig",
                "kty": "RSA",
                "kid": "ins_2PPaXNxTm0wHzWn7a6i2pvqv2zb",
                "alg": "RS256",
                "n": "taknl1HbKQCfX2j3bM7l84ONSjaQp2Z3lZ9Cj9nnAkMYfMJL1N5rt0pQtEx4h1Fauujr2_oeQwiyRZ6LfH9qU7Jsq95Ay5M-uW01GwduWRebL64LJu4rWVKpa79dBuIV9gZVsDxc-khXKBrblZLhYonSrMmdCl2wdBhC5Un9RQIH21FL-nujVk1HO6dVUGKmAGUTmvHdY-9SZ46PkLI2i9b8LjfUKt9QgGrlLUJL31PKCYf6oRb8J4DT_ED9QhtmbcTWL0qrGTG-yX7uh1gFSHAgsXSVceOFge0PwL1SR1EoAmMt47Tm3wJkydQbshXztZ-OKf5FCbxxt41KZzAvGQ",
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
