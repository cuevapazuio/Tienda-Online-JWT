from sqlmodel import SQLModel, Field


class Usuario(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    username: str = Field(
        min_length=3,
        max_length=50,
        index=True
    )

    email: str = Field(
        min_length=5,
        max_length=120,
        index=True
    )

    password_hash: str