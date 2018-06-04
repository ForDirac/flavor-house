from ..models import Stores, Reviews, Tags, StoreTags, Favorites


def make_favorite_list(user):

  filtered_favorites = Favorites.query.join(Stores).add_columns(
  	Stores.id, Stores.name, Stores.category, Stores.score, Favorites.user_id, Favorites.store_id
  	).filter(user.id == Favorites.user_id).filter(Favorites.store_id == Stores.id).all()

  favorite_list = []

  for e in filtered_favorites:
    favo = {
      'store_id': e.store_id,
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

    review_list = []
    tag_list = []

    for i in filtered_reviews:
      val1 = {
        'content': i.content,
        'likes': i.likes,
        'date': i.date
      }
      review_list.append(val1)
    
    for j in filtered_tags:
      val2 = j.name
      tag_list.append(val2)

    val = {
      'store_id': e.id,
      'name': e.name,
      'category': e.category,
      'description': e.description,
      'score': e.score,
      'review_list': review_list,
      'tag_list': tag_list
    }

    store_list.append(val)

  return store_list