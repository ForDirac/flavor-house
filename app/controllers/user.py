from flask import Blueprint, request, jsonify
from ..core import server
from ..models import Users

db = server.db
bp = Blueprint('user', __name__, url_prefix='/user')


# sign up a user
@bp.route('', methods=['POST'])
def sign_up():
  form = request.form
  user_id = form.get('user_id', type=str)
  password = form.get('password', type=str)
  name = form.get('name', type=str)

  if not user_id or not password or not name:
    return jsonify({'msg':'Invalid form data'}), 400
  
  user = Users()
  user.user_id = user_id
  user.password = password
  user.name = name
  try:
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    return jsonify({'msg':str(e)}), 500

  return jsonify({
    'result': 'success'
  })

# log in a user
@bp.route('/login', methods=['POST'])
def log_in():
  form = request.form
  user_id = form.get('user_id', type=str)
  password = form.get('password', type=str)

  if not id or not password:
    return jsonify({'msg':'Invalid form data'}), 400

  user = Users.query.filter_by(
    user_id=user_id,
    password=password
  ).first()

  return jsonify({
    'id': user.id,
    'name': user.name
  })