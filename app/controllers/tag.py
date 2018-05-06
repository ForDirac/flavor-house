from flask import Blueprint, request, jsonify
from ..core import server
from ..models import Tags

db = server.db
bp = Blueprint('tag', __name__, url_prefix='/tag')