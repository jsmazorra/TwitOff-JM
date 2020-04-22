from flask import Blueprint, jsonify, request, flash, redirect

from app.models import db

admin_routes = Blueprint("admin_routes", __name__)

# TODO: think about password protecting these admin routes

API_KEY = "abc123" # TODO: set as env var

# GET /admin/db/reset?api_key=abc123
@admin_routes.route("/admin/db/reset")
def reset_db():
    print("URL PARMS", dict(request.args))

    if "api_key" in dict(request.args) and request.args["api_key"] == API_KEY:
        print(type(db))
        db.drop_all()
        db.create_all()
        return jsonify({"message": "DB RESET OK"})
    else:
        flash("OOPS Permission Denied", "danger")
        return redirect("/users")
