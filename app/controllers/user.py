from flask import Blueprint, request, jsonify
from ..core import server
from ..models import Users, Stores, Favorites
from ..functions.cors import cross_domain
from ..functions.data import make_favorite_list

db = server.db
bp = Blueprint('user', __name__, url_prefix='/user')


# sign up an user
@bp.route('', methods=['POST', 'OPTIONS'])
@cross_domain('*')
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
    db.session.add(user)
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    return jsonify({'result':str(e)}), 500

  response = {
    'result': 'success'
  }
  return jsonify(response)

# get a user
@bp.route('', methods=['GET', 'OPTIONS'])
@cross_domain('*')
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

  user = Users.query.filter_by(id=user_id).first()

  if not user:
    return jsonify({'result':'Invalid user'}), 400

  favorite_list = make_favorite_list(user)

  response = {
    'result': 'success',
    'data': {
      'user_id': user.id,
      'name': user.name,
      'favorite_list': favorite_list #TODO
    }
  }
  return jsonify(response)


# log in a user
@bp.route('/login', methods=['POST', 'OPTIONS'])
@cross_domain('*')
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

  if not user_id or not password:
    return jsonify({'result':'Invalid form data'}), 400

  user = Users.query.filter_by(
    user_id=user_id,
    password=password
  ).first()
  
  if not user:
    return jsonify({'result':'Invalid user'}), 400

  response = {
    'result': 'success',
    'data': {
      'user_id': user.id,
      'name': user.name
    }
  }

  return jsonify(response)


# register user favorite
@bp.route('/favorite', methods=['POST', 'OPTIONS'])
@cross_domain('*')
def register_favorite():
  ## Request ##
  # Form Data
  # - user_id: 'users' table에서 id에 해당하는 값(favorite을 등록할 유저)
  # - store_id: 'stores' table에서 id에 해당하는 값(favorite을 등록할 식당)
  ## Response ##
  # JSON
  # - result: 성공 여부
  form = request.form
  user_id = form.get('user_id', type=int)
  store_id = form.get('store_id', type=int)

  if not user_id or not store_id:
    return jsonify({'result':'Invalid form data'}), 400

  user = Users.query.filter_by(id=user_id).first()
  store = Stores.query.filter_by(id=store_id).first()

  if not user:
    return jsonify({'result':'Invalid user'}), 400

  if not store:
    return jsonify({'result':'Invalid store'}), 400

  favorites = Favorites()
  favorites.user_id = user.id
  favorites.store_id = store.id

  try:
    db.session.add(favorites)
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    return jsonify({'result':str(e)}), 500

  response = {
    'result': 'success'
  }

  return jsonify(response)

# cancel user's favorite
@bp.route('/favorite', methods=['DELETE', 'OPTIONS'])
@cross_domain('*')
def cancel_favorite():
  ## Request ##
  # Query String
  # - user_id: 'users' table에서 id에 해당하는 값(favorite을 취소할 유저)
  # - store_id: 'stores' table에서 id에 해당하는 값(favorite을 취소할 식당)
  ## Response ##
  # JSON
  # - result: 성공 여부
  query_string = request.args
  user_id = query_string.get('user_id', type=int)
  store_id = query_string.get('store_id', type=int)
  
  if not user_id or not store_id:
    return jsonify({'result':'Invalid query string'}), 400

  user = Users.query.filter_by(id=user_id).first()
  store = Stores.query.filter_by(id=store_id).first()

  if not user:
    return jsonify({'result':'Invalid user'}), 400

  if not store:
    return jsonify({'result':'Invalid store'}), 400

  del_favorite = Favorites.query.filter(Favorites.user_id == user.id).filter(Favorites.store_id == store.id).first()

  if not del_favorite:
    return jsonify({'result':'Invalid del_favorite'}), 400

  try:
    db.session.delete(del_favorite)
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    return jsonify({'result':str(e)}), 500  

  response = {
    'result': 'success'
  }

  return jsonify(response)

# get user's favorite
@bp.route('/favorite', methods=['GET', 'OPTIONS'])
@cross_domain('*')
def get_favorite_list():
  ## Request ##
  # Query String
  # - user_id: 'users' table에서 id에 해당하는 값(favorite list을 가져올 유저)
  ## Response ##
  # JSON
  # - result: 성공 여부
  # - data : 모든 favorite list
  query_string = request.args
  user_id = query_string.get('user_id', type=int)

  if not user_id:
    return jsonify({'result':'Invalid query string'}), 400

  user = Users.query.filter_by(id=user_id).first()
  
  if not user:
    return jsonify({'result':'Invalid user'}), 400

  favorite_list = make_favorite_list(user)

  response = {
    'result': 'success',
    'data': favorite_list
  }

  return jsonify(response)
