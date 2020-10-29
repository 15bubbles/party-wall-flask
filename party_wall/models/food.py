from party_wall.models.base import BaseModel
from sqlalchemy import Column, String, Text, Integer, Float


class FoodModel(BaseModel):
    __tablename__ = "food"

    name = Column(String(255), unique=True, nullable=False)
    price = Column(Float(precision=2), nullable=False)
    quantity = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    weight = Column(Float(precision=3), nullable=False)

    def __repr__(self):
        return (
            "Food("
            f"id='{self.id!s}', "
            f"name={self.name!r}, "
            f"price={self.price!r}, "
            f"quantity={self.quantity!r}, "
            f"description={self.description!r}, "
            f"weight={self.weight!r}"
            ")"
        )
