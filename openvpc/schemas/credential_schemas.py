from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator
from pydantic_core.core_schema import FieldValidationInfo


class CredentialBase(BaseModel):
    name: str = Field(..., description="Unique name for the credential")
    user: str = Field(..., description="Username associated with the credential")
    private_key: Optional[str] = Field(None, description="Private key if applicable")
    password: Optional[str] = Field(None, description="Password if applicable")

    @field_validator("private_key", "password")
    def check_either_private_key_or_password(cls, v, info: FieldValidationInfo):
        if "private_key" in info.data and "password" in info.data:
            raise ValueError("Provide either private_key or password, not both")
        return v


class CredentialCreate(CredentialBase):
    pass


class CredentialUpdate(CredentialBase):
    pass


class CredentialRead(CredentialBase):
    id: str = Field(..., description="Unique identifier for the credential")
    is_active: bool = Field(True, description="Active status of the credential")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    deleted_at: Optional[datetime] = Field(None, description="Deletion timestamp")
