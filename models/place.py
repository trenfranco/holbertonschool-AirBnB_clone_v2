#!/usr/bin/python3
""" Place Module for HBNB project """
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship

place_amenity = Table('place_amenity', Base.metadata, Column('place_id',
                      String(60), ForeignKey('places.id', onupdate='CASCADE',
                                             ondelete='CASCADE'),
                                             primary_key=True),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id', onupdate='CASCADE',
                                        ondelete='CASCADE'), primary_key=True))

class Place(BaseModel, Base):
    """ Class Place """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        reviews = relationship("Review", cascade="all, delete-orphan",
                               backref='place')
        amenities = relationship("Amenity", secondary=place_amenity,
                                 backref="places", viewonly=False)
    else:
        @property
        def reviews(self):
            """getter Review """
            from models.review import Review
            review_list = []
            all_reviews = models.storage.all(Review)
            for review in all_reviews.values():
                if review.place_id == self.id:
                    review_list.append(models.storage.all(Review)[review])
            return review_list

        @property
        def amenities(self):
            """getter  am"""
            from models.amenity import Amenity
            amenity_list = []
            all_amenities = models.storage.all(Amenity)
            for amenity in all_amenities.values():
                if amenity.place_id == self.id:
                    amenity_list.append(models.storage.all(Amenity)[amenity])
            return amenity_list	

        @amenities.setter
        def amenities(self, amenity_object):
            if type(amenity_object).__name__ == "Amenity":
                self.amenity_ids.append(amenity_object.id)
