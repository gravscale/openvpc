import importlib
import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context
from app.config.db import Base
from app.config.settings import get_settings

settings = get_settings()


# Importando de forma dinâmica
def include_models_from_directory(directory: str):
    models = []
    sys.path.append(os.getcwd())  # Garantir que o diretório atual está no PATH
    for filename in os.listdir(directory):
        if filename.endswith("_models.py"):
            module_name_short = filename.replace("_models.py", "")
            module_name_full = f"models.{module_name_short}_models"
            # module_name_partial = f"{module_name_short}_models"

            # print("models filename: ", filename)
            # print("models module_name_short: ", module_name_short)
            # print("models module_name_partial: ", module_name_partial)
            # print("models module_name_full: ", module_name_full)

            module = importlib.import_module(f".{module_name_full}", package="app")

            model_base = getattr(module, "Base", None)
            if model_base:
                models.append(model_base)
    return models


include_models_from_directory("models")

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Set a sqlalchemy.url no objeto de configuração do Alembic
# para a URL do banco de dados importada de app.config.db
config.set_main_option("sqlalchemy.url", settings.DEFAULT_DATABASE)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Aqui você pode definir o target_metadata do seu projeto,
# importando a Base do seu módulo de definição de modelo.
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
# Por enquanto, deixaremos como None, pois não sei os detalhes dos seus modelos.
target_metadata = Base.metadata
# target_metadata = [base.metadata for base in include_models_from_directory("models")]


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
