#!/usr/bin/python3
"""New engine DBStorage"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from models.base_model import Base
from models.amenity import Amenity
from models.city import City
from models.state import State
from models.user import User
from models.place import Place
from models.review import Review


class DBStorage:
    """DB Storage"""

    __engine = None
    __session = None

    def __init__(self):
        """init"""

        host = getenv('HBNB_MYSQL_HOST')
        database = getenv('HBNB_MYSQL_DB')
        user = getenv('HBNB_MYSQL_USER')
        passw = getenv('HBNB_MYSQL_PWD')

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            user, passw, host, database), pool_pre_ping=True)

        env = getenv('HBNB_ENV')
        if (env == 'test'):
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """all"""

        classes = {
               'User': User, 'Place': Place,
               'State': State, 'City': City, 'Amenity': Amenity,
               'Review': Review
              }
        new_dict = {}
        for clss in classes:
            if cls is None or cls == classes[clss]:
                objects = self.__session.query(classes[clss]).all()
                for obj in objects:
                    key = type(obj).__name__ + '.' + obj.id
                    new_dict[key] = obj
        return new_dict

    def new(self, obj):
        """new"""

        self.__session.add(obj)

    def save(self):
        """save"""

        self.__session.commit()

    def delete(self, obj=None):
        """delete"""

        if obj is not None:
            self.__sesion.delete(obj)

    def reload(self):
        """reload"""
        Base.metadata.create_all(self.__engine)
        create_session = sessionmaker(bind=self.__engine,
                                      expire_on_commit=False)
        Session = scoped_session(create_session)
        self.__session = Session
