from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel, ConfigDict, Field, model_validator

from .constants import ErrorCode


class CredentialBase(BaseModel):
    name: str = Field(..., description="Unique name for the credential")
    username: str = Field(..., description="Username associated with the credential")
    password: Optional[str] = Field(None, description="Password if applicable")
    private_key: Optional[str] = Field(None, description="Private key if applicable")


class CredentialCreate(CredentialBase):
    @model_validator(mode="after")
    def check_either_private_key_or_password(self):
        if self.password and self.private_key:
            raise ValueError(ErrorCode.PRIVATE_KEY_AND_PASSWORD_PROVIDED)
        return self


class CredentialUpdate(CredentialCreate):
    pass


class CredentialResponse(CredentialBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4 = Field(..., description="Unique identifier for the credential")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
