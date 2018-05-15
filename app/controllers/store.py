from flask import Blueprint, request, jsonify
from ..core import server
from ..models import Stores

db = server.db
bp = Blueprint('store', __name__, url_prefix='/store')

# register store with 'score' and 'tags' using BABLABS API and Google Natural Language API
@bp.route('', methods=['POST'])
def register_store():
  ## Request ##
  # ??
  ## Response ##
  # JSON
  # - result: 성공 여부
  pass

# get store by store_id
@bp.route('', methods=['GET'])
def get_store():
  ## Request ##
  # Query String
  # - store_id: 'stores' table에서 id에 해당하는 값(찾을 식당)
  ## Response ##
  # JSON
  # - result: 성공 여부
  # - data: store_id에 해당하는 식당의 모든 정보(태그, 리뷰 포함)
  pass


# get store list by a keyword
@bp.route('/list/keyword', methods=['GET'])
def get_store_list_by_keyword():
  ## Request ##
  # Query String
  # - keyword: 찾을 키워드
  ## Response ##
  # JSON
  # - result: 성공 여부
  # - data: 키워드에 해당하는 식당 리스트(태그, 리뷰 포함)
  pass


# get store list by a tag
@bp.route('/list/tag', methods=['GET'])
def get_store_list_by_tag():
  ## Request ##
  # Query String
  # - tag: 찾을 태그
  ## Response ##
  # JSON
  # - result: 성공 여부
  # - data: 태그에 해당하는 식당 리스트(태그, 리뷰 포함)
  pass