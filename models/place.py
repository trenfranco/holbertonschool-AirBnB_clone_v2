#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Table
from sqlalchemy.orm import relationship
from models.review import Review
import os


if os.getenv('HBNB_TYPE_STORAGE') == 'db':
    place_amenity = Table("place_amenity", Base.metadata,
                          Column("place_id", String(60),
                                 ForeignKey("places.id"),
                                 primary_key=True),
                          Column("amenity_id", String(60),
                                 ForeignKey("amenities.id"),
                                 primary_key=True))


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':

        city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        amenity_ids = []

        reviews = relationship('Review', backref='place',
                               cascade='all, delete-orphan')
        r_amenities = relationship("Amenity",  secondary="place_amenity",
                                   viewonly=False)
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            list_reviews = []
            for key, value in models.storage.all(Review).items():
                if self.id == value.place_id:
                    list_reviews.append(value)
            return list_reviews

        """Getter task 10"""
        @property
        def amenities(self):
            """obtenemos la lista de instances"""
            return self.r_amenities
        """Setter task 10"""
        @amenities.setter
        def amenities(self, obj=None):
            """seteamos atributos de amenities"""
            list_ams = []
            if type(obj) == "Amenity":
                list_ams.append(obj)
