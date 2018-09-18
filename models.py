from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils.types.choice import ChoiceType

Base = declarative_base()


class User(Base):

    __tablename__ = 'users'

    GERNDER_CHOICES = [
        (u'male', u'Male'),
        (u'female', u'Female')
    ]

    id = Column(Integer, primary_key=True)
    fullname = Column(String(255))
    age = Column(Integer)
    gender = Column(ChoiceType(GERNDER_CHOICES))
    city = Column(String(255))
    country = Column(String(255))

    @classmethod
    def gender_list(cls):
        return [x[0] for x in cls.gender.type.choices]

    def set_fullname(self, fullname):
        if len(fullname) > User.fullname.type.length:
            raise ValueError("Fullname must be shorter than {} symbols".format(User.fullname.type.length))
        else:
            self.fullname = fullname

    def set_age(self, age):
        if not age.isdigit():
            raise ValueError("Value must be number")
        else:
            self.age = age

    def set_gender(self, gender):
        if not gender in [x[0] for x in User.gender.type.choices]:
            raise ValueError("Value must be one of: " + ", ".join([x[1] for x in User.gender.type.choices]))
        else:
            self.gender = gender

    def set_city(self, city):
        if len(city) > User.city.type.length:
            raise ValueError("City must be shorter than {} symbols".format(User.city.type.length))
        else:
            self.city = city

    def set_country(self, country):
        if len(country) > User.country.type.length:
            raise ValueError("Country must be shorter than {} symbols".format(User.country.type.length))
        else:
            self.country = country

    def __repr__(self):
       return "<User({})>".format(self.fullname)
