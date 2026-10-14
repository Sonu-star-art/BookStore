from flask import Blueprint

admin = Blueprint("admin", __name__, template_folder="templates", static_folder="static", static_url_path="/app/admin/static")

from . import routes