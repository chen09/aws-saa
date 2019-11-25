import os
import multiprocessing

from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

HASHIDS_SALT_LANGUAGE = os.environ.get("HASHIDS_SALT_LANGUAGE")
HASHIDS_SALT_QUESTION = os.environ.get("HASHIDS_SALT_QUESTION")
HASHIDS_SALT_CHOICE = os.environ.get("HASHIDS_SALT_CHOICE")

SERVER_ID = os.environ.get("SERVER_ID")
RELEASE = os.environ.get("RELEASE")
ENVIRONMENT = os.environ.get("ENVIRONMENT")

MODE = 'develop'  # develop: 开发模式; production: 生产模式


class ProductionConfig(object):
    """
    生产配置
    """
    BIND = '127.0.0.1:5000'
    WORKERS = multiprocessing.cpu_count() * 2 + 1
    WORKER_CONNECTIONS = 10000
    BACKLOG = 64
    TIMEOUT = 60
    LOG_LEVEL = 'INFO'
    LOG_DIR_PATH = os.path.join(os.path.dirname(__file__), 'logs')
    LOG_FILE_MAX_BYTES = 1024 * 1024 * 100
    LOG_FILE_BACKUP_COUNT = 10
    PID_FILE = 'run.pid'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'example.db')

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}:{port}/aws_saa?charset=utf8'.format(**{
        'user': os.environ.get("DB_USER"),
        'password': os.environ.get("DB_PASSWORD"),
        'host': os.environ.get("DB_HOST"),
        'port': os.environ.get("DB_PORT"),
    })

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopConfig(object):
    """
    开发配置
    """
    BIND = '0.0.0.0:5000'
    WORKERS = 2
    WORKER_CONNECTIONS = 1000
    BACKLOG = 64
    TIMEOUT = 30
    LOG_LEVEL = 'DEBUG'
    LOG_DIR_PATH = os.path.join(os.path.dirname(__file__), 'logs')
    LOG_FILE_MAX_BYTES = 1024 * 1024
    LOG_FILE_BACKUP_COUNT = 1
    PID_FILE = 'run.pid'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'example.db')

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}:{port}/aws_saa?charset=utf8'.format(**{
        'user': os.environ.get("DB_USER"),
        'password': os.environ.get("DB_PASSWORD"),
        'host': os.environ.get("DB_HOST"),
        'port': os.environ.get("DB_PORT"),
    })

    SQLALCHEMY_TRACK_MODIFICATIONS = False


if MODE == 'production':
    config = ProductionConfig
else:
    config = DevelopConfig
