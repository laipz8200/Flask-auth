from environs import Env

env = Env()
env.read_env()

ENV = env.str('FLASK_ENV', default='production')
DEBUG = ENV == 'development'
SECRET_KEY = env.str('SECRET_KEY', default='youwillneverguess')
SQLALCHEMY_DATABASE_URI = env.str('DATABASE_URL')
SQLALCHEMY_TRACK_MODIFICATIONS = False
