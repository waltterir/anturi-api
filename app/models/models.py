from sqlmodel import SQLModel, Relationship, Field

class AnturiBase(SQLModel):
    lohko_id: int
    tila: str
    mitta_tulos: int
    ajankohta: int



class LohkoBase(SQLModel):
    anturi_id: int


class LohkoDB(LohkoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    anturit: list["AnturiDB"] = Relationship(back_populates="lohko")



class AnturiDB(AnturiBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    lohko_id: int = Field(foreign_key="lohko_id")
    lohko: "LohkoDB" = Relationship(back_populates="anturit")


class AnturiOut(AnturiBase):
    id: int


class LohkoOut(LohkoBase):
    id: int
