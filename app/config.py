PORT = 3000
WTF_CSRF_ENABLED = True

MASTER_USERNAME="teamcook"
DB_PASSWORD="epdlxjqpdltmrofhs"
ENDPOINT="flavor-house.cahuvtrnsple.ap-northeast-2.rds.amazonaws.com"
DB_INSTANCE_NAME="flavor_house"
SQLALCHEMY_DATABASE_URI = "mysql://{}:{}@{}/{}".format(MASTER_USERNAME, DB_PASSWORD, ENDPOINT, DB_INSTANCE_NAME)
SQLALCHEMY_POOL_RECYCLE = 3600
SQLALCHEMY_TRACK_MODIFICATIONS = True

GCLOUD_KEY_FILE = "My_First_Project-341970818b4e.json"
