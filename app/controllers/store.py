from flask import Blueprint, request, jsonify
from ..core import server
from ..models import Stores, Reviews, Tags, StoreTags
from ..functions.data import make_store_list
from ..functions.api import sentiment_text
from ..functions.api import entities_text

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
  store_list = Stores.query.all()
  for store in store_list:
    review_list = Reviews.query.filter_by(store_id=store.id).all()

    total_score = 0
    tag_dic = {}

    for review in review_list:
      review.score = sentiment_text(review.content)
      total_score = total_score + review.score

      # Update the review.score
      try:
        db.session.commit()
      except Exception as e:
        db.session.rollback()
        return jsonify({'result':str(e)}), 500

      # make tags in that review 
      # tags which is appeared are in tag_dic
      tags = entities_text(review.content)
      for tag in tags:
        if tag.name in tag_dic:
          tag_dic[tag.name] = tag_dic[tag.name] + 1
        else:
          tag_dic[tag.name] = 1

    total_review = len(review_list)
    if(total_review == 0):
      store.score = None
    else:
      aver_score = total_score / len(review_list)
      if(aver_score < 0): # negative(0~50)
        store.score = (-aver_score) * 50
      else: # positive(50~100)
        store.score = aver_score * 50 + 50

    # Update the store.score
    try:
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      return jsonify({'result':str(e)}), 500

    # check all tags which is appeared more than twice
    real_taglist = []
    for tag_item in tag_dic.items():
      if(tag_item[1] > 3):
        real_taglist.append(tag_item[0])

    # register all tags which are in real_taglist in info into our Database (update the total_score)
    for tag_name in real_taglist:
      tag = Tags()
      tag.name = tag_name

      # register the tag
      try:
        db.session.add(tag)
        db.session.commit()
      except Exception as e:
        db.session.rollback()
        return jsonify({'result':str(e)}), 500

      # Recall the tag in Tags for get the tag_id
      recall_tag = Tags.query.filter_by(name=tag_name).first()
      storetag = StoreTags()
      storetag.store_id = store.id
      storetag.tag_id = recall_tag.id

      # register the storetag
      try:
        db.session.add(storetag)
        db.session.commit()
      except Exception as e:
        db.session.rollback()
        return jsonify({'result':str(e)}), 500

  response = {
    'result': 'success'
  }
  return jsonify(response)


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
  query_string = request.args
  store_id = query_string.get('store_id', type=int)

  if not store_id:
    return jsonify({'result':'Invalid store_id'}), 400

  store = Stores.query.filter_by(id=store_id).first()
  
  if not store:
    return jsonify({'result':'Invalid store'}), 400

  filtered_reviews = Reviews.query.filter_by(store_id=store.id).all()
  filtered_tags = StoreTags.query.join(Tags).add_columns(
    Tags.id, Tags.name, StoreTags.store_id, StoreTags.tag_id
    ).filter(StoreTags.store_id == store.id).filter(StoreTags.tag_id == Tags.id).all()

  review_list = []
  tag_list = []

  for e in filtered_reviews:
    val = {
      'content': e.content,
      'likes': e.likes,
      'date': e.date
    }
    review_list.append(favo)
  
  for i in filtered_tags:
    val = i.name
    tag_list.append(val)

  response = {
    'result': 'success',
    'data': {
      'store_id': store.id,
      'name': store.name,
      'category': store.category,
      'description': store.description,
      'score': store.score,
      'review_list': review_list,
      'tag_list': tag_list
    }
  }

  return jsonify(response)


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
  query_string = request.args
  keyword = query_string.get('keyword', type=str)

  if not keyword:
    return jsonify({'result':'Invalid query string'}), 400

  search = ""

  for i in keyword:
    search = search + "%" + i

  search = search + "%"

  filtered_stores = Stores.query.filter(Stores.name.like(search)).all()

  if not filtered_stores:
    return jsonify({'result':'Invalid filtered_stores'}), 400

  store_list = make_store_list(filtered_stores)
  
  response = {
    'result': 'success',
    'data': store_list
  }

  return jsonify(response)


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
  query_string = request.args
  tag = query_string.get('tag', type=str)

  if not tag:
    return jsonify({'result':'Invalid query string'}), 400

  storetag_list = StoreTags.query.join(Tags).add_columns(
  Tags.id, Tags.name, StoreTags.store_id, StoreTags.tag_id
  ).filter(Tags.name == tag).filter(Tags.id == StoreTags.store_id).all()

  if not storetag_list:
    response = {
      'result': 'success',
      'data': []
    }
    return jsonify(response)

  filtered_stores = []

  for i in storetag_list:
    val = Stores.query.filter_by(id=i.store_id).first()
    filtered_stores.append(val)

  store_list = make_store_list(filtered_stores)

  response = {
    'result': 'success',
    'data': store_list
  }

  return jsonify(response)
