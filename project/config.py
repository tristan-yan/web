#encoding: utf-8

import os

SECRET_KEY = os.urandom(24)

DIALECT = 'mysql'
DRIVER = 'mysqldb'
USERNAME = 'root'
PASSWORD = 'wfx123'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'proj'

SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST,
                                                                       PORT, DATABASE)

SQLALCHEMY_TRACK_MODIFICATIONS = False
