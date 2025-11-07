from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import Base and models
from app.database import Base
from app.models import user, address
from app.database import Base
from app.models.user import User
from app.models.address import Address
from app.models.ticket import Ticket
from app.models.issue_category import IssueCategory
from app.models.assignment import Assignment
from app.models.feedback import Feedback
from app.models.sla import SLA
from app.models.ticket_action_log import TicketActionLog
from app.models.refresh_token import RefreshToken


# ✅ THIS is the correct metadata reference
target_metadata = Base.metadata

# Alembic Config object
config = context.config

# Logging setup
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ❌ REMOVE this line — it overrides your metadata!
# target_metadata = None

def run_migrations_offline() -> None:
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
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
