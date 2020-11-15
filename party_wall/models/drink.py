from sqlalchemy import Column, Float, Integer, String, Text

from party_wall.models.base import BaseModel


class DrinkModel(BaseModel):
    __tablename__ = "drink"

    name = Column(String(255), unique=True, nullable=False)
    price = Column(Float(precision=2), nullable=False)
    quantity = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    volume = Column(Float(precision=3), nullable=False)

    def __repr__(self):
        return (
            "Drink("
            f"id='{self.id!s}', "
            f"name={self.name!r}, "
            f"price={self.price!r}, "
            f"quantity={self.quantity!r}, "
            f"description={self.description!r}, "
            f"volume={self.volume!r}"
            ")"
        )
