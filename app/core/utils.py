from uuid import UUID

from fastapi import HTTPException


# Helper function to validate UUID format
async def validate_uuid(uuid_str: str):
    try:
        UUID(uuid_str)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format.")
