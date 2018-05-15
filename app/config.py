PORT = 3000

MASTER_USERNAME="teamcook"
DB_PASSWORD="epdlxjqpdltmrofhs"
ENDPOINT="flavor-house.cahuvtrnsple.ap-northeast-2.rds.amazonaws.com"
DB_INSTANCE_NAME="flavor_house"
SQLALCHEMY_DATABASE_URI = "mysql://{}:{}@{}/{}".format(MASTER_USERNAME, DB_PASSWORD, ENDPOINT, DB_INSTANCE_NAME)
SQLALCHEMY_TRACK_MODIFICATIONS = True
