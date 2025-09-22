from pydantic import BaseModel

# Respuesta User por get
class UserAuthResponse(BaseModel):
    access_token: str
    token_type: str