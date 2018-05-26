from flask import Blueprint, request, jsonify
from ..core import server
from ..models import Stores, Reviews, Tags, StoreTags

db = server.db
bp = Blueprint('user', __name__, url_prefix='/user')


def make_favorite_list(user):

  filtered_favorites = Favorites.query.join(Stores).add_columns(
  	Stores.id, Stores.name, Stores.category, Stores.score, Favorites.user_id, Favorites.store_id
  	).filter(user.id == Favorites.user_id).filter(Favorites.store_id == Stores.id).all()

  if not filtered_favorites:
  	return 0

	favorite_list = []

  for e in filtered_favorites:
    favo = {
      'name': e.name,
      'category': e.category,
      'score': e.score
    }
    favorite_list.append(favo)

  return favorite_list



def make_store_list(filtered_stores):

  store_list = []

  for e in filtered_stores:
    filtered_reviews = Reviews.query.filter_by(store_id=e.id).all()
    filtered_tags = StoreTags.query.join(Tags).add_columns(
    Tags.id, Tags.name, StoreTags.store_id, StoreTags.tag_id
    ).filter(StoreTags.store_id == e.id).filter(StoreTags.tag_id == Tags.id).all()

    if not filtered_reviews or not filtered_tags:
      return 0

    review_list = []
    tag_list = []

    for i in filtered_reviews:
      favo1 = {
        'content': i.content,
        'likes': i.likes,
        'date': i.date
      }
      review_list.append(favo1)
    
    for j in filtered_tags:
      favo2 = {
        'name': j.name
      }
      tag_list.append(favo2)

    favo = {
      'store_id': e.store_id
      'name': e.name
      'category': e.category
      'score': e.score
      'review_list': review_list
      'tag_list': tag_list
    }

    store_list.append(favo)

  return store_list
