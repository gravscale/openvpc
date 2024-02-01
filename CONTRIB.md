# CONTRIBUTING.md

## OpenVPC Project Structure Overview

- **`models/`**: Contains SQLAlchemy models representing database tables.
- **`schemas/`**: Includes Pydantic schemas for data validation and serialization.
- **`crud/`**: CRUD operations files for database interaction.
- **`routes/`**: FastAPI routes for handling HTTP requests and responses.
- **`main.py`**: Application entry point, FastAPI setup, and automatic routing.
- **`alembic/`**: Database migration configurations.

## Coding Style Guidelines

- **Consistency and Clarity**: Code should be clean and consistent, following naming conventions (CamelCase for classes, snake_case for variables and functions).
- **Comments**: Comments should be clear, useful, and in English. Document classes, functions, and complex code blocks.
- **Function Documentation**: Include docstrings in all functions and methods, explaining the purpose, parameters, and return type.
- **Validations**: Use Pydantic validations to ensure data integrity.
- **Error Handling**: Implement exception handling to manage errors appropriately.
- **Testing**: Write unit and integration tests for critical and common use cases.

## Development Process

- **Branches and Pull Requests**: Use branches for new features or fixes. Create pull requests for review before merging into the main branch.
- **Code Reviews**: Request code reviews to ensure quality and adherence to best practices.
- **Database Migrations**: Use Alembic for database migrations. Ensure migrations are backward compatible when possible.
- **Code Updates**: Keep the code up-to-date with the latest practices and libraries.

## File Naming Conventions

- **Models**: `model_name_models.py` (e.g., `router_models.py`)
- **Schemas**: `model_name_schemas.py` (e.g., `router_schemas.py`)
- **CRUD**: `model_name_crud.py` (e.g., `router_crud.py`)
- **Routes**: `model_name_routes.py` (e.g., `router_routes.py`)

## Example File Creation

### Models
```python
# router_models.py
from sqlalchemy import Column, String
from .database import Base

class Router(Base):
    __tablename__ = 'router'
    id = Column(String, primary_key=True)
    # Additional fields...
```

### Schemas
```# router_schemas.py
from pydantic import BaseModel

class RouterBase(BaseModel):
    name: str
    # Additional fields...

```


### CRUD Operations
```
# router_crud.py
from .models.router_models import Router
# CRUD functions...
```


### Routes
```
# router_routes.py
from fastapi import APIRouter
from ..schemas.router_schemas import RouterBase
router = APIRouter()
# API route definitions...
```


## Useful Commands in Makefile
- **make alembic-revision MESSAGE="Your message"**: Creates an Alembic revision with the specified message.
- **make alembic-current**: Shows the current Alembic revision.
- **make alembic-history**: Shows the history of Alembic revisions.
- **make alembic-apply**: Applies the latest Alembic revision.
- **make run**: Runs the Uvicorn server.
- **make mysql**: Connects to the MySQL database.
- **make guidelines**: Shows the contribution guidelines for OpenVPC.

## Submitting Contributions
1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Write your code following the guidelines.
4. Ensure your code passes all tests and adheres to the coding style.
5. Submit a pull request for review.
6. Your contributions are greatly appreciated and will be thoroughly reviewed before merging.
