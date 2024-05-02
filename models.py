from config import bcrypt, db
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.hybrid import hybrid_property  #for password hashing


class Vendor(db.Model, SerializerMixin):
    pass