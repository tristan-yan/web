from flask import Flask, jsonify, request
from passlib.hash import pbkdf2_sha256
#from app import db
import uuid


class User:

    def signup(self):
        user = {
            "_id":"",
            "name":"",
            "email":"",
            "password":""
        }

        # user = {
        #     "_id":uuid.uuid4().hex,
        #     "name":request.form.get('name'),
        #     "email":request.form.get('phone'),
        #     "password":request.form.get('password')
        # }
        #
        #
        # user['password'] = pbkdf2_sha256.encrypt(user['password'])
        #
        # #check
        # db.users.insert(user)
        return jsonify(user), 200