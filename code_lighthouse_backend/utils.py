import os

import jwt


def get_request_user_id(request):
    token = retrieve_token(request)
    secret = retrieve_secret()
    decoded_user = jwt.decode(token, secret,
                              algorithms=["HS256"])
    decoded_user_id = decoded_user['user_id']
    return decoded_user_id

def retrieve_token(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    token = token.replace('Bearer ', '')

    return token

def retrieve_secret():
    return os.environ['SECRET_KEY']