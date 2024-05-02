from config import app, db, bcrypt
from flask_restful import Resource
from models import Vendor, VendorSweet, Sweet
from flask import jsonify, make_response, request

@app.route("/", methods=['GET'])
def home():
    return jsonify({"message":"Felix's API"})

@app.route("/sweets", methods=["GET", "POST"])
def sweets():
    if request.method == "GET":
        sweets = []

        for sweet in Sweet.query.all():
            sweet_dict = {
                'id': sweet.id,
                'name': sweet.name
            }
            sweets.append(sweet_dict)

        return make_response(sweets, 200,)

@app.route("/sweets/<int:id>", methods=["GET", "PATCH", "DELETE"])
def sweet_by_id(id):
    sweet = Sweet.query.filter(Sweet.id == id).first()
    if request.method == "GET":
        if sweet:
            sweet_dict = {
                'id':sweet.id,
                'name':sweet.name
            }
            return make_response(sweet_dict)
        return make_response({"error":"Sweet not found"})

    elif request.method == "PATCH":
        if sweet:
            for attr in request.json:
                setattr(sweet, attr, request.json[attr])
            db.session.add(sweet)
            db.session.commit()
            return make_response(sweet.to_dict(), 200)
        return make_response({"error":"Sweet not found"}, 404)

    elif request.method == "DELETE":
        db.session.delete(sweet)
        db.session.commit()
        return make_response({"message": "Sweet deleted"}, 200)


@app.route("/vendors", methods=["GET", "POST"])
def vendors():
    if request.method == "GET":
        vendors = []

        for vendor in Vendor.query.all():
            vendor_dict = {
                'id': vendor.id,
                'name': vendor.name
            }
            vendors.append(vendor_dict)
        return make_response(vendors, 200)

@app.route("/vendors/<int:id>", methods=["GET", "POST", "DELETE"])
def vendors_by_id(id):
    vendor = Vendor.query.filter(Vendor.id==id).first()

    if request.method == "GET":
        if vendor:
            vendor_dict = {
                'id':vendor.id,
                'name':vendor.name,
                'vendor_sweets':[
                    {
                        'id': vendor_sweet.id,
                        'price': vendor_sweet.price,
                        'sweet':{
                            'id': vendor_sweet.sweet.id,
                            'name': vendor_sweet.sweet.name,
                        },
                        'sweet_id':vendor_sweet.sweet.id,
                        'vendor_id':vendor_sweet.vendor.id
                    }
                    for vendor_sweet in vendor.vendor_sweets
                ]
            }
            return make_response(vendor_dict, 200)
        return make_response({"error":"Vendor not found"}, 404)

    elif request.method == "PATCH":
        if vendor:
            for attr in request.json:
                setattr(vendor, attr, request.json[attr])
            db.session.add(vendor)
            db.session.commit()
            vendor_dict = {
                'id':vendor.id,
                'name':vendor.name
            }
            return make_response(vendor_dict, 200)
        return make_response({"error":"Vendor not found"}, 404)

    elif request.method == "DELETE":
        if vendor:
            db.session.delete(vendor)
            db.session.commit()
            return make_response({"message":"Vendor deleted"})
        else:
            return make_response({"error":"Vendor not found"})


@app.route("/vendor_sweets", methods=["POST"])
def vendor_sweets():
    if request.method == "POST":
        try:
            new_vendor_sweets = VendorSweet(
                price = request.get_json("price"),
                vendor_id = request.get_json('vendor_id'),
                sweet_id = request.get_json('sweet_id'),
            )
            db.session.add(new_vendor_sweets)
            db.session.commit()

            sweet = Sweet.query.get(sweet_id)
            vendor = Vendor.query.get(vendor_id)

            response_dict = {
                'id':new_vendor_sweets.id,
                'price':new_vendor_sweets.price,
                'sweet':{
                    'id':sweet.id,
                    'name': sweet.name,
                },
                'sweet_id':new_vendor_sweets.sweet_id,
                    'vendor':{
                        'id':vendor.id,
                        'name':vendor.name,
                    },
                    'vendor_id':new_vendor_sweets.vendor_id,
                }

            return make_response(response_dict, 201)

        except Exception:
            return make_response({ "errors": ["validation errors"] })

@app.route("/vendor_sweets/<int:id>", methods=["DELETE"])
def vendor_sweets_by_id(id):
    vendor_sweet = VendorSweet.query.filter(VendorSweet.id==id).first()
    if vendor_sweet:
        db.session.delete(vendor_sweet)
        db.session.commit()
        return make_response({}, 404)
    else:
        return make_response({"error": "VendorSweet not found"})



if __name__ == '__main__':
    app.run(debug=True)