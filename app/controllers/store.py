from flask import Blueprint, request, jsonify
from ..core import server
from ..models import Stores

db = server.db
bp = Blueprint('store', __name__, url_prefix='/store')