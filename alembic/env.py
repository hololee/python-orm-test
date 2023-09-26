import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlalchemy import text
from sqlalchemy.schema import CreateSchema
from sqlalchemy.schema import CreateTable
from sqlalchemy.schema import MetaData

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# alembic.ini 파일의 sqlalchemy.url 속성을 동적으로 할당.
# sqlalchemy.url = postgresql://postgres:postgres@127.0.0.1:54321/db
'''
export ALEMBIC_ENGIN=postgresql ALEMBIC_USER_NAME=postgres ALEMBIC_PASSWORD=postgres ALEMBIC_HOST=127.0.0.1 ALEMBIC_PORT=54321 ALEMBIC_DB_NAME=db
'''
if not config.get_main_option('sqlalchemy.url'):
    config.set_main_option(
        'sqlalchemy.url',
        f'{os.environ["ALEMBIC_ENGIN"]}://{os.environ["ALEMBIC_USER_NAME"]}:{os.environ["ALEMBIC_PASSWORD"]}@{os.environ["ALEMBIC_HOST"]}:{os.environ["ALEMBIC_PORT"]}/{os.environ["ALEMBIC_DB_NAME"]}',
    )

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = None

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

target_schema = config.get_main_option('script_location')
target_ddl_path = config.get_main_option('ddl_path')


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
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=True,
            version_table_schema=target_schema,
        )

        if context.get_revision_argument() == 'init':
            # init argument로 넘어오는 경우 db 초기화 실행.
            head_revision_hash = context.get_head_revision()

            # alembic 버전 관리 테이블 복구.
            if not connection.dialect.has_schema(connection, target_schema):
                connection.execute(CreateSchema(target_schema))
                connection.execute(
                    text(
                        f'CREATE TABLE {target_schema}.alembic_version (version_num character varying(32) PRIMARY KEY);'
                    )
                )
                connection.execute(
                    text(f"INSERT INTO {target_schema}.alembic_version (version_num) VALUES ('{head_revision_hash}');")
                )

            # latest db 복구.
            with open(os.path.join(target_schema, target_ddl_path, f'post-{head_revision_hash}.sql')) as file:
                connection.execute(text(file.read()))

            connection.commit()
            connection.close()

        else:
            # upgrade or downgrade.
            if not connection.dialect.has_schema(connection, 'alembic'):
                connection.execute(CreateSchema('alembic'))  # 없는 경우 에러 발생 방지.

            with context.begin_transaction():
                context.run_migrations()

            # DDL 출력.
            get_current_revision = context.get_context().get_current_revision
            current_revision_hash = get_current_revision() if get_current_revision() is not None else 'base'

            meta = MetaData()
            meta.reflect(bind=connectable)

            ddl_path = os.path.join(target_schema, target_ddl_path)
            if not os.path.isdir(ddl_path):
                os.mkdir(ddl_path)

            # 해당 revision을 수행했을때의 구조 쓰기.
            with open(os.path.join(ddl_path, f'post-{current_revision_hash}.sql'), 'w') as file_ddl:
                for table in meta.sorted_tables:
                    print(str(CreateTable(table).compile(connectable)).rstrip() + ';', file=file_ddl)


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
