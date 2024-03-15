from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel, ConfigDict, Field, field_validator
from pydantic_core.core_schema import ValidationInfo


class CredentialBase(BaseModel):
    name: str = Field(..., description="Unique name for the credential")
    username: str = Field(..., description="Username associated with the credential")
    password: Optional[str] = Field(None, description="Password if applicable")
    private_key: Optional[str] = Field(None, description="Private key if applicable")

    @field_validator("private_key", "password")
    def check_either_private_key_or_password(cls, v, info: ValidationInfo):
        if "private_key" in info.data and "password" in info.data:
            raise ValueError("Provide either private_key or password, not both")
        return v


class CredentialCreate(CredentialBase):
    pass


class CredentialUpdate(CredentialBase):
    pass


class CredentialRead(CredentialBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4 = Field(..., description="Unique identifier for the credential")
    is_active: bool = Field(True, description="Active status of the credential")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    deleted_at: Optional[datetime] = Field(None, description="Deletion timestamp")
