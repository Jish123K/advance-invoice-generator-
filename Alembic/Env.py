import logging

from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

from alembic import context

from app.models import Base

from app.config import settings

# Configure logging

logging.basicConfig()

logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Create a database engine

engine = create_engine(

    f'postgresql+psycopg2://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}',

    echo=True  # Enable logging

)

# Create a session factory

Session = sessionmaker(bind=engine)

# Set the target metadata

target_metadata = Base.metadata

def run_migrations_offline():

    """Run migrations in 'offline' mode."""

    url = str(engine.url)

    context.configure(

        url=url,

        target_metadata=target_metadata,

        literal_binds=True,

        dialect_opts={"paramstyle": "named"},

    )

    with context.begin_transaction():

        context.run_migrations()

def run_migrations_online():

    """Run migrations in 'online' mode."""

    with engine.connect() as connection:

        context.configure(

            connection=connection, target_metadata=target_metadata

        )

        with context.begin_transaction():

            context.run_migrations()

if context.is_offline_mode():

    run_migrations_offline()

else:

    run_migrations_online()

