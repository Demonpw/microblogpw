import os
CSRF_ENABLED = True
SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/micblog?charset=utf8'
SQLALCHEMY_TRACK_MODIFICATIONS = True
POSTS_PER_PAGE = 5
DEFAULT_PASSWORD = "123456"