from flask import Blueprint, request, jsonify
from ..core import server
from ..models import Users, Stores

db = server.db
bp = Blueprint('user', __name__, url_prefix='/user')


# sign up a user
@bp.route('', methods=['POST'])
def sign_up():
  ## Request ##
  # Form Data
  # - id: 유저가 입력한 아이디
  # - password: 유저가 입력한 패스워드
  # - name: 유저이름
  ## Response ##
  # JSON
  # - result: 성공 여부
  form = request.form
  user_id = form.get('id', type=str)
  password = form.get('password', type=str)
  name = form.get('name', type=str)

  if not user_id or not password or not name:
    return jsonify({'result':'Invalid form data'}), 400

  user = Users()
  user.user_id = user_id
  user.password = password
  user.name = name
  try:
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    return jsonify({'result':str(e)}), 500

  response = {
    'result': 'success'
  }
  return jsonify(response)

# get a user
@bp.route('', methods=['GET'])
def get_user():
  ## Request ##
  # Query String
  # - user_id: 'users' table에서 id에 해당하는 값(찾을 유저의 id)
  ## Response ##
  # JSON
  # - result: 성공 여부
  # - data: user 정보 모두(favorite 포함)
  query_string = request.args
  user_id = query_string.get('user_id', type=int)
  
  if not user_id:
    return jsonify({'result':'Invalid query string'}), 400

  user = User.query.filter_by(id=user_id).first()
  if not user:
    return jsonify({'result':'Invalid user id'}), 400

  response = {
    'result': 'success',
    'data': {
      'user_id': user.id,
      'name': user.name,
      'favorites': []  #TODO
    }
  }
  pass


# log in a user
@bp.route('/login', methods=['POST'])
def log_in():
  ## Request ##
  # Form Data
  # - user_id: 유저가 입력한 아이디
  # - password: 유저가 입력한 패스워드
  ## Response ##
  # JSON
  # - result: 성공 여부
  # - data: 유저 정보
  form = request.form
  user_id = form.get('user_id', type=str)
  password = form.get('password', type=str)

  if not id or not password:
    return jsonify({'result':'Invalid form data'}), 400

  user = Users.query.filter_by(
    user_id=user_id,
    password=password
  ).first()
  
  if not user:
    return jsonify({'result':'Invalid user id'}), 400

  response = {
    'result': 'success',
    'data': {
      'user_id': user.id,
      'name': user.name
    }
  }

  return jsonify(response)


# register user favorite
@bp.route('/favorite', methods=['POST'])
def register_favorite():
  ## Request ##
  # Form Data
  # - user_id: 'users' table에서 id에 해당하는 값(favorite을 등록할 유저)
  # - store_id: 'stores' table에서 id에 해당하는 값(favorite을 등록할 식당)
  ## Response ##
  # JSON
  # - result: 성공 여부
  pass


# cancel user's favorite
@bp.route('/favorite', methods=['DELETE'])
def cancel_favorite():
  ## Request ##
  # Query String
  # - user_id: 'users' table에서 id에 해당하는 값(favorite을 취소할 유저)
  # - store_id: 'stores' table에서 id에 해당하는 값(favorite을 취소할 식당)
  ## Response ##
  # JSON
  # - result: 성공 여부
  pass

# get user's favorite
@bp.route('/favorite', methods=['GET'])
def get_favorite_list():
  ## Request ##
  # Query String
  # - user_id: 'users' table에서 id에 해당하는 값(favorite list을 가져올 유저)
  ## Response ##
  # JSON
  # - result: 성공 여부
  # - data : 모든 favorite list
  pass