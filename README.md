# py_web_HW13

poetry add sqlalchemy alembic psycopg2 uvicorn pydantic fastapi jinja2 faker libgravatar python-jose passlib python-multipart

1. in models.py add class User(Base)
2. migrations: alembic revision --autogenerate -m "add user"
    alembic upgrade heads

3. add class Role

4. add in class user:
    roles = Column('role', Enum(Role), default=Role.user)

5. alembic revision --autogenerate -m "add role of user"
    add in migrations:
        in def apgrade: op.execute("CREATE TYPE role AS ENUM('admin', 'moderator', 'user')")
        default='user'
        in def downgrade: op.execute("DROP TYPE role")

    alembic upgrade heads

6.