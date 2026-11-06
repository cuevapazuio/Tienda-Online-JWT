from sqlmodel import SQLModel, Field


class UsuarioCreate(SQLModel):
    username: str = Field(
        min_length=3,
        max_length=50
    )

    email: str = Field(
        min_length=5,
        max_length=120
    )

    password: str = Field(
        min_length=6,
        max_length=100
    )


class UsuarioLogin(SQLModel):
    username: str
    password: str


class UsuarioRead(SQLModel):
    id: int
    username: str
    email: str


class Token(SQLModel):
    access_token: str
    token_type: str