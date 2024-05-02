from config import bcrypt, db
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property  #for password hashing


class Vendor(db.Model, SerializerMixin):
    __tablename__ = "vendors"
    serialize_rules = ('-vendor_sweets.vendor')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # Relationship with sweets through vendor_sweets
    sweets = db.relationship("Sweet", secondary='vendor_sweets', back_populates="vendors", overlaps='vendor_sweets')
    vendor_sweets = db.relationship("VendorSweet", back_populates="vendor")

    def __repr__(self):
        return f"<Vendor {self.id}: {self.name}>"


class Sweet(db.Model, SerializerMixin):
    __tablename__ = "sweets"
    serialize_rules = ('-vendor_sweets.sweet')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # Relationship with vendors through vendorsweets
    vendors = db.relationship("Vendor", secondary='vendor_sweets', back_populates="sweets", overlaps='vendor_sweets')
    vendor_sweets = db.relationship("VendorSweet", back_populates='sweet')

    def __repr__(self):
        return f"<Sweet {self.id}: {self.name}>"


class VendorSweet(db.Model, SerializerMixin):
    __tablename__ = 'vendor_sweets'
    serialize_rules = ('-sweet.vendor_sweets', '-vendor.vendor_sweets')

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer)
    # Foreign key to store sweet and vendor id
    sweet_id = db.Column(db.Integer, db.ForeignKey('sweets.id'))
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'))

    # Relationship with vendors and sweets
    sweet = db.relationship("Sweet", back_populates='vendor_sweets', overlaps='sweets, vendors')
    vendor = db.relationship("Vendor", back_populates='vendor_sweets', overlaps='sweets, vendors')

    @validates("price")
    def validate_price(self, key, price):
        if price is None or price < 0:
            raise ValueError("Price cannot be empty, and it must be a positive number")
        return price

    def __repr__(self):
        return f"<Vendor_Sweet {self.id}: {self.price}>"

