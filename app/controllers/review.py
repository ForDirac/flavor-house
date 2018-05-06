from flask import Blueprint, request, jsonify
from ..core import server
from ..models import Reviews

db = server.db
bp = Blueprint('review', __name__, url_prefix='/review')