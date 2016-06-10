from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)


class Family(Base):
    __tablename__ = 'family'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    hemisphere = Column(String(100))
    description = Column(String(250))
    picture = Column(String(100))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'hemisphere': self.hemisphere,
            'description': self.description,
            'picture': self.picture
        }


class Plant(Base):
    __tablename__ = 'plant'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    family_id = Column(Integer, ForeignKey('family.id'))
    family = relationship(Family)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
        }


engine = create_engine('sqlite:///familywithplants.db')


Base.metadata.create_all(engine)
