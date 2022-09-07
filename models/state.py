#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv
from models.city import City


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    if (getenv("HBNB_TYPE_STORAGE") == "db"):
        cities = relationship("City", backref="state", cascade="all, \
                              delete-orphan")
    else:
        @property
        def cities(self):
            from models import storage
            all_cities = storage.all(City).values()

            new_list = []
            for city in all_cities:
                if (city.state_id == self.id):
                    new_list.append(city)
            return new_list
