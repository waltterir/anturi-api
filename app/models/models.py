from datetime import datetime
from sqlmodel import SQLModel, Relationship, Field

class AnturiBase(SQLModel):
    name: str
    lohko_id: int
    tila: str



class LohkoBase(SQLModel):
    lohko_name: str

class MittausBase(SQLModel):
    anturi_id: int
    mittaus: int
    ajankohta: datetime


class LohkoDB(LohkoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    anturi: list["AnturiDB"] = Relationship(back_populates="lohko")



class AnturiDB(AnturiBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    lohko_id: int = Field(foreign_key="lohko.id")
    lohko: "LohkoDB" = Relationship(back_populates="anturi")
    mittaus_tulos: list["MittausDB"] = Relationship(back_populates="anturi")

class MittausDB(MittausBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    anturi_id: int = Field(foreign_key="anturi.id")
    anturi: "AnturiDB" = Relationship(back_populates="mittaus_tulos")


class MittausOut(MittausBase):
    id: int


class AnturiOut(AnturiBase):
    id: int


class LohkoOut(LohkoBase):
    id: int

class AnturiMittausResponse(SQLModel):
    anturi: AnturiOut
    mittaukset: list[MittausOut]
