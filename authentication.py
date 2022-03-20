import os
import pymysql
from flask import jsonify, request
import secrets
import hashlib

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

# Authentication

def auth (user_api_key, user_email, user_password):

    user_exists = cursor.execute ('SELECT * FROM cloudcomputingtask.tbl_users WHERE user_email = ?', user_email)

    # Return a 404 if user not in database
    if user_exists == 0:
        return 404

    else:

        # Authenticate via API Key if provided
        if user_api_key != 0:
            cursor.execute ('SELECT user_api_key FROM cloudcomputingtask.tbl_users WHERE user_email = ?', user_email)
            key = cursor.fetchall()
            isAuthorized = True if key == user_api_key else False

        # Authenticate via user password if provided
        if user_password != 0:
            cursor.execute ('SELECT user_md5_pass FROM cloudcomputingtask.tbl_users WHERE user_email = ?', user_email)
            md5Pass_db = cursor.fetchall()
            isAuthorized = True if md5Pass_db == hashlib.md5(user_password.encode('utf-8')) else False

    return isAuthorized
